# ?? AEGIS-MONAD Change & Audit Log
> **Repository:** `eds-formal-rag` | **Hardware Invariant Signature:** `HW_KEY_0x889_BSU_DAS_2026_EDR`

All notable changes, security enhancements, and operational updates to the AEGIS-MONAD framework will be documented in this file to maintain an immutable audit trail for academic and defense review.

---

## [1.2.0] - 2026-09-23
### ?? Added
- **Real Linux Hardware Daemon (`aegis_hw_client.py`):** Lightweight telemetry collection client designed for physical edge servers, workstations, and field rigs running Linux distributions (Ubuntu, RHEL, Debian). Collects live `/proc` and `/sys` metrics (CPU load, memory bandwidth, network throughput, and kernel status).
- **Multi-Language Code Injection Sandbox:** Added interactive code test harness to `dashboard/app.py` supporting on-the-fly script execution in PowerShell, Python, C++, and Java with isolated temp directory management and runtime timing readouts.
- **Real Hardware Dashboard Ingestion Panel:** Added dedicated setup and live monitoring tab in Gradio v5 Command Center to display connected physical Linux node states alongside digital twin microgrid telemetry.

### ??? Verified Invariants
- Thread-isolated Z3 SMT Monad verification verified ($P_{\text{violation}} = 0.0000\%$).
- Hardware signature `HW_KEY_0x889_BSU_DAS_2026_EDR` bound across all active telemetry payloads.

---

## [1.1.0] - 2026-09-22
### ?? Added
- **Overwatch Speech-to-Speech AI Engine:** ElevenLabs Multilingual v2 integration (`Q9Vh1SycNbxygVIup9vI`) featuring JARVIS-style persona with Jamaican Patois accent and dynamic Base64 HTML5 audio player.
- **Datacenter & Microgrid Digital Twin:** Telemetry simulation for Cerebras CS-4/CS-3, NVIDIA B200/H200, and AMD AI Halo compute power draws paired with thermal recovery modeling for greenhouse microgrids.
- **Offsite Parquet Sync:** GitHub Actions CI/CD automation converting execution traces to compressed Parquet format streaming to private Hugging Face Datasets (`asaadmorman/aegis-monad-telemetry`).

---

## [1.0.0] - 2026-09-20
### ??? Initial Baseline
- **Dissertation Baseline:** Academic chapters (Chapter 1 & 2) committed under Bowie State University D.A.S. program requirements.
- **SMT Concurrency Harness:** 100-thread Z3 concurrency isolation test verifying zero memory access violations (`SIGSEGV`).
- **Core Governance:** License initialized under Apache 2.0 with Defense Provenance & Attestation Clause.
