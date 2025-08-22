import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
INSTANCE_DIR = BASE_DIR / 'instance'
UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
EXPORT_FOLDER = BASE_DIR / 'exports'

INSTANCE_DIR.mkdir(exist_ok=True)
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
EXPORT_FOLDER.mkdir(parents=True, exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-dev-key')
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{INSTANCE_DIR / 'ats.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = str(UPLOAD_FOLDER)
    EXPORT_FOLDER = str(EXPORT_FOLDER)
    ALLOWED_EXTENSIONS = {'.pdf', '.docx', '.txt', '.png', '.jpg', '.jpeg'}
