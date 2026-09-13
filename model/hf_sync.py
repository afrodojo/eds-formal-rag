# model/hf_sync.py - Hugging Face Hub Synchronization Engine
import os
import argparse
from huggingface_hub import HfApi, create_repo

class HuggingFaceSyncEngine:
    def __init__(self, token: str = None):
        self.token = token or os.getenv("HF_TOKEN")
        if not self.token:
            print("[!] Warning: HF_TOKEN environment variable not set. Write operations may fail.")
        self.api = HfApi(token=self.token)

    def create_repository(self, repo_id: str, repo_type: str = "model", private: bool = False):
        """Creates a repository on Hugging Face if it does not already exist."""
        try:
            url = create_repo(repo_id=repo_id, token=self.token, repo_type=repo_type, private=private, exist_ok=True)
            print(f"[SUCCESS] Target repository ready: {url}")
            return url
        except Exception as e:
            print(f"[!] Repository creation error: {str(e)}")
            return None

    def push_directory(self, local_dir: str, repo_id: str, repo_type: str = "model", commit_message: str = "Upload model artifacts"):
        """Uploads an entire local folder to the specified Hugging Face repository."""
        if not os.path.exists(local_dir):
            print(f"[!] Local directory '{local_dir}' does not exist.")
            return

        self.create_repository(repo_id=repo_id, repo_type=repo_type)

        print(f"[*] Uploading '{local_dir}' -> Hugging Face Repo: {repo_id}...")
        try:
            self.api.upload_folder(
                folder_path=local_dir,
                repo_id=repo_id,
                repo_type=repo_type,
                commit_message=commit_message
            )
            print(f"[SUCCESS] Folder '{local_dir}' successfully synced to Hugging Face repository '{repo_id}'!")
        except Exception as e:
            print(f"[!] Error uploading to Hugging Face: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hugging Face Synchronization Engine")
    parser.add_argument("--local-dir", type=str, default="data", help="Path to local directory to sync")
    parser.add_argument("--repo-id", type=str, default="dassensei/sat-constrained-qwen-poc", help="Hugging Face target repo ID")
    parser.add_argument("--repo-type", type=str, default="model", choices=["model", "dataset", "space"], help="Type of repository")
    args = parser.parse_args()

    engine = HuggingFaceSyncEngine()
    engine.push_directory(local_dir=args.local_dir, repo_id=args.repo_id, repo_type=args.repo_type)
