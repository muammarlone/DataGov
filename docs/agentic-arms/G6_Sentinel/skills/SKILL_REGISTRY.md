# G6 The Sentinel — Skill Registry

> **Persona:** G6 The Sentinel  
> **Version:** 1.0.0  
> **Date:** 2026-07-01  
> **Source Strategy:** `C:\KimiWork Projects\GAI-OBSERVE-DESIGN\skills-hooks-plugins-strategy\STRATEGY.md`  
> **Persona Definition:** `C:\KimiWork Projects\CORPORATE V 0.5\PERSONA_G6_The_Sentinel.md`  

---

## 1. Registry Overview

This document defines the skill bindings for G6 The Sentinel. Skills are **reusable procedural capabilities** that augment the arm's decision-making, evidence production, and artifact generation. Each skill entry includes the trigger condition, input/output contract, execution procedure, quality gates, error handling, evidence requirements, and usage examples.

All skills are pre-installed managed skills under `C:\Users\muamm\AppData\Roaming\kimi-desktop\daimon-share\daimon\skills\`.

---

## 2. Skill Definitions

### 2.1 `kimi-webbridge` — Browser Automation & Screenshot Evidence

| Field | Value |
|-------|-------|
| **Name** | `kimi-webbridge` |
| **Description** | Browser automation for capturing screenshot evidence, DOM snapshots, and web-based data source verification. Used when PII is detected in web applications, admin consoles, or cloud dashboards. |
| **Owner** | G6 The Sentinel (primary), D4 The Knowledge Curator (secondary), D8 The Doc Architect (secondary) |
| **Trigger** | Web-based data source ingestion; PII detected in web app; compliance evidence required for web UI |
| **Input** | `{"url": string, "action": "screenshot" | "navigate" | "click" | "extract", "selector": string, "wait_for": string, "viewport": object}` |
| **Output** | `{"screenshot": "base64:...", "dom_snapshot": object, "url": string, "title": string, "timestamp": string, "evidence_hash": string}` |
| **Procedure** | 1. Validate URL against allowlist. 2. Launch headless browser via Kimi WebBridge. 3. Navigate to URL, wait for selector. 4. Capture full-page screenshot. 5. Extract DOM snapshot. 6. Hash evidence with SHA-256. 7. Store in MinIO with provenance. |
| **Quality Gates** | Screenshot resolution >= 1920x1080; DOM snapshot JSON-parseable; URL matches allowlist; no credentials in DOM |
| **Error Handling** | `TIMEOUT` → retry with shorter wait; `NAVIGATION_ERROR` → fallback to cached screenshot; `AUTH_REQUIRED` → escalate to D2 |
| **Evidence** | Screenshot PNG + DOM JSON + URL + timestamp + SHA-256 hash |
| **Example** | `{"url": "https://console.aws.amazon.com/s3/buckets/analytics-backups", "action": "screenshot", "selector": ".bucket-region", "viewport": {"width": 1920, "height": 1080}}` → `{"screenshot": "base64:...", "dom_snapshot": {"region": "us-east-1"}, "url": "...", "evidence_hash": "sha256:abc..."}` |

### 2.2 `kimi-data-tools-v2` — Regulatory Research & Data Retrieval

| Field | Value |
|-------|-------|
| **Name** | `kimi-data-tools-v2` |
| **Description** | Web search, URL fetch, and structured data retrieval for regulatory research, jurisdiction law changes, GDPR adequacy decisions, and compliance framework mapping. |
| **Owner** | G6 The Sentinel (primary), G4 The Futurist (secondary), D4 The Knowledge Curator (secondary), D6 The Model Guardian (secondary) |
| **Trigger** | Policy ambiguity; jurisdiction change; new regulation published; compliance framework gap |
| **Input** | `{"query": string, "search_type": "web" | "news" | "academic", "sources_required": int, "time_range": string, "jurisdiction": string}` |
| **Output** | `{"results": [{"title": string, "url": string, "snippet": string, "published_date": string, "relevance_score": float}], "synthesis": string, "sources_count": int, "search_id": string}` |
| **Procedure** | 1. Formulate search query with jurisdiction context. 2. Execute via Kimi data tools v2. 3. Rank results by relevance and recency. 4. Synthesize findings into regulatory summary. 5. Cross-reference with active policy set. 6. Flag conflicts or gaps. |
| **Quality Gates** | >= 3 sources for regulatory claims; source URLs verified; published date within 2 years; no hallucinated citations |
| **Error Handling** | `SEARCH_TIMEOUT` → retry with narrower query; `NO_RESULTS` → fallback to regulatory database; `RATE_LIMIT` → queue for retry with backoff |
| **Evidence** | Search result URLs + snippets + synthesis + search_id |
| **Example** | `{"query": "Schrems II adequacy decision 2026 EU US data transfer", "sources_required": 5, "jurisdiction": "EU"}` → `{"results": [{"title": "EU Commission adequacy decision...", "url": "...", "snippet": "...", "relevance_score": 0.98}], "synthesis": "Adequacy decision updated...", "sources_count": 5}` |

### 2.3 `deep-research-swarm` — Privacy Research & Evidence Synthesis

| Field | Value |
|-------|-------|
| **Name** | `deep-research-swarm` |
| **Description** | Multi-agent deep research orchestration for privacy research, adversarial detection techniques, re-identification attacks, and emerging data governance frameworks. Produces evidence-backed research briefs. |
| **Owner** | G6 The Sentinel (primary), G3 The Synthesist (secondary), D4 The Knowledge Curator (secondary) |
| **Trigger** | Detection rate drops below 0.95; new PII pattern suspected; technique gap identified; adversarial evasion detected |
| **Input** | `{"topic": string, "research_questions": array, "required_sources": int, "depth": "standard" | "deep" | "exhaustive", "cross_verify": boolean}` |
| **Output** | `{"brief_id": string, "executive_summary": string, "findings": array, "sources": array, "confidence": float, "recommendations": array, "evidence_package": string}` |
| **Procedure** | 1. Decompose topic into sub-questions. 2. Spawn parallel research agents (web search, academic, regulatory, technical). 3. Cross-verify findings across agents. 4. Synthesize into structured brief. 5. Assign confidence scores. 6. Generate evidence package. |
| **Quality Gates** | >= 5 sources for deep research; cross-verification pass rate >= 80%; P3 review for claims; evidence package signed |
| **Error Handling** | `AGENT_FAILURE` → retry failed agent; `CONFLICTING_EVIDENCE` → flag for human review; `TIMEOUT` → deliver partial brief |
| **Evidence** | Research brief + source list + cross-verification matrix + evidence package |
| **Example** | `{"topic": "Adversarial evasion of PII detection in LLM prompts", "research_questions": ["What techniques hide PII?", "How do detectors fail?", "What countermeasures exist?"], "required_sources": 8, "depth": "deep"}` → `{"brief_id": "br-20260701-001", "executive_summary": "...", "findings": [...], "confidence": 0.92}` |

### 2.4 `batch-download` — Dataset Collection & Validation

| Field | Value |
|-------|-------|
| **Name** | `batch-download` |
| **Description** | Multi-agent batch download and dataset collection for PII model training, validation datasets, and regulatory document archives. Validates checksums, formats, and provenance. |
| **Owner** | G6 The Sentinel (primary), D4 The Knowledge Curator (secondary), D5 The SRE Commander (secondary) |
| **Trigger** | Dataset validation required; model training data needed; regulatory archive collection; evidence package assembly |
| **Input** | `{"urls": array, "expected_formats": array, "checksum_algorithm": string, "validation_rules": array, "max_size_mb": int, "timeout_per_file": int}` |
| **Output** | `{"downloads": [{"url": string, "status": string, "local_path": string, "checksum": string, "size_bytes": int, "format": string}], "failed": array, "manifest": string, "validation_report": object}` |
| **Procedure** | 1. Validate all URLs against allowlist. 2. Parallel download with retry. 3. Verify checksums. 4. Validate format and schema. 5. Scan for malware/PII before storage. 6. Generate manifest with provenance. |
| **Quality Gates** | 100% checksum match; format validation pass; no malware detected; provenance recorded |
| **Error Handling** | `DOWNLOAD_FAILURE` → retry with mirror; `CHECKSUM_MISMATCH` → flag for review; `FORMAT_INVALID` → reject file |
| **Evidence** | Download manifest + checksums + validation report + local paths |
| **Example** | `{"urls": ["https://example.com/dataset.csv"], "expected_formats": ["csv"], "checksum_algorithm": "sha256", "max_size_mb": 100}` → `{"downloads": [{"url": "...", "status": "success", "local_path": "/data/dataset.csv", "checksum": "sha256:abc..."}], "failed": []}` |

### 2.5 `report-writing` — Audit Report Generation

| Field | Value |
|-------|-------|
| **Name** | `report-writing` |
| **Description** | Structured long-form report generation for data boundary audits, PII detection reports, quarantine logs, and compliance evidence packages. Produces Markdown and PDF outputs. |
| **Owner** | G6 The Sentinel (primary), G5 The Chronicler (secondary), D8 The Doc Architect (secondary) |
| **Trigger** | Scan complete; audit requested; compliance deadline; customer deliverable |
| **Input** | `{"report_type": string, "data": object, "template": string, "output_format": "markdown" | "pdf" | "both", "audience": string, "classification": string}` |
| **Output** | `{"report_id": string, "markdown_path": string, "pdf_path": string, "word_count": int, "sections": array, "evidence_count": int, "generated_at": string}` |
| **Procedure** | 1. Load report template from registry. 2. Structure data into outline. 3. Generate executive summary. 4. Write findings with evidence citations. 5. Add recommendations and action items. 6. Export to Markdown + PDF. 7. Sign with Ed25519. |
| **Quality Gates** | All claims backed by evidence; P3 review for accuracy; G1 review for compliance assertions; PDF generation successful |
| **Error Handling** | `TEMPLATE_MISSING` → fallback to generic template; `DATA_INCOMPLETE` → flag missing sections; `PDF_GEN_FAILURE` → deliver Markdown only |
| **Evidence** | Report file paths + section list + evidence citations + signature |
| **Example** | `{"report_type": "data_boundary_audit", "data": {"violations": 14, "sources": 37}, "output_format": "both", "audience": "CISO"}` → `{"report_id": "rpt-20260701-001", "markdown_path": "...", "pdf_path": "...", "word_count": 3500}` |

### 2.6 `swarm-coding` — Anonymization Pipeline Development

| Field | Value |
|-------|-------|
| **Name** | `swarm-coding` |
| **Description** | Multi-agent code orchestration for building custom anonymization pipelines, data transformation scripts, and privacy-preserving ML pipelines. Uses git worktrees and parallel implementation. |
| **Owner** | G6 The Sentinel (primary), D9 The Forward Engineer (secondary), D7 The Test Automator (secondary) |
| **Trigger** | New dataset type encountered; custom anonymization technique required; pipeline performance issue; novel data format |
| **Input** | `{"spec": object, "language": string, "framework": string, "tests_required": boolean, "deployment_target": string, "agents": int}` |
| **Output** | `{"repository": string, "branch": string, "files": array, "test_results": object, "coverage": float, "deployed_to": string, "build_status": string}` |
| **Procedure** | 1. Decompose spec into modules. 2. Spawn parallel coding agents per module. 3. Code review and integration. 4. Run tests and coverage. 5. Merge to main branch. 6. Deploy to target environment. |
| **Quality Gates** | Test coverage >= 80%; Bandit scan pass; no hardcoded secrets; Pydantic v2 schemas; FastAPI endpoints if applicable |
| **Error Handling** | `BUILD_FAILURE` → retry with clean environment; `TEST_FAILURE` → fix and rerun; `MERGE_CONFLICT` → manual resolution |
| **Evidence** | Repository URL + branch + test results + coverage report + build status |
| **Example** | `{"spec": {"anonymization": "k_anonymity", "input_format": "parquet", "output_format": "parquet"}, "language": "python", "tests_required": true, "agents": 3}` → `{"repository": "https://github.com/...", "branch": "feature/k-anon-parquet", "coverage": 0.85}` |

### 2.7 `skill-creator` — Privacy Procedure Skill Authoring

| Field | Value |
|-------|-------|
| **Name** | `skill-creator` |
| **Description** | Creates and updates SKILL.md procedures for privacy-specific workflows, data handling procedures, and compliance checklists. Enables G6 to codify expertise into reusable skills. |
| **Owner** | G6 The Sentinel (primary), D9 The Forward Engineer (secondary), D8 The Doc Architect (secondary) |
| **Trigger** | New privacy workflow identified; compliance procedure updated; skill gap detected; recurring task pattern recognized |
| **Input** | `{"skill_name": string, "domain": string, "procedure": array, "quality_gates": array, "error_handling": array, "examples": array, "owner": string}` |
| **Output** | `{"skill_path": string, "skill_id": string, "version": string, "validation": boolean, "published": boolean, "registry_entry": string}` |
| **Procedure** | 1. Gather domain expertise from G6. 2. Structure into YAML frontmatter + Markdown body. 3. Define trigger, input, output, procedure, quality gates, error handling. 4. Validate against skill schema. 5. Publish to skills registry. 6. Notify dependent personas. |
| **Quality Gates** | SKILL.md schema valid; trigger unambiguous; procedure numbered; quality gates measurable; examples realistic |
| **Error Handling** | `VALIDATION_FAILURE` → fix schema and retry; `NAME_COLLISION` → rename and update references; `PERMISSION_DENIED` → escalate to G7 |
| **Evidence** | Skill file path + registry entry + validation result + version |
| **Example** | `{"skill_name": "gdpr-data-subject-request", "domain": "privacy", "procedure": ["Validate identity", "Locate data", "Export data", "Secure delivery"]}` → `{"skill_path": ".../skills/gdpr-data-subject-request/SKILL.md", "skill_id": "gdpr-dsr", "version": "1.0.0"}` |

### 2.8 `docx` — Compliance Document Generation

| Field | Value |
|-------|-------|
| **Name** | `docx` |
| **Description** | Create, edit, and review Word documents (.docx) for compliance certificates, data processing agreements, and audit response documents. |
| **Owner** | G6 The Sentinel (primary), D8 The Doc Architect (primary), D3 The Delivery Captain (secondary) |
| **Trigger** | Compliance certificate required; DPA needed; audit response document; customer contract with privacy clauses |
| **Input** | `{"template": string, "data": object, "sections": array, "output_path": string, "track_changes": boolean, "comments": array}` |
| **Output** | `{"docx_path": string, "page_count": int, "word_count": int, "sections": array, "validation": boolean, "signature_placeholder": boolean}` |
| **Procedure** | 1. Load DOCX template. 2. Merge data into template fields. 3. Generate sections with headings and tables. 4. Add signature placeholders. 5. Validate document structure. 6. Save to output path. |
| **Quality Gates** | Template fields all populated; no broken references; page count within expected range; accessible heading structure |
| **Error Handling** | `TEMPLATE_CORRUPT` → repair or use fallback; `FIELD_MISSING` → flag incomplete; `GENERATION_ERROR` → retry with simpler template |
| **Evidence** | DOCX file path + page count + validation result + checksum |
| **Example** | `{"template": "compliance_certificate.docx", "data": {"company": "HealthCo", "cert_date": "2026-07-01", "scope": "HIPAA"}, "output_path": "..."}` → `{"docx_path": "...", "page_count": 3, "word_count": 850}` |

### 2.9 `pdf` — Audit Package Generation

| Field | Value |
|-------|-------|
| **Name** | `pdf` |
| **Description** | Create and process PDF files for audit evidence packages, compliance reports, and signed anonymization packages. Supports charts, tables, and form filling. |
| **Owner** | G6 The Sentinel (primary), D8 The Doc Architect (primary), G1 The Arbiter (secondary) |
| **Trigger** | Audit package required; regulatory submission; evidence delivery; signed report needed |
| **Input** | `{"content": string, "source_format": "markdown" | "html" | "json", "output_path": string, "include_charts": boolean, "include_tables": boolean, "password_protect": boolean, "sign": boolean}` |
| **Output** | `{"pdf_path": string, "page_count": int, "file_size_bytes": int, "password_protected": boolean, "signed": boolean, "signature_valid": boolean, "checksum": string}` |
| **Procedure** | 1. Convert source content to HTML. 2. Inject charts and tables. 3. Apply GAI-OBSERVE print CSS. 4. Generate PDF via Playwright/Puppeteer. 5. Optionally password-protect. 6. Optionally sign with Ed25519. 7. Verify signature. |
| **Quality Gates** | PDF readable; all charts rendered; tables not broken; signature valid if signed; checksum generated |
| **Error Handling** | `RENDER_FAILURE` → retry with simpler layout; `SIGNATURE_FAILURE` → generate unsigned + alert; `PASSWORD_ERROR` → generate unprotected |
| **Evidence** | PDF path + page count + signature status + checksum |
| **Example** | `{"content": "# Data Boundary Audit...", "source_format": "markdown", "include_charts": true, "sign": true}` → `{"pdf_path": "...", "page_count": 12, "signed": true, "signature_valid": true}` |

### 2.10 `theme-factory` — Branded Report Styling

| Field | Value |
|-------|-------|
| **Name** | `theme-factory` |
| **Description** | Apply GAI-OBSERVE brand themes (colors, fonts, spacing) to reports, slide decks, and HTML outputs. Ensures all G6 deliverables are visually consistent with the design system. |
| **Owner** | G6 The Sentinel (primary), D8 The Doc Architect (primary) |
| **Trigger** | Report generation complete; presentation needed; customer-facing artifact created; branded HTML export |
| **Input** | `{"content": object, "target_format": "pdf" | "html" | "pptx" | "docx", "theme": "governance" | "editorial" | "dark", "accent": "teal" | "gold" | "coral", "logo": boolean, "watermark": string}` |
| **Output** | `{"styled_path": string, "theme_applied": string, "colors_used": array, "fonts_used": array, "preview_url": string, "validation": boolean}` |
| **Procedure** | 1. Load theme tokens from design system. 2. Apply CSS variables (colors, fonts, spacing). 3. Inject logo and watermark. 4. Render preview. 5. Validate against brand guidelines. 6. Export to target format. |
| **Quality Gates** | Theme tokens all resolved; no hardcoded colors; logo visible; watermark if specified; brand voice compliant |
| **Error Handling** | `THEME_MISSING` → fallback to default governance theme; `FONT_LOAD_FAILURE` → fallback to system fonts; `COLOR_CONTRAST_FAIL` → adjust for accessibility |
| **Evidence** | Styled file path + theme name + validation result + preview URL |
| **Example** | `{"content": {"markdown": "# Audit Report"}, "target_format": "pdf", "theme": "governance", "accent": "teal", "logo": true}` → `{"styled_path": "...", "theme_applied": "governance", "colors_used": ["#0B7E73", "#1B2433", "#FBF8F2"]}` |

---

## 3. Skill-to-Arm Mapping Matrix

| Skill | arm-g6-01 | arm-g6-02 | arm-g6-03 | arm-g6-05 | Primary Usage |
|-------|-----------|-----------|-----------|-----------|---------------|
| `kimi-webbridge` | Screenshot evidence | Admin console audit | Web ingestion | — | Evidence capture |
| `kimi-data-tools-v2` | Regulatory research | Jurisdiction research | Data source validation | Technique research | Research |
| `deep-research-swarm` | Adversarial detection | Cross-border frameworks | Multimodal techniques | Re-identification research | Deep research |
| `batch-download` | Dataset validation | — | Dataset ingestion | Training data | Data collection |
| `report-writing` | PII reports | Boundary audits | Multimodal reports | Anonymization reports | Documentation |
| `swarm-coding` | Custom detectors | Policy engine code | Pipeline code | Anonymization pipelines | Code generation |
| `skill-creator` | PII procedures | Boundary procedures | Ingestion procedures | Anonymization procedures | Knowledge capture |
| `docx` | — | Compliance certs | — | DPAs | Document generation |
| `pdf` | Audit packages | Evidence packages | Analysis packages | Signed packages | PDF generation |
| `theme-factory` | Branded reports | Branded audits | Branded analysis | Branded packages | Brand consistency |

---

**Document Owner:** GAI-OBSERVE Advisory Architecture Team  
**Classification:** Internal — Skill Registry  
**Next Review:** 2026-08-01
