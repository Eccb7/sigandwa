# LLM Model Persistence & Training - Quick Reference

## 📦 Package Model for Transfer

```bash
./scripts/package_model.sh
```
This creates a tarball containing:
- Model file (698 MB)
- Configuration files
- Environment settings

## 🚀 Deploy to Production Server

### 1. Transfer the Package
```bash
# Copy package to production server
scp sigandwa-llm-*.tar.gz user@prod-server:/opt/sigandwa/

# Or use cloud storage
aws s3 cp sigandwa-llm-*.tar.gz s3://your-bucket/
```

### 2. Extract on Production
```bash
cd /opt/sigandwa
tar -xzf sigandwa-llm-*.tar.gz
```

### 3. Configure Environment
```bash
# Copy and edit production config
cp .env.production.example .env.production
nano .env.production

# Set absolute paths
export LLM_MODEL_PATH=/opt/sigandwa/backend/models
```

### 4. Install Dependencies
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Start Application
```bash
./start_system.sh
```

## 🎓 Train Model on More Data

### 1. Add New Documents
```bash
# Copy your biblical texts to docs/ folder
cp your-document.txt docs/

# Or update environment variable
export LLM_TRAINING_CUSTOM_DOC=docs/your-document.txt
```

### 2. Generate Training Dataset
```bash
# Generate training data from database + documents
python3 scripts/generate_training_data.sh

# Output: data/training/biblical_corpus.json
```

### 3. Fine-tune with LoRA (Recommended)

**Option A: Quick Setup (Colab/Local)**
```python
# Install unsloth for fast training
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"

# Load and train
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="LiquidAI/LFM2-1.2B-RAG",
    load_in_4bit=True
)

model = FastLanguageModel.get_peft_model(
    model, r=16, lora_alpha=32
)

# Train on your data
# ... (see docs/LLM_DEPLOYMENT_GUIDE.md)

# Save adapters
model.save_pretrained("backend/models/lora_adapters")
```

**Option B: Production Training Pipeline**
```bash
# Schedule periodic retraining
crontab -e

# Add monthly retraining
0 0 1 * * /opt/sigandwa/scripts/retrain_model.sh
```

## 🔍 Verify Model on New System

```bash
# Test model loading
cd backend
python3 << 'EOF'
from llama_cpp import Llama
model = Llama(
    model_path='models/LFM2-1.2B-RAG-Q4_K_M.gguf',
    n_ctx=2048,
    n_gpu_layers=0,
    n_threads=4
)
response = model.create_chat_completion(
    messages=[{'role': 'user', 'content': 'Test'}],
    max_tokens=50
)
print('✅ Model works!', response['choices'][0]['message']['content'])
EOF
```

## 📊 Monitor Model Performance

```bash
# Check model status
curl http://localhost:8000/api/v1/llm/model-info

# Test inference
curl -X POST http://localhost:8000/api/v1/llm/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "When was the Exodus?", "max_tokens": 150}'

# View logs
tail -f logs/backend.log
```

## 🛠️ Troubleshooting

### Model Not Found
```bash
# Check file exists
ls -lh backend/models/LFM2-1.2B-RAG-Q4_K_M.gguf

# Set absolute path
export LLM_MODEL_PATH=/absolute/path/to/backend/models
```

### Memory Issues
```bash
# Reduce context window
export LLM_CONTEXT_WINDOW=1024

# Reduce threads
export LLM_N_THREADS=4
```

### Permission Denied
```bash
# Fix permissions
chmod 644 backend/models/*.gguf
chown $USER:$USER backend/models/*.gguf
```

## 📚 Key Files

- **Model**: `backend/models/LFM2-1.2B-RAG-Q4_K_M.gguf` (698 MB)
- **Config**: `backend/app/llm/config.py`
- **Environment**: `.env` or `.env.production`
- **Training Data**: `data/training/biblical_corpus.json`
- **Documentation**: `docs/LLM_DEPLOYMENT_GUIDE.md`

## 🔐 Security Checklist for Production

- [ ] Change all default passwords
- [ ] Generate new SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure HTTPS/SSL
- [ ] Update CORS origins
- [ ] Use environment variables (not hardcoded values)
- [ ] Restrict database access
- [ ] Set up firewall rules
- [ ] Enable rate limiting
- [ ] Configure backup strategy

## 💡 Best Practices

1. **Version Control**: Tag model versions (v1.0, v1.1, etc.)
2. **Backup**: Keep model file backups in cloud storage
3. **Monitoring**: Track inference latency and errors
4. **Updates**: Periodically retrain with new data
5. **Testing**: A/B test new models before full deployment
6. **Documentation**: Document training data sources and changes

---

📖 **Full Documentation**: See `docs/LLM_DEPLOYMENT_GUIDE.md`
🧪 **Test Suite**: Run `./scripts/test_llm.sh`
📦 **Package Tool**: Run `./scripts/package_model.sh`
