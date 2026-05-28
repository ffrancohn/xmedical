# XMedical Backend

Backend para el sistema de asistencia médica inteligente XMedical desarrollado con FastAPI.

## Instalación

1. Crear entorno virtual:
```bash
python -m venv env
source env/bin/activate  # Windows: .\env\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:
```bash
cp env.example .env
# Editar .env con tus valores
```

4. Ejecutar el servidor:
```bash
uvicorn main:app --reload
```

## Endpoints Disponibles

### Autenticación
- `POST /auth/register` - Registro de usuarios
- `POST /auth/login` - Login con JWT
- `POST /auth/refresh` - Refresh de tokens

### Usuarios
- `GET /users/` - Listar usuarios (solo administradores)
- `GET /users/me` - Obtener perfil del usuario actual

## Documentación API

Una vez ejecutado el servidor, accede a:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 