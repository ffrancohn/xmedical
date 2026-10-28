# Contrato visual — Registro preclínica

**Objetivo y usuario:** Enfermería; capturar signos vitales y alertas de riesgo para una cita.

**Decisión o tarea que habilita:** Registrar TA, FC, FR, temp, etc. y guardar antes de consulta médica.

**Contenido y estructura de datos:** Paciente/cita, form Django `form.as_p`, alertas de riesgo post-validación.

**Representación principal y alternativa:** Primaria = **formulario enfocado** (`preclinica/form.html`). Complemento Atlas = **banner** escena `enfermeria`. Lista `preclinica_lista` = tabla + banner.

**Por qué no usar otras representaciones:** Entrada numérica densa; isometría no mejora precisión; hilo ya cubre dashboard enfermería.

**Vistas / componentes:** `preclinica/form.html`, `preclinica/lista.html`, `atlas_scene_banner`.

**Interacciones y eventos:** POST guardar; alertas inline.

**Estados (vacío, carga, error, seleccionado):** Errores campo; alertas riesgo en bloque destacado.

**Accesibilidad / control táctil y teclado:** Labels en inputs; alertas con texto; banner presentational.

**Estrategia móvil y reducción de movimiento:** `max-w-3xl` card; teclado numérico en móvil vía tipos input.

**Rendimiento y presupuesto de recursos:** Mínimo JS.

**Criterios de aceptación verificables:**
- Guardar signos funciona en Atlas y classic.
- Banner visible en lista y formulario en modo Atlas.
- Alertas de riesgo legibles (no solo color rojo).
