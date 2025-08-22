# Application Tracking System - Upgraded

This upgraded ATS includes:
- Signup / Signin (Flask-Login)
- Protected ATS dashboard (upload/search/export)
- OCR-capable resume parsing (PDF/DOCX/TXT/PNG/JPG)
- Attractive dark UI with images and Modak logo placeholder
- Empty parsed fields are stored as "Not Mentioned"

## Setup
1. Create and activate virtualenv:
```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# Windows PowerShell: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Install system deps for OCR:
- **Ubuntu/Debian**: `sudo apt install -y tesseract-ocr poppler-utils`
- **macOS**: `brew install tesseract poppler`
- **Windows**: install Tesseract from https://github.com/UB-Mannheim/tesseract/wiki and add to PATH; install poppler binaries and add to PATH.

3. Run:
```bash
python app.py
```

Open http://127.0.0.1:5000

Default: create a user via Sign up. After login, you can access Dashboard (upload, search, export).

Notes: This is an MVP. For production, secure secrets, use HTTPS, and improve parsing & validation.
