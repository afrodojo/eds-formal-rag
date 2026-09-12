from huggingface_hub import HfApi, create_repo
import os

class HuggingFaceSyncEngine:
    """
    Automates deployment of fine-tuned adapter weights and SMT datasets
    to the dassensei Hugging Face organization hub.
    """
    def __init__(self, repo_id: str = "dassensei/sat-constrained-qwen-poc"):
        self.repo_id = repo_id
        self.api = HfApi()

    def upload_model_checkpoints(self, local_folder: str = "./checkpoints"):
        if not os.path.exists(local_folder):
            print(f"Directory '{local_folder}' does not exist. Run model/train_sft.py first.")
            return

        print(f"Uploading fine-tuned checkpoints from '{local_folder}' to HF Repo '{self.repo_id}'...")
        self.api.upload_folder(
            folder_path=local_folder,
            repo_id=self.repo_id,
            repo_type="model",
            commit_message="feat: automated deployment of SMT-constrained Qwen adapter weights"
        )
        print("--- HUGGING FACE SYNC COMPLETE ---")

if __name__ == "__main__":
    sync_engine = HuggingFaceSyncEngine()
    print("Hugging Face Sync Engine Initialized for 'dassensei/sat-constrained-qwen-poc'.")
