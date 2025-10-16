# Resume Parser with OCR

A web application for parsing resumes (PDF, DOCX, or image files) using OCR and extracting structured information such as name, email, phone, skills, education, and experience. Built with FastAPI, Tesseract OCR, and a modern HTML/JS frontend.

## Features

- **OCR-enabled extraction**: Supports PDF, DOCX, PNG, JPG, JPEG, and TIFF files.
- **Skill detection**: Uses fuzzy matching to extract known technical skills.
- **Structured output**: Returns parsed data as JSON.
- **Web interface**: Simple upload form and JSON viewer.
- **API endpoint**: `/api/parse` for programmatic access.

## Project Structure

```
README.md
requirements.txt
app/
    __init__.py
    main.py         # FastAPI app and API routes
    ocr.py          # OCR and file text extraction
    parser.py       # Resume parsing logic
static/
    index.html      # Frontend HTML
    script.js       # Frontend JS
    styles.css      # Frontend CSS
```

## Installation

1. **Clone the repository**:

   ```sh
   git clone <repo-url>
   cd Nlp_mpr_sem7
   ```

2. **Install Python dependencies**:

   ```sh
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR**:
   - **Ubuntu**: `sudo apt-get install tesseract-ocr`
   - **Mac**: `brew install tesseract`
   - **Windows**: Download from [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)

## Usage

1. **Start the server**:

   ```sh
   uvicorn app.main:app --reload
   ```

2. **Open the web interface**:

   - Visit [http://localhost:8000](http://localhost:8000) in your browser.

3. **Upload a resume**:
   - Select a PDF, DOCX, or image file.
   - Click "Parse Resume".
   - View the extracted JSON output.

## API

### `POST /api/parse`

- **Request**: Multipart form with a file (`file`)
- **Response**: JSON object:

  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-123-4567",
    "skills": ["python", "django", "aws"],
    "education": "...",
    "experience": "...",
    "raw_text": "..."
  }
  ```

- **Errors**: Returns HTTP 400 for unsupported file types or parsing errors.

## How It Works

- **OCR**: Uses Tesseract to extract text from images and PDFs.
- **DOCX**: Reads text using `python-docx`.
- **Parsing**: Extracts fields using regex and fuzzy matching ([`app/parser.py`](app/parser.py)).
- **Frontend**: Simple HTML/JS ([`static/index.html`](static/index.html), [`static/script.js`](static/script.js)).

## Troubleshooting

- **Tesseract not found**: Ensure Tesseract is installed and in your PATH.
- **PDF/image parsing issues**: Check file quality and format.
- **Skill extraction**: Add more skills to `KNOWN_SKILLS` in [`app/parser.py`](app/parser.py) if needed.

## License

MIT
