#!/bin/bash

# Model Transfer Script
# Use this to package and transfer the model to another system

set -e

echo "═══════════════════════════════════════════════════════"
echo "  Sigandwa LLM Model Package & Transfer Tool"
echo "═══════════════════════════════════════════════════════"
echo ""

# Check if model exists
MODEL_FILE="backend/models/LFM2-1.2B-RAG-Q4_K_M.gguf"

if [ ! -f "$MODEL_FILE" ]; then
    echo "❌ Model file not found: $MODEL_FILE"
    exit 1
fi

# Package the model and configuration
PACKAGE_NAME="sigandwa-llm-$(date +%Y%m%d-%H%M%S).tar.gz"

echo "📦 Packaging model and configuration..."
echo ""

# Create package
tar -czf "$PACKAGE_NAME" \
    backend/models/LFM2-1.2B-RAG-Q4_K_M.gguf \
    backend/app/llm/config.py \
    backend/.env \
    .env

PACKAGE_SIZE=$(du -h "$PACKAGE_NAME" | cut -f1)

echo "✅ Package created: $PACKAGE_NAME"
echo "📏 Package size: $PACKAGE_SIZE"
echo ""

echo "🚀 Transfer Options:"
echo ""
echo "1️⃣  Copy to another server via SCP:"
echo "    scp $PACKAGE_NAME user@server:/path/to/destination/"
echo ""
echo "2️⃣  Upload to cloud storage:"
echo "    # AWS S3"
echo "    aws s3 cp $PACKAGE_NAME s3://your-bucket/models/"
echo ""
echo "    # Google Cloud"
echo "    gsutil cp $PACKAGE_NAME gs://your-bucket/models/"
echo ""
echo "3️⃣  Extract on target system:"
echo "    tar -xzf $PACKAGE_NAME"
echo ""
echo "4️⃣  Verify on target system:"
echo "    ls -lh backend/models/LFM2-1.2B-RAG-Q4_K_M.gguf"
echo ""

# Create a README for the package
cat > "MODEL_TRANSFER_README.txt" << 'EOF'
Sigandwa LLM Model Package
===========================

This package contains:
1. LFM2-1.2B-RAG model file (698 MB, Q4_K_M quantized)
2. Configuration files (.env)
3. LLM config module

Installation on Target System:
-------------------------------

1. Extract the package:
   tar -xzf sigandwa-llm-*.tar.gz

2. Install dependencies:
   cd backend
   pip install llama-cpp-python==0.3.16 huggingface-hub pydantic-settings

3. Test the model:
   python3 -c "
   from llama_cpp import Llama
   model = Llama(
       model_path='models/LFM2-1.2B-RAG-Q4_K_M.gguf',
       n_ctx=2048,
       n_gpu_layers=0,
       n_threads=4
   )
   print('Model loaded successfully!')
   "

4. Set environment variables (copy from .env):
   export LLM_MODEL_PATH=/absolute/path/to/backend/models
   export LLM_MODEL_NAME=lfm2-1.2b-rag

5. Start the application:
   ./start_system.sh

Requirements:
-------------
- Python 3.12+
- 2 GB RAM minimum (4 GB recommended)
- CPU with AVX2 support
- 1 GB disk space for model

For more details, see docs/LLM_DEPLOYMENT_GUIDE.md
EOF

echo "📄 Created MODEL_TRANSFER_README.txt with installation instructions"
echo ""
echo "✨ Package ready for transfer!"
