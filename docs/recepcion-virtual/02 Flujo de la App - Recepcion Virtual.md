# 2. FLUJO DE LA APLICACIÓN
## Módulo: Recepción Virtual Omnicanal (XMedical)

| Versión | Fecha | Autor | Estado |
|---------|-------|-------|--------|
| 0.1 | 2026-07 | Equipo XMedical | **Borrador** |

> Responde a **¿qué hace el usuario paso a paso?**. Muestra el recorrido de usuarios, canales y decisiones. Se apoya en el [PRD](01%20PRD%20-%20Recepcion%20Virtual.md).

---

## 1. Flujo de alto nivel (mensaje entrante)

```mermaid
flowchart TD
    A[Mensaje entrante: Email / WhatsApp / Voz] --> B[Adaptador de canal normaliza el mensaje]
    B --> C{¿Firma/webhook válido?}
    C -->|No| Z[Descartar y registrar intento]
    C -->|Sí| D[Resolver TENANT por canal de destino]
    D --> E{¿Tenant identificado?}
    E -->|No| Z
    E -->|Sí| F[Resolver PACIENTE por remitente]
    F --> G{¿Paciente identificado?}
    G -->|No| H[Pedir documento/identificación]
    H --> F
    G -->|Sí| I[Clasificar intención con IA/NLU]
    I --> J{Confianza suficiente?}
    J -->|No| K[Escalar a recepcionista humano]
    J -->|Sí| L[Ejecutar acción de dominio]
    L --> M[Generar respuesta]
    M --> N[Enviar por el mismo canal]
    N --> O[Registrar conversación y auditoría]
    K --> O
```

---

## 2. Flujo de "registro" (opt-in del canal)

En este módulo el "registro" es el **consentimiento del paciente** para ser contactado por un canal.

```mermaid
flowchart TD
    A[Recepción crea/edita paciente] --> B{¿Tiene email/teléfono?}
    B -->|No| C[Solicitar contacto]
    B -->|Sí| D{¿Consentimiento registrado?}
    D -->|No| E[Enviar solicitud de opt-in]
    E --> F{¿Paciente acepta?}
    F -->|No| G[Marcar canal como no autorizado]
    F -->|Sí| H[Registrar opt-in + canal]
    D -->|Sí| H
    H --> I[Paciente habilitado para mensajes proactivos]
```

---

## 3. Flujo de identificación ("inicio de sesión" del paciente)

Los canales externos no usan sesión web; la identidad se resuelve por el remitente.

```mermaid
flowchart TD
    A[Remitente: email o teléfono] --> B[Buscar Paciente en el tenant]
    B --> C{¿Coincidencia única?}
    C -->|Sí| D[Identidad confirmada]
    C -->|Ninguna| E[Pedir documento]
    C -->|Varias| F[Pedir dato desambiguador: documento/fecha nac.]
    E --> G{¿Documento válido en el tenant?}
    F --> G
    G -->|Sí| D
    G -->|No| H[Ofrecer escalado a humano]
```

---

## 4. Flujo principal por tipo de usuario

### 4.1 Paciente — recordatorio y confirmación (CU-01)

```mermaid
flowchart TD
    A[Tarea Celery: citas de mañana] --> B[Enviar recordatorio con plantilla]
    B --> C{¿Respuesta del paciente?}
    C -->|Confirmo| D[Marcar cita = confirmada]
    C -->|Cancelo| E[Marcar cita = cancelada y liberar horario]
    C -->|Otra cosa| F[Clasificar intención]
    C -->|Sin respuesta| G[Registrar sin confirmar]
    D --> H[Responder acuse + auditar]
    E --> H
    F --> H
```

### 4.2 Paciente — agendamiento (CU-05, Fase 2)

```mermaid
flowchart TD
    A[Paciente pide cita] --> B[Seleccionar especialidad]
    B --> C[Sugerir médico]
    C --> D[Ofrecer fecha y hora disponibles]
    D --> E{¿Horario disponible y aceptado?}
    E -->|No| D
    E -->|Sí| F[Crear cita en estado pendiente]
    F --> G[Enviar confirmación]
    G --> H[Auditar]
```

### 4.3 Recepcionista humano — handoff

```mermaid
flowchart TD
    A[Conversación escalada] --> B[Aparece en panel de conversaciones]
    B --> C[Recepcionista abre conversación con historial]
    C --> D[Responde manualmente]
    D --> E{¿Resuelto?}
    E -->|No| D
    E -->|Sí| F[Cerrar conversación]
    F --> G[Auditar cierre]
```

---

## 5. Flujo de creación / edición / eliminación de datos

Las acciones sobre citas reutilizan la lógica de dominio existente (o la API REST planificada):

| Acción | Disparador conversacional | Resultado |
|--------|---------------------------|-----------|
| Confirmar cita | "confirmo", "sí asistiré" | `Cita.estado = confirmada` |
| Cancelar cita | "cancelar", "no puedo ir" | `Cita.estado = cancelada` + liberar cupo |
| Reprogramar (Fase 2) | "cambiar mi cita" | Cancelar + crear nueva |
| Crear cita (Fase 2) | "quiero una cita" | `Cita` nueva `pendiente` |

---

## 6. Validaciones

- Verificar **firma/HMAC** del webhook antes de procesar (email/WhatsApp/voz).
- Confirmar que el **paciente es titular** de la cita antes de modificarla (RN-06).
- Validar que la acción esté permitida en el **horario de atención** configurado (mensajes proactivos).
- Validar formato de contacto (email/teléfono) al registrar opt-in.
- Verificar disponibilidad real del horario antes de agendar (Fase 2).

---

## 7. Decisiones del sistema

- **Resolución de tenant:** por número/línea o alias de correo de destino.
- **Confianza de intención:** umbral configurable; por debajo → escalar.
- **Ventana de conversación (WhatsApp):** dentro de 24 h respuesta libre; fuera, solo plantillas aprobadas.
- **Elección de canal de respuesta:** siempre el mismo por el que llegó el mensaje.

---

## 8. Excepciones y errores

```mermaid
flowchart TD
    A[Procesar mensaje] --> B{¿Error del proveedor?}
    B -->|Timeout/caída| C[Reintentar con backoff en Celery]
    C --> D{¿Persiste?}
    D -->|Sí| E[Degradar de canal / avisar a recepción]
    D -->|No| F[Continuar]
    B -->|No| F
    F --> G{¿Error de negocio? p.ej. cita inexistente}
    G -->|Sí| H[Responder mensaje claro + ofrecer humano]
    G -->|No| I[Éxito]
```

Casos a cubrir: paciente no identificado, cita no encontrada, canal no autorizado, proveedor caído, mensaje no entendido, duplicados (idempotencia por `externo_id`).

---

## 9. Notificaciones

| Evento | Notificación | Canal |
|--------|--------------|-------|
| Cita agendada/confirmada | Acuse al paciente | Mismo canal |
| 24 h antes de la cita | Recordatorio proactivo | Email/WhatsApp |
| Conversación escalada | Aviso al recepcionista | Panel web / correo interno |
| Cita cancelada por paciente | Aviso a la clínica | Panel / correo interno |

---

## 10. Referencias

- [PRD — Recepción Virtual](01%20PRD%20-%20Recepcion%20Virtual.md)
- [Documento 5: Diagramas de Flujo (clínicos)](../5%20Documento%20Diagramas%20de%20Flujo.md)

---

**Fin del Flujo — Recepción Virtual**
