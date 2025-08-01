# Document Compliance & Certification System

A comprehensive AI-powered system for validating student documents against administrator-uploaded templates using advanced computer vision and machine learning techniques.

## Features

- **Template Management**: Upload and analyze document templates
- **Document Validation**: AI-powered comparison against templates
- **Visual Comparison**: SSIM, perceptual hashing, and layout analysis
- **Automated Certification**: Generate certified PDFs with QR codes
- **Real-time Processing**: Asynchronous document processing with Celery
- **Role-based Access**: Admin, Reviewer, and Student roles
- **RESTful API**: Comprehensive API with OpenAPI documentation

## Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Primary database
- **Redis**: Caching and message broker
- **Celery**: Distributed task queue
- **Azure Document Intelligence**: OCR and layout analysis
- **LayoutParser**: Document layout analysis
- **OpenCV & PIL**: Image processing

### Frontend
- **React 18**: Modern React with hooks
- **TypeScript**: Type-safe JavaScript
- **Material-UI**: React component library
- **Redux Toolkit**: State management
- **React Router**: Client-side routing

### Infrastructure
- **Docker**: Containerization
- **Kubernetes**: Container orchestration
- **Azure**: Cloud platform
- **Prometheus**: Monitoring and metrics

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Node.js 18+
- Azure Document Intelligence API key

### One-Command Installation

```bash
# Quick installation (recommended)
curl -fsSL https://raw.githubusercontent.com/$GITHUB_USER/$PROJECT_NAME/main/scripts/quickstart.sh | bash
```

### Manual Setup

1. Clone the repository:
```bash
git clone https://github.com/$GITHUB_USER/$PROJECT_NAME.git
cd $PROJECT_NAME
```

2. Copy environment variables:
```bash
cp .env.example .env
```

3. Update `.env` with your configuration:
```bash
# Azure Document Intelligence
AZURE_DOCUMENT_INTELLIGENCE_KEY=your-azure-key
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=your-azure-endpoint

# Database
DB_PASSWORD=your-secure-password

# Security
SECRET_KEY=your-very-secure-secret-key
```

### Development Setup

#### Using Docker Compose (Recommended)
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

#### Manual Setup

##### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Setup database
alembic upgrade head

# Run development server
uvicorn app.main:app --reload
```

##### Frontend
```bash
cd frontend
npm install
npm start
```

### Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432

## API Documentation

The API documentation is available at `/docs` when running the backend server.

### Key Endpoints

- `POST /api/v1/auth/login` - User authentication
- `POST /api/v1/templates/` - Create template
- `POST /api/v1/documents/upload` - Upload document
- `POST /api/v1/validation/validate` - Validate document

## Deployment

### Docker Production

```bash
# Build and start production containers
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/
```

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │  FastAPI Backend │    │  Azure Services │
│                 │────│                 │────│                 │
│  - Material-UI  │    │  - Authentication│    │  - Doc Intelligence│
│  - Redux        │    │  - File Upload   │    │  - Blob Storage │
│  - TypeScript   │    │  - Validation    │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       
         │              ┌─────────────────┐              
         │              │   PostgreSQL    │              
         │              │   + Redis       │              
         └──────────────│   Database      │              
                        └─────────────────┘              
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, create an issue in the GitHub repository.

## Version 2.0 - Open Source Edition

This version removes all Azure dependencies and uses open-source alternatives:

- **Tesseract OCR** instead of Azure Document Intelligence
- **LayoutParser** for document layout analysis
- **Local file storage** instead of Azure Blob Storage
- **OpenCV & PIL** for image processing

### New Features

- No cloud dependencies required
- Completely free and open-source
- Easier deployment and setup
- Support for multiple OCR languages
- Local file storage with organized structure

### Migration from Azure Version

If you're migrating from the Azure version:

1. Back up your data
2. Update environment variables (remove Azure keys)
3. Run database migrations
4. Reprocess documents with new OCR engine

