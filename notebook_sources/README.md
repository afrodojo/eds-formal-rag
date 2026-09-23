# 🛡️ Zero-Gravity SOC Command Center & Overwatch AI Voice Engine
> **`eds-formal-rag` — Deterministic SMT Logic Verification, Microgrid Digital Twin, Real Linux Hardware Client, and Speech-to-Speech Overwatch Assistant**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Gradio Dashboard](https://img.shields.io/badge/UI-Gradio_v5-orange.svg)](https://gradio.app/)
[![Z3 Prover](https://img.shields.io/badge/SMT-Z3_Solver-green.svg)](https://github.com/Z3Prover/z3)
[![ElevenLabs TTS](https://img.shields.io/badge/TTS-ElevenLabs_v1.0+-purple.svg)](https://elevenlabs.io/)
[![Audit Trail](https://img.shields.io/badge/Audit_Log-Active-brightgreen.svg)](CHANGELOG.md)

---

## 🏛️ Academic & Research Attribution

* **Principal Investigator:** Asaad Morman
* **Academic Program:** Doctor of Applied Science (D.A.S.) Candidate in Computer Science
* **Institution:** Bowie State University — Department of Computer Science
* **Primary Research Repository:** `eds-formal-rag`
* **Digital Signature & Provenance Invariant:** `HW_KEY_0x889_BSU_DAS_2026_EDR`

---

## 📋 System Overview

The **Zero-Gravity SOC Command Center (`eds-formal-rag`)** is a defense-grade security operation dashboard, open-research framework, and digital twin ecosystem engineered for high-assurance AI environments. It integrates:

1. **Deterministic Monad Logits Verification:** Powered by the Z3 SMT logic solver to guarantee zero policy-violation probability ($P_{\text{violation}} = 0$) during LLM token decoding in secure enclaves.
2. **Datacenter & Microgrid Telemetry Twin:** Real-time simulation of power draws across heterogeneous accelerators (Cerebras CS-4, NVIDIA B200/H200, AMD AI Halo), thermal recovery for greenhouse microgrids, and off-grid solar/battery balancing.
3. **Real Linux Hardware Daemon Client (`aegis_hw_client.py`):** Lightweight background telemetry daemon for field-deployed physical Linux devices (Ubuntu/RHEL/Debian) streaming CPU, memory, network, and kernel metrics live to the SOC dashboard.
4. **Multi-Language Code Injection Sandbox:** Dynamic execution panel allowing real-time test script injections in **PowerShell, Python, C++, and Java**.
5. **Conversational Speech-to-Speech Overwatch AI:** A wake-word-activated assistant ("OK Overwatch") featuring a persona modeled after JARVIS with a Jamaican Patois accent, powered by ElevenLabs Multilingual v2 audio synthesis (`Q9Vh1SycNbxygVIup9vI`).
6. **Differential Privacy & Provenance:** ($\epsilon, \delta$)-DP vector perturbation paired with zero-width steganographic watermarking (`U+200B`/`U+200C`) for immutable data tracking.

---

## 📐 Mathematical Framework & Equations

### 1. Monad SMT Logit Transformation Operator
To prevent policy violations (e.g., unauthorized Controlled Unclassified Information spillage), raw output logits $L_i$ are constrained deterministically prior to softmax sampling:

$$\hat{L}_i = L_i + \log \Phi(v_i)$$

Where:
* $L_i$ represents the raw model output logit for candidate token $v_i$.
* $\Phi(v_i) \in \{0, 1\}$ is an indicator function evaluated by the Z3 SMT solver graph:

$$\Phi(v_i) = \begin{cases} 1 & \text{if } \text{SMT\_Verify}(v_i) = \text{SAT} \\ 0 & \text{if } \text{SMT\_Verify}(v_i) = \text{UNSAT} \end{cases}$$

* If a candidate token violates security policies, $\log(0) = -\infty$, reducing $\hat{L}_i$ to $-\infty$ and guaranteeing zero probability of selection ($P_{\text{violation}} = 0$).

### 2. Grid Isolation Index ($GI$)
The off-grid independence ratio of the datacenter microgrid is calculated as:

$$GI = \max\left(0.0, 1.0 - \frac{\max\left(0, P_{\text{IT}} - P_{\text{solar}} - P_{\text{battery}}\right)}{P_{\text{IT}}}\right)$$

---

## 🐧 Real Hardware Integration (Linux Nodes)

To connect physical hardware running Ubuntu, RHEL, or Debian:

```bash
# 1. Transfer aegis_hw_client.py to the target machine
chmod +x aegis_hw_client.py

# 2. Set dashboard IP & start telemetry daemon
export AEGIS_DASHBOARD_URL="http://<YOUR_SOC_IP>:7860/api/hardware_telemetry"
python3 aegis_hw_client.py
⚡ Multi-Language Code Sandbox
The dashboard includes an interactive execution harness for research testing across multiple runtimes:

PowerShell: Native Windows execution policy testing & administrative automation.

Python: In-memory SMT solver validation and data processing.

C++: Native compilation (g++) for enclave memory safety testing.

Java: Cross-platform enterprise software verification (javac).

📄 Audit Trail & Change Log
All code updates, hardware signature bindings, and pipeline enhancements are tracked in CHANGELOG.md.

🚀 Quickstart Command Reference
PowerShell
# Set API Credentials & Launch Command Center Server
$env:ELEVENLABS_API_KEY="your_api_key_here"
python -B dashboard/app.py

---

### Instructions for Syncing Local Repo After Direct GitHub Edit:
Once you commit this file directly on GitHub, sync your local working folder by running:

```powershell
git pull origin main
Copy-Item -Path "README.md" -Destination "notebook_sources/README.md" -Force
