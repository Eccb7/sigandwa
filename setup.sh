#!/bin/bash

# Sigandwa Setup Script
# Initializes the development environment

set -e

echo "=================================================="
echo "Sigandwa: Biblical Cliodynamic Analysis System"
echo "Setup Script"
echo "=================================================="
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 is required but not installed."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "✗ Docker is required but not installed."
    exit 1
fi

echo "✓ Docker found: $(docker --version)"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo "⚠ Please review .env and update values as needed"
fi

# Create virtual environment
echo ""
echo "Creating Python virtual environment..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Go back to root
cd ..

# Start Docker containers
echo ""
echo "Starting database containers..."
docker-compose up -d
echo "✓ Databases starting (PostgreSQL and Neo4j)"

# Wait for databases
echo ""
echo "Waiting for databases to be ready..."
sleep 10

# Run migrations
echo ""
echo "Running database migrations..."
cd backend
alembic upgrade head
echo "✓ Migrations applied"

# Seed database
echo ""
echo "Seeding chronology database..."
cd ../data/seed
python seed_db.py
echo "✓ Database seeded"

cd ../..

echo ""
echo "=================================================="
echo "✓ Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Start the API server:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
echo "2. Access the API:"
echo "   - API: http://localhost:8000"
echo "   - Docs: http://localhost:8000/docs"
echo ""
echo "3. Access databases:"
echo "   - PostgreSQL: localhost:5432"
echo "   - Neo4j Browser: http://localhost:7474"
echo ""
echo "=================================================="
