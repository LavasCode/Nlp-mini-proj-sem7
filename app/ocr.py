import io
import os
import tempfile
from typing import List

import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
from docx import Document


async def extract_text_from_file(filename: str, contents: bytes) -> str:
    lower = filename.lower()
    if lower.endswith('.pdf'):
        return await _extract_text_from_pdf_bytes(contents)
    if lower.endswith('.png') or lower.endswith('.jpg') or lower.endswith('.jpeg') or lower.endswith('.tiff'):
        return await _extract_text_from_image_bytes(contents)
    if lower.endswith('.docx'):
        return await _extract_text_from_docx_bytes(contents)
    raise ValueError('Unsupported file type. Please upload PDF, DOCX, or image files.')


async def _extract_text_from_pdf_bytes(contents: bytes) -> str:
    # Convert PDF pages to images then OCR
    pages = convert_from_bytes(contents, dpi=300)
    texts: List[str] = []
    for page in pages:
        gray = page.convert('L')
        texts.append(pytesseract.image_to_string(gray))
    return "\n".join(texts)


async def _extract_text_from_image_bytes(contents: bytes) -> str:
    image = Image.open(io.BytesIO(contents))
    gray = image.convert('L')
    return pytesseract.image_to_string(gray)


async def _extract_text_from_docx_bytes(contents: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix='.docx', delete=True) as tmp:
        tmp.write(contents)
        tmp.flush()
        doc = Document(tmp.name)
        paragraphs = [p.text for p in doc.paragraphs]
        return "\n".join(paragraphs)
