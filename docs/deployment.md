# Deployment Guide

## Production Deployment Options

### Option 1: Docker Compose (Recommended for Small Scale)

1. **Prepare production environment:**
```bash
cp .env.example .env.prod
# Update .env.prod with production values
```

2. **Deploy:**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Option 2: Kubernetes (Recommended for Scale)

1. **Setup Kubernetes cluster** (e.g., EKS, GKE, AKS)

2. **Deploy:**
```bash
kubectl apply -f k8s/
```

### Option 3: Cloud Platform (Azure, AWS, GCP)

Deploy using cloud-specific services:
- **Container Registry**: Push Docker images
- **Container Service**: Deploy containers
- **Database Service**: Managed PostgreSQL
- **Cache Service**: Managed Redis
- **Storage**: Blob storage for files

## Environment Configuration

### Required Environment Variables

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db

# Azure Services
AZURE_DOCUMENT_INTELLIGENCE_KEY=your-key
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=your-endpoint

# Security
SECRET_KEY=very-secure-key-here

# Application
ENVIRONMENT=production
```

## Security Considerations

1. **Use HTTPS in production**
2. **Set strong SECRET_KEY**
3. **Configure proper CORS origins**
4. **Use managed database services**
5. **Enable monitoring and logging**

## Monitoring

The application includes Prometheus metrics. Configure monitoring:

1. **Prometheus** for metrics collection
2. **Grafana** for visualization
3. **Log aggregation** (ELK stack, etc.)

## Backup Strategy

1. **Database backups**: Regular PostgreSQL backups
2. **File storage backups**: Regular backup of uploaded files
3. **Configuration backups**: Store environment configs securely

## Scaling Considerations

- **Horizontal scaling**: Multiple backend replicas
- **Database scaling**: Read replicas, connection pooling
- **File storage**: Object storage (S3, Azure Blob)
- **Caching**: Redis clustering
- **Load balancing**: Nginx, cloud load balancers
