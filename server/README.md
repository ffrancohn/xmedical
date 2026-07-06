# XMedical Backend (FastAPI) — LEGADO

> **Este directorio corresponde a un prototipo anterior y no forma parte del stack activo de XMedical.**
>
> La arquitectura actual usa **Django** en la raíz del repositorio. Consulta el [`README.md`](../README.md) principal para instalación y uso.

## Qué contenía este prototipo

Backend de verificación de identidad y asistencia médica con:

- Autenticación JWT con refresh tokens
- OCR de documentos (Tesseract)
- Verificación facial (biometría)
- Gestión de usuarios, direcciones, beneficiarios y centros médicos
- Sistema de feedback

## Tecnologías

- FastAPI 0.104+
- SQLModel / PostgreSQL
- Pydantic, OpenCV, Pillow

## Ejecución (solo referencia histórica)

```bash
cd server
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux
pip install -r requirements.txt
cp env.example config.env
python init_db.py
python start_server.py
```

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

> **Conflicto de puerto:** Django también usa el puerto 8000. No ejecutar ambos stacks simultáneamente.

## Documentación relacionada (legado)

- [`docs/informe-tecnico.md`](../docs/informe-tecnico.md)
- [`docs/guia-integracion.md`](../docs/guia-integracion.md)
