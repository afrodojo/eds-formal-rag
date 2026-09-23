import json
import time
import os
from datetime import datetime

LOG_FILE = "notebook_sources/telemetry_metrics.json"

def log_telemetry_event(source, items_processed, elapsed_ms, failures, status):
    os.makedirs("notebook_sources", exist_ok=True)
    
    ingestion_rate = items_processed / (elapsed_ms / 1000.0) if elapsed_ms > 0 else 0
    
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "source": source, # e.g., 'HuggingFace', 'Render', 'Local_Harness'
        "items_processed": items_processed,
        "elapsed_ms": elapsed_ms,
        "ingestion_rate_per_sec": round(ingestion_rate, 2),
        "failures_detected": failures,
        "status": status,
        "hardware_key": "HW_KEY_0x889_BSU_DAS_2026_EDR"
    }
    
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except Exception:
            logs = []
            
    logs.append(entry)
    
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2)
        
    print(f"[TELEMETRY LOGGED] Source: {source} | Rate: {round(ingestion_rate, 2)} ops/s | Status: {status}")

if __name__ == "__main__":
    # Example baseline telemetry run
    log_telemetry_event("HuggingFace_Hub", 1500, 120.5, 0, "SUCCESS")
    log_telemetry_event("Render_Inference_Node", 500, 45.2, 0, "SUCCESS")
    log_telemetry_event("SMT_Monad_Evaluator", 2000, 180.0, 0, "PASSED_ZERO_VIOLATION")
