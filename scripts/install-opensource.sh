#!/bin/bash

# Installation script for open-source version

set -euo pipefail

echo "Installing Document Compliance System (Open Source Version)..."

# Install system dependencies
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Installing Linux dependencies..."
    sudo apt-get update
    sudo apt-get install -y \
        tesseract-ocr \
        tesseract-ocr-eng \
        tesseract-ocr-ara \
        poppler-utils \
        python3-pip \
        python3-venv
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Installing macOS dependencies..."
    brew install tesseract poppler
fi

# Setup Python environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r backend/requirements.txt

# Create directories
mkdir -p uploads/{templates,documents,certified,reports,visualizations,temp}

# Setup environment
cp .env.example .env
echo "Please edit .env file with your configuration"

echo "Installation complete!"
echo "To start the application:"
echo "1. Edit .env file"
echo "2. Run: docker-compose up -d"
echo "3. Access at: http://localhost:3000"
