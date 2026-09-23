# 🛡️ Zero-Gravity SOC Command Center & Overwatch AI Voice Engine
> **`eds-formal-rag` — Deterministic SMT Logic Verification, Microgrid Digital Twin, and Speech-to-Speech Overwatch Assistant**

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Gradio Dashboard](https://img.shields.io/badge/UI-Gradio_v5-orange.svg)](https://gradio.app/)
[![Z3 Prover](https://img.shields.io/badge/SMT-Z3_Solver-green.svg)](https://github.com/Z3Prover/z3)
[![ElevenLabs TTS](https://img.shields.io/badge/TTS-ElevenLabs_v1.0+-purple.svg)](https://elevenlabs.io/)

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
3. **Conversational Speech-to-Speech Overwatch AI:** A wake-word-activated assistant ("OK Overwatch") featuring a persona modeled after JARVIS with a Jamaican Patois accent, powered by ElevenLabs Multilingual v2 audio synthesis (`Q9Vh1SycNbxygVIup9vI`).
4. **Differential Privacy & Provenance:** ($\epsilon, \delta$)-DP vector perturbation paired with zero-width steganographic watermarking (`U+200B`/`U+200C`) for immutable data tracking.

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

### 2. SMT Access Control Implication Logic
The formal safety property enforced across all session tokens is expressed as:

$$\text{HasCUI}(v_i) \implies \left( \text{IsEncryptedEnclave} \land \text{IsVerifiedSession} \right)$$

### 3. Grid Isolation Index ($GI$)
The off-grid independence ratio of the datacenter microgrid is calculated as:

$$GI = \max\left(0.0, 1.0 - \frac{\max\left(0, P_{\text{IT}} - P_{\text{solar}} - P_{\text{battery}}\right)}{P_{\text{IT}}}\right)$$

Where $P_{\text{IT}}$ is the combined power draw of active compute racks.

---

## 💻 Hardware & System Requirements

### Minimum Infrastructure Requirements
* **Operating System:** Windows 11 / Server 2022, Ubuntu 22.04 LTS, or macOS Sonoma.
* **CPU:** 8-Core x86_64 or ARM64 (AMD EPYC, Intel Xeon, or Apple M-Series).
* **RAM:** 16 GB minimum.
* **Storage:** 20 GB free NVMe/SSD space.
* **Python Runtime:** Python 3.10, 3.11, or 3.12.
* **Database:** PostgreSQL 15+ with `pgvector` extension enabled.

### Simulated Datacenter Power Profiles
| Hardware Device | Power Draw (kW) | Thermal Exhaust Efficiency |
| :--- | :--- | :--- |
| **Cerebras CS-4 Engine** | 28.00 kW | 91% Heat Capture |
| **Cerebras CS-3 Engine** | 23.00 kW | 91% Heat Capture |
| **NVIDIA B200 HGX (8x)** | 14.30 kW | 91% Heat Capture |
| **NVIDIA H200 HGX (8x)** | 7.00 kW | 91% Heat Capture |
| **AMD AI Halo Cluster** | 0.75 kW | Direct Immersion |
| **100GbE RoCEv2 Switch** | 0.35 kW | Air/Coolant Exchange |

---

## 🎯 Primary Use Cases

1. **Defense & Tactical SOC Operations:** Real-time boundary checking on Classified/CUI token streams in Guest TEE enclaves (AMD SEV-SNP VMPL 0).
2. **Zero-Trust Token Decoding:** Eliminating LLM prompt injections and hallucination leakage in secure enclaves.
3. **Microgrid Energy Balance:** Off-grid peak shaving using solar generation and immersion cooling exhaust capture for local greenhouse agriculture.
4. **Hands-Free Tactical Guidance:** Voice-driven AI command interface for real-time status reporting without visual context switching.
5. **Academic Research Testbed:** D.A.S. doctoral benchmark for software engineering pipelines, algorithm verification, and hardware-level enclave telemetry.

---

## ❓ Frequently Asked Questions (FAQ)

#### Q: How does the wake-word engine work?
**A:** When you record audio in the dashboard, standard Speech-to-Text transcribes the input wave. The logic parser looks for `"OK OVERWATCH"` or `"HEY OVERWATCH"`. If present, it executes the command query and streams synthesized voice feedback.

#### Q: Why is ElevenLabs audio returned as a Base64 URI?
**A:** Modern browsers enforce strict autoplay restrictions on local audio files (`.mp3` saved to disk). By converting raw audio stream bytes into `data:audio/mp3;base64,...` data strings, the dashboard injects an HTML5 player that plays automatically across browser policies.

#### Q: Can I use a custom ElevenLabs Voice Clone?
**A:** Yes. Open `dashboard/overwatch_voice.py` and replace `voice_id="Q9Vh1SycNbxygVIup9vI"` with your custom Voice ID string from the ElevenLabs VoiceLab console.

---

## 🛠️ Troubleshooting Guide

| Issue / Symptom | Root Cause | Resolution |
| :--- | :--- | :--- |
| `OSError: Cannot find empty port in range 7870-7870` | An orphaned Python background process is holding port 7870 open. | Run `Stop-Process -Name "python" -Force` in PowerShell. |
| `ApiError: status_code: 401 ... missing_permissions` | ElevenLabs API key lacks `tts_write` permissions or key string is invalid. | Generate a **Full Access** key at `elevenlabs.io/app/settings/api-keys`. |
| Voice synthesis text returns but audio is silent | Browser autoplay policy muted the dynamic player. | Click anywhere on the dashboard once to grant audio focus, or ensure `autoplay=True` HTML injection is un-muted. |
| `ModuleNotFoundError: No module named 'dashboard'` | Python executed outside project root directory without local pathing. | Run app using `python -B dashboard/app.py` after ensuring `dashboard/__init__.py` exists. |

---

## ⚖️ License & Provenance Invariant

You are welcome to read, review, cite, and fork this research framework to deploy your own instance based on these foundational concepts.

1. **Research & Documentation (CC BY-NC-ND 4.0):** All research text, schematics, and academic documentation are licensed under Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International.
2. **Source Code (Modified MIT):** Free for non-commercial academic research and evaluation, provided original attribution to **Asaad Morman** and Bowie State University is preserved.
3. **Digital Signature Invariant:** All derived code, forks, and child instances **MUST RETAIN** the embedded steganographic watermarker (`dashboard/pi_rag_engine/stego_watermarker.py`) and primary signature constant `HW_KEY_0x889_BSU_DAS_2026_EDR`. Commercial use or stripping signatures is strictly prohibited.

---

## 🚀 Quickstart Command Reference

```powershell
# Set API Credentials & Launch Command Center Server
$env:ELEVENLABS_API_KEY="your_api_key_here"
python -B dashboard/app.py

---

### Instructions to Update on GitHub:
1. Select all text in your browser window on GitHub (`Ctrl + A`).
2. Paste the snippet above over it (`Ctrl + V`).
3. Click the green **"Commit changes..."** button at the top right.
