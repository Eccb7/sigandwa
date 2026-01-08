#!/bin/bash

# Biblical Cliodynamics System - Stop Script

echo "Stopping Biblical Cliodynamics System..."

# Stop frontend
if [ -f logs/frontend.pid ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if kill -0 $FRONTEND_PID 2>/dev/null; then
        kill $FRONTEND_PID
        echo "✓ Frontend stopped"
    fi
    rm logs/frontend.pid
fi

# Stop backend
if [ -f logs/backend.pid ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if kill -0 $BACKEND_PID 2>/dev/null; then
        kill $BACKEND_PID
        echo "✓ Backend stopped"
    fi
    rm logs/backend.pid
fi

# Optionally stop databases
read -p "Stop databases (PostgreSQL, Neo4j)? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    docker-compose stop
    echo "✓ Databases stopped"
fi

echo "System stopped successfully"
