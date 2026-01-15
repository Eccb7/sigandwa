#!/bin/bash

# Fix Docker iptables issues
# This script recreates Docker's iptables chains

echo "Fixing Docker iptables chains..."

# Stop Docker
sudo systemctl stop docker

# Clean up iptables
sudo iptables -t filter -F
sudo iptables -t filter -X
sudo iptables -t nat -F
sudo iptables -t nat -X

# Start Docker (it will recreate chains)
sudo systemctl start docker

# Wait for Docker to be ready
sleep 5

echo "Docker iptables chains fixed!"
