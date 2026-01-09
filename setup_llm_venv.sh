#!/bin/bash

echo "🚀 Setting up Sigandwa Local LLM (CPU-optimized)..."
echo ""

# Navigate to backend
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing LLM dependencies (CPU-only)..."
pip install --upgrade pip
pip install llama-cpp-python huggingface-hub

# Create models directory
mkdir -p models

echo ""
echo "✅ Setup complete!"
echo ""
echo "📥 The model (Phi-2, ~1.5GB) will be automatically downloaded on first API call"
echo ""
echo "🚀 To start the backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python -m uvicorn app.main:app --reload"
echo ""
echo "🔍 Check model status:"
echo "   curl http://localhost:8000/api/v1/llm/model-info"
echo ""
echo "💬 The chat interface will appear as a floating button on the frontend"
echo ""
echo "⚙️  System Info:"
echo "   CPU cores: $(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 'unknown')"
echo "   Model: Phi-2 (2.7B parameters, 4-bit quantized)"
echo "   Expected speed: 40-60 tokens/second on modern CPU"
echo ""
