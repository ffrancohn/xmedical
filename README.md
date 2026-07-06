# XMedical - Sistema de Gestión Clínica Multi-tenant

Sistema de gestión clínica para instituciones de primer y segundo nivel de atención. Soporta múltiples clínicas en una sola instalación (multi-tenant por subdominio), con flujos de pacientes, citas, preclínica y consulta médica guiada.

## Arquitectura actual

| Componente | Tecnología |
|---|---|
| Backend | **Django 4.2** (monolito modular) |
| Base de datos | **PostgreSQL 15** |
| Tareas asíncronas | **Celery** + **Redis** |
| Frontend | Plantillas Django (server-side) |
| Despliegue | **Docker Compose** + Gunicorn |

Documentación de producto y arquitectura en [`docs/`](docs/).

> **Nota:** Las carpetas [`server/`](server/) (FastAPI) y [`client/`](client/) (React) corresponden a un **prototipo anterior** de verificación de identidad y asistencia médica. No forman parte del stack activo. Ver sección [Código legado](#código-legado).

## Características principales

- **Multi-tenant** por subdominio e institución
- **Roles**: superadmin, admin, médico, enfermera, recepcionista
- **Pacientes**: registro, búsqueda y detalle clínico
- **Citas**: calendario, agendamiento y cancelación
- **Preclínica**: signos vitales y alertas clínicas
- **Consulta médica**: wizard de 7 pasos con diagnóstico CIE-10
- **Respaldos**: backup y restauración global o por institución

## Requisitos

- Python 3.11+
- Docker y Docker Compose (recomendado)
- PostgreSQL 14+ y Redis 7 (si se ejecuta sin Docker)

## Instalación rápida

### Opción 1: Docker (recomendado)

```bash
git clone <repository-url>
cd xmedical
cp .env.example .env
docker compose up -d
```

Servicios disponibles:

- Django: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### Opción 2: Desarrollo local (Windows)

```bash
# 1. Levantar PostgreSQL y Redis
levantar_xmedical.bat

# 2. Activar entorno virtual e iniciar Django
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata fixtures/initial_data.json
python manage.py runserver
```

### Opción 3: Desarrollo local (Linux)

```bash
docker compose up -d db redis
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py loaddata fixtures/initial_data.json
python manage.py runserver
```

## Acceso al sistema

- **URL**: http://localhost:8000/auth/login/
- **Usuarios de prueba**: ver [`USUARIOS_PRUEBA.md`](USUARIOS_PRUEBA.md)

## Estructura del proyecto

```
xmedical/
├── apps/              # Módulos Django (core, auth, pacientes, citas, preclínica, consulta)
├── xmedical/          # Configuración del proyecto Django
├── templates/         # Plantillas base compartidas
├── static/            # Archivos estáticos
├── fixtures/          # Datos iniciales de prueba
├── docs/              # Documentación de producto y arquitectura
├── docker-compose.yml # PostgreSQL + Redis + Django + Celery
├── manage.py
├── server/            # [LEGADO] Prototipo FastAPI
└── client/            # [LEGADO] Prototipo React
```

## Módulos Django

| App | Responsabilidad |
|---|---|
| `apps.core` | Instituciones, profesionales, horarios, respaldos, dashboard |
| `apps.auth_app` | Login, registro y preferencias de usuario |
| `apps.pacientes` | Registro y gestión de pacientes |
| `apps.citas` | Agendamiento y calendario de citas |
| `apps.preclinica` | Signos vitales y triaje |
| `apps.consulta` | Consulta médica (wizard de 7 pasos) |

## Variables de entorno

Copiar `.env.example` a `.env`:

```env
SECRET_KEY=dev-xmedical-change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,.localhost
DB_NAME=xmedical
DB_USER=xmedical_user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
TIME_ZONE=America/Tegucigalpa
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## Scripts útiles

```bash
# Migraciones
python manage.py migrate

# Cargar datos de prueba
python manage.py loaddata fixtures/initial_data.json

# Crear superusuario
python manage.py createsuperuser

# Servidor de desarrollo
python manage.py runserver
```

### Scripts Windows

| Script | Acción |
|---|---|
| `levantar_xmedical.bat` | Inicia PostgreSQL y Redis con Docker |
| `bajar_xmedical.bat` | Detiene servicios Docker |
| `reiniciar_xmedical.bat` | Reinicia PostgreSQL y Redis |
| `start_xmedical.bat` | Inicia Django en desarrollo (requiere Docker activo) |

## Documentación

| Documento | Contenido |
|---|---|
| [`GUIA_CONFIGURACION.md`](GUIA_CONFIGURACION.md) | Configuración paso a paso |
| [`USUARIOS_PRUEBA.md`](USUARIOS_PRUEBA.md) | Credenciales y rutas de prueba |
| [`docs/0 Documento de Descripcion General.md`](docs/0%20Documento%20de%20Descripcion%20General.md) | Visión del producto |
| [`docs/4 Documento Arquitectura de alto nivel.md`](docs/4%20Documento%20Arquitectura%20de%20alto%20nivel.md) | Arquitectura Django aprobada |

## Código legado

El directorio `server/` contiene un backend **FastAPI** y `client/` un frontend **React** del prototipo inicial (*verificación de identidad, OCR, biometría*). Ese stack **no se mantiene activamente** y puede eliminarse en futuras versiones.

- Documentación FastAPI (legado): [`server/README.md`](server/README.md), [`docs/informe-tecnico.md`](docs/informe-tecnico.md)
- Documentación React (legado): [`client/README.md`](client/README.md), [`docs/guia-integracion.md`](docs/guia-integracion.md)

## Licencia

Este proyecto está bajo la Licencia MIT.
