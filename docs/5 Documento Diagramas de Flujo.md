# DOCUMENTO 5: DIAGRAMAS DE FLUJO
## XMedical - Sistema de Gestión Clínica Multi-tenant para Primer y Segundo Nivel

| Versión | Fecha | Autor | Estado |
|---------|-------|-------|--------|
| 1.0 | 2026 | Agente de Documentación Técnica | **Aprobado** |

---

## 1. VISIÓN GENERAL

Este documento contiene los **diagramas de flujo** para los principales procesos de XMedical, organizados en:

- **User Flows**: Flujo que sigue el usuario en la interfaz (paso a paso)
- **System Flows**: Flujo interno del sistema (lógica, decisiones, integraciones)

**Formato:** Mermaid (compatible con GitHub, Markdown, y documentación técnica)

---

## 2. USER FLOWS (FLUJOS DE USUARIO)

### 2.1 Flujo de Autenticación Multi-tenant

```mermaid
flowchart TD
    A[Usuario ingresa URL] --> B{¿URL tiene subdominio?}
    B -->|Sí| C[Extraer subdominio]
    B -->|No| D[Mostrar selector de institución]
    
    C --> E[Buscar institución por subdominio]
    D --> F[Usuario selecciona institución]
    F --> E
    
    E --> G{¿Institución existe?}
    G -->|No| H[Mostrar error: Institución no válida]
    H --> A
    
    G -->|Sí| I[Mostrar pantalla de login]
    I --> J[Usuario ingresa credenciales]
    J --> K{¿Credenciales válidas?}
    K -->|No| L[Mostrar error: Credenciales incorrectas]
    L --> I
    
    K -->|Sí| M{¿Usuario pertenece a la institución?}
    M -->|No| N[Mostrar error: No tiene acceso a esta institución]
    N --> I
    
    M -->|Sí| O[Crear sesión con tenant_id]
    O --> P[Redirigir al dashboard según rol]
    P --> Q[Fin - Usuario autenticado]
```

---

### 2.2 Flujo de Registro de Paciente (Recepcionista)

```mermaid
flowchart TD
    A[Recepcionista accede a módulo] --> B[Selecciona 'Registrar paciente']
    B --> C[Completa formulario: nombre, documento, contacto]
    C --> D[Verificar si documento ya existe]
    D --> E{¿Documento duplicado?}
    
    E -->|Sí| F[Mostrar paciente existente]
    F --> G{¿Desea agendar cita?}
    G -->|Sí| H[Ir a agendamiento]
    G -->|No| I[Fin]
    
    E -->|No| J[Guardar paciente en BD con tenant_id]
    J --> K{¿Desea agendar cita?}
    K -->|Sí| L[Ir a flujo de agendamiento]
    K -->|No| M[Mostrar confirmación]
    M --> N[Fin]
```

---

### 2.3 Flujo de Agendamiento de Cita (Específico)

```mermaid
flowchart TD
    A[Usuario inicia agendamiento] --> B[Selecciona especialidad]
    B --> C[Sistema filtra médicos por especialidad y tenant]
    C --> D[Usuario selecciona médico]
    D --> E[Usuario selecciona fecha]
    E --> F[Sistema muestra horarios disponibles del médico]
    F --> G[Usuario selecciona hora]
    G --> H[Sistema bloquea turno temporalmente]
    H --> I[Usuario confirma cita]
    I --> J[Sistema guarda cita con tenant_id]
    J --> K[Sistema libera bloqueo temporal]
    K --> L{¿Paciente tiene email?}
    L -->|Sí| M[Programar envío de confirmación]
    L -->|No| N[Fin]
    M --> N
```

---

### 2.4 Flujo de Consulta Médica (7 pasos guiados)

```mermaid
flowchart TD
    A[Médico selecciona paciente] --> B[Inicia flujo de consulta - Paso 1/7]
    
    B --> C[Paso 1: Revisar preclínica]
    C --> D{¿Datos de preclínica completos?}
    D -->|No| E[Enfermera debe completar]
    D -->|Sí| F[Paso 2: Motivo de consulta]
    
    F --> G[Paso 3: Anamnesis]
    G --> H[Paso 4: Examen físico]
    H --> I{¿Especialidad tiene campos específicos?}
    I -->|Sí| J[Mostrar campos personalizados]
    I -->|No| K[Mostrar campos genéricos]
    
    J --> L[Paso 5: Diagnóstico CIE-10]
    K --> L
    L --> M{¿Médico solicita sugerencia IA?}
    M -->|Sí| N[Llamar a API de IA con datos anonimizados]
    M -->|No| O[Ingreso manual]
    N --> P[Mostrar sugerencias de diagnóstico]
    P --> O
    
    O --> Q[Paso 6: Plan terapéutico]
    Q --> R[Seleccionar conducta]
    R --> S{Cual conducta?}
    
    S -->|Alta| T[Marcar consulta como completada]
    S -->|Cita subsiguiente| U[Calcular fecha según días indicados]
    S -->|Referencia| V[Mostrar especialidades de 2do nivel]
    
    U --> W[Paso 7: Resumen]
    V --> W
    T --> W
    
    W --> X[Médico confirma datos]
    X --> Y[Guardar consulta en BD]
    Y --> Z{¿Se generó cita subsiguiente o referencia?}
    Z -->|Sí| AA[Crear tareas pendientes]
    Z -->|No| AB[Finalizar]
    AA --> AB
```

---

### 2.5 Flujo de Referencia a Especialista (1er → 2do nivel)

```mermaid
flowchart TD
    A[Médico general genera referencia] --> B[Selecciona especialidad destino]
    B --> C[Agrega comentarios y diagnóstico]
    C --> D[Guarda referencia en BD con tenant_id]
    D --> E[Notifica al especialista]
    E --> F[Referencia aparece en bandeja del especialista]
    
    F --> G[Especialista revisa referencia]
    G --> H{¿Acepta la referencia?}
    
    H -->|Rechazar| I[Notifica al médico general con motivo]
    I --> J[Referencia queda como 'Rechazada']
    
    H -->|Aceptar| K[Especialista agenda cita]
    K --> L[Sistema asigna fecha y hora]
    L --> M[Notifica al paciente]
    M --> N[Paciente asiste a consulta especializada]
    
    N --> O[Especialista completa consulta]
    O --> P[Genera contrarreferencia]
    P --> Q[Envía resumen al médico general]
    Q --> R[Fin del ciclo de referencia]
```

---

### 2.6 Flujo del Paciente (Autoagendamiento Web)

```mermaid
flowchart TD
    A[Paciente accede al portal] --> B{¿Tiene cuenta?}
    B -->|No| C[Registro de paciente]
    C --> D[Completa datos personales]
    D --> E[Verifica email]
    E --> F[Cuenta activada]
    
    B -->|Sí| G[Inicia sesión]
    G --> H[Ver dashboard paciente]
    
    F --> H
    H --> I[Selecciona 'Agendar cita']
    I --> J{¿Tipo de agendamiento?}
    
    J -->|Específico| K[Seleccionar especialidad → médico → fecha → hora]
    J -->|Flexible| L[Seleccionar rango de fechas]
    
    K --> M[Confirmar cita]
    L --> N[Sistema asigna primer turno disponible]
    N --> M
    
    M --> O[Recibir confirmación por email]
    O --> P[Ver cita en 'Mis citas']
    P --> Q[Fin]
```

---

## 3. SYSTEM FLOWS (FLUJOS DE SISTEMA)

### 3.1 Flujo de Identificación Multi-tenant (Middleware)

```mermaid
flowchart TD
    A[Request entrante] --> B[Middleware captura request]
    B --> C[Extraer subdominio del host]
    C --> D{¿Subdominio existe?}
    
    D -->|No| E[Buscar header X-Institution-ID]
    E --> F{¿Header presente?}
    F -->|No| G[Intentar session.tenant_id]
    G --> H{¿Session tiene tenant?}
    H -->|No| I[Redirigir a selector de institución]
    
    D -->|Sí| J[Buscar tenant por subdominio en cache/DB]
    J --> K{¿Tenant encontrado?}
    K -->|No| L[Mostrar error 404]
    
    K -->|Sí| M[Almacenar tenant_id en request y session]
    M --> N[Inyectar tenant en conexión DB]
    N --> O[SET app.current_institucion_id = tenant_id]
    O --> P[Continuar a siguiente middleware]
    
    F -->|Sí| M
    H -->|Sí| M
    I --> P
```

---

### 3.2 Flujo de Aislamiento de Datos (RLS PostgreSQL)

```mermaid
flowchart TD
    A[Aplicación ejecuta consulta SQL] --> B[Consulta: SELECT * FROM paciente]
    B --> C[PostgreSQL recibe consulta]
    C --> D[Verifica si tabla tiene RLS habilitado]
    D --> E{¿RLS activo?}
    
    E -->|No| F[Ejecutar consulta sin filtro]
    
    E -->|Sí| G[Verificar política para la tabla]
    G --> H[Política: WHERE institucion_id = current_setting(...)]
    H --> I[Obtener current_setting('app.current_institucion_id')]
    I --> J{¿Valor existe?}
    
    J -->|No| K[Rechazar consulta - sin contexto tenant]
    J -->|Sí| L[Filtrar resultados por tenant_id]
    
    L --> M[Ejecutar consulta con filtro]
    M --> N[Retornar solo resultados del tenant actual]
    
    F --> O[Retornar todos los resultados]
    K --> P[Retornar error]
```

---

### 3.3 Flujo de Agendamiento (Lógica de Disponibilidad)

```mermaid
flowchart TD
    A[Solicitud de agendamiento] --> B[Obtener médico y fecha]
    B --> C[Obtener horario configurado del médico]
    C --> D[Obtener citas ya agendadas para ese día]
    D --> E[Calcular bloques de tiempo disponibles]
    
    E --> F[Para cada bloque horario]
    F --> G{¿Bloque está dentro del horario laboral?}
    G -->|No| H[Excluir bloque]
    
    G -->|Sí| I{¿Bloque ya está ocupado por otra cita?}
    I -->|Sí| J[Excluir bloque - ya reservado]
    
    I -->|No| K[Agregar a lista de disponibles]
    
    K --> L[Siguiente bloque]
    L --> F
    
    H --> L
    J --> L
    
    F --> M[Retornar lista de horarios disponibles]
    M --> N[Usuario selecciona horario]
    N --> O[Sistema bloquea turno con optimistic lock]
    O --> P{¿Bloqueo exitoso?}
    
    P -->|Sí| Q[Confirmar cita]
    P -->|No| R[Mostrar: Horario ya no disponible]
    R --> N
```

---

### 3.4 Flujo de Recordatorios (Tarea Programada Celery)

```mermaid
flowchart TD
    A[Celery Beat ejecuta tarea cada hora] --> B[Obtener lista de instituciones activas]
    B --> C[Iterar por cada institución]
    
    C --> D[Cambiar tenant context]
    D --> E[SET app.current_institucion_id = tenant_id]
    E --> F[Buscar citas para mañana]
    
    F --> G{¿Hay citas para recordar?}
    G -->|Sí| H[Iterar por cada cita]
    H --> I{Obtener email del paciente}
    I -->|No| J[Registrar en log: sin email]
    I -->|Sí| K[Preparar plantilla de email]
    
    K --> L[Remplazar variables: nombre, fecha, hora, médico]
    L --> M[Enviar email vía SMTP/SendGrid]
    M --> N[Registrar envío en log_notificaciones]
    N --> O[Siguiente cita]
    O --> H
    
    G -->|No| P[Siguiente institución]
    J --> O
    P --> C
    
    C --> Q[Fin de iteración de instituciones]
    Q --> R[Tarea completada]
```

---

### 3.5 Flujo de Backups Automáticos

```mermaid
flowchart TD
    A[Celery Beat ejecuta tarea diaria a las 02:00] --> B[Generar timestamp: YYYY-MM-DD-HHMMSS]
    B --> C[Generar dump completo de PostgreSQL]
    C --> D{¿Backup por tenant?}
    
    D -->|Sí| E[Iterar por instituciones]
    E --> F[Extraer datos de un tenant específico]
    F --> G[Comprimir archivo SQL]
    G --> H[Subir a S3 con prefijo tenant_id]
    H --> I[Siguiente tenant]
    I --> E
    
    D -->|No| J[Comprimir dump completo]
    J --> K[Subir a S3 con prefijo 'full']
    
    K --> L[Rotar backups: eliminar backups con más de 30 días]
    I --> L
    L --> M[Registrar resultado en log_backups]
    M --> N[Notificar a superadministrador si hay error]
    N --> O[Tarea completada]
```

---

### 3.6 Flujo de Generación de QR

```mermaid
flowchart TD
    A[Médico genera orden o receta] --> B[Tipo de documento]
    B --> C{¿Qué tipo?}
    
    C -->|Examen| D[Generar payload: {\"tipo\":\"examen\",\"id\":123,\"tenant\":1}]
    C -->|Receta| E[Generar payload: {\"tipo\":\"receta\",\"id\":456,\"tenant\":1,\"caducidad\":\"2026-07-01\"}]
    C -->|Check-in| F[Generar payload: {\"tipo\":\"checkin\",\"cita_id\":789,\"tenant\":1}]
    
    D --> G[Encriptar payload (AES)]
    E --> G
    F --> G
    
    G --> H[Generar código QR con biblioteca segno]
    H --> I[Guardar imagen QR en storage S3/NFS]
    I --> J[Guardar referencia en BD: tabla documento_qr]
    J --> K[Devolver URL del QR]
    K --> L[Mostrar QR en pantalla]
    L --> M[Opción: enviar QR por email al paciente]
    M --> N[Fin]
```

---

## 4. DIAGRAMAS ADICIONALES

### 4.1 Flujo de Onboarding de Nuevo Tenant (Superadministrador)

```mermaid
flowchart TD
    A[Superadministrador inicia] --> B[Completa formulario de nueva institución]
    B --> C[Ingresa: nombre, subdominio, tipo, contacto]
    C --> D[Verificar disponibilidad de subdominio]
    D --> E{¿Subdominio disponible?}
    
    E -->|No| F[Mostrar error: subdominio ya existe]
    F --> B
    
    E -->|Sí| G[Crear registro en tabla institucion]
    G --> H[Crear estructura base del tenant]
    H --> I[Crear especialidades por defecto]
    I --> J[Crear perfiles por defecto]
    J --> K[Crear usuario administrador del tenant]
    K --> L[Enviar email de bienvenida al administrador]
    L --> M[Notificar al superadministrador: creación exitosa]
    M --> N[Fin]
```

---

### 4.2 Flujo de Recuperación de Contraseña

```mermaid
flowchart TD
    A[Usuario olvida contraseña] --> B[Hace clic en 'Olvidé mi contraseña']
    B --> C[Ingresa email asociado a cuenta]
    C --> D[Sistema verifica email existe y pertenece al tenant]
    D --> E{¿Email válido?}
    
    E -->|No| F[Mostrar mensaje: email no registrado]
    F --> C
    
    E -->|Sí| G[Generar token único con expiración (1 hora)]
    G --> H[Guardar token en BD]
    H --> I[Enviar email con enlace: /reset-password?token=XXX]
    I --> J[Usuario hace clic en enlace]
    J --> K[Validar token expiración]
    K --> L{¿Token válido?}
    
    L -->|No| M[Mostrar error: enlace expirado]
    M --> B
    
    L -->|Sí| N[Mostrar formulario nueva contraseña]
    N --> O[Usuario ingresa nueva contraseña]
    O --> P[Validar seguridad de contraseña]
    P --> Q[Actualizar password en BD]
    Q --> R[Marcar token como usado]
    R --> S[Redirigir a login]
    S --> T[Fin]
```

---

## 5. LEYENDA DE SÍMBOLOS

| Símbolo | Significado |
|---------|-------------|
| `A[Texto]` | Inicio o Fin del proceso |
| `B{Decisión}` | Condicional (Sí/No, Verdadero/Falso) |
| `C[Proceso]` | Acción o operación realizada por el sistema |
| `D[Tarea usuario]` | Acción realizada por el usuario |
| `E(Subproceso)` | Llamada a otro diagrama o subproceso |
| `F[/Almacenamiento/]` | Persistencia de datos (BD, archivo) |
| `G((Conector))` | Conexión entre diagramas |

---

## 6. APROBACIÓN

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| Product Owner | [Usuario] | ✅ Aprobado | 2026 |
| Agente Documentación | DeepSeek | Generado | 2026 |

---

**Fin del Documento 5: Diagramas de Flujo**

---

## RESUMEN DEL DOCUMENTO

| Aspecto | Valor |
|---------|-------|
| **Total de diagramas** | 11 |
| **User Flows** | 6 (autenticación, registro paciente, agendamiento, consulta, referencia, autoagendamiento) |
| **System Flows** | 6 (multi-tenant, RLS, disponibilidad, recordatorios, backups, QR) |
| **Flujos adicionales** | 2 (onboarding tenant, recuperación contraseña) |
| **Formato** | Mermaid (compatible con GitHub/Markdown) |

---