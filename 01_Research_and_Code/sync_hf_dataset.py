import os
import json
import pandas as pd
from datetime import datetime
from huggingface_hub import HfApi, create_repo

# Configuration
LOCAL_JSON_PATH = "notebook_sources/telemetry_metrics.json"
LOCAL_PARQUET_PATH = "notebook_sources/telemetry_traces.parquet"

# Set your dataset ID (e.g., 'username/aegis-monad-telemetry')
HF_DATASET_ID = os.getenv("HF_DATASET_ID", "asaadmorman/aegis-monad-telemetry")
HF_TOKEN = os.getenv("HF_TOKEN")  # Write token from Hugging Face settings

def sync_telemetry_to_huggingface():
    print("[+] Initializing Hugging Face Telemetry Sync...")
    print(f"[+] Target Dataset Repository: {HF_DATASET_ID}")
    
    if not HF_TOKEN:
        print("[!] ERROR: HF_TOKEN environment variable is not set. Skipping upload.")
        return

    if not os.path.exists(LOCAL_JSON_PATH):
        print(f"[!] WARNING: Local telemetry file '{LOCAL_JSON_PATH}' not found. Nothing to sync.")
        return

    # 1. Read JSON log and convert to Pandas DataFrame
    try:
        with open(LOCAL_JSON_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if not data:
            print("[!] Telemetry JSON is empty. Skipping upload.")
            return

        df = pd.DataFrame(data)
        df["synced_at"] = datetime.utcnow().isoformat()
        
        # Save as compressed Parquet for high-efficiency dataset storage
        df.to_parquet(LOCAL_PARQUET_PATH, index=False)
        print(f"[+] Converted {len(df)} telemetry trace records to Parquet format.")
    except Exception as e:
        print(f"[!] Failed to convert telemetry data: {e}")
        return

    # 2. Authenticate and ensure private dataset repo exists
    api = HfApi(token=HF_TOKEN)
    try:
        create_repo(
            repo_id=HF_DATASET_ID,
            repo_type="dataset",
            private=True,
            exist_ok=True,
            token=HF_TOKEN
        )
        print(f"[+] Verified private repository '{HF_DATASET_ID}' on Hugging Face.")
    except Exception as e:
        print(f"[!] Repository creation/verification warning: {e}")

    # 3. Upload file to HF Dataset repository
    try:
        api.upload_file(
            path_or_fileobj=LOCAL_PARQUET_PATH,
            path_in_repo="telemetry_traces.parquet",
            repo_id=HF_DATASET_ID,
            repo_type="dataset",
            commit_message=f"auto-sync: update SMT telemetry traces ({len(df)} records)"
        )
        print("[SUCCESS] SMT Telemetry traces successfully pushed to Hugging Face!")
    except Exception as e:
        print(f"[!] Failed to upload to Hugging Face Hub: {e}")

if __name__ == "__main__":
    sync_telemetry_to_huggingface()
