# Migration Guide: Azure to Open Source Version

## Overview

This guide helps you migrate from the Azure-dependent version to the fully open-source version.

## Changes

### Removed Dependencies
- Azure Document Intelligence
- Azure Storage Blob
- Azure Identity

### Added Dependencies
- Tesseract OCR
- PyMuPDF
- Enhanced LayoutParser usage

## Migration Steps

1. **Backup Your Data**
   ```bash
   pg_dump document_compliance > backup.sql
   cp -r uploads uploads_backup
   ```

2. **Update Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Install Tesseract**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install tesseract-ocr tesseract-ocr-eng tesseract-ocr-ara
   
   # macOS
   brew install tesseract
   
   # Windows
   # Download from: https://github.com/UB-Mannheim/tesseract/wiki
   ```

4. **Update Environment Variables**
   - Remove all AZURE_* variables
   - Update storage paths
   - Set OCR_ENGINE=tesseract

5. **Run Migrations**
   ```bash
   alembic revision --autogenerate -m "Remove Azure dependencies"
   alembic upgrade head
   ```

6. **Reprocess Documents**
   Use the reprocess endpoint to update existing documents with the new OCR engine.

## API Changes

All API endpoints remain the same. The only internal change is the document processing engine.

## Performance Considerations

- Tesseract OCR may be slower than Azure for large documents
- Consider using batch processing for multiple documents
- GPU acceleration available with specific configurations

