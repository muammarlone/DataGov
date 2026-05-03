"""DataGov API regression tests."""
from __future__ import annotations
import pytest
from fastapi.testclient import TestClient
from api import app

@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c

class TestHealth:
    def test_health_returns_200(self, client):
        assert client.get("/health").status_code == 200

    def test_health_body(self, client):
        b = client.get("/health").json()
        assert b["status"]  == "healthy"
        assert b["service"] == "DataGov"

class TestAssess:
    def test_assess_happy_path(self, client):
        r = client.post("/api/v1/governance/assess",
                        json={"intent": "detect PII in the raw event log dataset",
                              "workflow_id": "test-wf-001"})
        assert r.status_code == 200

    def test_assess_response_shape(self, client):
        b = client.post("/api/v1/governance/assess",
                        json={"intent": "data lineage for customer 360 pipeline",
                              "workflow_id": "test-wf-002"}).json()
        assert "assessment_id"  in b
        assert "workflow_id"    in b
        assert "source"         in b
        assert "classification" in b
        assert "pii_detected"   in b
        assert "pii_fields"     in b
        assert "lineage_gaps"   in b
        assert "quality_rules"  in b
        assert "steward"        in b
        assert "retention_policy" in b
        assert "catalog_entry"  in b
        assert "summary"        in b
        assert "actions"        in b

    def test_classification_is_valid(self, client):
        b = client.post("/api/v1/governance/assess",
                        json={"intent": "classify the HR records dataset"}).json()
        assert b["classification"] in ("PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED")

    def test_pii_detected_is_bool(self, client):
        b = client.post("/api/v1/governance/assess",
                        json={"intent": "PII scan on event logs"}).json()
        assert isinstance(b["pii_detected"], bool)

    def test_pii_fields_is_list(self, client):
        b = client.post("/api/v1/governance/assess",
                        json={"intent": "PII detection in CRM data"}).json()
        assert isinstance(b["pii_fields"], list)

    def test_lineage_gaps_is_list(self, client):
        b = client.post("/api/v1/governance/assess",
                        json={"intent": "lineage gap analysis"}).json()
        assert isinstance(b["lineage_gaps"], list)

    def test_quality_rules_is_list(self, client):
        b = client.post("/api/v1/governance/assess",
                        json={"intent": "data quality rules for product catalog"}).json()
        assert isinstance(b["quality_rules"], list)

    def test_catalog_entry_has_required_fields(self, client):
        b = client.post("/api/v1/governance/assess",
                        json={"intent": "catalog entry for customer dataset"}).json()
        cat = b["catalog_entry"]
        assert "domain"      in cat
        assert "owner"       in cat
        assert "sensitivity" in cat

    def test_assessment_id_deterministic(self, client):
        payload = {"intent": "PII check", "workflow_id": "wf-det-001"}
        id1 = client.post("/api/v1/governance/assess", json=payload).json()["assessment_id"]
        id2 = client.post("/api/v1/governance/assess", json=payload).json()["assessment_id"]
        assert id1 == id2

class TestCatalog:
    def test_catalog_returns_list(self, client):
        b = client.get("/api/v1/governance/catalog").json()
        assert "entries" in b
        assert "count"   in b
        assert isinstance(b["entries"], list)
