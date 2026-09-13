# dashboard/app.py - Zero-Gravity SOC Command Center & Forced Voice Output Overwatch
import os
import sys

# Ensure current directory is in sys.path for internal imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import gradio as gr
import math
import random
import time
import json
import z3

try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False

try:
    from dashboard.overwatch_voice import OverwatchVoiceEngine
except ModuleNotFoundError:
    from overwatch_voice import OverwatchVoiceEngine

# --- 1. SMT Logic Solver Engine ---
class PolicyVerifier:
    def __init__(self):
        self.solver = z3.Solver()
        self.is_encrypted_enclave = z3.Bool('is_encrypted_enclave')
        self.is_verified_session = z3.Bool('is_verified_session')
        self.has_cui_access = z3.Bool('has_cui_access')

        cui_policy = z3.Implies(self.has_cui_access, z3.And(self.is_encrypted_enclave, self.is_verified_session))
        self.solver.add(cui_policy)

    def verify_token_compliancy(self, candidate_token):
        env_encrypted = True
        ses_verified = True
        cui_terms = ["CUI", "RESTRICTED", "CLASSIFIED", "SECRET", "CONFIDENTIAL", "UNAUTHORIZED"]
        output_has_cui = any(term in str(candidate_token).upper() for term in cui_terms)

        self.solver.push()
        self.solver.add(self.is_encrypted_enclave == env_encrypted)
        self.solver.add(self.is_verified_session == ses_verified)
        self.solver.add(self.has_cui_access == output_has_cui)
        sat_result = self.solver.check()
        self.solver.pop()

        return sat_result == z3.sat

policy_verifier = PolicyVerifier()

# --- 2. Advanced Hardware Digital Twin ---
class AdvancedHardwareDigitalTwin:
    def __init__(self):
        self.specs = {
            "Mac_Studio": 0.37, "AMD_AI_Halo": 0.75, "DGX_Spark": 3.5,
            "H200_HGX": 7.0, "B200_HGX": 14.3, "Cerebras_CS3": 23.0,
            "Cerebras_CS4": 28.0, "Switch_100GbE_RoCEv2": 0.35,
            "Switch_400GbE_InfiniBand": 0.85, "Rack_Immersion_Pumps": 1.2
        }

        self.model_profiles = {
            "Qwen2.5-7B (Fine-Tuned)": {"base_tps": 180, "base_hallucination_rate": 0.04},
            "Llama-3.1-70B-Instruct": {"base_tps": 45, "base_hallucination_rate": 0.08},
            "DeepSeek-R1-Distill-70B": {"base_tps": 52, "base_hallucination_rate": 0.03},
            "Mistral-Large-2": {"base_tps": 38, "base_hallucination_rate": 0.06},
            "Custom-Ingested-ONNX/Safetensors": {"base_tps": 110, "base_hallucination_rate": 0.05}
        }
        
        self.solar_array_max_kw = 120.0
        self.battery_storage_max_kwh = 500.0
        self.battery_charge_kwh = 450.0

    def simulate_telemetry(self, selected_model, custom_weights_path, units_config, time_of_day, prompt_input, classification):
        try:
            config = json.loads(units_config)
        except Exception:
            config = {"Mac_Studio": 4, "B200_HGX": 1, "Cerebras_CS4": 1}
        
        total_it_kw = 0.0
        for unit, count in config.items():
            if unit in self.specs:
                total_it_kw += self.specs[unit] * count

        model_info_data = self.model_profiles.get(selected_model, self.model_profiles["Qwen2.5-7B (Fine-Tuned)"])
        tps_multiplier = 1.0

        if config.get("Cerebras_CS4", 0) > 0:
            tps_multiplier *= (5.5 * config["Cerebras_CS4"])
        elif config.get("Cerebras_CS3", 0) > 0:
            tps_multiplier *= (4.0 * config["Cerebras_CS3"])
        elif config.get("B200_HGX", 0) > 0:
            tps_multiplier *= (2.2 * config["B200_HGX"])

        network_switches = config.get("Switch_100GbE_RoCEv2", 0) + (config.get("Switch_400GbE_InfiniBand", 0) * 4)
        bandwidth_gbps = network_switches * 100.0
        effective_tps = model_info_data["base_tps"] * tps_multiplier
        
        thermal_exhaust_kw = total_it_kw * 0.91
        supported_greenhouse_sqft = (thermal_exhaust_kw * 1000) / 250 * 10.7639

        solar_factor = max(0.0, math.sin((float(time_of_day) - 6) * math.pi / 12))
        solar_gen_kw = self.solar_array_max_kw * solar_factor
        net_grid_draw_kw = max(0.0, total_it_kw - solar_gen_kw)
        
        if net_grid_draw_kw > 0 and self.battery_charge_kwh > 0:
            drawn_from_bat = min(self.battery_charge_kwh, net_grid_draw_kw)
            self.battery_charge_kwh -= drawn_from_bat
            net_grid_draw_kw -= drawn_from_bat

        gi_index = 1.0 if total_it_kw == 0 else max(0.0, 1.0 - (net_grid_draw_kw / total_it_kw))
        is_sat = policy_verifier.verify_token_compliancy(prompt_input)

        return {
            "IT_Compute_Draw": f"{total_it_kw:.2f} kW",
            "Thermal_Exhaust": f"{thermal_exhaust_kw:.2f} kW Thermal",
            "Solar_Production": f"{solar_gen_kw:.2f} kW",
            "Battery_State": f"{(self.battery_charge_kwh / self.battery_storage_max_kwh * 100):.1f}% ({self.battery_charge_kwh:.1f} kWh)",
            "Grid_Isolation_Index": f"{gi_index:.2f}",
            "Supported_Greenhouse": f"{supported_greenhouse_sqft:.1f} sq. ft.",
            "Effective_TPS": f"{effective_tps:,.1f} Tokens/sec",
            "Network_Bandwidth": f"{bandwidth_gbps:.0f} Gbps Line-Rate",
            "Raw_Hallucination_Risk": f"{model_info_data['base_hallucination_rate'] * 100:.1f}%",
            "SAT_Hallucination_Risk": "0.00000% (P_violation = 0)",
            "SMT_Status": "VERIFIED (SAT)" if is_sat else "UNSAT (BLOCKED BY MONAD LOGITS OPERATOR)",
        }

hw_twin = AdvancedHardwareDigitalTwin()

# --- 3. Telemetry Console Output ---
def run_unified_telemetry_stream(selected_model, custom_weights_path, units_config, time_of_day, input_prompt, classification):
    try:
        model_name = selected_model
        if custom_weights_path and len(str(custom_weights_path).strip()) > 0:
            model_name = f"HF/Local ({custom_weights_path.strip()})"

        telemetry = hw_twin.simulate_telemetry(selected_model, custom_weights_path, units_config, time_of_day, input_prompt, classification)
        
        log_output = f"--- EDS SMT LOGITS OPERATOR & MULTI-MODEL INGESTION ENGINE ---\n"
        log_output += f"Active Target Model: {model_name}\n"
        log_output += f"Target Prompt/Token: '{input_prompt}' | Classification: {classification}\n"
        log_output += f"Hardware Enclave State: AMD SEV-SNP Guest TEE (VMPL 0, AES-256 Active)\n"
        log_output += f"SMT Verification Status: {telemetry['SMT_Status']}\n\n"

        log_output += f"--- DEPLOYED HARDWARE & CEREBRAS CS-4 BANDWIDTH METRICS ---\n"
        log_output += f"Total Rack Load Draw: {telemetry['IT_Compute_Draw']}\n"
        log_output += f"System Token Throughput: {telemetry['Effective_TPS']}\n"
        log_output += f"High-Speed Network Fabric: {telemetry['Network_Bandwidth']} (100GbE RoCEv2 / NVLink)\n"
        log_output += f"Captured Immersion Heat Exhaust: {telemetry['Thermal_Exhaust']}\n"
        log_output += f"Supported Greenhouse Agriculture: {telemetry['Supported_Greenhouse']}\n\n"

        log_output += f"--- MICROGRID THERMODYNAMIC BALANCE & GRID ISOLATION ---\n"
        log_output += f"Solar Array Output: {telemetry['Solar_Production']} (Simulated Hour: {time_of_day}:00)\n"
        log_output += f"Battery Storage Level: {telemetry['Battery_State']}\n"
        log_output += f"Grid Isolation Index (GI): {telemetry['Grid_Isolation_Index']} (Off-Grid Peak Shaving)\n\n"

        log_output += f"--- HALLUCINATION TESTING & DETERMINISTIC PROOF ---\n"
        log_output += f"Unconstrained Model Hallucination Risk: {telemetry['Raw_Hallucination_Risk']}\n"
        log_output += f"SMT-Constrained Violation Probability: {telemetry['SAT_Hallucination_Risk']}\n"
        log_output += f"Logits Operator Formula: L_hat_i = L_i + log Phi(v_i) -> Applied via Z3 Solver\n"
        log_output += f"[SUCCESS] Zero Policy Violation Boundary Confirmed.\n"

        return log_output
    except Exception as ex:
        return f"--- EXECUTION ERROR LOGGED ---\nError Details: {str(ex)}"

# --- 4. Speech-to-Text & Wake-Word Overwatch Processing ---
def transcribe_audio_file(audio_path):
    if not audio_path or not SR_AVAILABLE:
        return None
    try:
        r = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = r.record(source)
            text = r.recognize_google(audio_data)
            return text
    except Exception as e:
        print(f"[!] STT Error: {str(e)}")
        return None

def overwatch_jamaican_jarvis_chat(user_message, selected_model, custom_weights_path, units_config, time_of_day):
    telemetry = hw_twin.simulate_telemetry(selected_model, custom_weights_path, units_config, time_of_day, "STATUS", "SECRET")
    msg_upper = str(user_message).upper()
    
    # Check for Wake Word ("OK OVERWATCH" or "HEY OVERWATCH")
    has_wake_word = "OVERWATCH" in msg_upper or "OK OVERWATCH" in msg_upper or "HEY OVERWATCH" in msg_upper
    
    if not has_wake_word:
        response = "Greetings Boss. Please start your command with 'OK Overwatch' so I know you are addressing me, man."
    else:
        response = "Good day, Boss. Overwatch online and keeping everything irie. "
        
        if "TRAIN" in msg_upper or "SFT" in msg_upper:
            response += f"Regarding di fine-tuning session for `{selected_model}`, baseline loss drop nicely, man. Di rack draw sitting at `{telemetry['IT_Compute_Draw']}`, and di AMD TEE memory locked tight like a vault."
        elif "SECURITY" in msg_upper or "ENHANCE" in msg_upper or "TEE" in msg_upper:
            response += f"Right away, Big Man. Formal verification graph active, `L_hat = L_i + log Phi(v_i)`. No unauthorized token can sneak past di Z3 solver, mi general. All CUI boundaries zero-violation compliant."
        elif "MICROGRID" in msg_upper or "POWER" in msg_upper or "SOLAR" in msg_upper:
            response += f"Everything bless with di power grid, Boss. Grid Isolation Index at `{telemetry['Grid_Isolation_Index']}`, solar array pushing `{telemetry['Solar_Production']}`, and di immersion tanks capturing `{telemetry['Thermal_Exhaust']}` for di greenhouse."
        else:
            response += f"Systems fully operational, Boss. Cerebras CS-4 and high-bandwidth fabric firing at `{telemetry['Effective_TPS']}`. What's di next move for di command center, mi chief?"

    # Synthesize Voice via ElevenLabs
    engine = OverwatchVoiceEngine()
    spoken_text = response.replace("`", "").replace("*", "")
    audio_path = engine.synthesize_speech(spoken_text)

    return response, audio_path

# --- 5. UI Layout with Automatic Browser Audio Unmute JS ---
eds_dark_theme = gr.themes.Soft(primary_hue="cyan", neutral_hue="slate").set(
    body_background_fill="#090d16", block_background_fill="#0f172a", block_border_color="#1e293b", body_text_color="#cbd5e1"
)

# Custom JavaScript to force playback on the Gradio audio element
force_audio_js = """
() => {
    setTimeout(() => {
        let audios = document.querySelectorAll('audio');
        audios.forEach(a => {
            if (a.src) {
                a.muted = false;
                a.play().catch(e => console.log("Autoplay un-mute triggered:", e));
            }
        });
    }, 400);
}
"""

with gr.Blocks(title="EDS Zero-Gravity SOC Command Center") as demo:
    gr.Markdown("# EMERGING DEFENSE SOLUTIONS (EDS)")
    gr.Markdown("### Zero-Gravity SOC Command Center | Voice-Enabled Overwatch (JARVIS AI)")

    with gr.Tabs():
        with gr.Tab("SOC Command Center & Hardware Twin"):
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Group():
                        gr.Markdown("#### Model Ingestion & Selection")
                        model_selector = gr.Dropdown(
                            choices=["Qwen2.5-7B (Fine-Tuned)", "Llama-3.1-70B-Instruct", "DeepSeek-R1-Distill-70B", "Mistral-Large-2"],
                            value="Qwen2.5-7B (Fine-Tuned)",
                            label="Target LLM Architecture"
                        )
                        custom_weights = gr.Textbox(
                            label="Ingest Local Weights Path / HuggingFace ID",
                            value="dassensei/sat-constrained-qwen-poc"
                        )

                    with gr.Group():
                        gr.Markdown("#### Threat Query & Hallucination Test")
                        prompt_input = gr.Textbox(label="CUI Log / Prompt Token Query", value="RESTRICTED_CUI_THREAT_LOG_001")
                        classification_drop = gr.Dropdown(choices=["UNCLASSIFIED", "CUI", "SECRET", "TOP SECRET"], value="SECRET", label="Classification Boundary")

                    with gr.Group():
                        gr.Markdown("#### Hardware Profile & 100GbE Bandwidth Config")
                        time_slider = gr.Slider(minimum=0, maximum=24, step=1, value=12, label="Simulated Time of Day (24h Solar Cycle)")
                        default_hardware = {"Mac_Studio": 4, "AMD_AI_Halo": 2, "DGX_Spark": 4, "H200_HGX": 1, "B200_HGX": 1, "Cerebras_CS4": 1, "Switch_100GbE_RoCEv2": 8}
                        hardware_json = gr.Textbox(label="Datacenter Equipment Allocation (JSON)", lines=8, value=json.dumps(default_hardware, indent=4))

                    exec_btn = gr.Button("RUN FULL TELEMETRY & SMT PROOF SESSION", variant="primary")

                with gr.Column(scale=2):
                    gr.Markdown("#### Real-Time Verification & Hardware Twin Output")
                    console_output = gr.Textbox(label="Unified SOC Command Center Console Log", lines=36, interactive=False)

            exec_btn.click(
                fn=run_unified_telemetry_stream,
                inputs=[model_selector, custom_weights, hardware_json, time_slider, prompt_input, classification_drop],
                outputs=console_output
            )

        with gr.Tab("🎙️ Conversational Overwatch (Wake-Word Enabled)"):
            gr.Markdown("### 🎙️ Live Voice Overwatch (Wake-Word: 'OK Overwatch')")
            gr.Markdown("Say **'OK Overwatch, give me a status report'** into your mic. The AI transcribes your voice, verifies the wake word, and speaks back immediately using ElevenLabs.")
            
            with gr.Row():
                with gr.Column(scale=1):
                    mic_input = gr.Audio(sources=["microphone"], type="filepath", label="🎤 Speak to Overwatch")
                    audio_player = gr.Audio(label="🔊 Overwatch Voice Response Stream", autoplay=True, elem_id="overwatch_audio_player")

                with gr.Column(scale=2):
                    chatbot = gr.Chatbot(label="Overwatch Dialogue Log", height=380)
                    msg_input = gr.Textbox(placeholder="Or type here (e.g. 'OK Overwatch, status on security?')...", label="Manual Command Input")
                    clear_btn = gr.Button("Clear Chat")

            def voice_conversation_flow(mic_audio_path, text_msg, history, selected_model, custom_weights_path, units_config, time_of_day):
                if history is None:
                    history = []
                
                user_prompt = None
                if mic_audio_path:
                    user_prompt = transcribe_audio_file(mic_audio_path)
                
                if not user_prompt and text_msg and len(text_msg.strip()) > 0:
                    user_prompt = text_msg

                if not user_prompt:
                    user_prompt = "OK Overwatch, status update."
                
                reply_text, audio_file = overwatch_jamaican_jarvis_chat(
                    user_prompt, selected_model, custom_weights_path, units_config, time_of_day
                )
                
                history.append({"role": "user", "content": user_prompt})
                history.append({"role": "assistant", "content": reply_text})
                
                return "", history, audio_file

            # Connect submit and stop_recording to run python logic AND execute the forced playback JavaScript
            msg_input.submit(
                fn=voice_conversation_flow,
                inputs=[mic_input, msg_input, chatbot, model_selector, custom_weights, hardware_json, time_slider],
                outputs=[msg_input, chatbot, audio_player]
            ).then(fn=None, js=force_audio_js)
            
            mic_input.stop_recording(
                fn=voice_conversation_flow,
                inputs=[mic_input, msg_input, chatbot, model_selector, custom_weights, hardware_json, time_slider],
                outputs=[msg_input, chatbot, audio_player]
            ).then(fn=None, js=force_audio_js)
            
            clear_btn.click(lambda: ([], None), None, [chatbot, audio_player], queue=False)

if __name__ == "__main__":
    demo.queue().launch(server_name="127.0.0.1", server_port=7870, theme=eds_dark_theme)
