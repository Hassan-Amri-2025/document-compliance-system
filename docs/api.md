# API Documentation

## Overview

The Document Compliance System provides a comprehensive REST API for managing templates, documents, and validations.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Endpoints

### Authentication

#### POST /auth/login
Login with username and password.

**Request:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Response:**
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

#### POST /auth/register
Register a new user.

**Request:**
```json
{
  "email": "string",
  "username": "string",
  "full_name": "string",
  "password": "string",
  "role": "student"
}
```

### Templates

#### GET /templates/
List all templates (paginated).

#### POST /templates/
Create a new template (multipart/form-data).

#### GET /templates/{template_id}
Get template details.

### Documents

#### POST /documents/upload
Upload a document for validation (multipart/form-data).

#### GET /documents/
List user's documents.

#### GET /documents/{document_id}
Get document details.

### Validations

#### POST /validation/validate
Start document validation process.

#### GET /validations/
List validations.

#### GET /validations/{validation_id}/report
Get detailed validation report.

## Error Responses

```json
{
  "error": {
    "message": "Error description",
    "type": "ErrorType",
    "status_code": 400
  }
}
```

## Rate Limits

- 1000 requests per hour per user
- 10 concurrent validations per user
- Maximum file size: 50MB
