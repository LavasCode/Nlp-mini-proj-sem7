from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import io
import shutil
import tempfile

from .ocr import extract_text_from_file
from .parser import parse_resume_text

app = FastAPI(title="Resume Parser with OCR")

static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
app.mount("/static", StaticFiles(directory=os.path.abspath(static_dir)), name="static")

class ParseResult(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = []
    education: Optional[str] = None
    experience: Optional[str] = None
    raw_text: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def index():
    index_path = os.path.abspath(os.path.join(static_dir, 'index.html'))
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Frontend not found")
    with open(index_path, 'r', encoding='utf-8') as f:
        return HTMLResponse(content=f.read())

@app.post("/api/parse", response_model=ParseResult)
async def parse_resume(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        text = await extract_text_from_file(file.filename, contents)
        parsed = parse_resume_text(text)
        parsed['raw_text'] = text
        return ParseResult(**parsed)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
