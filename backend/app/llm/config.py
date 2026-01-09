"""
LLM Configuration
"""
from typing import Optional
from pydantic import BaseModel, ConfigDict


class LLMConfig(BaseModel):
    """Configuration for local LLM"""
    model_config = ConfigDict(protected_namespaces=())
    
    model_name: str = "phi-2"  # Smaller model for CPU (2.7B params, fast on CPU)
    model_path: str = "./models"
    max_tokens: int = 512
    temperature: float = 0.7
    context_window: int = 2048
    device: str = "cpu"  # CPU only
    quantization: str = "Q4_K_M"  # 4-bit quantization for efficiency
    
    # Fine-tuning config (if needed later)
    lora_rank: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.1
    learning_rate: float = 2e-4
    batch_size: int = 4
    epochs: int = 3


class TrainingConfig(BaseModel):
    """Training dataset configuration"""
    # Biblical corpus sources
    ussher_annals: str = "./docs/James-Usher-Annals-of-the-World.txt"
    daniel_gems: str = "./docs/daniel_gems.txt"
    revelation_gems: str = "./docs/revelation_gems.txt"
    
    # Database sources
    use_chronology_db: bool = True
    use_prophecy_db: bool = True
    use_patterns_db: bool = True
    
    # Training parameters
    train_split: float = 0.9
    val_split: float = 0.1
    max_seq_length: int = 2048
