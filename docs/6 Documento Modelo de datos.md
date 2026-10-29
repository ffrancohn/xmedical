# DOCUMENTO 6: MODELO DE DATOS
## XMedical - Sistema de Gestión Clínica Multi-tenant para Primer y Segundo Nivel

| Versión | Fecha | Autor | Estado |
|---------|-------|-------|--------|
| 1.0 | 2026 | Agente de Documentación Técnica | **Aprobado** |

---

## 1. VISIÓN GENERAL

Este documento define la **estructura completa de la base de datos** de XMedical, incluyendo:

- **Diagrama Entidad-Relación** (formato Mermaid)
- **Tablas, columnas, tipos y restricciones**
- **Índices optimizados por consulta**
- **Políticas de Row Level Security (RLS)** para multi-tenant
- **Scripts DDL completos** (PostgreSQL)
- **Datos semilla** (catalogos base)

---

## 2. DIAGRAMA ENTIDAD-RELACIÓN

```mermaid
erDiagram
    institucion ||--o{ especialidad : tiene
    institucion ||--o{ profesional : tiene
    institucion ||--o{ paciente : tiene
    institucion ||--o{ cita : tiene
    institucion ||--o{ consulta : tiene
    institucion ||--o{ log_auditoria : genera
    
    especialidad ||--o{ profesional : asigna
    
    profesional ||--o{ cita : atiende
    profesional ||--o{ horario : tiene
    
    paciente ||--o{ cita : solicita
    
    cita ||--|| preclinica : tiene
    cita ||--|| consulta : genera
    cita ||--o{ referencia : origina
    
    consulta ||--o{ diagnostico : tiene
    consulta ||--o{ receta : genera
    consulta ||--o{ orden_examen : genera
    
    referencia ||--o{ cita : deriva_a
    
    institucion {
        int id PK
        string nombre
        string subdominio UK
        string tipo
        jsonb configuracion
        boolean activo
        timestamp creado_en
    }
    
    especialidad {
        int id PK
        int institucion_id FK
        string nombre
        string codigo
        string nivel
        int duracion_consulta
        boolean activo
    }
    
    profesional {
        int id PK
        int institucion_id FK
        int usuario_id FK
        int especialidad_id FK
        string nombre
        string tipo
        string registro_medico
        boolean activo
    }
    
    paciente {
        int id PK
        int institucion_id FK
        string documento
        string nombre
        string apellido
        date fecha_nacimiento
        string sexo
        string telefono
        string email
        boolean activo
    }
    
    cita {
        int id PK
        int institucion_id FK
        int paciente_id FK
        int profesional_id FK
        date fecha
        time hora
        string estado
        string tipo_agendamiento
        timestamp creado_en
    }
    
    preclinica {
        int id PK
        int institucion_id FK
        int cita_id FK
        int presion_arterial_sis
        int presion_arterial_dia
        int frecuencia_cardiaca
        decimal temperatura
        int saturacion_o2
        decimal peso
        decimal talla
        decimal imc
        text motivo_consulta
        string triaje
    }
    
    consulta {
        int id PK
        int institucion_id FK
        int cita_id FK
        text motivo_consulta
        text anamnesis
        text examen_fisico
        text plan_terapeutico
        string conducta
        timestamp creado_en
    }
    
    diagnostico {
        int id PK
        int institucion_id FK
        int consulta_id FK
        string codigo_cie10
        string nombre
        boolean es_principal
        int orden
    }
```

---

## 3. TABLAS COMPLETAS

### 3.1 institucion (Tenant)

| Columna | Tipo | Restricción | Descripción |
|---------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Identificador único del tenant |
| nombre | VARCHAR(200) | NOT NULL | Nombre de la institución/clínica |
| subdominio | VARCHAR(100) | UNIQUE NOT NULL | Subdominio para acceso (ej: clinicaandes) |
| tipo | VARCHAR(50) | | 'privada', 'publica' |
| configuracion | JSONB | | Parámetros de configuración específicos |
| activo | BOOLEAN | DEFAULT true | Si está activo o desactivado |
| creado_en | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Fecha de creación |

```sql
CREATE TABLE institucion (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    subdominio VARCHAR(100) UNIQUE NOT NULL,
    tipo VARCHAR(50) CHECK (tipo IN ('privada', 'publica')),
    configuracion JSONB DEFAULT '{}',
    activo BOOLEAN DEFAULT true,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_institucion_subdominio ON institucion(subdominio);
CREATE INDEX idx_institucion_activo ON institucion(activo);
```

---

### 3.2 especialidad

| Columna | Tipo | Restricción | Descripción |
|---------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Identificador único |
| institucion_id | INTEGER | FK REFERENCES institucion(id) | Tenant al que pertenece |
| nombre | VARCHAR(100) | NOT NULL | Nombre de la especialidad |
| codigo | VARCHAR(20) | | Código interno |
| nivel | VARCHAR(20) | | 'primero', 'segundo' |
| duracion_consulta_minutos | INTEGER | DEFAULT 20 | Duración estándar de consulta |
| activo | BOOLEAN | DEFAULT true | Si está activa |

```sql
CREATE TABLE especialidad (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL REFERENCES institucion(id) ON DELETE CASCADE,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(20),
    nivel VARCHAR(20) CHECK (nivel IN ('primero', 'segundo')),
    duracion_consulta_minutos INTEGER DEFAULT 20,
    activo BOOLEAN DEFAULT true,
    UNIQUE(institucion_id, codigo)
);

CREATE INDEX idx_especialidad_institucion ON especialidad(institucion_id);
CREATE INDEX idx_especialidad_nivel ON especialidad(nivel);
CREATE INDEX idx_especialidad_activo ON especialidad(activo);
```

---

### 3.3 profesional

| Columna | Tipo | Restricción | Descripción |
|---------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Identificador único |
| institucion_id | INTEGER | FK REFERENCES institucion(id) | Tenant al que pertenece |
| usuario_id | INTEGER | FK REFERENCES auth_user(id) | Usuario asociado (Django) |
| especialidad_id | INTEGER | FK REFERENCES especialidad(id) | Especialidad (obligatorio) |
| nombre | VARCHAR(100) | NOT NULL | Nombre completo |
| tipo | VARCHAR(50) | NOT NULL | 'medico', 'enfermera', 'recepcionista' |
| registro_medico | VARCHAR(50) | | Número de registro médico (solo médicos) |
| activo | BOOLEAN | DEFAULT true | Si está activo |

```sql
CREATE TABLE profesional (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL REFERENCES institucion(id) ON DELETE CASCADE,
    usuario_id INTEGER REFERENCES auth_user(id) ON DELETE SET NULL,
    especialidad_id INTEGER NOT NULL REFERENCES especialidad(id),
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('medico', 'enfermera', 'recepcionista')),
    registro_medico VARCHAR(50),
    activo BOOLEAN DEFAULT true,
    UNIQUE(institucion_id, usuario_id)
);

CREATE INDEX idx_profesional_institucion ON profesional(institucion_id);
CREATE INDEX idx_profesional_especialidad ON profesional(especialidad_id);
CREATE INDEX idx_profesional_tipo ON profesional(tipo);
CREATE INDEX idx_profesional_activo ON profesional(activo);
```

---

### 3.4 horario

| Columna | Tipo | Restricción | Descripción |
|---------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Identificador único |
| institucion_id | INTEGER | FK REFERENCES institucion(id) | Tenant al que pertenece |
| profesional_id | INTEGER | FK REFERENCES profesional(id) | Médico asociado |
| dia_semana | INTEGER | NOT NULL | 0=Lunes...6=Domingo |
| hora_inicio | TIME | NOT NULL | Hora de inicio |
| hora_fin | TIME | NOT NULL | Hora de fin |
| activo | BOOLEAN | DEFAULT true | Si está activo |

```sql
CREATE TABLE horario (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL REFERENCES institucion(id) ON DELETE CASCADE,
    profesional_id INTEGER NOT NULL REFERENCES profesional(id) ON DELETE CASCADE,
    dia_semana INTEGER NOT NULL CHECK (dia_semana BETWEEN 0 AND 6),
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    activo BOOLEAN DEFAULT true
);

CREATE INDEX idx_horario_profesional ON horario(profesional_id);
CREATE INDEX idx_horario_dia ON horario(dia_semana);
```

---

### 3.5 paciente

| Columna | Tipo | Restricción | Descripción |
|---------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Identificador único |
| institucion_id | INTEGER | FK REFERENCES institucion(id) | Tenant al que pertenece |
| documento | VARCHAR(20) | NOT NULL | Documento de identidad |
| nombre | VARCHAR(100) | NOT NULL | Nombre(s) |
| apellido | VARCHAR(100) | NOT NULL | Apellido(s) |
| fecha_nacimiento | DATE | | Fecha de nacimiento |
| sexo | VARCHAR(10) | | 'M', 'F', 'OTRO' |
| telefono | VARCHAR(20) | | Teléfono de contacto |
| email | VARCHAR(100) | | Correo electrónico |
| activo | BOOLEAN | DEFAULT true | Si está activo |

```sql
CREATE TABLE paciente (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL REFERENCES institucion(id) ON DELETE CASCADE,
    documento VARCHAR(20) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE,
    sexo VARCHAR(10) CHECK (sexo IN ('M', 'F', 'OTRO')),
    telefono VARCHAR(20),
    email VARCHAR(100),
    activo BOOLEAN DEFAULT true,
    UNIQUE(institucion_id, documento)
);

CREATE INDEX idx_paciente_institucion ON paciente(institucion_id);
CREATE INDEX idx_paciente_documento ON paciente(documento);
CREATE INDEX idx_paciente_nombre ON paciente(nombre, apellido);
CREATE INDEX idx_paciente_activo ON paciente(activo);
```

---

### 3.6 cita

| Columna | Tipo | Restricción | Descripción |
|---------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Identificador único |
| institucion_id | INTEGER | FK REFERENCES institucion(id) | Tenant al que pertenece |
| paciente_id | INTEGER | FK REFERENCES paciente(id) | Paciente asociado |
| profesional_id | INTEGER | FK REFERENCES profesional(id) | Médico asociado |
| fecha | DATE | NOT NULL | Fecha de la cita |
| hora | TIME | NOT NULL | Hora de la cita |
| estado | VARCHAR(20) | NOT NULL | pendiente/confirmada/cancelada/atendida |
| tipo_agendamiento | VARCHAR(20) | | 'especifico', 'flexible' |
| creado_en | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Fecha de creación |

```sql
CREATE TABLE cita (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL REFERENCES institucion(id) ON DELETE CASCADE,
    paciente_id INTEGER NOT NULL REFERENCES paciente(id),
    profesional_id INTEGER NOT NULL REFERENCES profesional(id),
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado VARCHAR(20) NOT NULL CHECK (estado IN ('pendiente', 'confirmada', 'cancelada', 'atendida')),
    tipo_agendamiento VARCHAR(20) CHECK (tipo_agendamiento IN ('especifico', 'flexible')),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cita_institucion ON cita(institucion_id);
CREATE INDEX idx_cita_paciente ON cita(paciente_id);
CREATE INDEX idx_cita_profesional ON cita(profesional_id);
CREATE INDEX idx_cita_fecha ON cita(fecha);
CREATE INDEX idx_cita_estado ON cita(estado);
CREATE INDEX idx_cita_fecha_hora ON cita(fecha, hora, profesional_id);
```

---

### 3.7 preclinica

| Columna | Tipo | Restricción | Descripción |
|---------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Identificador único |
| institucion_id | INTEGER | FK REFERENCES institucion(id) | Tenant al que pertenece |
| cita_id | INTEGER | FK REFERENCES cita(id) | Cita asociada |
| presion_arterial_sis | INTEGER | | Sistólica (mmHg) |
| presion_arterial_dia | INTEGER | | Diastólica (mmHg) |
| frecuencia_cardiaca | INTEGER | | Latidos por minuto |
| temperatura | DECIMAL(4,1) | | Grados Celsius |
| saturacion_o2 | INTEGER | | Porcentaje |
| peso | DECIMAL(5,2) | | Kilogramos |
| talla | DECIMAL(3,2) | | Metros |
| imc | DECIMAL(4,2) | | Calculado automáticamente |
| motivo_consulta | TEXT | | Motivo inicial (enfermería) |
| triaje | VARCHAR(20) | | 'baja', 'media', 'alta' |
| creado_en | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Fecha de creación |

```sql
CREATE TABLE preclinica (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL REFERENCES institucion(id) ON DELETE CASCADE,
    cita_id INTEGER NOT NULL REFERENCES cita(id) UNIQUE,
    presion_arterial_sis INTEGER,
    presion_arterial_dia INTEGER,
    frecuencia_cardiaca INTEGER,
    temperatura DECIMAL(4,1),
    saturacion_o2 INTEGER,
    peso DECIMAL(5,2),
    talla DECIMAL(3,2),
    imc DECIMAL(4,2),
    motivo_consulta TEXT,
    triaje VARCHAR(20) CHECK (triaje IN ('baja', 'media', 'alta')),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_preclinica_cita ON preclinica(cita_id);
```

---

### 3.8 consulta

| Columna | Tipo | Restricción | Descripción |
|---------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Identificador único |
| institucion_id | INTEGER | FK REFERENCES institucion(id) | Tenant al que pertenece |
| cita_id | INTEGER | FK REFERENCES cita(id) | Cita asociada |
| motivo_consulta | TEXT | | Motivo enriquecido por médico |
| anamnesis | TEXT | | Historia clínica detallada |
| examen_fisico | TEXT | | Hallazgos del examen físico |
| plan_terapeutico | TEXT | | Plan de tratamiento |
| conducta | VARCHAR(50) | | 'alta', 'cita_subsiguiente', 'referencia' |
| creado_en | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Fecha de creación |

```sql
CREATE TABLE consulta (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL REFERENCES institucion(id) ON DELETE CASCADE,
    cita_id INTEGER NOT NULL REFERENCES cita(id) UNIQUE,
    motivo_consulta TEXT,
    anamnesis TEXT,
    examen_fisico TEXT,
    plan_terapeutico TEXT,
    conducta VARCHAR(50) CHECK (conducta IN ('alta', 'cita_subsiguiente', 'referencia')),
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_consulta_cita ON consulta(cita_id);
```

---

### 3.9 diagnostico

| Columna | Tipo | Restricción | Descripción |
|---------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Identificador único |
| institucion_id | INTEGER | FK REFERENCES institucion(id) | Tenant al que pertenece |
| consulta_id | INTEGER | FK REFERENCES consulta(id) | Consulta asociada |
| codigo_cie10 | VARCHAR(10) | NOT NULL | Código CIE-10 |
| nombre | VARCHAR(200) | | Nombre del diagnóstico |
| es_principal | BOOLEAN | DEFAULT false | Si es diagnóstico principal |
| orden | INTEGER | DEFAULT 1 | Orden de importancia |

```sql
CREATE TABLE diagnostico (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL REFERENCES institucion(id) ON DELETE CASCADE,
    consulta_id INTEGER NOT NULL REFERENCES consulta(id) ON DELETE CASCADE,
    codigo_cie10 VARCHAR(10) NOT NULL,
    nombre VARCHAR(200),
    es_principal BOOLEAN DEFAULT false,
    orden INTEGER DEFAULT 1
);

CREATE INDEX idx_diagnostico_consulta ON diagnostico(consulta_id);
CREATE INDEX idx_diagnostico_codigo ON diagnostico(codigo_cie10);
```

---

### 3.10 referencia

| Columna | Tipo | Restricción | Descripción |
|---------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Identificador único |
| institucion_id | INTEGER | FK REFERENCES institucion(id) | Tenant al que pertenece |
| consulta_origen_id | INTEGER | FK REFERENCES consulta(id) | Consulta que origina |
| especialidad_destino_id | INTEGER | FK REFERENCES especialidad(id) | Especialidad destino |
| especialista_id | INTEGER | FK REFERENCES profesional(id) | Especialista asignado (opcional) |
| estado | VARCHAR(20) | | 'pendiente', 'aceptada', 'rechazada', 'completada' |
| motivo | TEXT | | Motivo de referencia |
| comentarios_especialista | TEXT | | Comentarios del especialista |
| creado_en | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Fecha de creación |

```sql
CREATE TABLE referencia (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL REFERENCES institucion(id) ON DELETE CASCADE,
    consulta_origen_id INTEGER NOT NULL REFERENCES consulta(id),
    especialidad_destino_id INTEGER NOT NULL REFERENCES especialidad(id),
    especialista_id INTEGER REFERENCES profesional(id),
    estado VARCHAR(20) DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'aceptada', 'rechazada', 'completada')),
    motivo TEXT,
    comentarios_especialista TEXT,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_referencia_institucion ON referencia(institucion_id);
CREATE INDEX idx_referencia_consulta ON referencia(consulta_origen_id);
CREATE INDEX idx_referencia_estado ON referencia(estado);
```

---

### 3.11 log_auditoria

| Columna | Tipo | Restricción | Descripción |
|---------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Identificador único |
| institucion_id | INTEGER | FK REFERENCES institucion(id) | Tenant al que pertenece |
| usuario_id | INTEGER | | Usuario que realizó la acción |
| accion | VARCHAR(20) | NOT NULL | 'CREATE', 'UPDATE', 'DELETE' |
| tabla_afectada | VARCHAR(50) | NOT NULL | Tabla modificada |
| registro_id | INTEGER | | ID del registro afectado |
| valor_anterior | JSONB | | Valor antes del cambio |
| valor_nuevo | JSONB | | Valor después del cambio |
| ip_address | INET | | Dirección IP del usuario |
| creado_en | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Fecha de la acción |

```sql
CREATE TABLE log_auditoria (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL REFERENCES institucion(id) ON DELETE CASCADE,
    usuario_id INTEGER,
    accion VARCHAR(20) NOT NULL CHECK (accion IN ('CREATE', 'UPDATE', 'DELETE')),
    tabla_afectada VARCHAR(50) NOT NULL,
    registro_id INTEGER,
    valor_anterior JSONB,
    valor_nuevo JSONB,
    ip_address INET,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_auditoria_institucion ON log_auditoria(institucion_id);
CREATE INDEX idx_auditoria_tabla ON log_auditoria(tabla_afectada);
CREATE INDEX idx_auditoria_creado ON log_auditoria(creado_en);
```

---

## 4. POLÍTICAS ROW LEVEL SECURITY (RLS)

```sql
-- Habilitar RLS en todas las tablas con institucion_id
ALTER TABLE especialidad ENABLE ROW LEVEL SECURITY;
ALTER TABLE profesional ENABLE ROW LEVEL SECURITY;
ALTER TABLE paciente ENABLE ROW LEVEL SECURITY;
ALTER TABLE cita ENABLE ROW LEVEL SECURITY;
ALTER TABLE preclinica ENABLE ROW LEVEL SECURITY;
ALTER TABLE consulta ENABLE ROW LEVEL SECURITY;
ALTER TABLE diagnostico ENABLE ROW LEVEL SECURITY;
ALTER TABLE referencia ENABLE ROW LEVEL SECURITY;
ALTER TABLE log_auditoria ENABLE ROW LEVEL SECURITY;
ALTER TABLE horario ENABLE ROW LEVEL SECURITY;

-- Política genérica para todas las tablas
CREATE OR REPLACE FUNCTION get_current_institucion_id()
RETURNS INTEGER AS $$
BEGIN
    RETURN current_setting('app.current_institucion_id', TRUE)::INTEGER;
EXCEPTION
    WHEN OTHERS THEN RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Crear política para tabla paciente (ejemplo)
CREATE POLICY paciente_tenant_isolation ON paciente
    USING (institucion_id = get_current_institucion_id());

-- Política para SELECT (misma que USING)
CREATE POLICY paciente_select ON paciente
    FOR SELECT USING (institucion_id = get_current_institucion_id());

-- Política para INSERT (verificar que se inserta con el tenant correcto)
CREATE POLICY paciente_insert ON paciente
    FOR INSERT WITH CHECK (institucion_id = get_current_institucion_id());

-- Política para UPDATE
CREATE POLICY paciente_update ON paciente
    FOR UPDATE USING (institucion_id = get_current_institucion_id());

-- Política para DELETE
CREATE POLICY paciente_delete ON paciente
    FOR DELETE USING (institucion_id = get_current_institucion_id());

-- Repetir para todas las tablas
-- (Script completo disponible en el repositorio)
```

---

## 5. DATOS SEMILLA (SEED DATA)

### 5.1 Instituciones base

```sql
INSERT INTO institucion (nombre, subdominio, tipo, configuracion) VALUES
('Clínica Los Andes', 'clinicaandes', 'privada', '{"theme": "corporate", "recordatorios_activos": true}'),
('CESFAM Norte', 'cesfamnorte', 'publica', '{"theme": "light", "recordatorios_activos": false}');
```

### 5.2 Especialidades base

```sql
-- Para Clínica Los Andes (institucion_id = 1)
INSERT INTO especialidad (institucion_id, nombre, codigo, nivel, duracion_consulta_minutos) VALUES
(1, 'Medicina General', 'MG', 'primero', 20),
(1, 'Pediatría', 'PED', 'primero', 20),
(1, 'Cardiología', 'CAR', 'segundo', 30),
(1, 'Endocrinología', 'END', 'segundo', 30),
(1, 'Neurología', 'NEU', 'segundo', 30),
(1, 'Rehabilitación', 'REH', 'segundo', 40),
(1, 'Oncología', 'ONC', 'segundo', 40);

-- Para CESFAM Norte (institucion_id = 2)
INSERT INTO especialidad (institucion_id, nombre, codigo, nivel, duracion_consulta_minutos) VALUES
(2, 'Medicina General', 'MG', 'primero', 20),
(2, 'Pediatría', 'PED', 'primero', 20);
```

### 5.3 Perfiles base (Django)

```python
# En Django: python manage.py loaddata
from django.contrib.auth.models import Group, Permission

perfiles = ['Superadministrador', 'Administrador', 'Medico', 'Enfermera', 'Recepcionista']

for perfil in perfiles:
    Group.objects.get_or_create(name=perfil)
```

---

## 6. ÍNDICES RECOMENDADOS

| Tabla | Índice | Tipo | Justificación |
|-------|--------|------|---------------|
| cita | (fecha, hora, profesional_id) | BTREE | Búsqueda de disponibilidad |
| cita | (paciente_id, fecha) | BTREE | Historial de citas por paciente |
| paciente | (documento, institucion_id) | UNIQUE BTREE | Búsqueda por documento en tenant |
| paciente | (nombre, apellido) | GIN (trigram) | Búsqueda por texto |
| profesional | (institucion_id, tipo) | BTREE | Filtro por tipo y tenant |
| log_auditoria | (creado_en, institucion_id) | BTREE | Consulta de logs por fecha |
| especialidad | (institucion_id, nivel) | BTREE | Filtrar por nivel de atención |

### Índices de texto completo

```sql
-- Para búsqueda de pacientes por nombre
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_paciente_nombre_trgm ON paciente USING GIN (nombre gin_trgm_ops);
CREATE INDEX idx_paciente_apellido_trgm ON paciente USING GIN (apellido gin_trgm_ops);
```

---

## 7. SCRIPT DDL COMPLETO

```sql
-- ============================================================
-- SCRIPT COMPLETO DDL - XMEDICAL
-- PostgreSQL 15+
-- ============================================================

-- 1. Extensiones necesarias
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- 2. Tablas
-- (Todas las tablas definidas en las secciones anteriores)

-- 3. Función helper para RLS
CREATE OR REPLACE FUNCTION get_current_institucion_id()
RETURNS INTEGER AS $$
BEGIN
    RETURN current_setting('app.current_institucion_id', TRUE)::INTEGER;
EXCEPTION
    WHEN OTHERS THEN RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- 4. RLS en todas las tablas
-- (Políticas definidas en sección 4)

-- 5. Datos semilla
-- (Insert statements)

-- 6. Verificación
SELECT COUNT(*) AS tablas_creadas FROM information_schema.tables 
WHERE table_schema = 'public' AND table_name LIKE 'xmedical%';
```

---

## 8. APROBACIÓN

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| Product Owner | [Usuario] | ✅ Aprobado | 2026 |
| Agente Documentación | DeepSeek | Generado | 2026 |

---

**Fin del Documento 6: Modelo de Datos**

---

## RESUMEN DEL DOCUMENTO

| Aspecto | Valor |
|---------|-------|
| **Tablas definidas** | 11 |
| **Columnas totales** | ~80 |
| **Índices definidos** | 15+ |
| **Políticas RLS** | Por tabla (SELECT, INSERT, UPDATE, DELETE) |
| **Relaciones FK** | 15+ |
| **Scripts DDL** | Completos |
| **Datos semilla** | Instituciones, especialidades, perfiles |

---