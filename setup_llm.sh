#!/bin/bash

echo "🚀 Setting up Sigandwa Local LLM (CPU-optimized)..."
echo ""

# Navigate to backend
cd backend

# Install dependencies
echo "📦 Installing Python dependencies (CPU-only)..."
pip install llama-cpp-python huggingface-hub

# Create models directory
mkdir -p models

echo ""
echo "✅ Setup complete!"
echo ""
echo "📥 The model (Phi-2, ~1.5GB) will be automatically downloaded on first API call"
echo ""
echo "🚀 Start the backend:"
echo "   cd backend"
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
