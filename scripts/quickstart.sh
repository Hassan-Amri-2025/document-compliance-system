#!/bin/bash

echo "🚀 Document Compliance System - Quick Start"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    
    # Generate secure secret key
    if command -v openssl &> /dev/null; then
        SECRET_KEY=$(openssl rand -hex 32)
        sed -i.bak "s/your-very-secret-key-here-minimum-32-characters/$SECRET_KEY/g" .env
    fi
    
    echo "⚠️  Please update .env file with your Azure Document Intelligence credentials:"
    echo "   - AZURE_DOCUMENT_INTELLIGENCE_KEY"
    echo "   - AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT"
    echo ""
    read -p "Press Enter after updating .env file to continue..."
fi

# Create upload directories
echo "📁 Creating upload directories..."
mkdir -p uploads/{templates,documents,certified,reports,visualizations,temp}

# Start the application
echo "🚀 Starting Document Compliance System..."
docker-compose up -d

echo ""
echo "✅ Application started successfully!"
echo "📍 Access points:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - API Documentation: http://localhost:8000/docs"
echo ""
echo "📋 Useful commands:"
echo "   - View logs: docker-compose logs -f"
echo "   - Stop services: docker-compose down"
echo "   - Restart services: docker-compose restart"
echo ""
echo "🎉 Happy document processing!"
