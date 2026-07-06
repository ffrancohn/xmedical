# XMedical - Sistema de Gestión Clínica Multi-tenant

Sistema de gestión clínica para instituciones de primer y segundo nivel de atención. Soporta múltiples clínicas en una sola instalación (multi-tenant por subdominio), con flujos de pacientes, citas, preclínica y consulta médica guiada.

## Arquitectura

| Componente | Tecnología |
|---|---|
| Backend | **Django 4.2** (monolito modular) |
| Base de datos | **PostgreSQL 15** |
| Tareas asíncronas | **Celery** + **Redis** |
| Frontend | Plantillas Django (server-side) |
| Despliegue | **Docker Compose** + Gunicorn + Apache |
| Producción | https://xmedical.cloud |
| App móvil | 🔮 Planificada — ver [`docs/13`](docs/13%20App%20movil%20y%20API%20REST.md) |

Documentación de producto y arquitectura en [`docs/`](docs/).

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
levantar_xmedical.bat
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata fixtures/initial_data.json
python manage.py runserver
```

### Opción 3: Desarrollo local (Linux)

```bash
./setup_venv.sh
./levantar_xmedical.sh
source venv/bin/activate
cp .env.example .env
python manage.py migrate
python manage.py loaddata fixtures/initial_data.json
python manage.py runserver
```

O todo en uno:

```bash
./start_xmedical.sh
```

## Acceso al sistema

- **Producción**: https://xmedical.cloud/auth/login/
- **Local**: http://localhost:8000/auth/login/
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
└── manage.py
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

Copiar `.env.example` a `.env` y ajustar valores. Ver `.env.example` para la lista completa.

## Scripts útiles

```bash
python manage.py migrate
python manage.py loaddata fixtures/initial_data.json
python manage.py createsuperuser
python manage.py runserver
python manage.py collectstatic --noinput
./run_tests.sh                    # pruebas automatizadas
python manage.py test apps.core   # solo tests
```

### Scripts Linux

| Script | Acción |
|---|---|
| `setup_venv.sh` | Crea o recrea el entorno virtual Linux |
| `levantar_xmedical.sh` | Inicia PostgreSQL y Redis con Docker |
| `bajar_xmedical.sh` | Detiene servicios Docker |
| `start_xmedical.sh` | Levanta Docker + Django en desarrollo |

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
| [`docs/README.md`](docs/README.md) | Índice y estado de implementación |
| [`docs/4 Documento Arquitectura de alto nivel.md`](docs/4%20Documento%20Arquitectura%20de%20alto%20nivel.md) | Arquitectura Django |
| [`docs/13 App movil y API REST.md`](docs/13%20App%20movil%20y%20API%20REST.md) | Hoja de ruta app móvil |

## Roadmap

| Fase | Entregable | Estado |
|------|------------|--------|
| MVP web | Django + flujos clínicos | ✅ En producción |
| API REST + JWT | `/api/v1/` para integraciones y móvil | 🔮 Planificado |
| App móvil | iOS/Android (repo separado) | 🔮 Planificado |
| IA (OCR, biometría) | Microservicio FastAPI (Fase 4 producto) | 🔮 Futuro |

## Licencia

Este proyecto está bajo la Licencia MIT.
