from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from ..middleware.auth_middleware import get_current_active_user
import os
import shutil
from uuid import uuid4
from ..config import MAX_FILE_SIZE, ALLOWED_FILE_TYPES

router = APIRouter(prefix="/upload", tags=["upload"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Convertir MAX_FILE_SIZE a bytes
size_map = {'kb': 1024, 'mb': 1024*1024, 'gb': 1024*1024*1024}
def parse_size(size_str):
    size_str = size_str.lower()
    for unit in size_map:
        if size_str.endswith(unit):
            return int(size_str.replace(unit, '')) * size_map[unit]
    return int(size_str)

MAX_SIZE_BYTES = parse_size(MAX_FILE_SIZE)
ALLOWED_EXTENSIONS = [ext.strip().lower() for ext in ALLOWED_FILE_TYPES.split(',')]

@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    current_user=Depends(get_current_active_user)
):
    # Validar extensión
    ext = file.filename.split('.')[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Tipo de archivo no permitido: {ext}")
    
    # Validar tamaño
    contents = await file.read()
    if len(contents) > MAX_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="El archivo excede el tamaño máximo permitido")
    
    # Guardar archivo con nombre único
    filename = f"{uuid4().hex}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, 'wb') as f:
        f.write(contents)
    
    # Generar URL relativa
    url = f"/uploads/{filename}"
    return {"success": True, "url": url, "filename": filename} 