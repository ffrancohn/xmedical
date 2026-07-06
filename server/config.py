import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv("config.env")

# Base de Datos
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:123@localhost:5432/xmedical")

# JWT
JWT_SECRET_KEY = os.getenv("SECRET_KEY", "tu_clave_secreta_muy_larga_y_segura_aqui_2024")
JWT_ALGORITHM = os.getenv("ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
JWT_REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

# Servidor
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# CORS
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", '["http://localhost:3000", "http://127.0.0.1:3000"]')

# Upload
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10485760"))

# Tesseract
TESSERACT_PATH = os.getenv("TESSERACT_CMD", "C:\\Program Files\\Tesseract-OCR\\tesseract.exe")

# Configuración para compatibilidad con scripts
class Settings:
    def __init__(self):
        self.DATABASE_URL = DATABASE_URL
        self.JWT_SECRET_KEY = JWT_SECRET_KEY
        self.JWT_ALGORITHM = JWT_ALGORITHM
        self.ACCESS_TOKEN_EXPIRE_MINUTES = JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        self.REFRESH_TOKEN_EXPIRE_DAYS = JWT_REFRESH_TOKEN_EXPIRE_DAYS
        self.HOST = HOST
        self.PORT = PORT
        self.DEBUG = DEBUG
        self.ALLOWED_ORIGINS = ALLOWED_ORIGINS
        self.UPLOAD_DIR = UPLOAD_DIR
        self.MAX_FILE_SIZE = MAX_FILE_SIZE
        self.TESSERACT_PATH = TESSERACT_PATH

# Instancia global
settings = Settings()

# Variables individuales para compatibilidad
DATABASE_URL = settings.DATABASE_URL
JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
JWT_REFRESH_TOKEN_EXPIRE_DAYS = settings.REFRESH_TOKEN_EXPIRE_DAYS
MAX_FILE_SIZE = settings.MAX_FILE_SIZE
ALLOWED_FILE_TYPES = "jpg,jpeg,png,pdf" 