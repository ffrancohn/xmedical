# DOCUMENTO 2: ALCANCE DEL MVP POR FASES (ACTUALIZADO CON MULTI-TENANT)
## XMedical - Sistema de Gestión Clínica Multi-tenant para Primer, Segundo y Futuro Tercer Nivel

| Versión | Fecha | Autor | Estado |
|---------|-------|-------|--------|
| 2.3 | 2026 | Agente de Documentación Técnica | **Aprobado** |

---

## 1. DEFINICIÓN DEL MVP

El **MVP (Producto Mínimo Viable)** de XMedical comprende las **4 semanas iniciales** de desarrollo, entregando un sistema funcional **multi-tenant** que permite:

- **Múltiples instituciones (clientes)** en una sola instalación con **aislamiento completo de datos**
- Registro de pacientes (presencial y en línea básico) **por institución**
- Agendamiento específico (fecha/hora fija) **por institución**
- **Flujo guiado completo**: Cita → Preclínica → Consulta (1er nivel)
- Registro estructurado de diagnósticos CIE-10 y variables clínicas básicas
- Control de acceso por **perfiles parametrizables** (4 roles básicos por institución + Superadministrador global)
- **Registro de médicos con selección de especialidad obligatoria** (dentro de su institución)
- **Dashboard filtrado por especialidad del médico y por institución**
- **Parametrización inicial por institución**: especialidades, profesionales, horarios
- Dashboard médico con vista de agenda y **flujo paso a paso**

**No incluye** en esta fase: agendamiento flexible, validación IA de documentos, QR, recordatorios, referencias a 2do nivel, modelos predictivos, FastAPI separado, **variables clínicas por especialidad** (Fase 2), ni **tercer nivel (hospitalización)** que está planificado como **visión a futuro**.

---

## 2. ARQUITECTURA MULTI-TENANT (MVP)

### 2.1 Modelo de aislamiento

XMedical utiliza **tabla única con `institucion_id`** + **Row Level Security (RLS)** en PostgreSQL:

```sql
-- Tabla base de tenants
CREATE TABLE institucion (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    subdominio VARCHAR(100) UNIQUE,  -- ej: 'clinicaandes'
    tipo VARCHAR(50),  -- 'privada', 'publica'
    configuracion JSONB,
    activo BOOLEAN DEFAULT true,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Todas las tablas de negocio incluyen institucion_id
CREATE TABLE profesional (
    id SERIAL PRIMARY KEY,
    institucion_id INTEGER NOT NULL REFERENCES institucion(id),
    nombre VARCHAR(100),
    especialidad_id INTEGER,
    -- ... resto de campos
);

-- Política RLS (PostgreSQL)
ALTER TABLE profesional ENABLE ROW LEVEL SECURITY;
CREATE POLICY profesional_tenant_isolation ON profesional
    USING (institucion_id = current_setting('app.current_institucion_id')::INTEGER);
```

### 2.2 Identificación de la institución (tenant)

| Método | Ejemplo | Uso en MVP |
|--------|---------|------------|
| **Subdominio** | `clinicaandes.xmedical.com` | ✅ Método principal |
| **Campo en login** | Usuario selecciona "Clínica Los Andes" | ✅ Respaldo |
| **Header en API** | `X-Institution-ID: 1` | ✅ Para integraciones |

### 2.3 Roles multi-tenant en MVP

| Rol | Alcance | Permisos en MVP |
|-----|---------|-----------------|
| **Superadministrador** | Global | Crear/editar instituciones, gestionar tenants, monitoreo básico |
| **Administrador de institución** | Su institución | Configurar su clínica, usuarios, horarios, especialidades |
| **Médico, Enfermera, Recepcionista** | Su institución | Operaciones diarias de su clínica |

---

## 3. NIVELES DE ATENCIÓN POR FASE

| Nivel | Fase 1 (MVP) | Fase 2 | Fase 3 | 🔮 Futuro |
|-------|--------------|--------|--------|-----------|
| **Primer nivel** (Medicina general) | ✅ Completo (multi-tenant) | ✅ Completo | ✅ Completo | ✅ Completo |
| **Segundo nivel** (Especialidades) | ❌ (solo preparación) | ✅ Completo | ✅ Completo | ✅ Completo |
| **Tercer nivel** (Hospitalización) | ❌ | ❌ | ❌ | 🔮 Planificado |

---

## 4. DESGLOSE POR FASE

### Fase 1 (MVP - 4 semanas) - 1er Nivel + Multi-tenant básico

| # | Componente | Módulo | Prioridad | Criterio de aceptación |
|---|------------|--------|-----------|------------------------|
| **MULTI-TENANT (NUEVO)** |
| 1 | Configuración de instituciones (tenants) | Superadmin | P0 | Crear/editar/desactivar instituciones con nombre, subdominio, tipo |
| 2 | Identificación de tenant por subdominio | Middleware | P0 | Sistema identifica automáticamente la institución por subdominio |
| 3 | Aislamiento de datos por RLS | Base de datos | P0 | Datos de una institución NO son visibles por otra |
| 4 | Login con selección de institución (fallback) | Auth | P1 | Si no hay subdominio, usuario selecciona institución manualmente |
| **PARAMETRIZACIÓN POR INSTITUCIÓN** |
| 5 | Configuración de institución | Admin | P0 | Nombre, logo, tipo (pública/privada), datos de contacto |
| 6 | Configuración de especialidades | Admin | P0 | Crear/editar/eliminar especialidades (por institución) |
| 7 | Configuración de profesionales | Admin | P0 | Registrar médicos, **especialidad obligatoria**, horarios base, **asociados a la institución** |
| 8 | Configuración de horarios | Admin | P0 | Días laborales, horas de atención, bloques por profesional |
| 9 | Configuración de perfiles/roles | Admin | P0 | 4 roles base: Administrador, Recepción, Médico general, Enfermera |
| **REGISTRO DE PACIENTES (POR INSTITUCIÓN)** |
| 10 | Registro presencial | Admisión | P0 | Recepcionista registra paciente < 2 min (asociado a su institución) |
| 11 | Registro en línea básico | Portal público | P0 | Paciente se auto-registra (asociado a la institución del subdominio) |
| 12 | Búsqueda de pacientes | Admisión | P0 | Por documento, nombre o teléfono (filtrado por institución) |
| **AGENDAMIENTO (POR INSTITUCIÓN)** |
| 13 | Agendamiento específico | Citas | P0 | Usuario selecciona especialidad → médico de esa especialidad (de su institución) → fecha → hora |
| 14 | Verificación de disponibilidad | Citas | P0 | Sistema bloquea turno automáticamente (no doble reserva) |
| 15 | Cancelación de cita | Citas | P0 | Con mínimo 2h de anticipación, libera cupo |
| 16 | Listado de citas por día | Citas | P0 | Vista de agenda para médico y recepción, **filtrada por institución y especialidad** |
| **FLUJO GUIADO - PRECLÍNICA (Enfermera)** |
| 17 | Registro de signos vitales | Enfermería | P0 | Peso, talla, TA, temperatura, FC, satO2 |
| 18 | Registro de motivo inicial | Enfermería | P0 | Campo texto para motivo de consulta |
| 19 | Triaje básico | Enfermería | P0 | Prioridad (baja/media/alta) |
| 20 | Finalización de preclínica | Enfermería | P0 | Marcar lista → paciente pasa a "en espera consulta" |
| **FLUJO GUIADO - CONSULTA (Médico 1er nivel)** |
| 21 | Dashboard médico con agenda | Dashboard | P0 | Ver pacientes del día **filtrados por su institución y especialidad** |
| 22 | Inicio de consulta guiada | Consulta | P0 | Botón "Atender" → carga flujo paso a paso |
| 23 | Paso 1: Revisar preclínica | Consulta | P0 | Mostrar signos vitales registrados |
| 24 | Paso 2: Motivo de consulta | Consulta | P0 | Campo texto (puede editar/enriquecer) |
| 25 | Paso 3: Anamnesis | Consulta | P0 | Historia de enfermedad actual, antecedentes básicos |
| 26 | Paso 4: Examen físico | Consulta | P0 | Campos genéricos (en Fase 2 serán por especialidad) |
| 27 | Paso 5: Diagnóstico CIE-10 | Consulta | P0 | Buscador de códigos, selección de 1 diagnóstico principal |
| 28 | Paso 6: Plan terapéutico | Consulta | P0 | Texto libre + opciones (alta/cita subsiguiente) |
| 29 | Paso 7: Resumen y confirmación | Consulta | P0 | Visualización de todos los datos antes de guardar |
| 30 | Guardado de consulta | Consulta | P0 | Persistir todos los datos en BD (con institucion_id) |
| **HISTORIA CLÍNICA** |
| 31 | Visualización de HCE | Consulta | P0 | Ver encuentros previos del paciente (solo de su institución) |
| 32 | Detalle de consulta anterior | HCE | P0 | Ver diagnóstico, plan, medicamentos de consultas previas |
| **SEGURIDAD MULTI-TENANT** |
| 33 | Autenticación con tenant | Seguridad | P0 | Login valida usuario Y su acceso a la institución |
| 34 | Autorización por rol + tenant | Seguridad | P0 | Control de acceso a vistas según perfil E institución |
| 35 | Auditoría básica con tenant | Seguridad | P0 | Registrar creación/edición/eliminación (incluye institucion_id) |
| **SUPERADMINISTRADOR (NUEVO)** |
| 36 | Panel de superadministrador | Superadmin | P1 | Ver lista de instituciones, crear nueva, desactivar |
| 37 | Dashboard de monitoreo global | Superadmin | P1 | Métricas de uso por tenant (cantidad de pacientes, citas, etc.) |

---

### Fase 2 (4 semanas) - 1er + 2do Nivel + Multi-tenant avanzado

| # | Componente | Módulo | Prioridad | Criterio de aceptación |
|---|------------|--------|-----------|------------------------|
| **PARAMETRIZACIÓN AVANZADA (POR TENANT)** |
| 1 | Configuración de especialidades 2do nivel | Admin | P1 | Activar cardiología, endocrinología, etc. para uso en referencias |
| 2 | Configuración de flujos clínicos | Admin | P1 | Definir pasos obligatorios/opcionales por especialidad (por tenant) |
| 3 | Configuración de variables clínicas | Admin | P1 | **Campos personalizables por especialidad** (ej: "Fracción eyección" para cardiología) |
| 4 | Configuración de servicios auxiliares | Admin | P1 | Exámenes, procedimientos, precios (opcional) |
| 5 | Configuración de horarios flexibles | Admin | P1 | Bloques por rango, overbooking, tiempos entre citas |
| **AGENDAMIENTO FLEXIBLE** |
| 6 | Agendamiento por rango | Citas | P1 | Paciente pide "próxima semana, mañana" → sistema asigna |
| 7 | Asignación automática | Citas | P1 | Algoritmo asigna primer turno disponible en rango |
| **IA - VISIÓN ARTIFICIAL** |
| 8 | Validación IA de documentos | Admisión | P1 | Cámara escanea cédula/pasaporte → extrae datos |
| 9 | Fallback validación manual | Admisión | P1 | Si IA falla, recepcionista ingresa manualmente |
| **REFERENCIA A 2DO NIVEL (DENTRO DEL MISMO TENANT)** |
| 10 | Referencia a especialista | Consulta | P1 | Médico 1er nivel selecciona especialidad → genera referencia (dentro de su institución) |
| 11 | Bandeja de referencias | Especialista | P1 | Especialista ve referencias entrantes pendientes (solo de su institución) |
| 12 | Aceptar/rechazar referencia | Especialista | P1 | Con comentario y prioridad |
| 13 | Asignación de cita con especialista | Citas | P1 | Desde referencia, agendar directamente |
| 14 | Contrarreferencia | Especialista | P1 | Especialista envía paciente de vuelta a 1er nivel con plan |
| **QR Y SERVICIOS** |
| 15 | Generación de QR en órdenes | Servicios | P1 | Exámenes, procedimientos con QR único (incluye tenant implícito) |
| 16 | Generación de QR en recetas | Farmacia | P1 | Medicamentos con QR validable |
| 17 | QR check-in paciente | Admisión | P1 | Escanear QR al llegar → marca "presente" |
| **DASHBOARDS (POR TENANT)** |
| 18 | Dashboard enfermería | Dashboard | P1 | Ver pacientes en preclínica, tiempos de espera (solo su institución) |
| 19 | Dashboard administración | Dashboard | P1 | Ocupación agenda, ausentismo, tiempos promedio (solo su institución) |
| 20 | Dashboard especialista | Dashboard | P1 | Ver referencias recibidas, agenda propia filtrada por especialidad |
| 21 | Dashboard superadministrador | Superadmin | P1 | Métricas comparativas entre tenants |
| **NOTIFICACIONES** |
| 22 | Recordatorio cita por correo | Notificaciones | P1 | Envío 24h antes + 1h antes (desde la institución del paciente) |
| 23 | Recordatorio medicamentos por correo | Notificaciones | P1 | Configurable por paciente, diario |
| **MEJORAS FLUJO GUIADO** |
| 24 | Guardado automático (autosave) | Consulta | P1 | Cada 30 segundos, no perder datos |
| 25 | Atajos de teclado | Consulta | P1 | Ctrl+Enter = siguiente paso |
| 26 | Sugerencia de diagnóstico (IA básica) | Consulta | P1 | Según motivo y especialidad, mostrar diagnósticos probables |
| 27 | **Variables clínicas por especialidad** | Consulta | P1 | Mostrar campos específicos según especialidad del médico |

---

### Fase 3 (6 semanas) - IA y Diferenciadores (con tenant context)

| # | Componente | Módulo | Prioridad | Criterio de aceptación |
|---|------------|--------|-----------|------------------------|
| **IA PREDICTIVA (POR TENANT)** |
| 1 | Modelo ausentismo | IA | P2 | Predice probabilidad de inasistencia por cita (entrenado por tenant o global) |
| 2 | Modelo demanda de citas | IA | P2 | Predice demanda por especialidad/día/horario |
| 3 | Detección riesgo diabetes | IA | P2 | Usa variables clínicas → riesgo alto/medio/bajo |
| 4 | Detección riesgo HTA | IA | P2 | Alerta en preclínica o consulta |
| 5 | Detección otras enfermedades crónicas | IA | P2 | Configurable por institución |
| **IA GENERATIVA** |
| 6 | API sugerencia diagnóstica | IA | P2 | Médico hace clic → prompt anonimizado → sugerencias |
| 7 | Prompt configurable por institución | Admin | P2 | Parámetro para personalizar el prompt de IA (por tenant) |
| **ARQUITECTURA** |
| 8 | FastAPI separado | Arquitectura | P2 | Migrar endpoints IA a microservicio independiente (con tenant context) |
| **PORTAL PACIENTE (POR TENANT)** |
| 9 | Ver próximas citas | Portal | P2 | Listado con opción de cancelar (solo de su institución) |
| 10 | Ver resultados de exámenes | Portal | P2 | Texto o PDF |
| 11 | Historia clínica portátil | Portal | P2 | Exportar HCE en PDF/JSON (solo de su institución) |
| 12 | Solicitar cita en línea | Portal | P2 | Con agendamiento flexible |
| **DASHBOARD EPIDEMIOLÓGICO (POR TENANT)** |
| 13 | Alertas de brotes | Dashboard | P2 | 5+ casos misma enfermedad en 7 días (por institución) |
| 14 | Tendencia de enfermedades | Dashboard | P2 | Gráficos mensuales por diagnóstico |
| **OPERACIONES MULTI-TENANT** |
| 15 | Backups automáticos diarios | Operaciones | P2 | Backup a S3/NFS, restauración 1-click (por tenant o global) |
| 16 | Modo oscuro | UI | P2 | Toggle, persistente por usuario |
| 17 | **Exportación/importación de tenant** | Superadmin | P2 | Migrar datos de una institución completa (backup/restore por tenant) |

---

### 🔮 Fase 4+ (Futuro - Tercer Nivel)

*Planificado para versiones posteriores, no incluido en alcance actual.*

| # | Componente | Módulo | Estimación |
|---|------------|--------|-------------|
| 1 | Gestión de camas (inventario, asignación, disponibilidad) | Hospitalización | 6-8 semanas |
| 2 | Registro de hospitalización (ingreso, egreso) | Hospitalización | 4 semanas |
| 3 | Evoluciones diarias en hospitalización | Hospitalización | 4 semanas |
| 4 | Block quirúrgico (programación de cirugías, pabellones, equipos) | Cirugía | 8-10 semanas |
| 5 | Gestión de UCI con monitoreo de signos vitales | UCI | 6-8 semanas |
| 6 | Integración con laboratorio clínico | Integración | 8-10 semanas |
| 7 | Integración con sistema de imágenes | Integración | 8-10 semanas |
| 8 | Facturación por día cama y procedimientos (privado) | Facturación | 6 semanas |
| 9 | Lista de espera quirúrgica | Cirugía | 4 semanas |
| 10 | Interconsultas hospitalarias | Hospitalización | 3 semanas |
| 11 | **Clasificaciones OMS especializadas** (CIE-O para oncología, CIF para rehabilitación) | Especialidades | 6-8 semanas |

---

## 5. FLUJOS GUIADOS COMPLETOS POR USUARIO (ACTUALIZADOS CON MULTI-TENANT)

### Flujo A: Médico de 1er Nivel (Medicina General) - 7 pasos

```
MÉDICO ingresa a clinicaandes.xmedical.com (subdominio)
       ↓
Sistema identifica institución = "Clínica Los Andes" (tenant_id = 1)
       ↓
Login valida credenciales Y pertenencia a tenant_id = 1
       ↓
┌──────────────────────────────────────────────────────────────────┐
│ DASHBOARD MÉDICO                                                  │
│ • Ver agenda del día (pacientes con hora)                        │
│ • Ver pacientes en preclínica (listos para consulta)             │
│ • Filtrado automático por su especialidad Y por tenant_id=1      │
│ • Botón destacado: "COMENZAR PRÓXIMO PACIENTE"                   │
└──────────────────────────────────────────────────────────────────┘
       ↓
... (resto del flujo igual, pero todas las consultas SQL tienen WHERE institucion_id = 1)
```

### Flujo B: Superadministrador (Global)

```
SUPERADMINISTRADOR ingresa a admin.xmedical.com
       ↓
Login con rol global (sin tenant asociado)
       ↓
┌──────────────────────────────────────────────────────────────────┐
│ DASHBOARD SUPERADMINISTRADOR                                      │
│ • Lista de todas las instituciones (tenants)                     │
│ • Crear nueva institución                                        │
│ • Editar/Desactivar institución                                  │
│ • Métricas globales:                                             │
│   - Total de pacientes por tenant                                │
│   - Total de citas por tenant                                    │
│   - Uso del sistema                                              │
│ • Acceso "modo soporte" a cualquier tenant (con auditoría)       │
└──────────────────────────────────────────────────────────────────┘
```

---

## 6. FUNCIONALIDADES EXCLUIDAS DEL MVP (Out of Scope)

| # | Funcionalidad | Motivo | Dónde se incluye |
|---|---------------|--------|------------------|
| 1 | Agendamiento flexible (rango) | Mayor complejidad lógica | Fase 2 |
| 2 | Validación IA de documentos | Dependencia API externa | Fase 2 |
| 3 | Códigos QR | No crítico para flujo básico | Fase 2 |
| 4 | Recordatorios por correo | Depende infraestructura | Fase 2 |
| 5 | Referencia a 2do nivel | Requiere módulo adicional | Fase 2 |
| 6 | Contrarreferencia | Depende de referencia | Fase 2 |
| 7 | Dashboards especialista/enfermera/admin | Prioridad menor | Fase 2 |
| 8 | Parametrización avanzada (flujos, variables) | Complejidad | Fase 2 |
| 9 | **Variables clínicas por especialidad** | Requiere diseño avanzado | Fase 2 |
| 10 | Modelos predictivos / IA | Requiere datos históricos | Fase 3 |
| 11 | API sugerencia diagnóstica | Depende LLM externo | Fase 3 |
| 12 | FastAPI separado | Complejidad arquitectónica | Fase 3 |
| 13 | Portal del paciente | Requiere autenticación externa | Fase 3 |
| 14 | Dashboard epidemiológico | Depende datos agregados | Fase 3 |
| 15 | Teleconsulta | Alcance mayor | Futuro |
| 16 | Integración HL7/FHIR | Sistemas externos complejos | Futuro |
| 17 | Aplicación móvil | Recurso adicional | Futuro |
| 18 | Facturación / pagos | Fuera del alcance clínico | Futuro |
| 19 | **Clasificaciones OMS especializadas** (CIE-O, CIF) | Complejidad, pocas especialidades | Futuro |
| 20 | **Tercer nivel (hospitalización)** | Visión a futuro | Fase 4+ (Futuro) |
| 21 | **Migración de datos entre tenants** | Complejidad, bajo demanda | Futuro |

---

## 7. CRITERIOS DE ACEPTACIÓN DEL MVP (ACTUALIZADOS)

| # | Criterio | Métrica | Umbral |
|---|----------|---------|--------|
| 1 | Registro de paciente por institución | Tiempo promedio | < 2 minutos |
| 2 | Agendamiento de cita (aislado por tenant) | Tasa de éxito | 100% (sin conflictos) |
| 3 | Flujo guiado Cita → Preclínica → Consulta | Integridad de datos | 100% |
| 4 | Diagnósticos CIE-10 | Estandarización | 100% consultas con código válido |
| 5 | Perfiles y permisos por institución | Seguridad | Ningún acceso fuera de rol |
| 6 | **Registro de médico con especialidad** | Completitud | 100% de médicos tienen especialidad asignada |
| 7 | **Dashboard filtrado por especialidad E institución** | Precisión | Médico solo ve pacientes de su especialidad Y su tenant |
| 8 | Auditoría con tenant | Trazabilidad | 100% cambios registrados con institucion_id |
| 9 | Dashboard médico | Carga útil | Agenda + pacientes en espera < 2 seg |
| 10 | Historia clínica (aislada por tenant) | Visualización | Encuentros previos ordenados por fecha (solo del tenant) |
| 11 | Parametrización por tenant | Configuración | Crear especialidad, médico, horario sin código |
| 12 | **Aislamiento multi-tenant** | Seguridad | 0 fugas de datos entre tenants |
| 13 | **Creación de nuevo tenant** | Superadmin | < 5 minutos |
| 14 | Flujo guiado UX | Satisfacción médico | > 4/5 en encuesta piloto |
| 15 | Pruebas unitarias con tenant | Cobertura backend | > 75% |
| 16 | Pruebas de integración multi-tenant | End-to-end | Flujo principal sin errores |

---

## 8. SUPUESTOS DEL MVP (ACTUALIZADOS)

| # | Supuesto | Riesgo | Plan de contingencia |
|---|----------|--------|---------------------|
| 1 | Cada institución tiene su propio subdominio | Configuración DNS | Fallback con campo en login |
| 2 | La institución tiene personal para capacitación | Baja adopción | Manual + videos + flujo guiado |
| 3 | El servidor cumple requisitos mínimos (4GB RAM, 2 vCPU) | Rendimiento bajo | Optimización + escalado |
| 4 | PostgreSQL disponible (con RLS) | Fallo despliegue | SQLite para pruebas, migrar después |
| 5 | Dataset CIE-10 disponible | Diagnósticos no estandarizados | Script de carga (~300 códigos) |
| 6 | El flujo guiado de 7 pasos es aceptable | Rechazo | Permitir saltos rápidos |
| 7 | **Las especialidades están predefinidas** | Configuración inicial | Catálogo base de especialidades |
| 8 | **El superadministrador existe inicialmente** | Gestión de tenants | Usuario semilla creado en despliegue |

---

## 9. RESTRICCIONES DEL MVP (ACTUALIZADAS)

| # | Restricción | Impacto | Mitigación |
|---|-------------|---------|-------------|
| 1 | Sin IA en MVP | Médicos sin apoyo diagnóstico | Documentar como Feature Plan Fase 3 |
| 2 | Sin recordatorios | Mayor ausentismo | Manual: recepción llama 24h antes |
| 3 | Sin agendamiento flexible | Pacientes con horarios complejos | Ofrecer múltiples opciones fijas |
| 4 | Sin referencias a 2do nivel | Flujo incompleto | Registrar "necesita referencia" en plan |
| 5 | Sin parametrización avanzada | Cambios requieren programador | Priorizar configuración básica funcional |
| 6 | Sin QR | Procesos con papel | Aceptable para MVP, prometer Fase 2 |
| 7 | **Sin variables clínicas por especialidad** | Examen físico genérico | Aceptable para MVP, implementar en Fase 2 |
| 8 | **Sin tercer nivel** | No aplica para hospitalización | Visión a futuro |
| 9 | **Sin migración de datos entre tenants** | No combinar clínicas | Bajo demanda, solución manual |

---

## 10. RIESGOS DEL MVP (ACTUALIZADOS)

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|-------------|
| Médicos rechazan flujo guiado | Media | Alto | UI simple, botones grandes, permitir saltos |
| Tiempos de carga con múltiples tenants | Baja | Medio | Índices DB, caching por tenant |
| Doble reserva de citas | Baja | Crítico | `select_for_update()` en transacción |
| Pérdida de datos clínicos | Baja | Crítico | Backups diarios manuales |
| Parametrización insuficiente | Media | Medio | Reunión previa para mapear |
| **Médicos sin especialidad asignada** | Baja | Medio | Validación al crear usuario |
| **Especialidad incorrecta afecta agendas** | Baja | Medio | Validación en agendamiento |
| **Fuga de datos entre tenants** | Baja | **Crítico** | RLS + pruebas de aislamiento + auditoría |
| **Superadministrador sin acceso global** | Baja | Alto | Usuario semilla con rol global |

---

## 11. ALCANCE DEL PILOTO (validación) - ACTUALIZADO

### Institución piloto recomendada (mínimo 2 tenants para probar multi-tenant)

| Tenant | Característica | Valor |
|--------|----------------|-------|
| **Tenant A** | Clínica privada | "Clínica Los Andes" |
| **Tenant B** | Consultorio público | "CESFAM Norte" |

### Configuración del piloto

| Característica | Tenant A | Tenant B |
|----------------|----------|----------|
| Médicos 1er nivel | 2-3 | 1-2 |
| Enfermeras | 1-2 | 1 |
| Recepcionistas | 1-2 | 1 |
| Pacientes/día | 30-50 | 20-30 |
| Especialidades activas | 2-3 | 2 |
| Duración piloto | 2 semanas | 2 semanas |

### Criterios de éxito del piloto (multi-tenant)

| # | Criterio | Objetivo |
|---|----------|----------|
| 1 | % de citas agendadas por el sistema (cada tenant) | > 80% |
| 2 | % consultas completadas con flujo guiado | > 90% |
| 3 | Tiempo promedio por consulta | < 25 min |
| 4 | Satisfacción médicos (encuesta 1-5) | > 4.0 |
| 5 | Incidentes críticos | 0 |
| 6 | Configuración inicial por tenant | < 1 día |
| 7 | **Todos los médicos tienen especialidad asignada** | 100% |
| 8 | **Aislamiento de datos entre tenants** | 0 fugas detectadas |
| 9 | **Superadministrador puede ver ambos tenants** | ✅ |

---

## 12. ENTREGABLES POR FASE (ACTUALIZADOS)

### Fase 1 (MVP) - Entregables tangibles

| # | Entregable | Formato |
|---|------------|---------|
| 1 | Código fuente Django con multi-tenant | Repositorio Git |
| 2 | Scripts de base de datos (DDL con RLS + institucion_id en todas las tablas) | SQL |
| 3 | Datos semilla (instituciones base, especialidades, perfiles, superadmin) | SQL |
| 4 | Manual de usuario (por rol: superadmin, admin, médico, etc.) | PDF/Markdown |
| 5 | Manual de administración multi-tenant (cómo crear nueva institución) | PDF/Markdown |
| 6 | Manual de instalación y configuración (con subdominios) | PDF/Markdown |
| 7 | Suite de pruebas unitarias (incluyendo pruebas de aislamiento) | Código Python |
| 8 | Documentación de API (con header X-Institution-ID) | Swagger/OpenAPI |
| 9 | Scripts de backup/restore (global y por tenant) | Bash |
| 10 | Prototipo interactivo del flujo guiado | Archivo demo |

### Fase 2 - Entregables adicionales

| # | Entregable |
|---|------------|
| 1 | Parametrización avanzada (flujos, variables clínicas por especialidad y tenant) |
| 2 | Integración con API de visión artificial |
| 3 | Módulo de referencia/contrarreferencia (1er ↔ 2do nivel, dentro del tenant) |
| 4 | Agendamiento flexible (rango) |
| 5 | Módulo de QR (generación + lectura) |
| 6 | Servicio de recordatorios por correo (Celery) |
| 7 | Dashboards enfermería, administración y especialista |
| 8 | Dashboard superadministrador avanzado |

### Fase 3 - Entregables adicionales

| # | Entregable |
|---|------------|
| 1 | Modelos predictivos (ausentismo, demanda) |
| 2 | Modelos de riesgo para enfermedades crónicas |
| 3 | API de sugerencia diagnóstica (prompt configurable por tenant) |
| 4 | FastAPI separado (con tenant context) |
| 5 | Portal del paciente (por tenant) |
| 6 | Dashboard epidemiológico (por tenant) |
| 7 | Backups automáticos |
| 8 | Exportación/importación de tenant |

---

## 13. MÉTRICAS DE ÉXITO POR FASE (ACTUALIZADAS)

| Fase | Métrica principal | Objetivo |
|------|-------------------|----------|
| Fase 1 (MVP) | Tiempo de atención total | < 60 minutos |
| Fase 1 (MVP) | Satisfacción médico | > 4/5 |
| Fase 1 (MVP) | **% de médicos con especialidad asignada** | 100% |
| Fase 1 (MVP) | **Aislamiento multi-tenant** | 0 fugas de datos |
| Fase 1 (MVP) | **Tiempo de creación nuevo tenant** | < 5 minutos |
| Fase 2 | Reducción de ausentismo | 25% |
| Fase 2 | Tiempo de referencia → especialista | < 7 días |
| Fase 3 | Precisión de modelos IA | > 80% |
| Fase 3 | Uso de sugerencia diagnóstica | > 50% consultas |

---

## 14. ESTRUCTURA DE PARAMETRIZACIÓN (MVP) - ACTUALIZADA

### Tablas base configurables desde admin (con multi-tenant)

| Tabla | Campos configurables | ¿En MVP? |
|-------|---------------------|----------|
| `Institucion` (tenant) | nombre, subdominio, tipo, configuracion, activo | ✅ Sí |
| `Especialidad` | nombre, codigo, nivel, duracion_consulta, **institucion_id** | ✅ Sí |
| `Profesional` | nombre, **especialidad_id**, usuario, horarios, **institucion_id** | ✅ Sí |
| `Horario` | dia_semana, hora_inicio, hora_fin, profesional, **institucion_id** | ✅ Sí |
| `Perfil` | nombre, permisos, **institucion_id** (NULL para roles globales) | ✅ Sí |
| `Paciente` | nombre, documento, contacto, **institucion_id** | ✅ Sí |
| `Cita` | paciente, profesional, fecha, hora, estado, **institucion_id** | ✅ Sí |
| `Consulta` | cita, diagnostico, plan, **institucion_id** | ✅ Sí |
| `VariableClinica` | nombre, tipo, especialidad, **institucion_id** | ❌ Fase 2 |
| `FlujoPaso` | paso_nombre, orden, obligatorio, especialidad, **institucion_id** | ❌ Fase 2 |

### Datos semilla

#### Instituciones base

| Nombre | Subdominio | Tipo |
|--------|------------|------|
| Clínica Los Andes | clinicaandes | privada |
| CESFAM Norte | cesfamnorte | publica |

#### Especialidades base (por institución, copiadas a cada tenant)

| Especialidad | Nivel | Duración (min) |
|--------------|-------|----------------|
| Medicina General | 1er nivel | 20 |
| Pediatría | 1er nivel | 20 |
| Cardiología | 2do nivel | 30 |
| Endocrinología | 2do nivel | 30 |
| Neurología | 2do nivel | 30 |
| Rehabilitación | 2do nivel | 40 |
| Oncología | 2do nivel | 40 |

---

## 15. HOJA DE RUTA DE EVOLUCIÓN COMPLETA (ACTUALIZADA)

| Fase | Duración | Entregable principal | Niveles | Multi-tenant |
|------|----------|----------------------|---------|--------------|
| **Fase 1 (MVP)** | 4 semanas | Citas + flujo guiado + especialidades + **multi-tenant básico** | 1er nivel | ✅ Aislamiento, subdominio, superadmin |
| **Fase 2** | 4 semanas | Agendamiento flexible + IA visión + QR + referencias + variables clínicas | 1er + 2do nivel | ✅ Dashboard superadmin |
| **Fase 3** | 6 semanas | Modelos predictivos + detección riesgos + portal paciente | 1er + 2do nivel | ✅ Export/import tenant |
| **Fase 4** | 4 semanas | FastAPI separado + dashboard epidemiológico | 1er + 2do nivel | ✅ Métricas por tenant |
| 🔮 **Fase 5** | 8-10 semanas | **Tercer nivel básico**: Camas, ingreso/egreso hospitalario | +3er nivel | ✅ Camas por tenant |
| 🔮 **Fase 6** | 10-12 semanas | **Tercer nivel avanzado**: Block quirúrgico, UCI, evolución | +3er nivel | ✅ Quirófanos por tenant |
| 🔮 **Fase 7** | 6-8 semanas | **Clasificaciones OMS especializadas**: CIE-O, CIF | +Oncología, Rehabilitación | ✅ Por especialidad/tenant |
| 🔮 **Fase 8+** | Continuo | Teleconsulta, app móvil, HL7/FHIR | Todos | ✅ Multi-tenant nativo |

---

## 16. APROBACIÓN

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| Product Owner | [Usuario] | ✅ Aprobado | 2026 |
| Agente Documentación | DeepSeek | Generado | 2026 |

---

**Fin del Documento 2: Alcance del MVP por Fases (Actualizado con Multi-tenant)**

---

## RESUMEN DE CAMBIOS REALIZADOS

| # | Cambio | Ubicación |
|---|--------|-----------|
| 1 | **Nueva Sección 2**: Arquitectura Multi-tenant (modelo RLS, identificación, roles) | Sección 2 |
| 2 | **Definición MVP**: incluye multi-tenant explícitamente | Sección 1 |
| 3 | **Nuevos componentes en Fase 1**: 4 componentes multi-tenant (instituciones, subdominio, RLS, superadmin) | Sección 4 (#1-4, #36-37) |
| 4 | **Todos los componentes existentes**: añaden "por institución" o "filtrado por tenant" | Sección 4 |
| 5 | **Nuevo rol**: Superadministrador global | Sección 2.3, Sección 4 |
| 6 | **Nuevo flujo**: Superadministrador (global) | Sección 5 |
| 7 | **Nueva exclusión**: Migración de datos entre tenants | Sección 6 (#21) |
| 8 | **Nuevos criterios de aceptación**: Aislamiento multi-tenant, creación de tenant | Sección 7 (#12, #13) |
| 9 | **Nuevos supuestos**: Superadministrador inicial, subdominios | Sección 8 (#8) |
| 10 | **Nueva restricción**: Sin migración de datos entre tenants | Sección 9 (#9) |
| 11 | **Nuevos riesgos**: Fuga de datos, superadministrador sin acceso | Sección 10 |
| 12 | **Piloto actualizado**: Mínimo 2 tenants para probar aislamiento | Sección 11 |
| 13 | **Entregables actualizados**: Incluyen RLS, superadmin, pruebas de aislamiento | Sección 12 |
| 14 | **Nuevas métricas**: Aislamiento multi-tenant, tiempo creación tenant | Sección 13 |
| 15 | **Tablas actualizadas**: institucion_id en todas las tablas | Sección 14 |
| 16 | **Datos semilla**: Instituciones base (2 tenants de ejemplo) | Sección 14 |
| 17 | **Hoja de ruta**: Columna "Multi-tenant" añadida | Sección 15 |

---