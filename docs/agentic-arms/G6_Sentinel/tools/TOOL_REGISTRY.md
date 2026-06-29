# G6 The Sentinel — Tool Registry

> **Persona:** G6 The Sentinel  
> **Arm Coverage:** arm-g6-01 (PII Detector), arm-g6-02 (Data Boundary Enforcer), arm-g6-03 (Multimodal Perceiver), arm-g6-05 (Anonymization Engine)  
> **Version:** 1.0.0  
> **Date:** 2026-07-01  
> **Backend Standard:** FastAPI + PostgreSQL + Redis + JWT + Pydantic v2  
> **Source Strategy:** `C:\KimiWork Projects\GAI-OBSERVE-DESIGN\skills-hooks-plugins-strategy\STRATEGY.md`  

---

## 1. Registry Overview

This document defines the complete tool registry for G6 The Sentinel's agentic arms. Each tool is a **reusable, observable, auth-gated execution unit** with defined input/output schemas, execution modes, and error contracts. All tools adhere to GAI-OBSERVE backend standards.

---

## 2. Detection & Classification Tools

### 2.1 `pii_scanner` (tool-pii-01)

| Field | Value |
|-------|-------|
| **Tool ID** | `tool-pii-01` |
| **Name** | `pii_scanner` |
| **Description** | Multi-regex + NER-based PII detection across text and structured data. Detects names, emails, phone numbers, addresses, SSNs, IDs, dates of birth, and custom patterns. |
| **Owner** | G6 The Sentinel |
| **Arm Binding** | arm-g6-01 (PII Detector) |
| **Input** | `{"text": string, "structured_data": object, "custom_patterns": array, "language": string, "jurisdiction": string}` |
| **Output** | `{"findings": [{"type": string, "value": string, "confidence": float, "position": object, "rule_id": string}], "summary": {"total": int, "by_type": object, "max_confidence": float, "min_confidence": float}}` |
| **Execution Mode** | Sync |
| **Auth** | JWT RS256 + `sentinel_tool_executor` role |
| **Timeout** | 30s |
| **Error** | `{"error": "MODEL_TIMEOUT", "fallback": "regex_only", "retry": 3}` |
| **Example** | `{"text": "Contact John Doe at john@example.com or 555-1234", "findings": [{"type": "person_name", "value": "John Doe", "confidence": 0.98}, {"type": "email", "value": "john@example.com", "confidence": 0.99}, {"type": "phone_number", "value": "555-1234", "confidence": 0.95}]}` |

### 2.2 `phi_detector` (tool-phi-02)

| Field | Value |
|-------|-------|
| **Tool ID** | `tool-phi-02` |
| **Name** | `phi_detector` |
| **Description** | HIPAA-specific PHI detection including patient names, medical record numbers, diagnoses, medications, procedure codes, dates of service, and health plan beneficiary numbers. |
| **Owner** | G6 The Sentinel |
| **Arm Binding** | arm-g6-01 (PII Detector) |
| **Input** | `{"text": string, "structured_data": object, "hipaa_context": boolean, "medical_terminology_boost": boolean}` |
| **Output** | `{"findings": [{"type": string, "phi_category": string, "value": string, "confidence": float, "hipaa_rule": string}], "summary": {"total_phi": int, "by_category": object, "hipaa_risk_level": string}}` |
| **Execution Mode** | Sync |
| **Auth** | JWT RS256 + `sentinel_tool_executor` role |
| **Timeout** | 45s |
| **Error** | `{"error": "MODEL_TIMEOUT", "fallback": "regex_only_medical", "retry": 3}` |
| **Example** | `{"text": "Patient: Jane Smith, MRN: 12345678, Dx: Type 2 Diabetes", "findings": [{"type": "patient_name", "phi_category": "A", "value": "Jane Smith", "confidence": 0.99, "hipaa_rule": "164.514(a)"}, {"type": "medical_record_number", "phi_category": "B", "value": "12345678", "confidence": 0.97, "hipaa_rule": "164.514(a)"}]}` |

### 2.3 `credential_scanner` (tool-cred-01)

| Field | Value |
|-------|-------|
| **Tool ID** | `tool-cred-01` |
| **Name** | `credential_scanner` |
| **Description** | Detects API keys, tokens, passwords, connection strings, and credential files in code, logs, and configuration files. Uses entropy analysis + known pattern matching. |
| **Owner** | G6 The Sentinel |
| **Arm Binding** | arm-g6-01 (PII Detector), arm-g6-04 (Secret Scanner) |
| **Input** | `{"content": string, "filename": string, "language": string, "entropy_threshold": float, "known_patterns": array}` |
| **Output** | `{"findings": [{"type": string, "value_hash": string, "entropy": float, "confidence": float, "file": string, "line": int}], "summary": {"total_secrets": int, "by_type": object, "high_entropy_count": int}}` |
| **Execution Mode** | Sync |
| **Auth** | JWT RS256 + `sentinel_tool_executor` role |
| **Timeout** | 15s |
| **Error** | `{"error": "ENTROPY_ENGINE_FAILURE", "fallback": "pattern_only", "retry": 3}` |
| **Example** | `{"content": "api_key = 'sk-live-abc123xyz789'", "findings": [{"type": "api_key", "value_hash": "sha256:a1b2...", "entropy": 4.2, "confidence": 0.96, "file": "config.py", "line": 12}]}` |

### 2.4 `secret_detector` (tool-secret-01)

| Field | Value |
|-------|-------|
| **Tool ID** | `tool-secret-01` |
| **Name** | `secret_detector` |
| **Description** | Entropy-based secret detection + known secret pattern matching (AWS keys, GitHub tokens, Slack webhooks, database passwords). Integrates with HashiCorp Vault for validation. |
| **Owner** | G6 The Sentinel |
| **Arm Binding** | arm-g6-01 (PII Detector), arm-g6-04 (Secret Scanner) |
| **Input** | `{"content": string, "filename": string, "validate_against_vault": boolean, "secret_types": array}` |
| **Output** | `{"findings": [{"type": string, "pattern_id": string, "value_hash": string, "vault_validated": boolean, "confidence": float, "severity": string}], "summary": {"total": int, "vault_validated": int, "unvalidated": int, "critical": int}}` |
| **Execution Mode** | Sync |
| **Auth** | JWT RS256 + `sentinel_tool_executor` + Vault token |
| **Timeout** | 15s |
| **Error** | `{"error": "VAULT_UNREACHABLE", "fallback": "local_patterns_only", "retry": 3}` |
| **Example** | `{"content": "AKIAIOSFODNN7EXAMPLE", "findings": [{"type": "aws_access_key", "pattern_id": "aws_ak_001", "value_hash": "sha256:c3d4...", "vault_validated": false, "confidence": 0.98, "severity": "critical"}]}` |

---

## 3. Multimodal Processing Tools

### 3.1 `ocr_engine` (tool-ocr-01)

| Field | Value |
|-------|-------|
| **Tool ID** | `tool-ocr-01` |
| **Name** | `ocr_engine` |
| **Description** | Tesseract 5 + cloud OCR (AWS Textract, Azure Form Recognizer) for image-to-text extraction with bounding box coordinates, confidence scores, and text region classification. |
| **Owner** | G6 The Sentinel |
| **Arm Binding** | arm-g6-03 (Multimodal Perceiver) |
| **Input** | `{"image": bytes, "format": string, "language_hint": string, "extract_regions": boolean, "cloud_ocr_fallback": boolean}` |
| **Output** | `{"text": string, "confidence": float, "regions": [{"text": string, "bbox": {"x": int, "y": int, "w": int, "h": int}, "confidence": float}], "language": string, "processing_time_ms": int}` |
| **Execution Mode** | Async |
| **Auth** | JWT RS256 + cloud API key (Vault-rotated) |
| **Timeout** | 120s |
| **Error** | `{"error": "OCR_FAILURE", "fallback": "cloud_ocr", "retry": 3}` |
| **Example** | `{"image": "<JPEG bytes>", "text": "Patient: John Doe | DOB: 1985-03-15", "confidence": 0.94, "regions": [{"text": "John Doe", "bbox": {"x": 45, "y": 120, "w": 200, "h": 30}, "confidence": 0.96}]}` |

### 3.2 `audio_transcriber` (tool-transcribe-01)

| Field | Value |
|-------|-------|
| **Tool ID** | `tool-transcribe-01` |
| **Name** | `audio_transcriber` |
| **Description** | OpenAI Whisper + local Whisper.cpp for audio transcription with speaker diarization, timestamps, and language detection. Optimized for call recordings and meeting audio. |
| **Owner** | G6 The Sentinel |
| **Arm Binding** | arm-g6-03 (Multimodal Perceiver) |
| **Input** | `{"audio": bytes, "format": string, "language_hint": string, "diarize": boolean, "model_size": string}` |
| **Output** | `{"segments": [{"start": float, "end": float, "text": string, "speaker": string, "confidence": float}], "language": string, "word_count": int, "processing_time_ms": int}` |
| **Execution Mode** | Async |
| **Auth** | JWT RS256 + GPU resource token |
| **Timeout** | 300s |
| **Error** | `{"error": "GPU_UNAVAILABLE", "fallback": "cpu_whisper", "retry": 2}` |
| **Example** | `{"segments": [{"start": 0.0, "end": 4.5, "text": "Hello, this is Dr. Smith calling about patient Jane Doe.", "speaker": "SPEAKER_01", "confidence": 0.97}]}` |

### 3.3 `video_frame_analyzer` (tool-frame-01)

| Field | Value |
|-------|-------|
| **Tool ID** | `tool-frame-01` |
| **Name** | `video_frame_analyzer` |
| **Description** | FFmpeg frame extraction + OCR + face detection (OpenCV/dlib) + object detection (YOLO) for video content analysis. Generates frame-level metadata and aggregates across the video timeline. |
| **Owner** | G6 The Sentinel |
| **Arm Binding** | arm-g6-03 (Multimodal Perceiver) |
| **Input** | `{"video": bytes, "format": string, "sample_rate_fps": int, "detect_faces": boolean, "detect_text": boolean, "detect_objects": array}` |
| **Output** | `{"frame_count": int, "sampled_frames": int, "frames_with_text": int, "frames_with_faces": int, "text_findings": [{"frame": int, "timestamp": float, "text": string, "confidence": float}], "face_count": int, "processing_time_ms": int}` |
| **Execution Mode** | Async |
| **Auth** | JWT RS256 + GPU resource token |
| **Timeout** | 600s |
| **Error** | `{"error": "DECODE_FAILURE", "fallback": "audio_extraction_only", "retry": 2}` |
| **Example** | `{"frame_count": 3000, "sampled_frames": 60, "frames_with_text": 12, "frames_with_faces": 3, "text_findings": [{"frame": 120, "timestamp": 4.0, "text": "Patient Name: John Doe", "confidence": 0.92}]}` |

---

## 4. Boundary Enforcement Tools

### 4.1 `data_boundary_checker` (tool-boundary-01)

| Field | Value |
|-------|-------|
| **Tool ID** | `tool-boundary-01` |
| **Name** | `data_boundary_checker` |
| **Description** | Validates data movement against residency and jurisdiction rules. Checks source and target locations against active policy rules from OPA / DataGov. |
| **Owner** | G6 The Sentinel |
| **Arm Binding** | arm-g6-02 (Data Boundary Enforcer) |
| **Input** | `{"data_source_id": string, "source_jurisdiction": string, "target_jurisdiction": string, "target_service": string, "data_classification": string, "policy_set_id": string, "volume_bytes": int}` |
| **Output** | `{"allowed": boolean, "violation_type": string, "policy_rule_id": string, "policy_explanation": string, "confidence": float, "recommended_action": string, "audit_hash": string}` |
| **Execution Mode** | Sync |
| **Auth** | JWT RS256 + OPA API token |
| **Timeout** | 200ms |
| **Error** | `{"error": "OPA_TIMEOUT", "fallback": "default_deny", "retry": 3}` |
| **Example** | `{"data_source_id": "ds-analytics-db", "source_jurisdiction": "EU", "target_jurisdiction": "US", "target_service": "openrouter.api", "allowed": false, "violation_type": "gdpr_cross_border", "policy_rule_id": "pol-gdpr-001", "policy_explanation": "EU personal data may not be transferred to US without SCC+TIA", "recommended_action": "block_and_notify"}` |

### 4.2 `jurisdiction_validator` (tool-jurisdiction-01)

| Field | Value |
|-------|-------|
| **Tool ID** | `tool-jurisdiction-01` |
| **Name** | `jurisdiction_validator` |
| **Description** | Resolves IP addresses, cloud regions, and DNS records to jurisdictional classifications with confidence scores. Uses GeoIP2 + cloud provider metadata + regulatory mapping. |
| **Owner** | G6 The Sentinel |
| **Arm Binding** | arm-g6-02 (Data Boundary Enforcer) |
| **Input** | `{"ip_address": string, "cloud_region": string, "cloud_provider": string, "dns_name": string}` |
| **Output** | `{"jurisdiction": string, "jurisdiction_code": string, "confidence": float, "data_residency_requirement": string, "adequacy_status": string, "transfer_mechanisms": array}` |
| **Execution Mode** | Sync |
| **Auth** | JWT RS256 + GeoIP license key (Vault-rotated) |
| **Timeout** | 100ms |
| **Error** | `{"error": "GEOIP_LOOKUP_FAILURE", "fallback": "cloud_metadata_only", "retry": 3}` |
| **Example** | `{"ip_address": "52.94.236.0", "cloud_region": "us-east-1", "cloud_provider": "aws", "jurisdiction": "US", "jurisdiction_code": "US", "confidence": 0.99, "data_residency_requirement": "none", "adequacy_status": "not_adequate", "transfer_mechanisms": ["SCC", "TIA", "DPF"]}` |

### 4.3 `quarantine_manager` (tool-quarantine-01)

| Field | Value |
|-------|-------|
| **Tool ID** | `tool-quarantine-01` |
| **Name** | `quarantine_manager` |
| **Description** | Blocks, redirects, or isolates violating data streams. Implements egress blocking, API gateway interception, and data migration to compliant regions. |
| **Owner** | G6 The Sentinel |
| **Arm Binding** | arm-g6-02 (Data Boundary Enforcer) |
| **Input** | `{"event_id": string, "violation_type": string, "data_source_id": string, "action": "block" | "migrate" | "encrypt" | "delete", "target_location": string, "justification": string}` |
| **Output** | `{"action_id": string, "status": string, "executed_at": string, "affected_records": int, "new_location": string, "ledger_hash": string}` |
| **Execution Mode** | Sync |
| **Auth** | JWT RS256 + cloud admin credentials (Vault-rotated) |
| **Timeout** | 500ms |
| **Error** | `{"error": "CLOUD_API_FAILURE", "fallback": "manual_ticket", "retry": 5}` |
| **Example** | `{"event_id": "evt-20260701-001", "violation_type": "wrong_jurisdiction", "action": "migrate", "target_location": "eu-west-1", "status": "completed", "affected_records": 1, "new_location": "s3://eu-backups/", "ledger_hash": "a3f2..."}` |

---

## 5. Anonymization Tools

### 5.1 `anonymization_engine` (tool-anon-01)

| Field | Value |
|-------|-------|
| **Tool ID** | `tool-anon-01` |
| **Name** | `anonymization_engine` |
| **Description** | Applies k-anonymity, l-diversity, t-closeness, and differential privacy to structured datasets. Configurable column-level transformation rules. |
| **Owner** | G6 The Sentinel |
| **Arm Binding** | arm-g6-05 (Anonymization Engine) |
| **Input** | `{"dataset": object, "schema": object, "techniques": array, "k": int, "l": int, "epsilon": float, "delta": float, "suppression_limit": float}` |
| **Output** | `{"anonymized_dataset": object, "transformations_applied": array, "k_achieved": int, "l_achieved": int, "suppressed_rows": int, "processing_time_ms": int}` |
| **Execution Mode** | Async |
| **Auth** | JWT RS256 + `sentinel_anonymization` role |
| **Timeout** | 600s |
| **Error** | `{"error": "K_NOT_ACHIEVABLE", "fallback": "increase_suppression", "retry": 3}` |
| **Example** | `{"anonymized_dataset": {"rows": 50000, "columns": 5}, "transformations_applied": [{"column": "age", "technique": "generalization", "bins": 10}], "k_achieved": 5, "suppressed_rows": 12}` |

### 5.2 `pseudonymization_mapper` (tool-pseudo-01)

| Field | Value |
|-------|-------|
| **Tool ID** | `tool-pseudo-01` |
| **Name** | `pseudonymization_mapper` |
| **Description** | Generates reversible pseudonym mappings using cryptographically secure random identifiers. Stores keys in HashiCorp Vault; retains only references in the mapping table. |
| **Owner** | G6 The Sentinel |
| **Arm Binding** | arm-g6-05 (Anonymization Engine) |
| **Input** | `{"identifiers": array, "mapping_strategy": "uuid" | "hash" | "deterministic_encryption", "vault_path": string, "key_rotation_days": int}` |
| **Output** | `{"mappings": [{"original_hash": string, "pseudonym": string, "vault_key_id": string}], "mapping_id": string, "vault_path": string, "created_at": string}` |
| **Execution Mode** | Sync |
| **Auth** | JWT RS256 + Vault write token |
| **Timeout** | 30s |
| **Error** | `{"error": "VAULT_WRITE_FAILURE", "fallback": "local_encryption", "retry": 3}` |
| **Example** | `{"mappings": [{"original_hash": "sha256:abc...", "pseudonym": "P-7f3a...", "vault_key_id": "keys/pseudo-001"}], "mapping_id": "map-20260701-001"}` |

### 5.3 `reidentification_tester` (tool-reid-01)

| Field | Value |
|-------|-------|
| **Tool ID** | `tool-reid-01` |
| **Name** | `reidentification_tester` |
| **Description** | Runs re-identification attacks (uniqueness analysis, linkage attacks, inference attacks) on anonymized datasets to validate effectiveness. Uses adversarial simulation. |
| **Owner** | G6 The Sentinel |
| **Arm Binding** | arm-g6-05 (Anonymization Engine) |
| **Input** | `{"anonymized_dataset": object, "original_dataset": object, "attack_types": array, "auxiliary_data": object, "threshold": float}` |
| **Output** | `{"risk_score": float, "attack_results": [{"attack_type": string, "success_rate": float, "records_at_risk": int}], "below_threshold": boolean, "recommendations": array}` |
| **Execution Mode** | Async |
| **Auth** | JWT RS256 + `sentinel_anonymization` role |
| **Timeout** | 300s |
| **Error** | `{"error": "ATTACK_SIMULATION_FAILURE", "fallback": "basic_uniqueness_only", "retry": 2}` |
| **Example** | `{"risk_score": 0.03, "attack_results": [{"attack_type": "linkage", "success_rate": 0.02, "records_at_risk": 1000}], "below_threshold": true, "recommendations": ["approved_for_downstream"]}` |

---

## 6. Audit & Compliance Tools

### 6.1 `retention_policy_checker` (tool-retention-01)

| Field | Value |
|-------|-------|
| **Tool ID** | `tool-retention-01` |
| **Name** | `retention_policy_checker` |
| **Description** | Verifies data retention schedules against organizational policies and regulatory requirements. Flags expired data, recommends deletion, and generates retention compliance reports. |
| **Owner** | G6 The Sentinel |
| **Arm Binding** | arm-g6-06 (Retention Compliance Auditor) |
| **Input** | `{"data_source_id": string, "policy_set_id": string, "check_date": string, "include_recommendations": boolean}` |
| **Output** | `{"compliant": boolean, "expired_records": int, "total_records": int, "retention_violations": [{"record_id": string, "data_type": string, "created_date": string, "required_retention_days": int, "actual_age_days": int}], "deletion_recommendations": array, "compliance_score": float}` |
| **Execution Mode** | Sync |
| **Auth** | JWT RS256 + `sentinel_audit` role |
| **Timeout** | 60s |
| **Error** | `{"error": "POLICY_LOOKUP_FAILURE", "fallback": "default_7_year", "retry": 3}` |
| **Example** | `{"compliant": false, "expired_records": 12, "total_records": 50000, "retention_violations": [{"record_id": "rec-001", "data_type": "phi_log", "created_date": "2019-01-01", "required_retention_days": 2555, "actual_age_days": 2740}], "deletion_recommendations": ["secure_delete_12_records"], "compliance_score": 0.99976}` |

### 6.2 `lineage_tracker` (tool-lineage-01)

| Field | Value |
|-------|-------|
| **Tool ID** | `tool-lineage-01` |
| **Name** | `lineage_tracker` |
| **Description** | Traces data from source to destination across all hops using OpenLineage integration. Supports column-level lineage, impact analysis, and forensic investigation. |
| **Owner** | G6 The Sentinel |
| **Arm Binding** | arm-g6-02 (Data Boundary Enforcer), arm-g6-06 (Retention Compliance Auditor) |
| **Input** | `{"data_source_id": string, "target_id": string, "depth": int, "column_level": boolean, "time_range": object}` |
| **Output** | `{"lineage_graph": {"nodes": array, "edges": array}, "hops": int, "source": object, "destinations": array, "transformation_log": array, "impact_analysis": {"affected_by": array, "affects": array}}` |
| **Execution Mode** | Async |
| **Auth** | JWT RS256 + OpenLineage API token |
| **Timeout** | 120s |
| **Error** | `{"error": "LINEAGE_GRAPH_TIMEOUT", "fallback": "direct_source_only", "retry": 3}` |
| **Example** | `{"lineage_graph": {"nodes": [{"id": "ds-legacy-api", "type": "source"}, {"id": "ds-github", "type": "store"}, {"id": "ds-backup-service", "type": "destination"}], "edges": [{"from": "ds-legacy-api", "to": "ds-github", "type": "commit"}, {"from": "ds-github", "to": "ds-backup-service", "type": "sync"}]}, "hops": 2}` |

---

## 7. Tool Dependency Graph

```mermaid
flowchart TB
    subgraph Detection["Detection"]
        PII[pii_scanner] --> PHI[phi_detector]
        PII --> CRED[credential_scanner]
        PII --> SEC[secret_detector]
    end
    subgraph Processing["Processing"]
        OCR[ocr_engine] --> NLP[nlp_engine]
        TRANS[audio_transcriber] --> NLP
        FRAME[video_frame_analyzer] --> OCR
    end
    subgraph Enforcement["Enforcement"]
        BOUND[data_boundary_checker] --> JURIS[jurisdiction_validator]
        BOUND --> QUAR[quarantine_manager]
    end
    subgraph Anonymization["Anonymization"]
        ANON[anonymization_engine] --> PSEUDO[pseudonymization_mapper]
        ANON --> REID[reidentification_tester]
    end
    subgraph Audit["Audit"]
        RET[retention_policy_checker] --> LINEAGE[lineage_tracker]
    end
    Detection --> Enforcement
    Processing --> Detection
    Enforcement --> Anonymization
    Anonymization --> Audit

    style Detection fill:#0B7E73,stroke:#1B2433,color:#fff
    style Processing fill:#B5791C,stroke:#1B2433,color:#1B2433
    style Enforcement fill:#0B7E73,stroke:#FBF8F2,color:#fff
    style Anonymization fill:#B5791C,stroke:#1B2433,color:#1B2433
    style Audit fill:#1B2433,stroke:#FBF8F2,color:#fff
```

---

**Document Owner:** GAI-OBSERVE Advisory Architecture Team  
**Classification:** Internal — Tool Registry  
**Next Review:** 2026-08-01
