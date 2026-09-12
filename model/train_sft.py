import os
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

class DefenseLLMTrainer:
    """
    Manages QLoRA (4-bit) Supervised Fine-Tuning (SFT) for domain-adapted defense LLMs
    to optimize token output generation for downstream SMT logic verification.
    """
    def __init__(self, model_id: str = "Qwen/Qwen2.5-7B-Instruct", output_dir: str = "./checkpoints"):
        self.model_id = model_id
        self.output_dir = output_dir

    def setup_qlora_config(self) -> tuple[BitsAndBytesConfig, LoraConfig]:
        """
        Configures NF4 4-bit quantization and LoRA adapter target modules.
        """
        # 4-bit Quantization Configuration for Exxact B200 / H200 Clusters
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
        )

        # LoRA Adapter Configuration targeted at Attention & MLP projections
        peft_config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM",
        )
        return bnb_config, peft_config

    def initialize_model_and_tokenizer(self):
        """
        Loads base model in 4-bit NF4 format and wraps it with LoRA adapters.
        """
        print(f"Loading Base Model: {self.model_id} in 4-bit NF4...")
        bnb_config, peft_config = self.setup_qlora_config()

        tokenizer = AutoTokenizer.from_pretrained(self.model_id, trust_remote_code=True)
        tokenizer.pad_token = tokenizer.eos_token

        # Load quantized base model
        model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True
        )

        # Prepare for k-bit training and apply LoRA adapters
        model = prepare_model_for_kbit_training(model)
        model = get_peft_model(model, peft_config)

        model.print_trainable_parameters()
        return model, tokenizer

    def get_training_args(self) -> TrainingArguments:
        """
        Sets hyperparameter configuration optimized for multi-GPU HGX clusters.
        """
        return TrainingArguments(
            output_dir=self.output_dir,
            per_device_train_batch_size=4,
            gradient_accumulation_steps=4,
            warmup_ratio=0.03,
            max_steps=100,
            learning_rate=2e-4,
            fp16=False,
            bf16=True,
            logging_steps=10,
            save_strategy="steps",
            save_steps=50,
            optim="paged_adamw_8bit",
            report_to="none"
        )

if __name__ == "__main__":
    print("--- EDS DEFENSE LLM QLoRA FINE-TUNING PIPELINE ---")
    trainer_engine = DefenseLLMTrainer()
    bnb_cfg, lora_cfg = trainer_engine.setup_qlora_config()
    print("QLoRA Configuration Successfully Initialized.")
    print(f"LoRA Rank (r): {lora_cfg.r} | Target Modules: {lora_cfg.target_modules}")
