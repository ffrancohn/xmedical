# DOCUMENTO 15: RECEPCIÓN VIRTUAL OMNICANAL
## XMedical - Sistema de Gestión Clínica Multi-tenant

| Versión | Fecha | Autor | Estado |
|---------|-------|-------|--------|
| 0.1 | 2026-07 | Equipo XMedical | **Planificado (borrador de diseño)** |

> Este documento es un **borrador de diseño**. Define el alcance, la arquitectura y las **opciones de proveedores** para un nuevo módulo de comunicación con pacientes. La elección final de proveedores (especialmente WhatsApp y voz) **queda pendiente de definición** y se marca explícitamente donde aplica.

---

## 1. OBJETIVO

Definir un nuevo módulo que actúe como **recepcionista virtual omnicanal**: un asistente que **recibe y envía comunicaciones** con los pacientes por varios canales (correo electrónico, WhatsApp y voz), entiende su intención y ejecuta acciones clínicas y administrativas sobre XMedical (agendar/cancelar citas, responder dudas, enviar recordatorios y confirmaciones), respetando el modelo **multi-tenant** y las políticas de seguridad existentes.

El objetivo NO es reemplazar al personal de recepción, sino **descargar tareas repetitivas** (recordatorios, confirmaciones, preguntas frecuentes, agendamiento simple) y ofrecer atención fuera de horario.

---

## 2. NOMBRE DEL MÓDULO (PROPUESTA)

El nombre "módulo recepcionista" es funcional pero ambiguo (el rol `recepcionista` ya existe como usuario). Se proponen alternativas más precisas:

| Opción | Nombre visible | App Django | Comentario |
|--------|----------------|------------|------------|
| A | **Recepción Virtual** | `apps/recepcion_virtual/` | ✅ Recomendada. Claro, no colisiona con el rol `recepcionista`. |
| B | Asistente Omnicanal | `apps/asistente/` | Enfatiza IA; menos explícito sobre "recepción". |
| C | Comunicaciones | `apps/comunicaciones/` | Genérico; útil si crece a marketing/campañas. |
| D | Conserje Digital | `apps/conserje/` | Marketinero; menos técnico. |

**Recomendación:** usar **Recepción Virtual** (`apps/recepcion_virtual/`) como nombre del módulo, y reservar el término "recepcionista" para el rol humano existente.

---

## 3. ESTADO ACTUAL vs. PLANIFICADO

| Componente | Estado actual | Para Recepción Virtual |
|------------|---------------|------------------------|
| Backend Django + Celery + Redis | ✅ Implementado | Se reutiliza (Celery para tareas asíncronas) |
| `apps.core.ai_services` (LLM: OpenAI/OpenRouter) | ✅ Implementado | Se reutiliza para NLU/generación de respuestas |
| Multi-tenant (subdominio) | ✅ `TenantMiddleware` | Se respeta; canales entrantes deben resolver el tenant sin subdominio (ver §9) |
| Email saliente | ⚠️ Diseñado, no implementado ([Doc 9 §3.1](9%20Documento%20de%20integraciones.md)) | Se implementa (envío + **recepción**) |
| WhatsApp / SMS | 🔮 Futuro ([Doc 9 §4.5](9%20Documento%20de%20integraciones.md)) | Se implementa; **proveedor a definir** |
| Voz (llamadas / IVR) | ❌ No existe | 🔮 Nuevo; **proveedor a definir** |
| API REST (`/api/v1/`) | 🔮 Planificada ([Doc 13](13%20App%20movil%20y%20API%20REST.md)) | Recomendable para exponer acciones al orquestador |

---

## 4. ALCANCE Y CANALES

| Canal | Entrante (recibir) | Saliente (enviar) | Prioridad sugerida |
|-------|--------------------|--------------------|--------------------|
| **Email** | ✅ Recibir correos de pacientes | ✅ Recordatorios, confirmaciones, respuestas | Fase 1 |
| **WhatsApp** | ✅ Mensajes de pacientes | ✅ Notificaciones y conversación | Fase 2 |
| **Voz** | ✅ Llamadas entrantes (STT) | ✅ Respuestas habladas (TTS) / IVR | Fase 3 |
| SMS (opcional) | ➖ | ✅ Recordatorios simples | Complementario a WhatsApp |

**Capacidades transversales (todos los canales):**

- Identificar al paciente (por email/teléfono/documento) dentro del tenant correcto.
- Clasificar la intención (agendar, cancelar, confirmar, consultar, hablar con humano).
- Ejecutar la acción vía servicios de dominio o API REST.
- **Escalar a un humano** (recepcionista) cuando no hay confianza suficiente o el paciente lo pide.
- Registrar toda la conversación para auditoría y trazabilidad.

---

## 5. ARQUITECTURA OBJETIVO

```
        Pacientes
   ┌───────┬────────────┬───────────┐
   │ Email │  WhatsApp  │    Voz    │
   └───┬───┴──────┬─────┴─────┬─────┘
       │          │           │
   IMAP/SMTP   Webhook API  Webhook/telefonía
   (SES/etc.)  (a definir)  (a definir)
       │          │           │
       ▼          ▼           ▼
┌─────────────────────────────────────────────┐
│  apps/recepcion_virtual/  (adaptadores)      │
│  ┌──────────┐ ┌──────────┐ ┌──────────────┐ │
│  │ email/   │ │ whatsapp/│ │ voz/         │ │
│  └────┬─────┘ └────┬─────┘ └──────┬───────┘ │
│       └────────────┼──────────────┘         │
│                    ▼                         │
│        Orquestador de conversación           │
│  (identidad tenant/paciente + NLU + estado)  │
│                    │                         │
│         apps.core.ai_services (LLM)          │
└────────────────────┬────────────────────────┘
                     ▼
        Servicios de dominio / API REST
   (citas, pacientes, preclínica, consulta)
                     │
                     ▼
        PostgreSQL + Redis + Celery
```

**Principios de diseño:**

1. **Adaptadores por canal:** cada canal (email/whatsapp/voz) implementa una interfaz común (`recibir()`, `enviar()`), aislando al proveedor concreto. Cambiar de proveedor no debe tocar el orquestador.
2. **Orquestador único:** un componente central resuelve tenant + paciente, mantiene el estado de la conversación e invoca la lógica de negocio.
3. **Asíncrono con Celery:** el procesamiento de mensajes entrantes, llamadas a LLM y envíos se hacen en tareas Celery para no bloquear los webhooks (deben responder rápido).
4. **Reutilizar dominio, no duplicar:** las acciones (agendar cita, etc.) deben llamarse desde servicios compartidos, idealmente los mismos que la [API REST planificada (Doc 13)](13%20App%20movil%20y%20API%20REST.md).

**Estructura propuesta de la app:**

```
apps/recepcion_virtual/
├── __init__.py
├── models.py            # Conversacion, Mensaje, PlantillaMensaje, ConfiguracionCanal
├── orquestador.py       # Resolución tenant/paciente + intención + acción
├── intents.py           # Catálogo de intenciones y su mapeo a acciones
├── tasks.py             # Tareas Celery (procesar entrante, enviar saliente)
├── adapters/
│   ├── base.py          # Interfaz CanalAdapter (recibir/enviar)
│   ├── email.py         # SMTP/IMAP o API (SES/SendGrid/Postmark)
│   ├── whatsapp.py      # Proveedor a definir (§7)
│   └── voz.py           # Proveedor a definir (§8)
├── webhooks.py          # Endpoints entrantes (WhatsApp/voz/email inbound)
└── admin.py
```

---

## 6. CANAL EMAIL (RECIBIR Y ENVIAR)

### 6.1 Envío (saliente)

Reutiliza la configuración de email ya diseñada en [Doc 9 §3.1](9%20Documento%20de%20integraciones.md) (Django `EMAIL_BACKEND`). Casos: recordatorios de cita, confirmaciones, respuestas del asistente.

### 6.2 Recepción (entrante)

Para **recibir** correos hay dos estrategias:

| Estrategia | Cómo funciona | Ventaja | Desventaja |
|------------|---------------|---------|------------|
| **Inbound webhook** | El proveedor (SES + SNS, SendGrid Inbound Parse, Postmark, Mailgun Routes) hace POST a XMedical al llegar un correo | Tiempo real, sin polling | Requiere endpoint público y verificación de firma |
| **Polling IMAP** | Tarea Celery periódica que lee un buzón vía IMAP | Simple, sin webhook público | Latencia, gestión de estado leído/no leído |

### 6.3 Proveedores sugeridos (email)

| Proveedor | Envío | Recepción entrante | Notas |
|-----------|-------|--------------------|-------|
| **Amazon SES** | ✅ | ✅ (SES + SNS/S3) | Bajo costo a volumen; buen fit con S3 ya previsto |
| **SendGrid** | ✅ | ✅ (Inbound Parse) | Fácil de integrar; plantillas |
| **Postmark** | ✅ | ✅ (Inbound) | Buena entregabilidad transaccional |
| **Mailgun** | ✅ | ✅ (Routes) | Reglas de enrutamiento flexibles |
| SMTP/IMAP genérico | ✅ | ✅ (IMAP polling) | Para clínicas con su propio correo |

> El enrutamiento del buzón entrante debe permitir mapear la dirección/alias al **tenant** correcto (ej. `citas+clinicademo@xmedical.cloud`, o un buzón por institución).

---

## 7. CANAL WHATSAPP (PROVEEDOR A DEFINIR)

> **Decisión pendiente.** WhatsApp Business **no permite** conexiones no oficiales para producción; debe usarse la **WhatsApp Business Platform (Cloud API)** de Meta, directamente o a través de un BSP (Business Solution Provider). Estas son las opciones a evaluar.

| Proveedor | Tipo | Ventajas | Consideraciones |
|-----------|------|----------|-----------------|
| **Meta WhatsApp Cloud API** (directo) | Oficial (API propia) | Sin intermediario, menor costo por mensaje, control total | Más trabajo de integración; gestión de plantillas y verificación de negocio |
| **Twilio** (WhatsApp) | BSP | API madura, buena documentación, también voz/SMS (sinergia con §8) | Costo por mensaje mayor; vendor lock-in parcial |
| **360dialog** | BSP | Especializado en WhatsApp, precio por API (no por conversación intermediada) | Menos servicios adicionales |
| **MessageBird / Infobip / Gupshup** | BSP omnicanal | Un solo proveedor para varios canales | Evaluar costos y cobertura regional (Honduras/LatAm) |

**Elementos a considerar antes de elegir:**

- **Plantillas (HSM):** los mensajes proactivos (recordatorios) fuera de la ventana de 24 h requieren **plantillas preaprobadas** por Meta.
- **Ventana de 24 horas:** fuera de ella solo se pueden enviar plantillas; dentro, conversación libre.
- **Costo:** modelo por conversación (Meta) vs. por mensaje (algunos BSP). Estimar volumen.
- **Número/verificación:** se necesita un número dedicado y verificación del negocio (Meta Business Manager).
- **Región:** confirmar soporte y latencia para **Honduras / Centroamérica**.

**Recepción entrante:** todos los proveedores entregan los mensajes vía **webhook** (POST). El adaptador `whatsapp.py` normaliza el payload del proveedor a un formato interno común.

---

## 8. CANAL VOZ / INTERFAZ CONVERSACIONAL (PROVEEDOR A DEFINIR)

El canal de voz combina **telefonía** (recibir/emitir llamadas) con **STT** (voz→texto), **TTS** (texto→voz) y el **orquestador IA**. Hay dos enfoques:

### 8.1 Enfoque A: piezas separadas (telefonía + STT + TTS + LLM)

| Componente | Proveedores sugeridos | Notas |
|------------|-----------------------|-------|
| **Telefonía / SIP** | Twilio Voice, Amazon Connect, Vonage, Telnyx | Número entrante y control de llamada (webhooks) |
| **STT (voz→texto)** | OpenAI Whisper/gpt-4o-transcribe, Google Speech-to-Text, Azure Speech, AWS Transcribe, Deepgram | Verificar calidad en **español latino** |
| **TTS (texto→voz)** | ElevenLabs, Amazon Polly (Neural), Google TTS, Azure Neural TTS, OpenAI TTS | Naturalidad y voces en español; latencia |
| **NLU/LLM** | `apps.core.ai_services` (OpenAI/OpenRouter) | Ya disponible en el proyecto |

### 8.2 Enfoque B: plataformas de "voz IA" integradas

| Proveedor | Qué aporta | Consideraciones |
|-----------|-----------|-----------------|
| **Vapi** | Orquesta telefonía+STT+TTS+LLM con baja latencia | Servicio gestionado; costo por minuto |
| **Retell AI** | Agentes de voz llave en mano | Similar a Vapi |
| **Twilio ConversationRelay / Voice + Media Streams** | Streaming de audio hacia tu backend | Más control, más desarrollo |
| **OpenAI Realtime API** | Voz a voz de baja latencia | Requiere puente de telefonía (SIP/WebRTC) |

**Consideraciones clave del canal voz:**

- **Latencia:** para una conversación natural, el ciclo STT→LLM→TTS debe ser bajo (idealmente < 1–1.5 s). Favorece streaming.
- **Idioma:** priorizar calidad de STT/TTS en **español (LatAm)**.
- **Costo por minuto:** suele ser el canal más caro; usarlo para casos de alto valor (agendamiento, confirmaciones) y con opción de "marcar 0 para un humano".
- **Fallback humano:** transferir a recepción si baja la confianza o el paciente lo pide.
- **Grabación y consentimiento:** informar y registrar consentimiento (dato sensible, ver §11).

**Recomendación de arranque:** empezar por el **Enfoque B** (p. ej. Twilio Voice + una plataforma de voz IA) para validar el caso de uso rápido, y migrar a piezas separadas (Enfoque A) si se requiere control de costos/latencia a escala. **Proveedor final a definir.**

---

## 9. ORQUESTADOR: IDENTIDAD, TENANT E INTENCIÓN

Los canales entrantes (WhatsApp, voz, email) **no llegan por subdominio**, por lo que el `TenantMiddleware` actual no puede resolver el tenant. El orquestador debe resolverlo explícitamente:

| Señal | Cómo mapea al tenant |
|-------|----------------------|
| Número WhatsApp / línea telefónica de destino | Cada institución tiene su número → tabla `ConfiguracionCanal` |
| Dirección/alias de email de destino | `citas@clinicademo...` o alias por institución |
| Teléfono/email del paciente | Búsqueda del `Paciente` (puede existir en más de un tenant → desambiguar) |

Flujo del orquestador:

```
1. Recibir mensaje (adaptador) ─────────────► normalizar payload
2. Resolver TENANT (por canal de destino) ──► set contexto institución
3. Resolver PACIENTE (por remitente) ───────► identidad (o pedir documento)
4. Clasificar INTENCIÓN (LLM/NLU) ──────────► agendar | cancelar | confirmar
                                              | consultar | hablar_con_humano
5. Ejecutar ACCIÓN (servicio dominio / API) ► resultado
6. Generar RESPUESTA (LLM + plantilla) ─────► enviar por el mismo canal
7. Registrar CONVERSACIÓN (auditoría) ──────► Conversacion + Mensaje
```

Reutiliza `apps.core.ai_services` para los pasos 4 y 6 (ya soporta OpenAI/OpenRouter configurable por entorno).

---

## 10. MODELO DE DATOS PROPUESTO

```python
# apps/recepcion_virtual/models.py (borrador)

class ConfiguracionCanal(models.Model):
    institucion = models.ForeignKey("core.Institucion", on_delete=models.CASCADE)
    canal = models.CharField(max_length=20)      # email | whatsapp | voz | sms
    proveedor = models.CharField(max_length=40)  # ses | meta_cloud | twilio | vapi ...
    identificador = models.CharField(max_length=120)  # nº telefónico, email, phone_id
    credenciales = models.JSONField(default=dict)     # claves cifradas / referencia a secreto
    activo = models.BooleanField(default=True)

class Conversacion(models.Model):
    institucion = models.ForeignKey("core.Institucion", on_delete=models.CASCADE)
    paciente = models.ForeignKey("pacientes.Paciente", null=True, on_delete=models.SET_NULL)
    canal = models.CharField(max_length=20)
    externo_id = models.CharField(max_length=120)     # id de conversación del proveedor
    estado = models.CharField(max_length=20, default="abierta")  # abierta|cerrada|escalada
    creada = models.DateTimeField(auto_now_add=True)

class Mensaje(models.Model):
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name="mensajes")
    direccion = models.CharField(max_length=10)       # entrante | saliente
    contenido = models.TextField()
    intencion = models.CharField(max_length=40, blank=True)
    metadatos = models.JSONField(default=dict)        # audio_url, confianza, tokens...
    creado = models.DateTimeField(auto_now_add=True)

class PlantillaMensaje(models.Model):
    institucion = models.ForeignKey("core.Institucion", on_delete=models.CASCADE)
    canal = models.CharField(max_length=20)
    clave = models.CharField(max_length=60)           # recordatorio_cita | confirmacion ...
    contenido = models.TextField()                    # con placeholders {{ }}
    aprobada_proveedor = models.BooleanField(default=False)  # p.ej. plantilla HSM WhatsApp
```

> Las **credenciales** de proveedor no deben guardarse en claro en la BD: usar variables de entorno / gestor de secretos y almacenar solo referencias (coherente con la política de [Doc 7 Seguridad](7%20Documento%20de%20Seguridad.md)).

---

## 11. SEGURIDAD Y PRIVACIDAD

Los datos clínicos son **sensibles**. Este módulo amplía la superficie de exposición, por lo que:

| Medida | Descripción |
|--------|-------------|
| **Verificación de webhooks** | Validar firma/HMAC de cada proveedor entrante (email/WhatsApp/voz) antes de procesar |
| **Aislamiento por tenant** | Toda conversación y acción se limita al `institucion_id` resuelto; nunca cruzar tenants |
| **Minimización de datos** | Enviar por canales externos solo lo imprescindible (evitar volcar historia clínica por WhatsApp/email) |
| **Consentimiento** | Registrar opt-in del paciente para cada canal; en voz, aviso de grabación |
| **Cifrado** | TLS en tránsito; secretos de proveedor fuera de la BD |
| **Retención** | Política de retención/borrado de audios y transcripciones |
| **Escalado seguro** | Handoff a humano sin exponer credenciales ni datos de otros pacientes |
| **Auditoría** | Registrar cada mensaje y acción (coherente con auditoría existente en `apps.core`) |

Alinear con [Documento 7: Seguridad](7%20Documento%20de%20Seguridad.md) y [Documento 14: Roadmap Seguridad](14%20Roadmap%20Seguridad.md).

---

## 12. CONFIGURACIÓN (VARIABLES DE ENTORNO PREVISTAS)

```env
# Email entrante/saliente (reutiliza EMAIL_* de Doc 9)
RECEPCION_EMAIL_INBOUND=webhook   # webhook | imap
IMAP_HOST=
IMAP_USER=
IMAP_PASSWORD=

# WhatsApp (proveedor a definir - ejemplo Meta Cloud API)
WHATSAPP_PROVIDER=                 # meta_cloud | twilio | 360dialog ...
WHATSAPP_PHONE_ID=
WHATSAPP_TOKEN=
WHATSAPP_VERIFY_TOKEN=            # verificación de webhook

# Voz (proveedor a definir)
VOICE_PROVIDER=                   # twilio | vapi | retell ...
VOICE_STT_PROVIDER=              # whisper | google | deepgram ...
VOICE_TTS_PROVIDER=             # elevenlabs | polly | azure ...

# IA / NLU: se reutiliza la config existente (OPENAI_*/OPENROUTER_* del .env)
```

La configuración fina (número, credenciales, plantillas) vive **por institución** en `ConfiguracionCanal`, permitiendo que cada clínica use su propio proveedor/número.

---

## 13. CASOS DE USO (EJEMPLOS)

| # | Canal | Escenario | Acción del asistente |
|---|-------|-----------|----------------------|
| 1 | WhatsApp | "Quiero una cita con medicina general el jueves" | Buscar disponibilidad, proponer horario, agendar `Cita` |
| 2 | WhatsApp | Recordatorio 24 h antes | Enviar plantilla; procesar "confirmo"/"cancelo" |
| 3 | Email | Paciente pide reprogramar | Identificar cita, ofrecer opciones, actualizar |
| 4 | Voz | Llamada: "¿A qué hora es mi cita?" | Identificar paciente, leer próxima cita (TTS) |
| 5 | Cualquiera | "Quiero hablar con una persona" | Escalar a recepcionista humano |

> En todos los casos, si la confianza del NLU es baja o la acción es sensible, el flujo **escala a un humano** en lugar de adivinar.

---

## 14. CONSIDERACIONES Y RIESGOS

- **Costos operativos:** voz > WhatsApp > email. Estimar volumen por tenant y establecer límites.
- **Idioma:** priorizar calidad en **español (Honduras/LatAm)** para STT/TTS y prompts.
- **Cumplimiento WhatsApp:** plantillas HSM, ventana de 24 h y verificación de negocio de Meta.
- **Latencia en voz:** exige streaming y proveedores de baja latencia.
- **Responsabilidad clínica:** el asistente **no** debe dar diagnóstico ni consejo médico; se limita a lo administrativo y deriva a un profesional.
- **Dependencia de proveedores:** los adaptadores por canal mitigan el lock-in; documentar contratos y SLAs.
- **Fallbacks:** ante caída de un proveedor, degradar con elegancia (p. ej. de voz a mensaje, o a agenda web).

---

## 15. PLAN DE IMPLEMENTACIÓN POR FASES

| Fase | Entregable | Depende de |
|------|-----------|------------|
| 0 | App `apps/recepcion_virtual/` + modelos + orquestador base | — |
| 1 | **Email** saliente + entrante + intents básicos (recordatorio/confirmación) | Proveedor email (§6) |
| 2 | **WhatsApp** entrante/saliente + plantillas + agendamiento | **Definir proveedor WhatsApp (§7)** |
| 3 | **Voz** (llamadas + STT/TTS + IVR simple) | **Definir proveedor voz (§8)** |
| 4 | Handoff a humano + panel de conversaciones en la web | Fases 1–3 |
| 5 | Métricas (tasa de resolución, escalados, costos) | Fase 4 |

> **Prerrequisito recomendado:** exponer las acciones de dominio como servicios compartidos (o la [API REST del Doc 13](13%20App%20movil%20y%20API%20REST.md)) para que el orquestador no dependa de las vistas web.

---

## 16. DECISIONES PENDIENTES (A DEFINIR)

| Tema | Opciones (§) | Estado |
|------|--------------|--------|
| Proveedor de **email entrante** | SES / SendGrid / Postmark / Mailgun / IMAP (§6.3) | 🔴 Pendiente |
| Proveedor de **WhatsApp** | Meta Cloud API / Twilio / 360dialog / otros (§7) | 🔴 Pendiente |
| Proveedor de **voz** (telefonía+STT+TTS) | Enfoque A vs. B (§8) | 🔴 Pendiente |
| Uso de **API REST** vs. servicios internos | Doc 13 | 🟡 A confirmar |
| Nombre definitivo del módulo | §2 (recomendado: Recepción Virtual) | 🟡 A confirmar |

---

## 17. REFERENCIAS

- [Documento 4: Arquitectura de alto nivel](4%20Documento%20Arquitectura%20de%20alto%20nivel.md)
- [Documento 6: Modelo de datos](6%20Documento%20Modelo%20de%20datos.md)
- [Documento 7: Seguridad](7%20Documento%20de%20Seguridad.md)
- [Documento 9: Integraciones](9%20Documento%20de%20integraciones.md)
- [Documento 13: App móvil y API REST](13%20App%20movil%20y%20API%20REST.md)
- [Documento 14: Roadmap Seguridad](14%20Roadmap%20Seguridad.md)

---

**Fin del Documento 15: Recepción Virtual Omnicanal**
