#!/bin/bash

echo "🚀 Setting up Sigandwa Local LLM (CPU-only)..."
echo ""

# Check if we're in the right directory
if [ ! -f "backend/app/main.py" ]; then
    echo "❌ Error: Please run this script from the sigandwa root directory"
    exit 1
fi

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Navigate to backend
cd backend

echo "📦 Installing Python dependencies for LLM..."
echo "   This will install:"
echo "   - llama-cpp-python (CPU version)"
echo "   - huggingface-hub"
echo "   - Additional dependencies"
echo ""

# Install CPU-only version of llama-cpp-python
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu

# Install other dependencies
pip install huggingface-hub datasets

# Create models directory
echo ""
echo "📁 Creating models directory..."
mkdir -p models
mkdir -p training_data

echo ""
echo "✅ Setup complete!"
echo ""
echo "📚 Next steps:"
echo ""
echo "1. Activate the virtual environment (if not already active):"
echo "   source venv/bin/activate"
echo ""
echo "2. Start the backend:"
echo "   cd backend"
echo "   python -m uvicorn app.main:app --reload"
echo ""
echo "3. The model will auto-download on first API call (~4GB)"
echo "   Default model: Mistral-7B-Instruct-v0.2 (4-bit quantized)"
echo ""
echo "4. Check model status:"
echo "   curl http://localhost:8000/api/v1/llm/model-info"
echo ""
echo "5. Test chat interface:"
echo "   Visit http://localhost:3000 and click the chat button"
echo ""
echo "⚠️  Note: First model download may take 5-10 minutes depending on internet speed"
