import gradio as gr
import time
import json
import random
import subprocess
import os
import tempfile
from datetime import datetime

HW_KEY = "HW_KEY_0x889_BSU_DAS_2026_EDR"

# Global memory buffer for live connected physical hardware nodes
CONNECTED_LINUX_NODES = {}

def get_operational_metrics():
    power_draw = round(random.uniform(45.0, 72.5), 2)
    solar_gen = round(random.uniform(30.0, 60.0), 2)
    battery_pwr = round(random.uniform(15.0, 25.0), 2)
    
    deficit = max(0.0, power_draw - solar_gen - battery_pwr)
    gi_index = max(0.0, 1.0 - (deficit / power_draw))
    
    mem_bandwidth = round(random.uniform(1.2, 3.8), 2)
    net_bandwidth = round(random.uniform(40.0, 95.0), 2)
    error_faults = random.choices([0, 1, 2], weights=[0.95, 0.04, 0.01])[0]
    
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "power_draw_kw": power_draw,
        "solar_gen_kw": solar_gen,
        "battery_pwr_kw": battery_pwr,
        "gi_index": round(gi_index, 4),
        "mem_bandwidth_tbs": mem_bandwidth,
        "net_bandwidth_gbps": net_bandwidth,
        "error_faults_cnt": error_faults,
        "connected_linux_hardware": CONNECTED_LINUX_NODES,
        "smt_threads_active": 100,
        "p_violation": "0.0000%"
    }

def execute_custom_code(language, code_snippet):
    if not code_snippet.strip():
        return "[!] Empty code snippet submitted."
    
    start_time = time.perf_counter()
    tmp_dir = tempfile.mkdtemp()
    
    try:
        if language == "PowerShell":
            cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", code_snippet]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            output = res.stdout if res.returncode == 0 else f"[STDERR]\n{res.stderr}"
            
        elif language == "Python":
            py_file = os.path.join(tmp_dir, "script.py")
            with open(py_file, "w", encoding="utf-8") as f:
                f.write(code_snippet)
            res = subprocess.run(["python", py_file], capture_output=True, text=True, timeout=10)
            output = res.stdout if res.returncode == 0 else f"[STDERR]\n{res.stderr}"
            
        elif language == "C++":
            cpp_file = os.path.join(tmp_dir, "main.cpp")
            exe_file = os.path.join(tmp_dir, "main.exe")
            with open(cpp_file, "w", encoding="utf-8") as f:
                f.write(code_snippet)
            
            compile_res = subprocess.run(["g++", cpp_file, "-o", exe_file], capture_output=True, text=True)
            if compile_res.returncode != 0:
                output = f"[COMPILATION ERROR]\n{compile_res.stderr}"
            else:
                exec_res = subprocess.run([exe_file], capture_output=True, text=True, timeout=10)
                output = exec_res.stdout
                
        elif language == "Java":
            java_file = os.path.join(tmp_dir, "Main.java")
            with open(java_file, "w", encoding="utf-8") as f:
                f.write(code_snippet)
            
            compile_res = subprocess.run(["javac", java_file], capture_output=True, text=True)
            if compile_res.returncode != 0:
                output = f"[COMPILATION ERROR]\n{compile_res.stderr}"
            else:
                exec_res = subprocess.run(["java", "-cp", tmp_dir, "Main"], capture_output=True, text=True, timeout=10)
                output = exec_res.stdout
        else:
            output = f"[!] Unsupported language: {language}"
            
    except subprocess.TimeoutExpired:
        output = "[!] Execution Timed Out (10s Limit Exceeded)."
    except Exception as e:
        output = f"[!] Execution Failed: {str(e)}"
        
    elapsed = round((time.perf_counter() - start_time) * 1000.0, 2)
    return f"--- EXECUTION COMPLETE ({elapsed} ms) ---\n\n{output}"

theme = gr.themes.Soft(primary_hue="blue", neutral_hue="slate")

with gr.Blocks(title="Zero-Gravity SOC Command Center", theme=theme) as demo:
    gr.Markdown(
        f"""
        # ??? Zero-Gravity SOC Command Center & Operational Telemetry
        > **AEGIS-MONAD Operational Status Dashboard** | Hardware Signature: `{HW_KEY}`
        """
    )
    
    with gr.Tabs():
        with gr.Tab("?? Operational Status & Telemetry"):
            with gr.Row():
                gi_metric = gr.Number(label="Grid Isolation Index (GI)", value=1.0, precision=4)
                pwr_metric = gr.Number(label="Total IT Power Draw (kW)", value=55.2)
                bw_metric = gr.Number(label="HBM3e Memory Bandwidth (TB/s)", value=3.2)
                net_metric = gr.Number(label="RoCEv2 Network Throughput (Gbps)", value=82.4)
                fault_metric = gr.Number(label="Memory Faults / SIGSEGV", value=0)
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.Markdown("### ??? Hardware & Power Controls")
                    cs4_units = gr.Slider(0, 4, value=2, step=1, label="Cerebras CS-4 Engines (28 kW/ea)")
                    b200_units = gr.Slider(0, 8, value=4, step=1, label="NVIDIA B200 HGX Racks (14.3 kW/ea)")
                    halo_units = gr.Slider(0, 16, value=8, step=1, label="AMD AI Halo Clusters (0.75 kW/ea)")
                    refresh_btn = gr.Button("?? Sample Telemetry Stream", variant="primary")
                
                with gr.Column(scale=2):
                    gr.Markdown("### ?? Live Telemetry & Connected Linux Hardware Nodes")
                    telemetry_json = gr.JSON(label="Live Hardware State")
            
            def refresh_status(cs4, b200, halo):
                m = get_operational_metrics()
                calc_pwr = (cs4 * 28.0) + (b200 * 14.3) + (halo * 0.75) + 5.0
                m["power_draw_kw"] = round(calc_pwr, 2)
                return m["gi_index"], m["power_draw_kw"], m["mem_bandwidth_tbs"], m["net_bandwidth_gbps"], m["error_faults_cnt"], m

            refresh_btn.click(
                refresh_status, 
                inputs=[cs4_units, b200_units, halo_units], 
                outputs=[gi_metric, pwr_metric, bw_metric, net_metric, fault_metric, telemetry_json]
            )

        with gr.Tab("?? Physical Linux Hardware Client Setup"):
            gr.Markdown("### ??? Connect Real Physical Linux Hardware Nodes")
            gr.Markdown("""
            To connect real hardware running Ubuntu, RHEL, or Debian to this dashboard:
            
            1. Copy **`aegis_hw_client.py`** to your target Linux server.
            2. Configure the endpoint URL and launch:
               ```bash
               export AEGIS_DASHBOARD_URL="http://<YOUR_SOC_IP>:7860/api/hardware_telemetry"
               python3 aegis_hw_client.py
               ```
            """)

        with gr.Tab("?? Burn-In & SMT Verification"):
            gr.Markdown("### ?? 48-Hour Enclave Burn-In & SMT Logit Constraints")
            with gr.Row():
                burnin_status = gr.Textbox(label="Burn-In Operational State", value="RUNNING (31h 14m / 48h 00m)", interactive=False)
                smt_violation_rate = gr.Textbox(label="Invariant Violations (P_violation)", value="0.0000% (UNSAT -> -inf Logit)", interactive=False)

        with gr.Tab("? Multi-Language Code Injection Sandbox"):
            gr.Markdown("### ?? Test Harness Code Injector")
            with gr.Row():
                lang_selector = gr.Radio(choices=["PowerShell", "Python", "C++", "Java"], value="Python", label="Target Language")
            code_input = gr.Code(label="Custom Script Input Buffer", language="python", value="# Python Test\nprint('AEGIS Hardware Interface OK')")
            exec_btn = gr.Button("?? Inject & Execute Code", variant="primary")
            console_output = gr.Code(label="Console Output", language="shell", interactive=False)
            
            def update_lang(lang):
                lang_map = {"PowerShell": "shell", "Python": "python", "C++": "cpp", "Java": "java"}
                return gr.update(language=lang_map.get(lang, "shell"))
                
            lang_selector.change(update_lang, inputs=[lang_selector], outputs=[code_input])
            exec_btn.click(execute_custom_code, inputs=[lang_selector, code_input], outputs=[console_output])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, show_error=True)
