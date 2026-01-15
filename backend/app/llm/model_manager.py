"""
Model download, loading, and inference management (CPU-optimized)
"""
import os
from pathlib import Path
from typing import Optional, Dict, Any
from llama_cpp import Llama
from huggingface_hub import hf_hub_download
from .config import LLMConfig


class ModelManager:
    """Manages local LLM model lifecycle (CPU-optimized)"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.model: Optional[Llama] = None
        self.model_path = Path(config.model_path)
        self.model_path.mkdir(parents=True, exist_ok=True)
    
    def download_model(self, force: bool = False) -> str:
        """
        Download model from HuggingFace if not exists
        
        CPU-optimized models:
        - LiquidAI/LFM2-1.2B-RAG-GGUF (1.2B, optimized for RAG tasks)
        - TheBloke/phi-2-GGUF (2.7B, excellent for CPU)
        - TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF (1.1B, very fast)
        - TheBloke/Mistral-7B-Instruct-v0.2-GGUF (7B, slower but better quality)
        """
        # Map model name to filename
        filename_map = {
            "lfm2-1.2b-rag": f"LFM2-1.2B-RAG-{self.config.quantization}.gguf",
            "phi-2": f"phi-2.{self.config.quantization}.gguf",
            "tinyllama": f"tinyllama-1.1b-chat-v1.0.{self.config.quantization}.gguf",
            "mistral-7b-instruct": f"mistral-7b-instruct-v0.2.{self.config.quantization}.gguf",
        }
        model_filename = filename_map.get(self.config.model_name, f"{self.config.model_name}.{self.config.quantization}.gguf")
        local_path = self.model_path / model_filename
        
        if local_path.exists() and not force:
            print(f"✅ Model already exists: {local_path}")
            return str(local_path)
        
        print(f"📥 Downloading {self.config.model_name} (CPU-optimized)...")
        print(f"   This may take a few minutes (model size: ~1-2GB)")
        
        # Map model names to HuggingFace repos (CPU-friendly models)
        model_repos = {
            "lfm2-1.2b-rag": "LiquidAI/LFM2-1.2B-RAG-GGUF",
            "phi-2": "TheBloke/phi-2-GGUF",
            "tinyllama": "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
            "mistral-7b-instruct": "TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
        }
        
        repo_id = model_repos.get(self.config.model_name, "LiquidAI/LFM2-1.2B-RAG-GGUF")
        
        try:
            # Download from HuggingFace
            downloaded_path = hf_hub_download(
                repo_id=repo_id,
                filename=model_filename,
                local_dir=str(self.model_path),
                local_dir_use_symlinks=False
            )
            
            print(f"✅ Downloaded to: {downloaded_path}")
            return downloaded_path
        except Exception as e:
            print(f"❌ Download failed: {e}")
            print(f"   Please manually download from: https://huggingface.co/{repo_id}")
            raise
    
    def load_model(self) -> None:
        """Load model into memory (CPU-optimized)"""
        model_path = self.download_model()
        
        print(f"🔄 Loading model from {model_path}...")
        print(f"   Using CPU with {os.cpu_count() or 4} threads")
        
        self.model = Llama(
            model_path=model_path,
            n_ctx=self.config.context_window,
            n_gpu_layers=0,  # CPU only - no GPU layers
            n_threads=os.cpu_count() or 4,  # Use all CPU cores
            n_batch=512,  # Batch size for CPU
            verbose=False
        )
        
        print(f"✅ Model loaded successfully (CPU mode)")
    
    def generate(
        self, 
        prompt: str, 
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        stop: Optional[list] = None
    ) -> str:
        """Generate text from prompt"""
        if not self.model:
            self.load_model()
        
        try:
            response = self.model(
                prompt,
                max_tokens=max_tokens or self.config.max_tokens,
                temperature=temperature or self.config.temperature,
                stop=stop or ["</s>", "Human:", "User:"],
                echo=False
            )
            return response["choices"][0]["text"].strip()
        except Exception as e:
            # If decode fails, reset the model and try again with shorter context
            print(f"Generation error: {e}. Resetting model...")
            self.model.reset()
            # Try again with much shorter prompt
            short_prompt = prompt[-1500:] if len(prompt) > 1500 else prompt
            response = self.model(
                short_prompt,
                max_tokens=256,  # Reduce tokens
                temperature=temperature or self.config.temperature,
                stop=stop or ["</s>", "Human:", "User:"],
                echo=False
            )
            return response["choices"][0]["text"].strip()
    
    def chat(self, messages: list[Dict[str, str]]) -> str:
        """Chat interface with conversation history"""
        # Format messages into prompt
        prompt = self._format_chat_prompt(messages)
        
        # Reset model context for each new conversation to avoid decode errors
        if self.model:
            try:
                self.model.reset()
            except:
                pass  # Some models may not support reset
                
        return self.generate(prompt)
    
    def _format_chat_prompt(self, messages: list[Dict[str, str]]) -> str:
        """Format chat messages into model-specific prompt format"""
        # LiquidAI LFM2 format (instruction-tuned for RAG)
        # Falls back to simple instruction format for other models
        formatted = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                formatted += f"System: {content}\n\n"
            elif role == "user":
                formatted += f"User: {content}\n\nAssistant:"
            elif role == "assistant":
                formatted += f" {content}\n\n"
        return formatted
