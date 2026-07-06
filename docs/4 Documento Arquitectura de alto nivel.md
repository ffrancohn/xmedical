# DOCUMENTO 4: ARQUITECTURA DE ALTO NIVEL
## XMedical - Sistema de Gestión Clínica Multi-tenant para Primer y Segundo Nivel

| Versión | Fecha | Autor | Estado |
|---------|-------|-------|--------|
| 1.1 | 2026-07 | Equipo XMedical | **Actualizado** |
| 1.0 | 2026 | Agente de Documentación Técnica | Aprobado |

---

## 1. VISIÓN GENERAL DE LA ARQUITECTURA

XMedical utiliza una **arquitectura monolítica modular** con separación de responsabilidades, diseñada para soportar **multi-tenant** desde el inicio, con capacidad de evolución hacia **microservicios** para componentes de IA en fases posteriores.

### 1.0 Estado de implementación (julio 2026)

| Capa | Implementado | Pendiente |
|------|--------------|-----------|
| Django + apps clínicas | ✅ | — |
| Frontend web (plantillas) | ✅ | — |
| Producción `xmedical.cloud` | ✅ Apache + Gunicorn + HTTPS | — |
| API REST `/api/v1/` | — | 🔮 [Doc 13](13%20App%20movil%20y%20API%20REST.md) |
| App móvil | — | 🔮 Repo separado |
| Auth web | ✅ Sesión Django | — |
| Auth API | — | 🔮 JWT |
| Microservicio IA (FastAPI) | — | 🔮 Fase 4 producto |

### 1.1 Diagrama de arquitectura de alto nivel

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              CLIENTES                                                 │
├───────────────┬───────────────┬───────────────┬───────────────┬─────────────────────┤
│   Navegador   │   Navegador   │   Navegador   │   App móvil   │   API Externa       │
│   (Médico)    │  (Enfermera)  │(Recepcionista)│  (futuro)     │   (Integraciones)   │
└───────┬───────┴───────┬───────┴───────┬───────┴───────┬───────┴─────────┬───────────┘
        │               │               │               │                 │
        ▼               ▼               ▼               ▼                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              CDN / LOAD BALANCER (Nginx)                              │
│                              - SSL Termination                                        │
│                              - Rate Limiting                                          │
│                              - Subdomain Routing (multi-tenant)                       │
└─────────────────────────────────────────────────────────────────────────────────────┘
        │               │               │               │                 │
        ▼               ▼               ▼               ▼                 ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              DJANGO APPLICATION (Gunicorn)                           │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                         MIDDLEWARE (Multi-tenant)                             │   │
│  │  - TenantIdentificationMiddleware (subdominio → tenant_id)                    │   │
│  │  - AuthenticationMiddleware (JWT/Session)                                    │   │
│  │  - RBACMiddleware (control de acceso por rol)                                │   │
│  │  - AuditMiddleware (registro de acciones)                                    │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                      │
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐           │
│  │   MÓDULOS      │ │   MÓDULOS     │ │   MÓDULOS     │ │   MÓDULOS     │           │
│  │   PRINCIPALES  │ │   CLÍNICOS    │ │   ADMINS      │ │   IA (Futuro) │           │
│  ├───────────────┤ ├───────────────┤ ├───────────────┤ ├───────────────┤           │
│  │ • Gestión      │ │ • Preclínica  │ │ • Parametri-  │ │ • Sugerencia  │           │
│  │   de Usuarios  │ │ • Consulta    │ │   zación      │ │   diagnóstica │           │
│  │ • Citas        │ │   Médica      │ │ • Especiali-  │ │ • Modelos     │           │
│  │ • Pacientes    │ │ • Referencias │ │   dades       │ │   predictivos │           │
│  │ • Facturación  │ │ • Farmacia    │ │ • Horarios    │ │ • Visión      │           │
│  │   (opcional)   │ │ • Exámenes    │ │ • Perfiles    │ │   artificial  │           │
│  └───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘           │
│                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                          ORM (Django Models)                                  │   │
│  │  - Filtrado automático por institucion_id (RLS)                              │   │
│  │  - Relaciones con prefetch_related optimizado                                │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘
        │               │               │               │
        ▼               ▼               ▼               ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              POSTGRESQL DATABASE                                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                         ROW LEVEL SECURITY (RLS)                              │   │
│  │  - Políticas por tabla: WHERE institucion_id = current_setting(...)         │   │
│  │  - Aislamiento automático sin código adicional                               │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐        │   │
│  │  │  Tablas de    │ │  Tablas de   │ │  Tablas de   │ │  Tablas de   │        │   │
│  │  │  Tenant       │ │  Negocio     │ │  Clínicas    │ │  Auditoría   │        │   │
│  │  ├──────────────┤ ├──────────────┤ ├──────────────┤ ├──────────────┤        │   │
│  │  │ • institucion │ │ • paciente   │ │ • consulta   │ │ • log_       │        │   │
│  │  │ • especialidad│ │ • cita       │ │ • preclinica │ │   auditoria  │        │   │
│  │  │ • profesional │ │ • referencia │ │ • diagnostico│ │ • log_acceso │        │   │
│  │  │ • horario     │ │ • examen     │ │ • receta     │ │              │        │   │
│  │  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘        │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              TAREAS PROGRAMADAS (Celery + Redis)                     │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────────┐           │
│  │ Recordatorios │ │   Backups     │ │   Reportes    │ │   IA Batch    │           │
│  │ de citas      │ │ automáticos   │ │ programados   │ │ (entrenamiento)│           │
│  └───────────────┘ └───────────────┘ └───────────────┘ └───────────────┘           │
└─────────────────────────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              SERVIDORES EXTERNOS                                     │
├───────────────┬───────────────┬───────────────┬───────────────┬─────────────────────┤
│   Email       │   IA - Visión │   IA - LLM    │   Storage     │   Monitoreo         │
│   (SMTP/      │   (Google/AWS/│   (OpenAI/    │   (S3/NFS)    │   (Prometheus/      │
│   SendGrid)   │   Tesseract)  │   Local LLM)  │               │   Grafana)          │
└───────────────┴───────────────┴───────────────┴───────────────┴─────────────────────┘
```

---

## 2. DECISIONES ARQUITECTÓNICAS CLAVE

| Decisión | Elección | Justificación |
|----------|----------|---------------|
| **Arquitectura base** | Monolítica modular (Django) | MVP rápido, menos complejidad, fácil de desplegar |
| **Multi-tenant** | Tabla única + RLS PostgreSQL | Aislamiento garantizado, sin fugas de datos, rendimiento |
| **Base de datos** | PostgreSQL | RLS nativo, JSONB, índices avanzados, fiabilidad |
| **Frontend** | Django templates + DaisyUI | SSR rápido, accesible, SEO amigable, componentes listos |
| **Tareas asíncronas** | Celery + Redis | Recordatorios, backups, IA batch |
| **Separación IA (futuro)** | FastAPI (microservicio) | Escalabilidad independiente, latencia baja |
| **Almacenamiento** | S3 / NFS | Archivos (documentos, logos, QR) |
| **Cache** | Redis | Sesiones, consultas frecuentes, rate limiting |

---

## 3. CAPAS DE LA ARQUITECTURA

### 3.1 Capa de Presentación (Frontend)

| Tecnología | Uso |
|------------|-----|
| **Django Templates** | Vistas server-side renderizadas |
| **DaisyUI + Tailwind CSS** | Componentes UI y estilos |
| **HTMX** (opcional) | Interactividad sin JS pesado |
| **Chart.js / Plotly** | Gráficos en dashboards |
| **Alpine.js** | Interactividad ligera (modales, toggles) |

### 3.2 Capa de Aplicación (Backend)

| Componente | Tecnología | Responsabilidad |
|------------|------------|-----------------|
| **Web Server** | Gunicorn | Servir aplicación Django |
| **Reverse Proxy** | Nginx | SSL, load balancing, subdominios, archivos estáticos |
| **Aplicación** | Django 4.x | Lógica de negocio, ORM, admin, auth |
| **API** | Django REST Framework | Endpoints para integraciones y SPA futuro |
| **Multi-tenant** | Middleware + RLS | Identificación de tenant, aislamiento |

### 3.3 Capa de Datos

| Componente | Tecnología | Responsabilidad |
|------------|------------|-----------------|
| **Base de datos** | PostgreSQL 15+ | Datos transaccionales |
| **Row Level Security** | PostgreSQL RLS | Aislamiento multi-tenant a nivel BD |
| **Cache** | Redis | Sesiones, consultas frecuentes, rate limiting |
| **Message Broker** | Redis (Celery) | Cola de tareas asíncronas |

### 3.4 Capa de Integración

| Componente | Tecnología | Propósito |
|------------|------------|-----------|
| **Email** | SMTP / SendGrid | Recordatorios, notificaciones |
| **IA - Visión** | Google Cloud Vision / AWS Rekognition / Tesseract | Validación de documentos |
| **IA - LLM** | OpenAI API / Local LLM (Ollama) | Sugerencia diagnóstica |
| **Storage** | S3 / NFS | Logos, documentos, QR |
| **Monitoreo** | Prometheus + Grafana | Métricas, alertas |

---

## 4. FLUJOS DE DATOS PRINCIPALES

### 4.1 Flujo de autenticación multi-tenant

```
1. Usuario ingresa a clinicaandes.xmedical.com
       ↓
2. Nginx identifica subdominio → header X-Tenant-ID
       ↓
3. Django middleware: TenantIdentificationMiddleware
   - Extrae subdominio
   - Busca tenant_id en tabla institucion
   - Inyecta en conexión DB: SET app.current_institucion_id = X
       ↓
4. Usuario ingresa credenciales
       ↓
5. Django valida usuario Y pertenencia al tenant
   (usuario.institucion_id = tenant_id)
       ↓
6. Sesión establecida, todas las consultas SQL tienen RLS activo
       ↓
7. Usuario accede a dashboard filtrado por su tenant
```

### 4.2 Flujo de consulta médica (con RLS)

```
1. Médico autenticado (tenant_id = 1)
       ↓
2. Solicita lista de pacientes (SELECT * FROM paciente)
       ↓
3. PostgreSQL RLS aplica automáticamente:
   WHERE institucion_id = current_setting('app.current_institucion_id')
       ↓
4. Solo retorna pacientes del tenant 1
       ↓
5. Médico selecciona paciente → inicia consulta
       ↓
6. Guarda consulta con institucion_id = 1 (automático)
       ↓
7. Consulta guardada, solo visible por tenant 1
```

### 4.3 Flujo de recordatorios (tarea programada)

```
1. Celery Beat programa tarea cada hora
       ↓
2. Tarea itera sobre todas las instituciones activas
       ↓
3. Para cada institución, cambia el tenant context:
   connection.execute("SET app.current_institucion_id = X")
       ↓
4. Consulta citas del día siguiente de esa institución
       ↓
5. Envía correos usando plantillas por tenant
       ↓
6. Registra envíos en log_notificaciones
```

---

## 5. MODELO DE DATOS PRELIMINAR

### 5.1 Tablas principales y relaciones

```sql
-- Tenant (institución)
CREATE TABLE institucion (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    subdominio VARCHAR(100) UNIQUE NOT NULL,
    tipo VARCHAR(50), -- 'privada', 'publica'
    configuracion JSONB,
    activo BOOLEAN DEFAULT true,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Especialidades (por tenant)
CREATE TABLE especialidad (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL REFERENCES institucion(id),
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(20),
    nivel VARCHAR(20), -- 'primero', 'segundo'
    duracion_consulta_minutos INTEGER DEFAULT 20,
    activo BOOLEAN DEFAULT true
);

-- Profesionales (médicos, enfermeras, recepcionistas)
CREATE TABLE profesional (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL REFERENCES institucion(id),
    usuario_id INTEGER REFERENCES auth_user(id),
    especialidad_id INTEGER REFERENCES especialidad(id),
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(50), -- 'medico', 'enfermera', 'recepcionista'
    registro_medico VARCHAR(50),
    activo BOOLEAN DEFAULT true
);

-- Pacientes (por tenant)
CREATE TABLE paciente (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL REFERENCES institucion(id),
    documento VARCHAR(20) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    sexo VARCHAR(10),
    telefono VARCHAR(20),
    email VARCHAR(100),
    activo BOOLEAN DEFAULT true
);

-- Citas
CREATE TABLE cita (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL REFERENCES institucion(id),
    paciente_id INTEGER NOT NULL REFERENCES paciente(id),
    profesional_id INTEGER NOT NULL REFERENCES profesional(id),
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado VARCHAR(20), -- 'pendiente', 'confirmada', 'cancelada', 'atendida'
    tipo_agendamiento VARCHAR(20), -- 'especifico', 'flexible'
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Preclínica
CREATE TABLE preclinica (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL REFERENCES institucion(id),
    cita_id INTEGER NOT NULL REFERENCES cita(id),
    presion_arterial_sis INTEGER,
    presion_arterial_dia INTEGER,
    frecuencia_cardiaca INTEGER,
    temperatura DECIMAL(4,1),
    saturacion_o2 INTEGER,
    peso DECIMAL(5,2),
    talla DECIMAL(3,2),
    imc DECIMAL(4,2), -- calculado
    motivo_consulta TEXT,
    triaje VARCHAR(20), -- 'baja', 'media', 'alta'
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Consulta médica
CREATE TABLE consulta (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL REFERENCES institucion(id),
    cita_id INTEGER NOT NULL REFERENCES cita(id),
    motivo_consulta TEXT,
    anamnesis TEXT,
    examen_fisico TEXT,
    plan_terapeutico TEXT,
    conducta VARCHAR(50), -- 'alta', 'cita_subsiguiente', 'referencia'
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Diagnósticos (CIE-10)
CREATE TABLE diagnostico (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL REFERENCES institucion(id),
    consulta_id INTEGER NOT NULL REFERENCES consulta(id),
    codigo_cie10 VARCHAR(10) NOT NULL,
    nombre VARCHAR(200),
    es_principal BOOLEAN DEFAULT false,
    orden INTEGER DEFAULT 1
);

-- Auditoría (con tenant)
CREATE TABLE log_auditoria (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL REFERENCES institucion(id),
    usuario_id INTEGER,
    accion VARCHAR(20), -- 'CREATE', 'UPDATE', 'DELETE'
    tabla_afectada VARCHAR(50),
    registro_id INTEGER,
    valor_anterior JSONB,
    valor_nuevo JSONB,
    ip_address INET,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Políticas RLS
ALTER TABLE paciente ENABLE ROW LEVEL SECURITY;
CREATE POLICY paciente_tenant_isolation ON paciente
    USING (institucion_id = current_setting('app.current_institucion_id')::INTEGER);

ALTER TABLE cita ENABLE ROW LEVEL SECURITY;
CREATE POLICY cita_tenant_isolation ON cita
    USING (institucion_id = current_setting('app.current_institucion_id')::INTEGER);

-- (repetir para todas las tablas con institucion_id)
```

### 5.2 Diagrama entidad-relación (simplificado)

```
┌─────────────────┐
│   institucion   │
│  (TENANT)       │
└────────┬────────┘
         │ 1
         │
         ├──────────────────────────────────────┐
         │                                      │
         ▼ 1:N                                  ▼ 1:N
┌─────────────────┐                    ┌─────────────────┐
│  especialidad   │                    │   profesional   │
└─────────────────┘                    └────────┬────────┘
                                                  │ 1
                                                  │
         ┌──────────────────────────────────────┘
         │
         ▼ 1:N
┌─────────────────┐
│     paciente    │
└────────┬────────┘
         │ 1
         │
         ▼ 1:N
┌─────────────────┐      ┌─────────────────┐
│      cita       │──────│   preclinica    │
└────────┬────────┘ 1:1  └─────────────────┘
         │ 1
         │
         ▼ 1:1
┌─────────────────┐      ┌─────────────────┐
│    consulta     │──────│   diagnostico   │
└─────────────────┘ 1:N  └─────────────────┘
```

---

## 6. ENDPOINTS API PRINCIPALES

### 6.1 API REST (Django REST Framework)

| Endpoint | Método | Descripción | Autenticación |
|----------|--------|-------------|---------------|
| `/api/auth/login` | POST | Autenticación | No |
| `/api/auth/logout` | POST | Cerrar sesión | Sí |
| `/api/me` | GET | Usuario actual + tenant | Sí |
| `/api/pacientes` | GET/POST | CRUD pacientes | Sí |
| `/api/pacientes/{id}` | GET/PUT/DELETE | Detalle paciente | Sí |
| `/api/citas` | GET/POST | CRUD citas | Sí |
| `/api/citas/disponibles` | GET | Horarios disponibles | Sí |
| `/api/consultas` | GET/POST | CRUD consultas | Sí |
| `/api/especialidades` | GET | Lista especialidades (del tenant) | Sí |
| `/api/profesionales` | GET | Lista profesionales (del tenant) | Sí |
| `/api/reportes/ausentismo` | GET | Reporte de ausentismo | Sí (admin) |
| `/api/reportes/ocupacion` | GET | Ocupación de agenda | Sí (admin) |

### 6.2 Headers requeridos (integración)

| Header | Valor | Descripción |
|--------|-------|-------------|
| `Authorization` | `Bearer <token>` | Token JWT |
| `X-Institution-ID` (opcional) | `1` | Si no se usa subdominio |
| `Content-Type` | `application/json` | Formato |

---

## 7. DESPLIEGUE SUGERIDO

### 7.1 Arquitectura de despliegue (MVP)

```
┌─────────────────────────────────────────────────────────────────┐
│                         SERVIDOR (VPS/Cloud)                     │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │    Nginx    │  │   Gunicorn  │  │   Celery    │              │
│  │   (proxy)   │──│  (Django)   │  │  (worker)   │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│         │               │               │                        │
│         ▼               ▼               ▼                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    PostgreSQL + Redis                     │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### 7.2 Escalamiento futuro

```
                    ┌─────────────────┐
                    │  Load Balancer  │
                    │    (Nginx)      │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ Django 1 │  │ Django 2 │  │ Django 3 │
        └──────────┘  └──────────┘  └──────────┘
              │              │              │
              └──────────────┼──────────────┘
                             │
                    ┌────────┴────────┐
                    │  PostgreSQL     │
                    │  (Primary +     │
                    │   Replicas)     │
                    └─────────────────┘
```

### 7.3 Requisitos mínimos (MVP)

| Recurso | Mínimo | Recomendado |
|---------|--------|-------------|
| **CPU** | 2 vCPU | 4 vCPU |
| **RAM** | 4 GB | 8 GB |
| **Disco** | 50 GB SSD | 100 GB SSD |
| **Sistema operativo** | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |
| **PostgreSQL** | 15+ | 15+ |
| **Redis** | 6+ | 6+ |

---

## 8. SEGURIDAD EN ARQUITECTURA

| Capa | Medida | Descripción |
|------|--------|-------------|
| **Red** | HTTPS (TLS 1.3) | Todo el tráfico cifrado |
| **Aplicación** | JWT + Sesiones | Tokens con expiración |
| **Base de datos** | RLS | Aislamiento multi-tenant nativo |
| **API** | Rate limiting | 100 req/min por usuario |
| **Auditoría** | Logs | Todos los cambios registrados |
| **Backups** | Cifrados | Almacenados en S3 encriptado |

---

## 9. DECISIONES TECNOLÓGICAS JUSTIFICADAS

| Tecnología | Justificación | Alternativa considerada | Decisión |
|------------|---------------|------------------------|----------|
| **Django** | ORM potente, admin, auth, maduro | FastAPI (menos integrado), Flask (menos funcional) | ✅ Django |
| **PostgreSQL** | RLS nativo para multi-tenant | MySQL (sin RLS) | ✅ PostgreSQL |
| **DaisyUI** | Componentes accesibles, temas | Bootstrap (más genérico), Tailwind solo (más trabajo) | ✅ DaisyUI |
| **Celery** | Estándar para tareas asíncronas | Django Q (menos soporte) | ✅ Celery |
| **FastAPI (futuro)** | Performance para IA | Django + async (menos maduro) | 🔮 Futuro |

---

## 10. DIAGRAMA DE SECUENCIA: CONSULTA MÉDICA

```
Médico      Nginx      Django      PostgreSQL    Celery      Email
   │          │           │            │           │           │
   │───HTTPS──►│           │            │           │           │
   │          │───Subdominio→│           │           │           │
   │          │           │───SET tenant─►│           │           │
   │          │           │            │           │           │
   │          │           │◄───OK───────│           │           │
   │          │           │            │           │           │
   │◄───HTML──│◄──────────│            │           │           │
   │          │           │            │           │           │
   │───POST───►│──────────►│───SELECT───►│           │           │
   │ (guardar)│           │ (con RLS)   │           │           │
   │          │           │            │           │           │
   │          │           │◄───Data────│           │           │
   │          │           │            │           │           │
   │          │           │───INSERT───►│           │           │
   │          │           │            │           │           │
   │          │           │            │───task────►│           │
   │          │           │            │ (recordatorio│           │
   │          │           │            │  si cita   │           │
   │          │           │            │  subsig.)  │           │
   │          │           │            │           │───email───►│
   │          │           │            │           │           │
   │◄───JSON──│◄──────────│◄───────────│           │           │
   │ (éxito)  │           │            │           │           │
```

---

## 11. MONITOREO Y OBSERVABILIDAD

| Componente | Herramienta | Propósito |
|------------|-------------|-----------|
| **Logs** | ELK Stack / Loki | Agregación de logs por tenant |
| **Métricas** | Prometheus + Grafana | CPU, RAM, consultas DB, latencia |
| **Alertas** | Alertmanager | Uso de CPU > 80%, error rate > 1% |
| **APM** | Django Silk / New Relic | Trazabilidad de requests lentos |
| **Health checks** | Django + Nginx | `/health/` endpoint para balanceador |

---

## 12. APROBACIÓN

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| Product Owner | [Usuario] | ✅ Aprobado | 2026 |
| Agente Documentación | DeepSeek | Generado | 2026 |

---

**Fin del Documento 4: Arquitectura de Alto Nivel**

---

## RESUMEN DEL DOCUMENTO

| Aspecto | Valor |
|---------|-------|
| **Diagramas** | 4 (Arquitectura general, ER, despliegue, secuencia) |
| **Capas arquitectónicas** | 4 (Presentación, Aplicación, Datos, Integración) |
| **Tablas en modelo de datos** | 9 principales + RLS |
| **Endpoints API** | 11 endpoints documentados |
| **Decisiones tecnológicas** | 5 justificadas |
| **Multi-tenant** | RLS + TenantIdentificationMiddleware |
| **Escalamiento** | Horizontal (Django) + replicación (PostgreSQL) |

---
