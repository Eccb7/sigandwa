"""
LLM Configuration
"""
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import BaseSettings
from pathlib import Path
import os


def get_default_model_path() -> str:
    """Get the absolute path to the models directory"""
    # Check for environment variable first
    if env_path := os.getenv("LLM_MODEL_PATH"):
        path = Path(env_path)
        if not path.is_absolute():
            # Relative to project root
            backend_dir = Path(__file__).parent.parent.parent
            path = backend_dir.parent / path
        return str(path.absolute())
    
    # Default: backend/models
    backend_dir = Path(__file__).parent.parent.parent
    models_dir = backend_dir / "models"
    return str(models_dir.absolute())


class LLMConfig(BaseSettings):
    """Configuration for local LLM with environment variable support"""
    model_config = ConfigDict(
        protected_namespaces=(),
        env_prefix="LLM_",
        env_file=".env",
        case_sensitive=False
    )
    
    model_name: str = Field(default="lfm2-1.2b-rag", description="Model identifier")
    model_path: str = Field(default_factory=get_default_model_path, description="Path to models directory")
    max_tokens: int = Field(default=512, description="Maximum tokens to generate")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    context_window: int = Field(default=2048, description="Context window size")
    device: str = Field(default="cpu", description="Device (cpu/cuda)")
    quantization: str = Field(default="Q4_K_M", description="Model quantization level")
    n_threads: int = Field(default=8, description="Number of CPU threads")
    
    # Fine-tuning config
    lora_rank: int = Field(default=16, description="LoRA rank for fine-tuning")
    lora_alpha: int = Field(default=32, description="LoRA alpha parameter")
    lora_dropout: float = Field(default=0.1, description="LoRA dropout rate")
    learning_rate: float = Field(default=2e-4, description="Learning rate for training")
    batch_size: int = Field(default=4, description="Training batch size")
    epochs: int = Field(default=3, description="Number of training epochs")
    enable_training: bool = Field(default=True, description="Enable training capabilities")


class TrainingConfig(BaseSettings):
    """Training dataset configuration with environment variable support"""
    model_config = ConfigDict(
        env_prefix="LLM_TRAINING_",
        env_file=".env",
        case_sensitive=False
    )
    
    # Biblical corpus sources
    ussher_annals: str = Field(default="./docs/James-Usher-Annals-of-the-World.txt")
    daniel_gems: str = Field(default="./docs/daniel_gems.txt")
    revelation_gems: str = Field(default="./docs/revelation_gems.txt")
    studies_daniel: str = Field(default="./docs/Studies-in-the-Book-of-Daniel.txt")
    data_dir: str = Field(default="data/training", description="Training data output directory")
    
    # Database sources
    use_chronology_db: bool = Field(default=True, description="Include chronology events")
    use_prophecy_db: bool = Field(default=True, description="Include prophecy data")
    use_patterns_db: bool = Field(default=True, description="Include pattern data")
    
    # Training parameters
    train_split: float = Field(default=0.9, ge=0.0, le=1.0)
    val_split: float = Field(default=0.1, ge=0.0, le=1.0)
    max_seq_length: int = Field(default=2048)
