#!/bin/bash

echo "🧪 Testing Sigandwa LLM Integration"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if backend is running
echo -n "Checking if backend is running... "
if curl -s http://localhost:8000/api/v1/llm/model-info > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
else
    echo -e "${RED}✗${NC}"
    echo ""
    echo "❌ Backend is not running on port 8000"
    echo ""
    echo "Start it with:"
    echo "  cd backend"
    echo "  source ../venv/bin/activate"
    echo "  python -m uvicorn app.main:app --reload"
    exit 1
fi

echo ""
echo "📊 Model Information:"
echo "--------------------"
curl -s http://localhost:8000/api/v1/llm/model-info | python3 -m json.tool
echo ""

echo "💬 Testing Chat Endpoint:"
echo "------------------------"
echo "Question: 'When was the Exodus from Egypt?'"
echo ""

RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/llm/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "When was the Exodus from Egypt according to Ussher chronology? Give a brief answer.",
    "max_tokens": 200,
    "temperature": 0.7
  }')

echo "$RESPONSE" | python3 -m json.tool
echo ""

echo "📅 Testing Event Analysis:"
echo "-------------------------"
echo "Analyzing event ID 1 (Creation)..."
echo ""

EVENT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/v1/llm/analyze-event \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1
  }')

echo "$EVENT_RESPONSE" | python3 -m json.tool | head -30
echo ""

echo "✅ LLM Integration Tests Complete!"
echo ""
echo "Next steps:"
echo "1. Visit http://localhost:3000 to test the chat interface"
echo "2. Click the floating chat button (blue circle, bottom right)"
echo "3. Ask questions about Biblical history"
