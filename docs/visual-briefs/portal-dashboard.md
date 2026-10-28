# Contrato visual — Portal paciente (inicio)

**Objetivo y usuario:** Paciente; ver resumen de citas e historial y acceder a acciones self-service.

**Decisión y tarea que habilita:** Confirmar próxima cita, solicitar cita o ver historia sin soporte recepción.

**Contenido y estructura de datos:** Próximas citas, enlaces a `portal_citas`, `portal_historia`, mensajes institución.

**Representación principal y alternativa:** Primaria = **cards y listas** consumidor (`portal_paciente/dashboard.html`). Complemento Atlas = **banner** escena `paciente` (contexto acogedor, no mapa clicable).

**Por qué no usar otras representaciones:** Paciente no opera “estaciones” clínicas; isometría interactiva añade fricción; storytelling en deck para onboarding, no dashboard diario.

**Vistas / componentes:** `portal/dashboard.html`, layout portal, `atlas_scene_banner`.

**Interacciones y eventos:** Enlaces cards; preferencias portal para modo Atlas.

**Estados (vacío, carga, error, seleccionado):** Sin citas → empty state amigable.

**Accesibilidad / control táctil y teclado:** Targets grandes; contraste en layout portal.

**Estrategia móvil y reducción de movimiento:** Grid responsive; banner no full-screen.

**Rendimiento y presupuesto de recursos:** Un SVG opcional.

**Criterios de aceptación verificables:**
- Dashboard usable sin modo Atlas.
- Con Atlas, banner no oculta CTAs principales.
- No requerir interacción con SVG para ninguna tarea.
