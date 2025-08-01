"""
Open-source alternative to Azure Document Intelligence
Uses Tesseract OCR, LayoutParser, and other open-source tools
"""

import logging
from typing import Optional, Dict, Any, List, Tuple
import numpy as np
from PIL import Image
import cv2
import pytesseract
import layoutparser as lp
from pdf2image import convert_from_path
import fitz  # PyMuPDF
from pathlib import Path
import json
import os
from dataclasses import dataclass, asdict
import torch
import io

logger = logging.getLogger(__name__)


@dataclass
class BoundingBox:
    """Represents a bounding box for text or layout elements"""
    x: float
    y: float
    width: float
    height: float
    
    def to_dict(self):
        return asdict(self)


@dataclass
class TextElement:
    """Represents a text element with position and content"""
    text: str
    bounding_box: BoundingBox
    confidence: float
    
    def to_dict(self):
        return {
            "text": self.text,
            "bounding_box": self.bounding_box.to_dict(),
            "confidence": self.confidence
        }


@dataclass
class LayoutElement:
    """Represents a layout element (paragraph, table, etc.)"""
    type: str  # paragraph, table, figure, title, etc.
    bounding_box: BoundingBox
    confidence: float
    text_content: Optional[str] = None
    
    def to_dict(self):
        return {
            "type": self.type,
            "bounding_box": self.bounding_box.to_dict(),
            "confidence": self.confidence,
            "text_content": self.text_content
        }


class OpenSourceDocumentClient:
    """Open-source document intelligence client replacing Azure services"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        
        # Initialize LayoutParser model for document layout analysis
        self.layout_model = lp.AutoLayoutModel(
            'lp://EfficientDete/PubLayNet',
            extra_config={'confidence_threshold': 0.5}
        )
        
        # Configure Tesseract OCR
        self.tesseract_config = '--oem 3 --psm 6 -l eng'
        
        # Check if Tesseract is installed
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            logger.error(f"Tesseract not found: {e}")
            raise RuntimeError("Tesseract OCR must be installed. Run: sudo apt-get install tesseract-ocr")
    
    async def analyze_document_layout(
        self, 
        document_path: str,
        features: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Analyze document layout using open-source tools"""
        try:
            # Default features if not specified
            if features is None:
                features = ["layout", "text", "tables", "style"]
            
            # Convert document to images if PDF
            if document_path.lower().endswith('.pdf'):
                images = self._pdf_to_images(document_path)
            else:
                images = [Image.open(document_path)]
            
            # Process each page
            layout_data = {
                "pages": [],
                "tables": [],
                "styles": [],
                "paragraphs": [],
                "document_metadata": self._extract_metadata(document_path)
            }
            
            for page_num, image in enumerate(images, 1):
                page_data = await self._analyze_page(image, page_num, features)
                layout_data["pages"].append(page_data)
                
                # Aggregate tables and paragraphs
                if "tables" in page_data:
                    layout_data["tables"].extend(page_data["tables"])
                if "paragraphs" in page_data:
                    layout_data["paragraphs"].extend(page_data["paragraphs"])
            
            return layout_data
            
        except Exception as e:
            logger.error(f"Error analyzing document: {str(e)}")
            raise
    
    async def _analyze_page(self, image: Image.Image, page_num: int, features: List[str]) -> Dict[str, Any]:
        """Analyze a single page"""
        # Convert PIL Image to numpy array for processing
        image_np = np.array(image)
        
        page_data = {
            "page_number": page_num,
            "width": image.width,
            "height": image.height,
            "unit": "pixel"
        }
        
        # Layout analysis
        if "layout" in features:
            layout_elements = self._detect_layout(image)
            page_data["layout_elements"] = [elem.to_dict() for elem in layout_elements]
        
        # Text extraction with OCR
        if "text" in features:
            text_elements = self._extract_text_with_positions(image_np)
            page_data["lines"] = self._group_text_into_lines(text_elements)
            page_data["words"] = [elem.to_dict() for elem in text_elements]
        
        # Table detection
        if "tables" in features:
            tables = self._detect_tables(image_np, layout_elements if "layout" in features else None)
            page_data["tables"] = tables
        
        # Style analysis
        if "style" in features:
            styles = self._analyze_styles(image_np, text_elements if "text" in features else [])
            page_data["styles"] = styles
        
        # Extract paragraphs
        if "text" in features and "layout" in features:
            paragraphs = self._extract_paragraphs(text_elements, layout_elements)
            page_data["paragraphs"] = paragraphs
        
        return page_data
    
    def _pdf_to_images(self, pdf_path: str) -> List[Image.Image]:
        """Convert PDF to images for processing"""
        try:
            # Use pdf2image for conversion
            images = convert_from_path(pdf_path, dpi=300)
            return images
        except Exception as e:
            logger.error(f"Error converting PDF to images: {e}")
            # Fallback to PyMuPDF
            pdf_document = fitz.open(pdf_path)
            images = []
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
                img_data = pix.pil_tobytes(format="PNG")
                images.append(Image.open(io.BytesIO(img_data)))
            pdf_document.close()
            return images
    
    def _detect_layout(self, image: Image.Image) -> List[LayoutElement]:
        """Detect document layout elements"""
        # Use LayoutParser for layout detection
        layout = self.layout_model.detect(image)
        
        layout_elements = []
        for element in layout:
            bbox = BoundingBox(
                x=element.coordinates[0],
                y=element.coordinates[1],
                width=element.coordinates[2] - element.coordinates[0],
                height=element.coordinates[3] - element.coordinates[1]
            )
            
            layout_elem = LayoutElement(
                type=element.type,
                bounding_box=bbox,
                confidence=element.score
            )
            layout_elements.append(layout_elem)
        
        return layout_elements
    
    def _extract_text_with_positions(self, image_np: np.ndarray) -> List[TextElement]:
        """Extract text with positions using Tesseract OCR"""
        # Get detailed OCR data
        ocr_data = pytesseract.image_to_data(
            image_np, 
            output_type=pytesseract.Output.DICT,
            config=self.tesseract_config
        )
        
        text_elements = []
        n_boxes = len(ocr_data['text'])
        
        for i in range(n_boxes):
            if ocr_data['text'][i].strip():
                bbox = BoundingBox(
                    x=ocr_data['left'][i],
                    y=ocr_data['top'][i],
                    width=ocr_data['width'][i],
                    height=ocr_data['height'][i]
                )
                
                text_elem = TextElement(
                    text=ocr_data['text'][i],
                    bounding_box=bbox,
                    confidence=ocr_data['conf'][i] / 100.0
                )
                text_elements.append(text_elem)
        
        return text_elements
    
    def _group_text_into_lines(self, text_elements: List[TextElement]) -> List[Dict[str, Any]]:
        """Group text elements into lines based on vertical position"""
        if not text_elements:
            return []
        
        # Sort by vertical position
        sorted_elements = sorted(text_elements, key=lambda e: (e.bounding_box.y, e.bounding_box.x))
        
        lines = []
        current_line = []
        current_y = sorted_elements[0].bounding_box.y
        line_threshold = 10  # pixels
        
        for elem in sorted_elements:
            if abs(elem.bounding_box.y - current_y) <= line_threshold:
                current_line.append(elem)
            else:
                if current_line:
                    lines.append(self._create_line_dict(current_line))
                current_line = [elem]
                current_y = elem.bounding_box.y
        
        if current_line:
            lines.append(self._create_line_dict(current_line))
        
        return lines
    
    def _create_line_dict(self, elements: List[TextElement]) -> Dict[str, Any]:
        """Create a line dictionary from text elements"""
        sorted_elems = sorted(elements, key=lambda e: e.bounding_box.x)
        
        min_x = min(e.bounding_box.x for e in sorted_elems)
        max_x = max(e.bounding_box.x + e.bounding_box.width for e in sorted_elems)
        min_y = min(e.bounding_box.y for e in sorted_elems)
        max_y = max(e.bounding_box.y + e.bounding_box.height for e in sorted_elems)
        
        return {
            "text": " ".join(e.text for e in sorted_elems),
            "bounding_box": BoundingBox(
                x=min_x,
                y=min_y,
                width=max_x - min_x,
                height=max_y - min_y
            ).to_dict(),
            "words": [e.to_dict() for e in sorted_elems]
        }
    
    def _detect_tables(self, image_np: np.ndarray, layout_elements: Optional[List[LayoutElement]] = None) -> List[Dict[str, Any]]:
        """Detect and extract tables from the document"""
        tables = []
        
        # If layout elements are provided, use them to find table regions
        if layout_elements:
            table_regions = [elem for elem in layout_elements if elem.type == "Table"]
            
            for table_region in table_regions:
                # Extract table region from image
                bbox = table_region.bounding_box
                table_img = image_np[
                    int(bbox.y):int(bbox.y + bbox.height),
                    int(bbox.x):int(bbox.x + bbox.width)
                ]
                
                # Process table
                table_data = self._extract_table_structure(table_img)
                table_data["bounding_box"] = bbox.to_dict()
                tables.append(table_data)
        else:
            # Use computer vision to detect tables
            table_regions = self._detect_table_regions_cv(image_np)
            for region in table_regions:
                table_data = self._extract_table_structure(region["image"])
                table_data["bounding_box"] = region["bbox"].to_dict()
                tables.append(table_data)
        
        return tables
    
    def _detect_table_regions_cv(self, image_np: np.ndarray) -> List[Dict[str, Any]]:
        """Detect table regions using computer vision"""
        # Convert to grayscale
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY) if len(image_np.shape) == 3 else image_np
        
        # Detect horizontal and vertical lines
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
        
        horizontal_lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
        vertical_lines = cv2.morphologyEx(gray, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
        
        # Combine lines
        table_mask = cv2.add(horizontal_lines, vertical_lines)
        
        # Find contours
        contours, _ = cv2.findContours(table_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        table_regions = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 100 and h > 50:  # Filter small regions
                bbox = BoundingBox(x=x, y=y, width=w, height=h)
                table_img = image_np[y:y+h, x:x+w]
                table_regions.append({"bbox": bbox, "image": table_img})
        
        return table_regions
    
    def _extract_table_structure(self, table_img: np.ndarray) -> Dict[str, Any]:
        """Extract table structure and content"""
        # This is a simplified implementation
        # In production, you might use more sophisticated table extraction libraries
        
        # Extract text from table region
        text = pytesseract.image_to_string(table_img, config=self.tesseract_config)
        
        # Simple row detection based on line breaks
        rows = [row.strip() for row in text.split('\n') if row.strip()]
        
        # Simple column detection based on consistent spacing
        cells = []
        for row in rows:
            # Split by multiple spaces (simple heuristic)
            row_cells = [cell.strip() for cell in row.split('  ') if cell.strip()]
            if row_cells:
                cells.append(row_cells)
        
        return {
            "rows": len(cells),
            "columns": max(len(row) for row in cells) if cells else 0,
            "cells": cells,
            "raw_text": text
        }
    
    def _analyze_styles(self, image_np: np.ndarray, text_elements: List[TextElement]) -> Dict[str, Any]:
        """Analyze text styles and formatting"""
        styles = {
            "fonts": [],
            "colors": [],
            "sizes": []
        }
        
        # Basic style analysis using image processing
        # This is a simplified version - production might use more sophisticated methods
        
        # Detect dominant colors
        if len(image_np.shape) == 3:
            # Convert to RGB if needed
            rgb_img = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB) if image_np.shape[2] == 3 else image_np
            
            # Get dominant colors using k-means clustering
            pixels = rgb_img.reshape(-1, 3)
            from sklearn.cluster import KMeans
            
            n_colors = 5
            kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
            kmeans.fit(pixels)
            
            colors = kmeans.cluster_centers_.astype(int)
            styles["colors"] = [{"r": int(c[0]), "g": int(c[1]), "b": int(c[2])} for c in colors]
        
        # Estimate font sizes based on bounding box heights
        if text_elements:
            heights = [elem.bounding_box.height for elem in text_elements]
            unique_heights = list(set(heights))
            unique_heights.sort()
            
            # Group similar heights as same font size
            font_sizes = []
            threshold = 2  # pixels
            for height in unique_heights:
                if not font_sizes or abs(height - font_sizes[-1]) > threshold:
                    font_sizes.append(height)
            
            styles["sizes"] = font_sizes
        
        return styles
    
    def _extract_paragraphs(self, text_elements: List[TextElement], layout_elements: List[LayoutElement]) -> List[Dict[str, Any]]:
        """Extract paragraphs by combining text elements within layout regions"""
        paragraphs = []
        
        # Find paragraph layout elements
        paragraph_regions = [elem for elem in layout_elements if elem.type in ["Text", "List", "Title"]]
        
        for region in paragraph_regions:
            # Find text elements within this region
            region_text = []
            for text_elem in text_elements:
                if self._is_inside(text_elem.bounding_box, region.bounding_box):
                    region_text.append(text_elem)
            
            if region_text:
                # Sort by position
                region_text.sort(key=lambda e: (e.bounding_box.y, e.bounding_box.x))
                
                # Combine text
                paragraph_text = " ".join(elem.text for elem in region_text)
                
                paragraphs.append({
                    "type": region.type,
                    "text": paragraph_text,
                    "bounding_box": region.bounding_box.to_dict(),
                    "confidence": region.confidence
                })
        
        return paragraphs
    
    def _is_inside(self, inner: BoundingBox, outer: BoundingBox) -> bool:
        """Check if inner bounding box is inside outer bounding box"""
        return (inner.x >= outer.x and 
                inner.y >= outer.y and 
                inner.x + inner.width <= outer.x + outer.width and 
                inner.y + inner.height <= outer.y + outer.height)
    
    def _extract_metadata(self, document_path: str) -> Dict[str, Any]:
        """Extract document metadata"""
        metadata = {
            "filename": os.path.basename(document_path),
            "file_size": os.path.getsize(document_path),
            "file_type": os.path.splitext(document_path)[1].lower()
        }
        
        # Extract PDF metadata if applicable
        if document_path.lower().endswith('.pdf'):
            try:
                pdf_document = fitz.open(document_path)
                pdf_metadata = pdf_document.metadata
                metadata.update({
                    "title": pdf_metadata.get("title", ""),
                    "author": pdf_metadata.get("author", ""),
                    "subject": pdf_metadata.get("subject", ""),
                    "creator": pdf_metadata.get("creator", ""),
                    "creation_date": str(pdf_metadata.get("creationDate", "")),
                    "modification_date": str(pdf_metadata.get("modDate", "")),
                    "pages": len(pdf_document)
                })
                pdf_document.close()
            except Exception as e:
                logger.warning(f"Could not extract PDF metadata: {e}")
        
        return metadata


# Compatibility wrapper to match Azure client interface
class DocumentAnalysisCompatibilityWrapper:
    """Wrapper to provide Azure-compatible interface"""
    
    def __init__(self):
        self.client = OpenSourceDocumentClient()
    
    async def analyze_document_layout(self, document_path: str, features: Optional[List[str]] = None) -> Dict[str, Any]:
        """Analyze document with Azure-compatible response format"""
        result = await self.client.analyze_document_layout(document_path, features)
        
        # Transform to Azure-compatible format if needed
        # This ensures existing code continues to work
        return result
