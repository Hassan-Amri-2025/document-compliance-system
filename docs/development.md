# Development Guide

## Setup Development Environment

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose
- Git

### Backend Development

1. **Create virtual environment:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Setup database:**
```bash
# Start PostgreSQL with Docker
docker-compose up -d postgres

# Run migrations
alembic upgrade head
```

4. **Start development server:**
```bash
uvicorn app.main:app --reload
```

### Frontend Development

1. **Install dependencies:**
```bash
cd frontend
npm install
```

2. **Start development server:**
```bash
npm start
```

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Code Quality

### Backend
```bash
# Format code
black .
isort .

# Type checking
mypy .

# Linting
flake8 .
```

### Frontend
```bash
# Linting
npm run lint

# Type checking
npm run type-check
```

## Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Environment Variables

See `.env.example` for all available configuration options.

## Architecture

The application follows a clean architecture pattern:

- **API Layer**: FastAPI routes and dependencies
- **Service Layer**: Business logic and orchestration
- **Data Layer**: SQLAlchemy models and database operations
- **Utils**: Shared utilities and helpers
