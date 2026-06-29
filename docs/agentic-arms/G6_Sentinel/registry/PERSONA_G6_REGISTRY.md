# G6 The Sentinel — Master Registry

> **Persona:** G6 The Sentinel  
> **Persona Definition:** `C:\KimiWork Projects\CORPORATE V 0.5\PERSONA_G6_The_Sentinel.md`  
> **Master Strategy:** `C:\KimiWork Projects\GAI-OBSERVE-DESIGN\skills-hooks-plugins-strategy\STRATEGY.md`  
> **Version:** 1.0.0  
> **Date:** 2026-07-01  
> **Status:** Active  

---

## 1. Registry Overview

This document is the **single source of truth** for all agentic components belonging to G6 The Sentinel. It serves as the master index, cross-reference matrix, and quick-lookup guide for architects, operators, and auditors. Every component listed here is fully documented in its respective file within the `PERSONA_G6_Sentinel_AgenticArms` directory.

---

## 2. Arms Registry (6 Arms)

| Arm ID | Name | Type | Critical Gate | Status | Document |
|--------|------|------|---------------|--------|----------|
| `arm-g6-01` | PII Detector | Primary | R-ARM-DATA-1 (recall >= 0.95) | Active | `arms/ARM_01_G6_PII_Detector.md` |
| `arm-g6-02` | Data Boundary Enforcer | Primary | R-ARM-DATA-4 (PII never leaves boundary) | Active | `arms/ARM_02_G6_Data_Boundary_Enforcer.md` |
| `arm-g6-03` | Multimodal Perceiver | Primary | R-ARM-DATA-2 (lineage graph queryable) | Active | `arms/ARM_03_G6_Multimodal_Perceiver.md` |
| `arm-g6-04` | Secret / Credential Scanner | Secondary | R-ARM-DATA-1 | Active | Sub-arm within `ARM_01_G6_PII_Detector.md` |
| `arm-g6-05` | Anonymization Engine | Secondary | R-ARM-DATA-3 (retention enforced) | Active | `arms/ARM_04_G6_Anonymization_Engine.md` |
| `arm-g6-06` | Retention Compliance Auditor | Secondary | R-ARM-DATA-3 | Active | Sub-arm within `ARM_02_G6_Data_Boundary_Enforcer.md` |

---

## 3. Tools Registry (15 Tools)

| Tool ID | Name | Arm Binding | Type | Execution | Timeout | Document |
|---------|------|-------------|------|-----------|---------|----------|
| `tool-pii-01` | `pii_scanner` | arm-g6-01 | Detection | Sync | 30s | `tools/TOOL_REGISTRY.md` |
| `tool-phi-02` | `phi_detector` | arm-g6-01 | Detection | Sync | 45s | `tools/TOOL_REGISTRY.md` |
| `tool-cred-01` | `credential_scanner` | arm-g6-01, arm-g6-04 | Detection | Sync | 15s | `tools/TOOL_REGISTRY.md` |
| `tool-secret-01` | `secret_detector` | arm-g6-01, arm-g6-04 | Detection | Sync | 15s | `tools/TOOL_REGISTRY.md` |
| `tool-ocr-01` | `ocr_engine` | arm-g6-03 | Processing | Async | 120s | `tools/TOOL_REGISTRY.md` |
| `tool-transcribe-01` | `audio_transcriber` | arm-g6-03 | Processing | Async | 300s | `tools/TOOL_REGISTRY.md` |
| `tool-frame-01` | `video_frame_analyzer` | arm-g6-03 | Processing | Async | 600s | `tools/TOOL_REGISTRY.md` |
| `tool-boundary-01` | `data_boundary_checker` | arm-g6-02 | Enforcement | Sync | 200ms | `tools/TOOL_REGISTRY.md` |
| `tool-jurisdiction-01` | `jurisdiction_validator` | arm-g6-02 | Enforcement | Sync | 100ms | `tools/TOOL_REGISTRY.md` |
| `tool-quarantine-01` | `quarantine_manager` | arm-g6-02 | Enforcement | Sync | 500ms | `tools/TOOL_REGISTRY.md` |
| `tool-anon-01` | `anonymization_engine` | arm-g6-05 | Anonymization | Async | 600s | `tools/TOOL_REGISTRY.md` |
| `tool-pseudo-01` | `pseudonymization_mapper` | arm-g6-05 | Anonymization | Sync | 30s | `tools/TOOL_REGISTRY.md` |
| `tool-reid-01` | `reidentification_tester` | arm-g6-05 | Anonymization | Async | 300s | `tools/TOOL_REGISTRY.md` |
| `tool-retention-01` | `retention_policy_checker` | arm-g6-06 | Audit | Sync | 60s | `tools/TOOL_REGISTRY.md` |
| `tool-lineage-01` | `lineage_tracker` | arm-g6-02, arm-g6-06 | Audit | Async | 120s | `tools/TOOL_REGISTRY.md` |

---

## 4. Plugins Registry (20 Plugins)

| Plugin | Type | Priority | Arm Integration | Auth | Status | Document |
|--------|------|----------|---------------|------|--------|----------|
| Presidio | PII Detection / Anonymization | P2 | arm-g6-01, arm-g6-05 | Local / API key | Planned | `plugins/PLUGIN_REGISTRY.md` |
| Apache Ranger | Data Access Policy | P2 | arm-g6-02 | Kerberos / LDAP | Planned | `plugins/PLUGIN_REGISTRY.md` |
| HashiCorp Vault | Secret Management | P0 | All arms | Kubernetes / AppRole | Planned | `plugins/PLUGIN_REGISTRY.md` |
| OPA | Policy-as-Code | P1 | arm-g6-02 | Bearer + mTLS | Planned | `plugins/PLUGIN_REGISTRY.md` |
| Keycloak | Identity / SSO | P0 | arm-g6-02 | OAuth2 / SAML | Planned | `plugins/PLUGIN_REGISTRY.md` |
| GDPR Compliance API | Regulatory Framework | P2 | arm-g6-02 | OAuth2 | Planned | `plugins/PLUGIN_REGISTRY.md` |
| CCPA Compliance API | Regulatory Framework | P2 | arm-g6-02 | OAuth2 | Planned | `plugins/PLUGIN_REGISTRY.md` |
| HIPAA Compliance API | Regulatory Framework | P2 | arm-g6-01, arm-g6-02 | API key | Planned | `plugins/PLUGIN_REGISTRY.md` |
| DataGov API | Internal Governance | P0 | All arms | JWT RS256 | Core | `plugins/PLUGIN_REGISTRY.md` |
| Splunk | SIEM / Log Aggregation | P1 | All arms | HEC token | Planned | `plugins/PLUGIN_REGISTRY.md` |
| Datadog | Cloud Monitoring | P1 | All arms | API key | Planned | `plugins/PLUGIN_REGISTRY.md` |
| Elasticsearch | Search / Log Analytics | P1 | arm-g6-03 | Basic auth | Planned | `plugins/PLUGIN_REGISTRY.md` |
| MinIO | Object Storage | P1 | arm-g6-03, arm-g6-05 | Access key | Core | `plugins/PLUGIN_REGISTRY.md` |
| PostgreSQL | Relational Database | P0 | All arms | DB auth | Core | `plugins/PLUGIN_REGISTRY.md` |
| Redis | Cache / Queue | P0 | All arms | AUTH + TLS | Core | `plugins/PLUGIN_REGISTRY.md` |
| Kafka | Event Streaming | P1 | arm-g6-02, P2 | SASL/SCRAM | Core | `plugins/PLUGIN_REGISTRY.md` |
| OpenSearch | Search / Analytics | P1 | arm-g6-03 | Basic auth | Planned | `plugins/PLUGIN_REGISTRY.md` |
| AWS Macie | Cloud PII Detection | P2 | arm-g6-01 | AWS IAM | Optional | `plugins/PLUGIN_REGISTRY.md` |
| Azure Purview | Cloud Data Catalog | P2 | arm-g6-01, arm-g6-02 | Azure AD | Optional | `plugins/PLUGIN_REGISTRY.md` |
| Google Cloud DLP | Cloud PII Detection | P2 | arm-g6-01, arm-g6-05 | GCP SA | Optional | `plugins/PLUGIN_REGISTRY.md` |

---

## 5. Skills Registry (10 Skills)

| Skill | Owner | Trigger | Output | Primary Arm | Document |
|-------|-------|---------|--------|-------------|----------|
| `kimi-webbridge` | G6, D4, D8 | Web evidence needed | Screenshot + DOM | arm-g6-01, arm-g6-02, arm-g6-03 | `skills/SKILL_REGISTRY.md` |
| `kimi-data-tools-v2` | G6, G4, D4, D6 | Regulatory research | Search results + synthesis | arm-g6-01, arm-g6-02 | `skills/SKILL_REGISTRY.md` |
| `deep-research-swarm` | G6, G3, D4 | Detection gap | Research brief | arm-g6-01, arm-g6-05 | `skills/SKILL_REGISTRY.md` |
| `batch-download` | G6, D4, D5 | Dataset collection | Validated downloads | arm-g6-03 | `skills/SKILL_REGISTRY.md` |
| `report-writing` | G6, G5, D8 | Audit complete | PDF + JSON report | All arms | `skills/SKILL_REGISTRY.md` |
| `swarm-coding` | G6, D9, D7 | Custom pipeline needed | Code + tests | arm-g6-05 | `skills/SKILL_REGISTRY.md` |
| `skill-creator` | G6, D9, D8 | New workflow pattern | SKILL.md file | All arms | `skills/SKILL_REGISTRY.md` |
| `docx` | G6, D8, D3 | Compliance document | .docx file | arm-g6-02 | `skills/SKILL_REGISTRY.md` |
| `pdf` | G6, D8, G1 | Audit package | PDF file | All arms | `skills/SKILL_REGISTRY.md` |
| `theme-factory` | G6, D8 | Branded output | Styled artifact | All arms | `skills/SKILL_REGISTRY.md` |

---

## 6. Memory Layers (3 Layers)

| Layer | Technology | TTL | Purpose | Schema | Document |
|-------|------------|-----|---------|--------|----------|
| STM | Redis + pgvector | 24h active, 7d recent | Active scan cache, quarantine buffer, alert queue | `turn_id, timestamp, persona_id, arm_id, data_source_id, pii_findings, boundary_status, quarantine_action, confidence, tags` | `memory/RESILIENT_MEMORY_ARCHITECTURE.md` |
| LTM | PostgreSQL JSONB + Filesystem | Indefinite (policies) / 1yr (maps) | PII patterns, boundary policies, data lineage, retention schedules, anonymization maps | `fact_id, category, key, value, source, timestamp, confidence, expiry, data_source_id, pii_type, jurisdiction, retention_policy, anonymization_method` | `memory/RESILIENT_MEMORY_ARCHITECTURE.md` |
| EM | TimescaleDB | 7 years (regulatory) | Scan sessions, audit sessions, quarantine episodes, anonymization jobs | `session_id, persona_id, arm_id, data_source_id, start_time, end_time, scan_results, boundary_violations, quarantine_actions, anonymization_summary, embedding, compression_ratio` | `memory/RESILIENT_MEMORY_ARCHITECTURE.md` |

---

## 7. Hook Contracts (5 Hooks)

| Hook ID | From | To | Trigger | Timeout | PII Handling | Document |
|---------|------|----|---------|---------|------------|----------|
| `g6_to_g2_breach_v1` | G6 | G2 Red Team | Quarantine violation | 60s | Redact all | `contracts/HOOK_CONTRACTS.md` |
| `g6_to_g1_compliance_v1` | G6 | G1 Arbiter | Boundary audit complete | 120s | Redact all | `contracts/HOOK_CONTRACTS.md` |
| `g6_to_p2_ledger_v1` | G6 | P2 Ledger Keeper | Quarantine action | 30s | Redact all | `contracts/HOOK_CONTRACTS.md` |
| `g6_to_d4_knowledge_v1` | G6 | D4 Knowledge Curator | Anonymization package | 300s | Already anonymized | `contracts/HOOK_CONTRACTS.md` |
| `g6_to_edguide_v1` | G6 | EdGuide | Student PII detected | 120s | Redact all | `contracts/HOOK_CONTRACTS.md` |

---

## 8. Cross-Reference Matrix

### 8.1 Arm × Tool Matrix

| Arm / Tool | `pii_scanner` | `phi_detector` | `credential_scanner` | `secret_detector` | `ocr_engine` | `audio_transcriber` | `video_frame_analyzer` | `data_boundary_checker` | `jurisdiction_validator` | `quarantine_manager` | `anonymization_engine` | `pseudonymization_mapper` | `reidentification_tester` | `retention_policy_checker` | `lineage_tracker` |
|------------|---------------|----------------|----------------------|-------------------|--------------|---------------------|------------------------|------------------------|------------------------|----------------------|------------------------|--------------------------|--------------------------|---------------------------|-------------------|
| arm-g6-01 | ✅ | ✅ | ✅ | ✅ | — | — | — | — | — | — | — | — | — | — | — |
| arm-g6-02 | — | — | — | — | — | — | — | ✅ | ✅ | ✅ | — | — | — | — | ✅ |
| arm-g6-03 | — | — | — | — | ✅ | ✅ | ✅ | — | — | — | — | — | — | — | — |
| arm-g6-04 | — | — | ✅ | ✅ | — | — | — | — | — | — | — | — | — | — | — |
| arm-g6-05 | — | — | — | — | — | — | — | — | — | — | ✅ | ✅ | ✅ | — | — |
| arm-g6-06 | — | — | — | — | — | — | — | — | — | — | — | — | — | ✅ | ✅ |

### 8.2 Arm × Plugin Matrix

| Arm / Plugin | Presidio | Ranger | Vault | OPA | Keycloak | GDPR | CCPA | HIPAA | DataGov | Splunk | Datadog | ES | MinIO | PG | Redis | Kafka | OS | Macie | Purview | DLP |
|--------------|----------|--------|-------|-----|----------|------|------|-------|---------|--------|---------|----|-------|----|-------|-------|----|-------|---------|-----|
| arm-g6-01 | ✅ | — | ✅ | — | — | — | — | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | ✅ | — | ✅ | ✅ | ✅ | ✅ |
| arm-g6-02 | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | ✅ | — | ✅ | — |
| arm-g6-03 | — | — | — | — | — | — | — | — | ✅ | — | — | ✅ | ✅ | ✅ | ✅ | — | ✅ | — | — | — |
| arm-g6-04 | — | — | ✅ | — | — | — | — | — | ✅ | ✅ | ✅ | ✅ | — | ✅ | ✅ | — | ✅ | — | — | — |
| arm-g6-05 | ✅ | — | ✅ | — | — | — | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | — | — | ✅ |
| arm-g6-06 | — | — | — | — | — | — | — | — | ✅ | ✅ | ✅ | ✅ | — | ✅ | ✅ | ✅ | ✅ | — | — | — |

### 8.3 Arm × Skill Matrix

| Arm / Skill | `kimi-webbridge` | `kimi-data-tools-v2` | `deep-research-swarm` | `batch-download` | `report-writing` | `swarm-coding` | `skill-creator` | `docx` | `pdf` | `theme-factory` |
|-------------|------------------|----------------------|------------------------|------------------|------------------|-----------------|-----------------|--------|-------|-----------------|
| arm-g6-01 | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | — | ✅ | ✅ |
| arm-g6-02 | ✅ | ✅ | ✅ | — | ✅ | — | ✅ | ✅ | ✅ | ✅ |
| arm-g6-03 | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | — | ✅ | ✅ |
| arm-g6-04 | — | ✅ | ✅ | — | ✅ | — | ✅ | — | ✅ | ✅ |
| arm-g6-05 | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| arm-g6-06 | — | ✅ | — | — | ✅ | — | ✅ | — | ✅ | ✅ |

### 8.4 Arm × Hook Matrix

| Arm / Hook | `g6_to_g2_breach` | `g6_to_g1_compliance` | `g6_to_p2_ledger` | `g6_to_d4_knowledge` | `g6_to_edguide` |
|------------|-------------------|------------------------|--------------------|-----------------------|-----------------|
| arm-g6-01 | ✅ | — | ✅ | — | ✅ |
| arm-g6-02 | ✅ | ✅ | ✅ | — | — |
| arm-g6-03 | — | — | ✅ | ✅ | — |
| arm-g6-04 | ✅ | — | ✅ | — | — |
| arm-g6-05 | — | — | ✅ | ✅ | — |
| arm-g6-06 | — | ✅ | ✅ | — | — |

---

## 9. File Registry

| File | Purpose | Size (KB) | Path |
|------|---------|-----------|------|
| `AGENTIC_ARMS_OVERVIEW.md` | Master architecture overview | ~11 | `architecture/AGENTIC_ARMS_OVERVIEW.md` |
| `ARM_01_G6_PII_Detector.md` | Primary arm — PII detection | ~10 | `arms/ARM_01_G6_PII_Detector.md` |
| `ARM_02_G6_Data_Boundary_Enforcer.md` | Primary arm — boundary enforcement | ~11 | `arms/ARM_02_G6_Data_Boundary_Enforcer.md` |
| `ARM_03_G6_Multimodal_Perceiver.md` | Primary arm — multimodal ingestion | ~13 | `arms/ARM_03_G6_Multimodal_Perceiver.md` |
| `ARM_04_G6_Anonymization_Engine.md` | Secondary arm — anonymization | ~13 | `arms/ARM_04_G6_Anonymization_Engine.md` |
| `TOOL_REGISTRY.md` | Complete tool registry (15 tools) | ~14 | `tools/TOOL_REGISTRY.md` |
| `PLUGIN_REGISTRY.md` | Plugin configurations (20 plugins) | ~15 | `plugins/PLUGIN_REGISTRY.md` |
| `SKILL_REGISTRY.md` | Skill definitions (10 skills) | ~12 | `skills/SKILL_REGISTRY.md` |
| `RESILIENT_MEMORY_ARCHITECTURE.md` | 3-layer memory architecture | ~13 | `memory/RESILIENT_MEMORY_ARCHITECTURE.md` |
| `HOOK_CONTRACTS.md` | 5 hook contracts (full YAML) | ~15 | `contracts/HOOK_CONTRACTS.md` |
| `PERSONA_G6_REGISTRY.md` | This master index file | ~10 | `registry/PERSONA_G6_REGISTRY.md` |

**Total Files:** 11  
**Estimated Total Size:** ~127 KB  

---

## 10. Operational Quick Reference

### 10.1 Arm Invocation Quick Reference

```yaml
arm_invocation:
  trigger: "data_source_ingested" | "scheduled_audit" | "policy_violation" | "manual_request"
  timeout:
    sync: 30s
    async: 600s
  retry:
    policy: "exponential_backoff"
    max_attempts: 3
  circuit_breaker:
    failure_threshold: 5
    fallback: "queue_for_manual_review"
  auth: "JWT RS256 + sentinel_arm_executor role"
```

### 10.2 Critical Gates Status

| Gate | Target | Owner | Measurement | Status |
|------|--------|-------|-------------|--------|
| R-ARM-DATA-1 | PII recall >= 0.95 | arm-g6-01 | Prometheus counter | Target set |
| R-ARM-DATA-2 | Lineage graph queryable | arm-g6-03 | OpenLineage API | Target set |
| R-ARM-DATA-3 | Retention policy enforced | arm-g6-06 | Compliance score | Target set |
| R-ARM-DATA-4 | PII never leaves boundary | arm-g6-02 | Quarantine success rate | Target set |

### 10.3 Escalation Path

```
G6 Operator → D5 SRE Commander (infrastructure)
          → D2 Security Architect (secrets, encryption)
          → D3 Delivery Captain (projects, scheduling)
          → G2 Red Team (breach investigation)
          → G1 Arbiter (compliance certification)
          → P2 Ledger Keeper (audit, provenance)
          → P3 Hallucination Guard (claim verification)
          → G3 Synthesist (pattern research)
          → D4 Knowledge Curator (safe ingestion)
          → D8 Doc Architect (documentation)
          → D9 Forward Engineer (code, automation)
```

---

**Document Owner:** GAI-OBSERVE Advisory Architecture Team  
**Classification:** Internal — Master Registry  
**Next Review:** 2026-08-01
