from fastapi import APIRouter

api_router = APIRouter()

# Health check endpoint
@api_router.get("/health")
async def health_check():
    return {"status": "ok", "message": "Document Compliance System API"}

# Placeholder endpoints
@api_router.get("/templates/")
async def list_templates():
    return {"message": "Template endpoints will be implemented here"}

@api_router.get("/documents/")
async def list_documents():
    return {"message": "Document endpoints will be implemented here"}

@api_router.get("/validations/")
async def list_validations():
    return {"message": "Validation endpoints will be implemented here"}
