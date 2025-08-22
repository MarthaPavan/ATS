import os
from pathlib import Path
import pdfplumber
import docx
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

def extract_text(filepath):
    path = Path(filepath)
    ext = path.suffix.lower()
    text = ''

    try:
        if ext == '.pdf':
            try:
                with pdfplumber.open(str(path)) as pdf:
                    for page in pdf.pages:
                        page_txt = page.extract_text()
                        if page_txt:
                            text += page_txt + '\n'
            except Exception:
                pass
            if not text.strip():
                images = convert_from_path(str(path))
                for img in images:
                    text += pytesseract.image_to_string(img) + '\n'
        elif ext == '.docx':
            doc = docx.Document(str(path))
            for p in doc.paragraphs:
                text += p.text + '\n'
        elif ext in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            img = Image.open(str(path))
            text = pytesseract.image_to_string(img)
        elif ext == '.txt':
            text = path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print('extract_text error:', e)
    return text
