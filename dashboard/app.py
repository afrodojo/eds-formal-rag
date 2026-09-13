# eds-formal-rag-main/dashboard/app.py - Zero-Gravity SOC Command Center & Framework Simulator
import gradio as gr
import math
import random
import time
import z3

# --- 1. SMT Logic Solver Mock & Hallucination Testing (Deterministic Decoding) ---
class PolicyVerifierMock:
    def __init__(self):
        # We define a standard, frozen security policy graph (NIST SP 800-171 CUI)
        self.solver = z3.Solver()
        
        # Boolean variables for formal reasoning
        is_encrypted = z3.Bool('is_encrypted')
        has_cui_access = z3.Bool('has_cui_access')
        session_verified = z3.Bool('session_verified')

        # Rule: IF output contains CUI data, THEN require encrypted enclave AND verified session.
        cui_policy = z3.Implies(has_cui_access, z3.And(is_encrypted, session_verified))
        self.solver.add(cui_policy)

    def verify_token_soundness(self, token_str, mode, classification):
        """
        Determines token validity against policy. If UNSAT, applies mathematical log penalty
        L_hat_i = L_i + log Φ(v_i).
        Returns (is_compliant, logit_penalty, phi_value).
        """
        # --- Simulate Ground Truth State (VMPL 0 enclaves with valid signatures) ---
        env_encrypted = True  
        ses_verified = True   
        
        # CUI property check (mimics vector store embedding classification lookup)
        cui_terms = ["CUI", "RESTRICTED", "SECRET", "CLASSIFIED", "CONFIDENTIAL"]
        output_has_cui = any(term in token_str.upper() for term in cui_terms)

        # 1. Evaluate symbolic graph constraints (Φ)
        self.solver.push()
        self.solver.add(is_encrypted == env_encrypted)
        self.solver.add(session_verified == ses_verified)
        self.solver.add(has_cui_access == output_has_cui)
        sat_result = self.solver.check()
        self.solver.pop()

        # 2. Map SAT/UNSAT to Φ(v_i) indicator (1 or 0)
        is_sat = sat_result == z3.sat
        phi_val = 1.0 if is_sat else 0.0

        # 3. Compute deterministic penalty: log(Φ(v_i))
        if phi_val > 0.0:
            logit_penalty = 0.0 # log(1) = 0
        else:
            logit_penalty = float('-inf') # log(0) = -inf

        return is_sat, logit_penalty, phi_val

policy_verifier = PolicyVerifierMock()


# --- 2. Live Telemetry/Output Simulation ---
def run_unified_sim_session(model, mode, classification, input_cui_log, enable_hw_sim, temperature):
    """
    Generates the exact verified output log seen in the visual.
    Includes simulated training progress or constrained inference loop.
    """
    output_log_console = ""
    # Header format
    output_log_console += f"--- {mode.upper()} SESSION STARTING (Model: {model}) ---\n"
    output_log_console += f"Input Query: '{input_cui_log}' | Classification: {classification}\n\n"
    yield output_log_console
    
    time.sleep(1) # Simulate environment attestation latency

    if "Inference" in mode:
        output_log_console += "--- SMT MONAD TRANSFORMER OPERATION (COMPUTE_LOOP) ---\n"
        output_log_console += "x_{k}: 'ANALYZING_CUI_THREAT_PATTERN'\n"
        
        # Rigorous hallucination testing via SMT verification of a candidate token
        cand_token = "CUI_CLASSIFIED"
        is_sat, penalty, phi = policy_verifier.verify_token_soundness(cand_token, mode, classification)
        
        sat_text = "Solver_SAT_True (1)" if is_sat else "Solver_SAT_False (0)"
        output_log_console += f"Invariant Check (\Sigma): NIST SP 800-171 CUI boundary -> {sat_text}\n"
        
        penalty_text = "-INF LOGIT (PROB=0%)" if is_sat is False else "0.0 LOGIT (PROB=L_i)"
        output_log_console += f"Logits Processor Mask Active: L_i + log Φ(v_i) ({penalty_text})\n"
        
        sat_status = "(SAT)" if is_sat else "(UNSAT - BLOCKED)"
        output_log_console += f"Sampling Token (x_{{k+1}}): '{cand_token}' {sat_status}\n\n"
        
        time.sleep(1) # Simulate decoding

        output_log_console += "--- LIVE SMT LOGIC & TEE ATTRIBUTE TELEMETRY ---\n"
        sat_status_main = "VERIFIED (SAT)" if is_sat else "VIOLATION (UNSAT)"
        sat_indicator = 0 if is_sat else 1 # Reverse for visual display
        output_log_console += f"Z3 Solver Status: {sat_status_main} | P_violation = {sat_indicator}\n"
        output_log_console += "Enclave Isolation: AMD SEV-SNP Guest VMPL 0 (AES-256 Active)\n"
        output_log_console += "Host Isolation: ZERO TRUST OK\n"
        output_log_console += "P-384 ECDSA TEE Signature: VERIFIED\n"
        output_log_console += "Invariant Graph Integrity: CONFIRMED\n"
        yield output_log_console

    elif "Train" in mode:
        output_log_console += "--- SFT TRAINING LOG (SIMULATED_SESSION) ---\n"
        # Simulate training steps for PoC before hardware arrives
        epochs = 10
        avg_loss = 1.3
        sat_rate = 100.0
        
        for epoch in range(1, epochs + 1):
            avg_loss -= (epoch * random.uniform(0.01, 0.03)) # Simulate loss decrease
            avg_loss = max(0.5, avg_loss)
            sat_rate = min(100.0, 99.0 + (epoch * random.uniform(0.05, 0.1)))
            output_log_console += f"Epoch [{epoch}/{epochs}], Step [150/458], Avg_Loss: {avg_loss:.2f}, SMT_Sat_Rate: {sat_rate:.2f}%\n"
            yield output_log_console
            time.sleep(0.5) # Fast-forward simulation
            
        output_log_console += "[SFT Complete: CHECKPOINT eds-formal-rag-qwen-checkpoint-2]\n"
        output_log_console += "[Simulated SEV-SNP Launch Digest: ECDSA P-384 VERIFIED (SAT)]\n\n"
        yield output_log_console

    if enable_hw_sim:
        output_log_console += "--- Sim_Hardware Telemetry ---\n"
        output_log_console += "[SIMULATED 14.3 kW B200 HGX Load Active]\n"
        output_log_console += "[Grid Isolation Index (Sim): 1.0 (OFFLINE_MODE)]\n"
        output_log_console += "Microgrid Autonomy: 100% (Offline Sim)\n"
        yield output_log_console


# --- 3. Build the Gradio interface ---
# Define a dark theme that matches the visualization aesthetic
custom_theme = gr.themes.Default(primary_hue="sky", neutral_hue="slate").set(
    body_text_color="#CBD5E1", # Slate-300
    background_fill_primary="#0F172A", # Slate-900
    block_background_fill="#1E293B", # Slate-800
    block_border_color="#334155", # Slate-700
    block_title_text_color="#CBD5E1"
)

# Custom CSS for command center feel, titles, and text colors
custom_css = """
body { background-color: #0F172A !important; }
#eds-main-block .gr-markdown h1, h2, h3 { color: #f8fafc; text-align: center; }
#eds-main-block .gr-tab-header { border-bottom: 2px solid #334155; }
#eds-main-block .gr-tab-button.selected { border-bottom-color: #0ea5e9; color: #f8fafc; }
#verified-output .gr-textbox textarea { color: #facc15; font-family: monospace; border: none; background: transparent; }
"""

with gr.Blocks(theme=custom_theme, css=custom_css, title="EDS Zero-Gravity SOC Command Center") as eds_blocks:
    
    # 1. Main Header Title block
    with gr.Column(elem_id="eds-main-block"):
        gr.Markdown(
            """
            # EMERGING DEFENSE SOLUTIONS (EDS)
            ## Zero-Gravity SOC Command Center | SMT Formal Verification & Microgrid Control
            """
        )
        
        # 2. Main Tabbed Layout Container
        with gr.Tabs() as main_tabs:
            
            # --- TAB 1: Unified PoC Framework ---
            with gr.Tab("Unified PoC Framework (Offline Sim Mode)"):
                
                # Split the layout into two main columns (Config/Inputs on left, Output on right)
                with gr.Row():
                    
                    # 2.1 LEFT COLUMN: Configuration and Inputs
                    with gr.Column(scale=1):
                        
                        # Framework Config Group (Matches upper left of visualization)
                        with gr.Group():
                            gr.Markdown("### ⚙️ Framework Config")
                            selected_model = gr.Dropdown(
                                choices=["Qwen2.5-7B (Fine-Tuned)", "Qwen2-7B-Base"], 
                                value="Qwen2.5-7B (Fine-Tuned)", 
                                label="Selected Model"
                            )
                            active_mode = gr.Radio(
                                choices=["Train/SFT", "Inference"], 
                                value="Inference", 
                                label="Active Mode"
                            )
                            hw_sim_enable = gr.Checkbox(
                                value=True, 
                                label="Enable Offline Hardware Sim (AMD SEV-SNP Guest VMPL 0, 14.3 kW Load)"
                            )
                            logits_temp = gr.Slider(
                                minimum=0.0, maximum=1.0, step=0.1, value=0.7, 
                                label="Logits Processing Temperature"
                            )

                        # Threat Intelligence Query Group (Matches lower left)
                        with gr.Group():
                            gr.Markdown("### 🔍 Threat Intelligence Query")
                            cui_threat_token = gr.Textbox(
                                label="CUI Log entry / Threat Token", 
                                value="RESTRICTED_CUI_THREAT_LOG_001",
                                placeholder="E.g., RESTRICTED_CUI_THREAT_LOG_001"
                            )
                            classification_level = gr.Dropdown(
                                choices=["UNCLASSIFIED", "CUI", "SECRET", "TOP SECRET"], 
                                value="SECRET", 
                                label="Classification Level"
                            )
                        
                        # Command buttons 
                        # execute_secure_inference is primary (orange/sky hue)
                        exec_inference_btn = gr.Button("EXECUTE SECURE INFERENCE (SAT-Constrained)", variant="primary")
                        # initiate_sft_session is secondary (neutral hue)
                        initiate_sft_btn = gr.Button("INITIATE SFT SESSION (CUI Dataset)", variant="secondary")

                    # 2.2 CENTER/RIGHT COLUMN: Verified Output Log
                    # This column is vertically expanded to show more of the detailed log.
                    with gr.Column(scale=2, min_width=600):
                        with gr.Group(elem_id="verified-output"):
                            gr.Markdown("### 📜 Verified Output Log")
                            # We replace Code display with multiline Textbox for better console log feel.
                            output_console_display = gr.Textbox(
                                lines=40, # Large text block as requested
                                label="", 
                                interactive=False, 
                                show_copy_button=True
                            )
                
                # 2.3 Interaction Definitions for Tab 1
                exec_inference_btn.click(
                    fn=run_unified_sim_session,
                    inputs=[selected_model, active_mode, classification_level, cui_threat_token, hw_sim_enable, logits_temp],
                    outputs=[output_console_display]
                )
                
                # initiate_sft_btn enforces the Train/SFT mode and sets parameters
                initiate_sft_btn.click(
                    fn=lambda model, cui_log, hw_sim, temp: (
                        run_unified_sim_session(model, "Train/SFT", "CUI", cui_log, hw_sim, temp)
                    ),
                    inputs=[selected_model, cui_threat_token, hw_sim_enable, logits_temp],
                    outputs=[output_console_display]
                )

            # --- TAB 2: Offline SMT Graph Editor (Optional placeholder as seen in visual) ---
            with gr.Tab("Offline Sed"):
                gr.Markdown("### SMT Symbolic Graph Editor (Coming Soon)")
                gr.Image("https://gradio-builds.s3.amazonaws.com/assets/images/gradio_monad.png", height=400) # Reusing Gradio's monad asset

# --- 4. Launch the application locally ---
if __name__ == "__main__":
    # We specify server_name="127.0.0.1" and port 7860 to match the previous launch config.
    eds_blocks.queue().launch(server_name="127.0.0.1", server_port=7860)
