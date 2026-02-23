#!/bin/bash

echo "Starting Disaster Relief Management System..."
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed or not in your PATH."
    echo ""
    echo "Starting Flask server directly..."
    cd backend
    python3 app.py
    exit
fi

echo "Starting with Node.js..."
node start.js 