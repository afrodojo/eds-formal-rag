# model/hf_sync.py - Syncs local model weights and constraints to Hugging Face Hub
import os
import sys
from huggingface_hub import HfApi, create_repo

def sync_repository(repo_id="dassensei/sat-constrained-qwen-poc", local_dir="."):
    """Pushes local project changes directly to Hugging Face Model Hub."""
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        print("[!] HF_TOKEN environment variable not set. Please log in via 'huggingface-cli login' or set HF_TOKEN.")
        return False

    api = HfApi()
    try:
        print(f"[*] Verifying repository target: {repo_id}")
        create_repo(repo_id=repo_id, token=hf_token, exist_ok=True, repo_type="model")
        
        print(f"[*] Uploading files from {local_dir} to Hugging Face Hub...")
        api.upload_folder(
            folder_path=local_dir,
            repo_id=repo_id,
            repo_type="model",
            token=hf_token,
            ignore_patterns=["*.git*", "__pycache__*", "*.vhdx", "*.tmp"]
        )
        print(f"[SUCCESS] Repository {repo_id} updated successfully on Hugging Face Hub.")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to sync with Hugging Face: {str(e)}")
        return False

if __name__ == "__main__":
    target_repo = sys.argv[1] if len(sys.argv) > 1 else "dassensei/sat-constrained-qwen-poc"
    sync_repository(repo_id=target_repo)
