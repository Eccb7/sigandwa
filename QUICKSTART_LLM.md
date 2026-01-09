# Sigandwa Local LLM - Quick Start

## What Was Added

✅ **Backend LLM Module** (`backend/app/llm/`)
- `config.py` - CPU-optimized configuration (Phi-2 model)
- `model_manager.py` - Model download and inference
- `prompt_templates.py` - Your custom Biblical prompts
- `api.py` - 4 REST endpoints
- `fine_tune.py` - Training data preparation script

✅ **Frontend Chat Interface** (`frontend/components/ChatInterface.tsx`)
- Floating chat button (bottom-right)
- Conversation history
- Beautiful UI with loading states

✅ **API Integration**
- Updated `main.py` to include LLM router
- Added CPU-only dependencies to `requirements.txt`
- Chat interface integrated in layout.tsx

## Installation (5 Minutes)

### Step 1: Install Python Dependencies

```bash
cd backend
pip install llama-cpp-python huggingface-hub
```

**Note**: This installs CPU-only versions. No GPU dependencies!

### Step 2: Start Backend

```bash
python -m uvicorn app.main:app --reload
```

On first API call, the model will auto-download (~1.5GB for Phi-2).

### Step 3: Test LLM

Open a new terminal:

```bash
# Check model status
curl http://localhost:8000/api/v1/llm/model-info

# Test chat
curl -X POST http://localhost:8000/api/v1/llm/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "When was the Exodus from Egypt?"
  }'
```

### Step 4: Start Frontend

```bash
cd frontend
npm run dev
```

Visit http://localhost:3000 and look for the blue chat button (bottom-right corner).

## Usage Examples

### Chat Interface (Frontend)

Click the floating blue button and ask:
- "When was the Exodus from Egypt?"
- "Explain Daniel's 70 weeks prophecy"
- "Who was King Josiah?"
- "What happened in 586 BC?"

### API Examples

#### 1. General Chat
```bash
curl -X POST http://localhost:8000/api/v1/llm/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain the year-day principle in Bible prophecy"
  }'
```

#### 2. Analyze Event
```bash
curl -X POST http://localhost:8000/api/v1/llm/analyze-event \
  -H "Content-Type: application/json" \
  -d '{"event_id": 42}'
```

#### 3. Interpret Prophecy
```bash
curl -X POST http://localhost:8000/api/v1/llm/interpret-prophecy \
  -H "Content-Type: application/json" \
  -d '{
    "prophecy_text": "Daniel 9:24-27",
    "context": "70 weeks prophecy"
  }'
```

#### 4. Ask Chronology Question
```bash
curl -X POST http://localhost:8000/api/v1/llm/ask-chronology \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Who were the kings of Judah during the divided kingdom?"
  }'
```

## Model Performance (CPU)

**Model**: Phi-2 (2.7B parameters, 4-bit quantized)
**Size**: ~1.5GB RAM
**Speed**: 40-60 tokens/second on modern CPU (8+ cores)
**Context**: 2048 tokens

### First Request
- Downloads model automatically (~1.5GB)
- Takes 1-2 minutes for first download
- Loads into memory (~30 seconds)

### Subsequent Requests
- Model stays loaded in memory
- Response time: 5-10 seconds for typical answer
- No internet required

## Training Data Preparation

Generate training dataset from your 7,440+ events:

```bash
cd backend
python -m app.llm.fine_tune
```

This creates:
- `training_data.json` - All examples
- `train.json` - Training set (90%)
- `val.json` - Validation set (10%)

**Data sources**:
- 7,440+ chronology events from database
- Prophecy interpretations
- Ussher's Annals text
- Daniel/Revelation commentary

## System Requirements

### Minimum
- **CPU**: 4+ cores
- **RAM**: 4GB available
- **Storage**: 2GB free (for model)
- **OS**: Linux, macOS, Windows

### Recommended
- **CPU**: 8+ cores
- **RAM**: 8GB available
- **Storage**: 5GB free
- **OS**: Linux (best performance)

## Troubleshooting

### Model won't download
```bash
# Check models directory
ls backend/models/

# If empty, manually download
cd backend
python -c "from app.llm.model_manager import ModelManager; from app.llm.config import LLMConfig; ModelManager(LLMConfig()).download_model(force=True)"
```

### Backend crashes (Out of Memory)
Edit `backend/app/llm/config.py`:
```python
model_name: str = "tinyllama"  # Smaller model (1GB instead of 1.5GB)
```

### Slow responses
This is normal on older CPUs. Options:
1. Use TinyLlama (faster but lower quality)
2. Reduce `max_tokens` in requests
3. Close other applications
4. Check CPU usage: `htop`

### Chat button not appearing
```bash
# Rebuild frontend
cd frontend
npm run build
npm run dev

# Check browser console (F12) for errors
```

### CORS errors
Make sure both servers are running:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000

## Configuration

Edit `backend/app/llm/config.py`:

```python
class LLMConfig(BaseModel):
    model_name: str = "phi-2"  # phi-2, tinyllama, or mistral-7b-instruct
    max_tokens: int = 512  # Reduce for faster responses
    temperature: float = 0.7  # 0.0-1.0 (lower = more deterministic)
    context_window: int = 2048  # Max conversation context
```

## API Documentation

Full API docs: http://localhost:8000/docs

Navigate to the **LLM** section to see all endpoints with interactive testing.

## What's Next?

1. ✅ **Basic Setup**: Install dependencies ← YOU ARE HERE
2. 🧪 **Test Chat**: Try the chat interface
3. 📚 **Prepare Training Data**: Run fine-tuning script
4. 🎯 **Customize**: Edit prompts in `prompt_templates.py`
5. 🚀 **Deploy**: Use in production

## Key Features

✅ **CPU-Optimized**: No GPU required, runs on any modern laptop  
✅ **Privacy**: All data stays on your server  
✅ **Free**: No API costs, no rate limits  
✅ **Offline**: Works without internet (after initial download)  
✅ **Biblical Expertise**: Custom prompts for Ussher chronology + historicism  
✅ **Customizable**: Fine-tune on your 7,440+ events  

## Support

- **Documentation**: `/docs/LLM_GUIDE.md`
- **API Docs**: http://localhost:8000/docs
- **Model Status**: http://localhost:8000/api/v1/llm/model-info

---

**Status**: ✅ Ready to install
**Model**: Phi-2 (CPU-optimized)
**Time to First Response**: ~2 minutes (includes download + load)
