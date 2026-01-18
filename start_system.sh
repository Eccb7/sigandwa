#!/bin/bash

# Biblical Cliodynamics System - Complete Startup Script
# Phase 6: Frontend + Backend Integration

echo "═══════════════════════════════════════════════════════════════"
echo "  Biblical Cliodynamics Analysis System"
echo "  Complete System Startup"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo -e "${RED}Error: Must run from sigandwa project root${NC}"
    exit 1
fi

# Function to check if a service is running
check_service() {
    local service=$1
    local port=$2
    if nc -z localhost $port 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $service running on port $port"
        return 0
    else
        echo -e "${RED}✗${NC} $service not running on port $port"
        return 1
    fi
}

# Step 1: Check Prerequisites
echo -e "${BLUE}Step 1: Checking Prerequisites${NC}"
echo "─────────────────────────────────────"

if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 3 not found"
    exit 1
fi

if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓${NC} Node.js $NODE_VERSION"
else
    echo -e "${RED}✗${NC} Node.js not found"
    exit 1
fi

if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓${NC} Docker installed"
else
    echo -e "${RED}✗${NC} Docker not found"
    exit 1
fi

echo ""

# Step 2: Check Databases
echo -e "${BLUE}Step 2: Checking Databases${NC}"
echo "─────────────────────────────────────"

check_service "PostgreSQL" 5434
PG_STATUS=$?

check_service "Neo4j" 7687
NEO4J_STATUS=$?

if [ $PG_STATUS -ne 0 ] || [ $NEO4J_STATUS -ne 0 ]; then
    echo ""
    echo -e "${YELLOW}Starting databases with Docker Compose...${NC}"
    
    # Fix Docker iptables chains if they don't exist
    if ! sudo iptables -t filter -L DOCKER-ISOLATION-STAGE-2 &>/dev/null; then
        echo -e "${YELLOW}Fixing Docker iptables chains...${NC}"
        sudo iptables -t filter -N DOCKER-ISOLATION-STAGE-2 2>/dev/null || true
        sudo iptables -t filter -N DOCKER-ISOLATION-STAGE-1 2>/dev/null || true
        sudo systemctl restart docker
        sleep 3
    fi
    
    docker compose up -d
    
    # Wait for containers to be healthy
    echo "Waiting for databases to be ready..."
    for i in {1..30}; do
        check_service "PostgreSQL" 5434 &>/dev/null && check_service "Neo4j" 7687 &>/dev/null && break
        sleep 1
    done
    
    echo -e "${GREEN}✓${NC} Databases started"
fi

echo ""

# Step 3: Start Backend
echo -e "${BLUE}Step 3: Starting FastAPI Backend${NC}"
echo "─────────────────────────────────────"

if check_service "FastAPI" 8000; then
    echo -e "${YELLOW}Backend already running${NC}"
else
    echo "Starting backend..."
    cd backend
    
    # Use venv from parent directory
    if [ ! -d "../venv" ]; then
        echo "Creating virtual environment..."
        cd ..
        python3 -m venv venv
        cd backend
    fi
    
    cd ..
    source venv/bin/activate
    
    # Ensure logs directory exists
    mkdir -p logs
    
    # Start backend with correct PYTHONPATH
    export PYTHONPATH="$(pwd)/backend"
    nohup python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > logs/backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > logs/backend.pid
    
    sleep 5
    
    if check_service "FastAPI" 8000; then
        echo -e "${GREEN}✓${NC} Backend started (PID: $BACKEND_PID)"
    else
        echo -e "${RED}✗${NC} Failed to start backend. Check logs/backend.log"
        tail -n 20 logs/backend.log
        exit 1
    fi
fi

echo ""

# Step 4: Start Frontend
echo -e "${BLUE}Step 4: Starting Next.js Frontend${NC}"
echo "─────────────────────────────────────"

if check_service "Next.js" 3000; then
    echo -e "${YELLOW}Frontend already running${NC}"
else
    echo "Starting frontend..."
    cd frontend
    
    if [ ! -d "node_modules" ]; then
        echo "Installing dependencies..."
        npm install
    fi
    
    nohup npm run dev > ../logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../logs/frontend.pid
    
    sleep 5
    
    if check_service "Next.js" 3000; then
        echo -e "${GREEN}✓${NC} Frontend started (PID: $FRONTEND_PID)"
    else
        echo -e "${RED}✗${NC} Failed to start frontend"
        exit 1
    fi
    
    cd ..
fi

echo ""

# Step 5: System Status
echo -e "${BLUE}Step 5: System Status${NC}"
echo "─────────────────────────────────────"

check_service "PostgreSQL" 5434
check_service "Neo4j" 7687
check_service "FastAPI Backend" 8000
check_service "Next.js Frontend" 3000

echo ""

# Step 6: URLs
echo "═══════════════════════════════════════════════════════════════"
echo -e "${GREEN}System Ready!${NC}"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Access Points:"
echo "  • Frontend:        http://localhost:3000"
echo "  • Backend API:     http://localhost:8000"
echo "  • API Docs:        http://localhost:8000/docs"
echo "  • Neo4j Browser:   http://localhost:7474"
echo ""
echo "Logs:"
echo "  • Backend:  tail -f logs/backend.log"
echo "  • Frontend: tail -f logs/frontend.log"
echo ""
echo "Stop System:"
echo "  • ./stop_system.sh"
echo ""
echo "System Components:"
echo "  Phase 1: ✅ Database & Chronology (96 events)"
echo "  Phase 2: ✅ Pattern Recognition (6 patterns)"
echo "  Phase 3: ✅ Prophecy-Fulfillment (6 prophecies)"
echo "  Phase 4: ✅ Simulation Engine (25 indicators)"
echo "  Phase 5: ✅ Graph Analysis (108 nodes, 107 relationships)"
echo "  Phase 6: 🔄 Frontend Dashboard (In Progress)"
echo ""
echo "═══════════════════════════════════════════════════════════════"
