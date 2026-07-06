# DOCUMENTO 13: APP MÓVIL Y API REST
## XMedical - Sistema de Gestión Clínica Multi-tenant

| Versión | Fecha | Autor | Estado |
|---------|-------|-------|--------|
| 1.0 | 2026-07 | Equipo XMedical | **Planificado** |

---

## 1. OBJETIVO

Definir cómo XMedical dará soporte a una **aplicación móvil** (iOS/Android) sin reemplazar el sistema web actual. La app móvil consumirá una **API REST JSON** sobre el mismo backend Django.

---

## 2. ESTADO ACTUAL vs. PLANIFICADO

| Componente | Estado actual | Para app móvil |
|------------|---------------|----------------|
| Backend Django | ✅ Implementado | Se mantiene |
| Frontend web (plantillas) | ✅ Implementado | Coexiste con la app |
| Autenticación | ✅ Sesión/cookies (web) | ➕ JWT (API) |
| API REST (`/api/v1/`) | ❌ No implementada | 🔮 A implementar |
| CORS | ⚠️ Dependencia instalada, sin configurar | 🔮 Activar en settings |
| Multi-tenant | ✅ Subdominio (web) | ➕ `institucion_id` en JWT o header |
| Push notifications | ❌ | 🔮 Fase posterior (FCM/APNs) |

> El prototipo FastAPI/React fue eliminado del repositorio. La API móvil se construirá **dentro de Django** con Django REST Framework.

---

## 3. ARQUITECTURA OBJETIVO

```
┌─────────────────┐     ┌─────────────────┐
│  App móvil      │     │  Navegador web  │
│  iOS / Android  │     │  (plantillas)   │
└────────┬────────┘     └────────┬────────┘
         │ HTTPS JSON            │ HTTPS HTML
         │ Bearer JWT            │ Session cookie
         ▼                       ▼
┌─────────────────────────────────────────────┐
│  Apache (SSL)                                │
│  • xmedical.cloud      → web                 │
│  • api.xmedical.cloud  → API (futuro)        │
└────────────────────┬────────────────────────┘
                     ▼
┌─────────────────────────────────────────────┐
│  Gunicorn → Django 4.2                       │
│  ┌─────────────┐  ┌─────────────────────┐   │
│  │ apps/*      │  │ apps/api/ (nuevo)   │   │
│  │ views HTML  │  │ DRF + JWT           │   │
│  └──────┬──────┘  └──────────┬──────────┘   │
│         └──────────┬─────────┘               │
│                    ▼                         │
│              models.py (compartidos)         │
└────────────────────┬────────────────────────┘
                     ▼
              PostgreSQL + Redis + Celery
```

---

## 4. CAMBIOS EN EL BACKEND (NO REEMPLAZOS)

### 4.1 Nueva app Django: `apps/api/`

```
apps/api/
├── __init__.py
├── urls.py              # /api/v1/...
├── authentication.py    # JWT custom claims (institucion_id, rol)
├── permissions.py       # RBAC por rol de Profesional
├── auth/
│   ├── serializers.py
│   └── views.py         # login, refresh, logout
├── pacientes/
│   ├── serializers.py
│   └── views.py
├── citas/
├── preclinica/
└── consulta/
```

### 4.2 Dependencias a añadir

```
djangorestframework
djangorestframework-simplejwt
drf-spectacular          # OpenAPI / Swagger
```

`django-cors-headers` ya está en `requirements.txt`; falta registrarlo en `INSTALLED_APPS` y `MIDDLEWARE`.

### 4.3 Patrón recomendado: servicios compartidos

Extraer lógica de negocio de `views.py` hacia `services.py` en cada app para que web y API no dupliquen reglas:

```python
# apps/citas/services.py
def crear_cita(institucion, datos, usuario): ...

# apps/citas/views.py      → llama a crear_cita (web)
# apps/api/citas/views.py  → llama a crear_cita (API)
```

---

## 5. AUTENTICACIÓN API

### 5.1 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/v1/auth/login/` | Usuario + contraseña → access + refresh |
| POST | `/api/v1/auth/refresh/` | Renovar access token |
| POST | `/api/v1/auth/logout/` | Invalidar refresh (opcional) |

### 5.2 Payload JWT (claims custom)

```json
{
  "user_id": 12,
  "institucion_id": 1,
  "rol": "medico",
  "exp": 1750000000
}
```

### 5.3 Multi-tenant en móvil

La web usa subdominio (`clinica.xmedical.cloud`). La app **no puede depender del subdominio**; alternativas:

| Opción | Descripción | Recomendación |
|--------|-------------|---------------|
| A | `institucion_id` en JWT tras login | ✅ Preferida |
| B | Header `X-Institucion-ID` | Complemento |
| C | Subdominio `api.xmedical.cloud` | Solo endpoint, tenant en token |

El `TenantMiddleware` actual ya excluye el subdominio `api`.

---

## 6. ENDPOINTS API (MVP MÓVIL)

Alineados con el [Documento 9](9%20Documento%20de%20integraciones.md):

| Método | Ruta | Rol típico | Descripción |
|--------|------|------------|-------------|
| GET | `/api/v1/pacientes/` | recepcionista, médico | Listar pacientes |
| POST | `/api/v1/pacientes/` | recepcionista | Crear paciente |
| GET | `/api/v1/pacientes/{id}/` | todos clínicos | Detalle |
| GET | `/api/v1/citas/` | recepcionista, médico | Listar/agenda |
| POST | `/api/v1/citas/` | recepcionista | Agendar |
| PATCH | `/api/v1/citas/{id}/` | recepcionista | Cancelar/reprogramar |
| GET | `/api/v1/preclinica/pendientes/` | enfermera | Cola de triaje |
| POST | `/api/v1/preclinica/` | enfermera | Registrar signos vitales |
| GET | `/api/v1/consultas/` | médico | Consultas del día |
| POST | `/api/v1/consultas/` | médico | Iniciar/guardar consulta |
| GET | `/api/v1/dashboard/` | médico | Resumen agenda |

Documentación interactiva: `/api/v1/docs/` (drf-spectacular).

---

## 7. INFRAESTRUCTURA

| Elemento | Web (actual) | API (futuro) |
|----------|--------------|--------------|
| Dominio | `xmedical.cloud` | `api.xmedical.cloud` |
| SSL | ✅ Let's Encrypt | Certificado adicional |
| Auth | Sesión Django | JWT Bearer |
| Rate limit | — | 100 req/min (doc. seguridad) |

Variables `.env` adicionales previstas:

```env
CORS_ALLOWED_ORIGINS=https://app.xmedical.cloud
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=10080
```

---

## 8. APP MÓVIL (REPOSITORIO SEPARADO)

La app nativa/híbrida **no vive en este repositorio**. Opciones de stack:

| Stack | Ventaja |
|-------|---------|
| Flutter | Una codebase iOS + Android |
| React Native | Equipo con experiencia web |
| Kotlin + Swift | Máximo control nativo |

Funcionalidades por fase:

| Fase | App móvil |
|------|-----------|
| 1 | Login, agenda citas, listado pacientes |
| 2 | Preclínica, consulta simplificada |
| 3 | Push (recordatorios de cita) |
| 4 | Cámara (documentos), modo offline parcial |

---

## 9. QUÉ NO CAMBIA

- Modelos Django existentes (`Paciente`, `Cita`, `Consulta`, etc.)
- PostgreSQL, Redis, Celery
- Sitio web actual para uso en PC
- Flujos clínicos y roles actuales
- Respaldos y multi-institución en BD

---

## 10. PLAN DE IMPLEMENTACIÓN

| Fase | Entregable | Duración estimada |
|------|------------|-------------------|
| 1 | DRF + JWT + login API | 1–2 semanas |
| 2 | API pacientes + citas (lectura/escritura) | 2 semanas |
| 3 | API preclínica + consulta | 2–3 semanas |
| 4 | `api.xmedical.cloud` + CORS + OpenAPI | 1 semana |
| 5 | App móvil MVP (repo aparte) | 4–6 semanas |
| 6 | Push notifications | 2 semanas |

---

## 11. REFERENCIAS

- [Documento 4: Arquitectura](4%20Documento%20Arquitectura%20de%20alto%20nivel.md)
- [Documento 9: Integraciones](9%20Documento%20de%20integraciones.md)
- [Documento 7: Seguridad](7%20Documento%20de%20Seguridad.md)

---

**Fin del Documento 13: App móvil y API REST**
