#!/bin/bash

# Document Compliance System - Installation Script
set -euo pipefail

echo "🔧 Installing Document Compliance System..."

# Check system requirements
echo "🔍 Checking system requirements..."

# Check memory (minimum 4GB)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    memory_gb=$(free -g | awk '/^Mem:/{print $2}')
elif [[ "$OSTYPE" == "darwin"* ]]; then
    memory_gb=$(( $(sysctl -n hw.memsize) / 1024 / 1024 / 1024 ))
fi

if [ "$memory_gb" -lt 4 ]; then
    echo "⚠️  Warning: System has ${memory_gb}GB RAM. Minimum 4GB recommended."
fi

# Install dependencies based on OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Detected Linux system"
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y git curl wget
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 Detected macOS system"
    if ! command -v brew &> /dev/null; then
        echo "📦 Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
fi

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker..."
    curl -fsSL https://get.docker.com | sh
fi

echo "✅ Installation dependencies ready!"
echo "🚀 Run ./scripts/quickstart.sh to start the application"
