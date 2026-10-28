# Contrato visual — Wizard de consulta

**Objetivo y usuario:** Médico / profesional clínico; completar documentación de consulta en 7 pasos.

**Decisión o tarea que habilita:** Registrar preclínica integrada, motivo, anamnesis, examen, variables, diagnóstico, plan y resumen.

**Contenido y estructura de datos:** Paso actual, lista pasos, formulario del paso, autoguardado opcional, cita/paciente en cabecera.

**Representación principal y alternativa:** Primaria = **wizard stepper** (`xm-wizard-steps` + partials por paso). Complemento Atlas = **banner** escena `medico` (contexto, no interactivo).

**Por qué no usar otras representaciones:** Flujo secuencial obligatorio; isometría no acelera captura clínica; timeline HCE es otra pantalla.

**Vistas / componentes:** `consulta/wizard.html`, pasos `paso1_*` … `paso7_*`, `atlas_scene_banner` en cabecera.

**Interacciones y eventos:** Navegación paso anterior/siguiente; autosave AJAX; CIE-10 autocomplete.

**Estados (vacío, carga, error, seleccionado):** Paso activo/done; indicador autosave; errores de formulario por campo.

**Accesibilidad / control táctil y teclado:** Orden de foco en formulario; stepper visible sin depender de color; banner decorativo.

**Estrategia móvil y reducción de movimiento:** Stepper scroll; formulario una columna; banner compacto.

**Rendimiento y presupuesto de recursos:** Un SVG banner; pasos render server-side.

**Criterios de aceptación verificables:**
- Completar consulta igual en classic y Atlas.
- Banner no intercepta clics del formulario.
- Stepper indica paso actual con texto, no solo color.
