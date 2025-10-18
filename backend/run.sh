#!/bin/bash

# Quick start script for Math Explanation Backend

set -e

echo "======================================"
echo "Math Explanation Backend - Quick Start"
echo "======================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if [ ! -f "venv/pyvenv.cfg" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found"
    echo "Creating .env from .env.example..."
    
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ .env file created"
        echo "⚠️  Please edit .env and add your API keys before running the server"
        exit 1
    else
        echo "❌ .env.example not found"
        exit 1
    fi
fi

# Create required directories
echo "Ensuring required directories exist..."
mkdir -p static/audio static/videos static/uploads

# Run the application
echo ""
echo "Starting Flask server..."
echo "======================================="
python app.py

