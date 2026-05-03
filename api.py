"""DataGov — Data Governance Agent.

Endpoints:
  GET  /health
  POST /api/v1/governance/assess   — SVAS data governance assessment
  GET  /api/v1/governance/catalog  — data catalog entries

LLM: OpenRouter. Mock fallback when key absent.
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import sqlite3
import urllib.error
import urllib.request
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

logger = logging.getLogger("DataGov")
logging.basicConfig(level=logging.INFO)

_DB       = os.getenv("DATAGOV_DB_PATH", "datagov.db")
_OR_KEY   = os.getenv("OPENROUTER_API_KEY", "")
_OR_BASE  = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
_OR_MODEL = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-haiku")

_SYSTEM_PROMPT = """You are DataGov, an enterprise data governance expert.
Given a data governance intent, produce an assessment in JSON:
{
  "classification": "PUBLIC|INTERNAL|CONFIDENTIAL|RESTRICTED",
  "pii_detected": true|false,
  "pii_fields": ["...", "..."],
  "lineage_gaps": ["...", "..."],
  "quality_rules": ["...", "..."],
  "steward": "...",
  "retention_policy": "...",
  "catalog_entry": {"domain": "...", "owner": "...", "sensitivity": "..."},
  "summary": "...",
  "actions": ["...", "..."]
}
Respond with valid JSON only. Be specific to the data domain described."""

_MOCK_ASSESS = {
    "classification": "CONFIDENTIAL",
    "pii_detected": True,
    "pii_fields": ["email", "phone", "national_id"],
    "lineage_gaps": ["ETL source not documented", "Transformation rules missing"],
    "quality_rules": [
        "Not null: id, email, created_at",
        "Format: email must match RFC 5322",
        "Range: age must be 0–120",
    ],
    "steward": "Data Platform Team",
    "retention_policy": "7 years (SOX requirement)",
    "catalog_entry": {
        "domain": "Customer",
        "owner": "Product Analytics",
        "sensitivity": "HIGH",
    },
    "summary": "Dataset contains PII. CONFIDENTIAL classification applied. Lineage gaps require remediation.",
    "actions": [
        "Register dataset in enterprise data catalog",
        "Apply column-level encryption for PII fields",
        "Document ETL lineage within 14 days",
        "Schedule quarterly data quality review",
    ],
}


def _init_db():
    conn = sqlite3.connect(_DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS assessments (
        id TEXT PRIMARY KEY, workflow_id TEXT, intent TEXT,
        classification TEXT, pii_detected INTEGER,
        steward TEXT, summary TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit(); conn.close()


def _call_or(intent: str) -> dict:
    payload = json.dumps({
        "model": _OR_MODEL, "max_tokens": 768,
        "messages": [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user",   "content": f"Data governance intent: {intent}"},
        ],
    }).encode()
    req = urllib.request.Request(
        f"{_OR_BASE}/chat/completions", data=payload,
        headers={"Authorization": f"Bearer {_OR_KEY}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.loads(resp.read().decode())
    return json.loads(body["choices"][0]["message"]["content"].strip())


@asynccontextmanager
async def _lifespan(app: FastAPI):
    _init_db(); yield


app = FastAPI(title="DataGov", version="1.0.0", lifespan=_lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])


class GovRequest(BaseModel):
    intent: str
    workflow_id: str = ""
    context: dict = {}
    dataset_name: Optional[str] = None


@app.get("/health")
def health():
    return {"status": "healthy", "service": "DataGov", "llm_available": bool(_OR_KEY)}


@app.post("/api/v1/governance/assess")
def assess(req: GovRequest):
    gid = hashlib.sha256(f"{req.workflow_id}:{req.intent}".encode()).hexdigest()[:12]
    source = "openrouter"
    if _OR_KEY:
        try:
            data = _call_or(req.intent)
        except Exception as exc:
            logger.warning("OR failed (%s) — mock", exc)
            data = {**_MOCK_ASSESS}; source = "mock"
    else:
        data = {**_MOCK_ASSESS}; source = "mock"

    conn = sqlite3.connect(_DB)
    conn.execute(
        "INSERT OR IGNORE INTO assessments "
        "(id, workflow_id, intent, classification, pii_detected, steward, summary) "
        "VALUES (?,?,?,?,?,?,?)",
        (gid, req.workflow_id, req.intent[:200],
         data.get("classification", "INTERNAL"),
         int(data.get("pii_detected", False)),
         data.get("steward", "")[:100],
         data.get("summary", "")[:300]),
    )
    conn.commit(); conn.close()

    logger.info("DataGov assess: id=%s workflow=%s class=%s",
                gid, req.workflow_id, data.get("classification"))
    return {"assessment_id": gid, "workflow_id": req.workflow_id, "source": source, **data}


@app.get("/api/v1/governance/catalog")
def catalog(limit: int = 50):
    conn = sqlite3.connect(_DB); conn.row_factory = sqlite3.Row
    rows = [dict(r) for r in conn.execute(
        "SELECT id, workflow_id, classification, pii_detected, steward, created_at "
        "FROM assessments ORDER BY created_at DESC LIMIT ?",
        (limit,)).fetchall()]
    conn.close()
    return {"entries": rows, "count": len(rows)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8014")))
