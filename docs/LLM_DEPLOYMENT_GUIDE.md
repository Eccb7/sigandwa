# LLM Deployment & Training Guide

## 🚀 Model Persistence Across Systems

### 1. Model File Management

The LFM2-1.2B-RAG model file is located in:
```
backend/models/LFM2-1.2B-RAG-Q4_K_M.gguf (698 MB)
```

**To transfer to another system:**

#### Option A: Copy the model file directly
```bash
# From source system
tar -czf sigandwa-model.tar.gz backend/models/LFM2-1.2B-RAG-Q4_K_M.gguf

# Transfer to target system (via scp, rsync, etc.)
scp sigandwa-model.tar.gz user@target-server:/path/to/sigandwa/

# On target system
cd /path/to/sigandwa/
tar -xzf sigandwa-model.tar.gz
```

#### Option B: Use cloud storage
```bash
# Upload to cloud storage (S3, Google Cloud, etc.)
aws s3 cp backend/models/LFM2-1.2B-RAG-Q4_K_M.gguf \
  s3://your-bucket/models/

# Download on production server
aws s3 cp s3://your-bucket/models/LFM2-1.2B-RAG-Q4_K_M.gguf \
  backend/models/
```

#### Option C: Download from HuggingFace (if available)
```bash
# Run this script on any new system
cd backend
python3 << 'EOF'
from huggingface_hub import hf_hub_download
import os

os.makedirs('models', exist_ok=True)
model_path = hf_hub_download(
    repo_id='LiquidAI/LFM2-1.2B-RAG-GGUF',
    filename='LFM2-1.2B-RAG-Q4_K_M.gguf',
    local_dir='models',
    local_dir_use_symlinks=False
)
print(f'Model downloaded to: {model_path}')
EOF
```

---

## ⚙️ Production Configuration

### 1. Environment Variables

Create `.env.production` file:

```bash
# Production Database Configuration
POSTGRES_HOST=prod-db.example.com
POSTGRES_PORT=5432
POSTGRES_USER=sigandwa_prod
POSTGRES_PASSWORD=your-secure-password
POSTGRES_DB=sigandwa_prod

NEO4J_URI=bolt://prod-neo4j.example.com:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-secure-neo4j-password

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# Security
SECRET_KEY=generate-a-secure-random-key-here
ALGORITHM=HS256

# CORS (adjust for your production domain)
ALLOWED_ORIGINS=["https://yourdomain.com","https://api.yourdomain.com"]

# LLM Model Configuration
LLM_MODEL_NAME=lfm2-1.2b-rag
LLM_MODEL_PATH=/app/backend/models  # Absolute path in production
LLM_QUANTIZATION=Q4_K_M
LLM_MAX_TOKENS=512
LLM_TEMPERATURE=0.7
LLM_CONTEXT_WINDOW=2048
LLM_N_THREADS=16  # Use more threads in production

# Training Configuration
LLM_ENABLE_TRAINING=true
LLM_TRAINING_DATA_DIR=/app/data/training
LLM_LORA_RANK=16
LLM_LORA_ALPHA=32
LLM_LEARNING_RATE=0.0002
```

### 2. Docker Configuration for Production

Create `Dockerfile.production`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ backend/
COPY data/ data/
COPY docs/ docs/

# Create model directory
RUN mkdir -p backend/models

# Copy model file (or download in build process)
# COPY backend/models/LFM2-1.2B-RAG-Q4_K_M.gguf backend/models/

# Environment variables
ENV PYTHONPATH=/app/backend
ENV LLM_MODEL_PATH=/app/backend/models

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### 3. Docker Compose for Production

Update `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.production
    container_name: sigandwa_backend_prod
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_HOST=postgres
      - NEO4J_URI=bolt://neo4j:7687
    env_file:
      - .env.production
    volumes:
      - ./backend/models:/app/backend/models:ro  # Read-only model
      - ./data/training:/app/data/training  # Training data
    depends_on:
      - postgres
      - neo4j
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    container_name: sigandwa_postgres_prod
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_prod_data:/var/lib/postgresql/data
    restart: unless-stopped

  neo4j:
    image: neo4j:5.15-community
    container_name: sigandwa_neo4j_prod
    environment:
      NEO4J_AUTH: ${NEO4J_USER}/${NEO4J_PASSWORD}
    volumes:
      - neo4j_prod_data:/data
    restart: unless-stopped

volumes:
  postgres_prod_data:
  neo4j_prod_data:
```

---

## 📚 Training on More Data

### 1. Prepare Training Data

The system already has infrastructure for training. Here's how to add more data:

#### Add New Documents

```bash
# Add new biblical texts
cp your-new-document.txt docs/

# Update TrainingConfig in backend/app/llm/config.py
# Or use environment variables in .env:
LLM_TRAINING_CUSTOM_DOC_1=docs/your-new-document.txt
```

#### Generate Training Dataset

```bash
cd backend
python3 -m app.llm.fine_tune
```

This will:
- Extract data from chronology database (7,440+ events)
- Extract prophecy-fulfillment pairs
- Parse biblical documents
- Generate Q&A pairs in JSON format
- Save to `data/training/biblical_corpus.json`

### 2. Fine-tune the Model

Create a fine-tuning script `scripts/train_model.py`:

```python
#!/usr/bin/env python3
"""
Fine-tune LFM2 model on Biblical corpus using LoRA
"""
import json
from pathlib import Path
from llama_cpp import Llama
from app.llm.config import LLMConfig, TrainingConfig

def load_training_data():
    """Load prepared training data"""
    config = TrainingConfig()
    data_path = Path(config.data_dir) / "biblical_corpus.json"
    
    with open(data_path, 'r') as f:
        return json.load(f)

def fine_tune_model():
    """Fine-tune model with LoRA adapters"""
    llm_config = LLMConfig()
    training_config = TrainingConfig()
    
    print(f"Loading model from: {llm_config.model_path}")
    print(f"Training data from: {training_config.data_dir}")
    
    training_data = load_training_data()
    print(f"Loaded {len(training_data)} training examples")
    
    # Initialize model with LoRA training enabled
    # Note: This requires llama-cpp-python with training support
    # For full training, consider using llama.cpp directly or
    # frameworks like unsloth, axolotl, or transformers
    
    print("\n⚠️  For production fine-tuning, consider:")
    print("1. Using HuggingFace Transformers + PEFT (LoRA)")
    print("2. Using Unsloth for faster training")
    print("3. Using cloud GPUs (Colab, Runpod, Lambda Labs)")
    
    # Save adapter weights
    adapter_path = Path(llm_config.model_path) / "lora_adapters"
    adapter_path.mkdir(exist_ok=True)
    
    return adapter_path

if __name__ == "__main__":
    fine_tune_model()
```

### 3. Training with External Tools

#### Option A: Use Unsloth (Recommended for LoRA training)

```python
# Install unsloth
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"

# Training script
from unsloth import FastLanguageModel
import torch

# Load model
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="LiquidAI/LFM2-1.2B-RAG",
    max_seq_length=2048,
    dtype=None,
    load_in_4bit=True,
)

# Add LoRA adapters
model = FastLanguageModel.get_peft_model(
    model,
    r=16,  # LoRA rank
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_alpha=32,
    lora_dropout=0.1,
)

# Train on your data
# ... training loop ...

# Save adapters
model.save_pretrained("backend/models/lora_adapters")
tokenizer.save_pretrained("backend/models/lora_adapters")
```

#### Option B: Use HuggingFace Transformers + PEFT

```bash
pip install transformers peft datasets

# See scripts/training/train_with_peft.py for full example
```

### 4. Load Fine-tuned Model

Update model_manager.py to load LoRA adapters:

```python
# In model_manager.py load_model() method
adapter_path = self.model_path / "lora_adapters"
if adapter_path.exists():
    print(f"Loading LoRA adapters from {adapter_path}")
    self.model = Llama(
        model_path=model_path,
        lora_path=str(adapter_path),  # Load LoRA weights
        n_ctx=self.config.context_window,
        n_gpu_layers=0,
        n_threads=os.cpu_count() or 4,
    )
```

---

## 🔄 Continuous Training Pipeline

### 1. Automated Data Collection

```python
# scripts/collect_training_data.py
# Regularly update training data from:
# - New chronology events
# - User queries and responses
# - Biblical text additions
```

### 2. Periodic Retraining

```bash
# Cron job for monthly retraining
0 0 1 * * /path/to/sigandwa/scripts/retrain_model.sh
```

### 3. A/B Testing

- Keep multiple model versions
- Test new fine-tuned models against base model
- Gradually roll out improvements

---

## 📋 Checklist for Production Deployment

- [ ] Copy model file to production server (698 MB)
- [ ] Set environment variables in `.env.production`
- [ ] Configure absolute paths for model location
- [ ] Set appropriate thread count for production CPU
- [ ] Enable HTTPS and update CORS settings
- [ ] Set DEBUG=False
- [ ] Use strong SECRET_KEY
- [ ] Configure database connection pooling
- [ ] Set up model file backup strategy
- [ ] Document training data sources
- [ ] Set up monitoring for model inference latency
- [ ] Configure logging for model errors
- [ ] Test model loading on production environment

---

## 🛠️ Troubleshooting

### Model Not Found Error
```bash
# Verify model file exists
ls -lh backend/models/LFM2-1.2B-RAG-Q4_K_M.gguf

# Check permissions
chmod 644 backend/models/LFM2-1.2B-RAG-Q4_K_M.gguf
```

### Path Issues
```bash
# Set absolute path in .env
LLM_MODEL_PATH=/absolute/path/to/sigandwa/backend/models
```

### Memory Issues
```bash
# Reduce context window
LLM_CONTEXT_WINDOW=1024

# Reduce threads
LLM_N_THREADS=4
```

---

## 📞 Support

For issues or questions:
- Check logs: `tail -f logs/backend.log`
- Test model: `./scripts/test_llm.sh`
- API docs: http://localhost:8000/docs
