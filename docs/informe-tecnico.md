# Informe Técnico - Backend XMedical (FastAPI — LEGADO)

> **Documento histórico.** Describe el prototipo FastAPI en `server/`, que ya no es el stack activo.
>
> La arquitectura actual usa **Django** (ver [`README.md`](../README.md) y [`4 Documento Arquitectura de alto nivel.md`](4%20Documento%20Arquitectura%20de%20alto%20nivel.md)).

## Resumen Ejecutivo

El backend de XMedical fue desarrollado inicialmente como un sistema de asistencia médica inteligente utilizando FastAPI (Python 3.11+). El sistema incluye autenticación JWT, verificación biométrica, gestión de usuarios, documentos, direcciones, beneficiarios, feedback y centros médicos.

## Arquitectura del Sistema

### Tecnologías Utilizadas

- **Framework**: FastAPI 0.104.1
- **Lenguaje**: Python 3.11+
- **ORM**: SQLModel 0.0.14
- **Base de Datos**: PostgreSQL (vía Neon)
- **Autenticación**: JWT con OAuth2PasswordBearer
- **Validación**: Pydantic 2.5.0
- **Procesamiento de Imágenes**: Pillow, OpenCV
- **OCR**: Tesseract (pytesseract)
- **Reconocimiento Facial**: face-recognition
- **Subida de Archivos**: python-multipart, aiofiles

### Estructura de Carpetas

```
server/
├── main.py                 # Aplicación principal FastAPI
├── config.py              # Configuración y variables de entorno
├── database.py            # Configuración de base de datos
├── requirements.txt       # Dependencias del proyecto
├── env.example           # Ejemplo de variables de entorno
├── README.md             # Documentación básica
├── models/               # Modelos SQLModel
│   ├── user.py
│   ├── user_profile.py
│   ├── nationality.py
│   ├── address.py
│   ├── document.py
│   ├── beneficiary.py
│   ├── feedback.py
│   ├── center.py
│   └── facial_verification.py
├── schemas/              # Esquemas Pydantic
│   ├── user.py
│   ├── auth.py
│   ├── user_profile.py
│   ├── nationality.py
│   ├── address.py
│   ├── document.py
│   ├── beneficiary.py
│   ├── feedback.py
│   ├── center.py
│   └── facial_verification.py
├── routes/               # Endpoints de la API
│   ├── auth.py
│   ├── users.py
│   ├── user_profiles.py
│   ├── nationalities.py
│   ├── addresses.py
│   ├── documents.py
│   ├── beneficiaries.py
│   ├── feedback.py
│   ├── centers.py
│   ├── biometric.py
│   └── upload.py
├── services/             # Lógica de negocio
│   ├── auth_service.py
│   ├── ocr_service.py
│   └── facial_recognition.py
├── middleware/           # Middleware personalizado
│   └── auth_middleware.py
├── validators/           # Validaciones de negocio
│   ├── document_validator.py
│   └── user_validator.py
├── uploads/              # Archivos subidos (se crea automáticamente)
└── __init__.py
```

## Módulos Implementados

### 1. Sistema de Autenticación

**Archivos**: `routes/auth.py`, `services/auth_service.py`, `middleware/auth_middleware.py`

**Funcionalidades**:
- Registro de usuarios con hasheo de contraseñas (bcrypt)
- Login con generación de tokens JWT
- Refresh de tokens automático
- Middleware de autenticación para rutas protegidas
- Validación de usuarios activos

**Endpoints**:
- `POST /auth/register` - Registro de usuarios
- `POST /auth/login` - Login con JWT
- `POST /auth/refresh` - Refresh de tokens

### 2. Gestión de Usuarios

**Archivos**: `routes/users.py`, `models/user.py`, `schemas/user.py`

**Funcionalidades**:
- CRUD completo de usuarios
- Control de acceso basado en roles
- Perfil de usuario actual
- Validaciones de datos personales

**Endpoints**:
- `GET /users/` - Listar usuarios (solo admin)
- `GET /users/me` - Perfil del usuario actual

### 3. Perfiles y Nacionalidades

**Archivos**: `routes/user_profiles.py`, `routes/nationalities.py`

**Funcionalidades**:
- Gestión de perfiles de usuario (Administrador, Médico, Enfermera, etc.)
- Gestión de nacionalidades
- Control de acceso solo para administradores

**Endpoints**:
- CRUD completo para perfiles (`/profiles/`)
- CRUD completo para nacionalidades (`/nationalities/`)

### 4. Gestión de Documentos

**Archivos**: `routes/documents.py`, `models/document.py`, `schemas/document.py`

**Funcionalidades**:
- CRUD de documentos de identidad
- Validación de tipos de documento
- Control de acceso por usuario
- Integración con OCR

**Endpoints**:
- CRUD completo para documentos (`/documents/`)

### 5. Gestión de Direcciones

**Archivos**: `routes/addresses.py`, `models/address.py`, `schemas/address.py`

**Funcionalidades**:
- CRUD de direcciones de usuarios
- Coordenadas geográficas (latitud/longitud)
- Control de acceso por usuario
- Preparado para integración con mapas

**Endpoints**:
- CRUD completo para direcciones (`/addresses/`)

### 6. Gestión de Beneficiarios

**Archivos**: `routes/beneficiaries.py`, `models/beneficiary.py`, `schemas/beneficiary.py`

**Funcionalidades**:
- CRUD de beneficiarios por usuario
- Relaciones familiares
- Control de acceso por usuario

**Endpoints**:
- CRUD completo para beneficiarios (`/beneficiaries/`)

### 7. Sistema de Feedback

**Archivos**: `routes/feedback.py`, `models/feedback.py`, `schemas/feedback.py`

**Funcionalidades**:
- Sistema de retroalimentación completo
- Tipos: Sugerencia, Queja, Elogio, Bug, Feature Request, General
- Prioridades: Baja, Media, Alta, Crítica
- Estados: Pendiente, En proceso, Resuelto, Cerrado

**Endpoints**:
- CRUD completo para feedback (`/feedback/`)

### 8. Gestión de Centros Médicos

**Archivos**: `routes/centers.py`, `models/center.py`, `schemas/center.py`

**Funcionalidades**:
- CRUD de centros médicos
- Control de acceso solo para administradores
- Información de contacto y ubicación

**Endpoints**:
- CRUD completo para centros (`/centers/`)

### 9. Verificación Biométrica

**Archivos**: `routes/biometric.py`, `services/ocr_service.py`, `services/facial_recognition.py`

**Funcionalidades**:
- OCR de documentos con Tesseract
- Reconocimiento facial con face-recognition
- Validación de calidad de imágenes
- Scoring de confianza
- Almacenamiento de verificaciones

**Endpoints**:
- `POST /biometric/ocr/process` - Procesar OCR
- `POST /biometric/facial/verify` - Verificación facial
- `GET /biometric/verifications` - Listar verificaciones

### 10. Subida de Archivos

**Archivos**: `routes/upload.py`

**Funcionalidades**:
- Subida segura de archivos
- Validación de tipo y tamaño
- Nombres únicos con UUID
- Servir archivos estáticos
- Integración con módulos de documentos y biometría

**Endpoints**:
- `POST /upload/` - Subir archivo

## Base de Datos

### Estructura de Tablas

1. **nationalities** - Nacionalidades
2. **user_profiles** - Perfiles de usuario
3. **users** - Usuarios del sistema
4. **documents** - Documentos de identidad
5. **addresses** - Direcciones de usuarios
6. **beneficiaries** - Beneficiarios
7. **facial_verifications** - Verificaciones faciales
8. **feedback** - Sistema de retroalimentación
9. **centers** - Centros médicos

### Relaciones Principales

- `users.profileId` → `user_profiles.id`
- `users.nationalityId` → `nationalities.id`
- `documents.userId` → `users.id`
- `addresses.userId` → `users.id`
- `beneficiaries.userId` → `users.id`
- `facial_verifications.userId` → `users.id`
- `feedback.userId` → `users.id`

## Seguridad

### Autenticación y Autorización

- **JWT Tokens**: Access token (30 min) y refresh token (7 días)
- **Hasheo de Contraseñas**: bcrypt con salt automático
- **Control de Acceso**: Middleware basado en roles
- **Validación de Usuarios**: Verificación de usuarios activos

### Validaciones

- **Contraseñas**: Mínimo 8 caracteres, mayúsculas, minúsculas, números, caracteres especiales
- **Emails**: Formato válido y longitud máxima
- **Documentos**: Formato específico para Honduras (13 dígitos)
- **Teléfonos**: Formato hondureño (8 dígitos)
- **Fechas**: Validación de edad mínima (18 años) y máxima (120 años)

### Subida de Archivos

- **Tipos Permitidos**: jpg, jpeg, png, pdf
- **Tamaño Máximo**: Configurable (por defecto 10MB)
- **Nombres Únicos**: UUID para evitar conflictos
- **Validación**: Tipo y tamaño antes del guardado

## Configuración

### Variables de Entorno

```env
DATABASE_URL=postgresql://username:password@host:port/database
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
MAX_FILE_SIZE=10mb
ALLOWED_FILE_TYPES=jpg,jpeg,png,pdf
```

### Dependencias Principales

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlmodel==0.0.14
psycopg2-binary==2.9.9
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pytesseract==0.3.10
face-recognition==1.3.0
opencv-python==4.8.1.78
```

## API Documentation

### Swagger UI
- **URL**: http://localhost:8000/docs
- **Descripción**: Documentación interactiva de la API
- **Funcionalidades**: Pruebas de endpoints, esquemas, respuestas

### ReDoc
- **URL**: http://localhost:8000/redoc
- **Descripción**: Documentación alternativa más limpia

### Health Check
- **URL**: http://localhost:8000/health
- **Propósito**: Verificar estado del servidor

## Decisiones Técnicas

### 1. FastAPI como Framework

**Razones**:
- Rendimiento superior a Django/Flask
- Documentación automática con OpenAPI
- Soporte nativo para async/await
- Validación automática con Pydantic
- Type hints completos

### 2. SQLModel como ORM

**Razones**:
- Compatible con Pydantic
- Sintaxis moderna y limpia
- Soporte para SQLAlchemy
- Migraciones automáticas

### 3. JWT para Autenticación

**Razones**:
- Stateless (no requiere sesiones en servidor)
- Escalabilidad
- Seguridad robusta
- Refresh tokens para mejor UX

### 4. Verificación Biométrica

**Razones**:
- Cumplimiento de requisitos de identidad
- Seguridad adicional
- Automatización del proceso de registro
- Validación de documentos reales

### 5. Subida de Archivos Local

**Razones**:
- Simplicidad de implementación
- Control total sobre archivos
- Sin dependencias externas
- Fácil migración a cloud storage

## Métricas de Calidad

### Cobertura de Funcionalidades
- ✅ Autenticación completa
- ✅ Gestión de usuarios y roles
- ✅ CRUD de todos los módulos
- ✅ Verificación biométrica
- ✅ Subida de archivos
- ✅ Validaciones de negocio
- ✅ Documentación automática

### Seguridad
- ✅ Hasheo de contraseñas
- ✅ Tokens JWT seguros
- ✅ Control de acceso por roles
- ✅ Validación de archivos
- ✅ Sanitización de datos

### Escalabilidad
- ✅ Arquitectura modular
- ✅ Separación de responsabilidades
- ✅ Configuración externalizada
- ✅ Base de datos relacional
- ✅ API RESTful

## Próximos Pasos Recomendados

### 1. Producción
- Configurar HTTPS
- Implementar rate limiting
- Configurar logging
- Backup automático de base de datos
- Monitoreo y alertas

### 2. Funcionalidades Adicionales
- Notificaciones push
- Reportes y analytics
- Integración con servicios externos
- Cache con Redis
- Background jobs con Celery

### 3. Testing
- Unit tests con pytest
- Integration tests
- API tests
- Performance tests

### 4. DevOps
- Docker containerization
- CI/CD pipeline
- Kubernetes deployment
- Monitoring con Prometheus/Grafana

## Conclusiones

El backend de XMedical ha sido desarrollado siguiendo las mejores prácticas de desarrollo de APIs modernas. El sistema es robusto, escalable y mantiene altos estándares de seguridad. La arquitectura modular permite fácil mantenimiento y extensión de funcionalidades.

La implementación incluye todas las funcionalidades requeridas:
- Sistema de autenticación completo
- Gestión de usuarios y roles
- Verificación biométrica avanzada
- CRUD de todos los módulos
- Validaciones de negocio específicas
- Documentación automática

El sistema está listo para integración con el frontend y despliegue en producción. 