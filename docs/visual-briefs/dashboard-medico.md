# Contrato visual — Dashboard médico (hub Atlas)

**Objetivo y usuario:** Médico general o especialista de primer nivel; entender su jornada antes de la primera consulta del día.

**Decisión o tarea que habilita:** Decidir a quién atender ahora, si la sala está presionada y qué se ha atendido, sin salir del inicio.

**Contenido y estructura de datos:** Agregados por institución y profesional: citas de hoy por estado (`agenda_medico_exploracion`), presión de sala con signos tomados y tiempos de espera (`espera_medico_exploracion`), consultas y diagnósticos de 30 días (`historia_medico_exploracion`). Sin nombres ni documentos de pacientes.

**Representación principal y alternativa:** Primaria = **tabla de agenda del día** (`dashboard_medico.html`) más tarjetas de conteo. Complemento Atlas = **hub isométrico de 3 módulos** (`atlas/hub_medico.html`) con panel de exploración y acciones por panel.

**Por qué no usar otras representaciones:** Un tablero isométrico completo sustituiría la tabla y perdería densidad por fila; el grafo no aporta relaciones entre entidades de la jornada; el mapa geográfico no aplica (la institución es una sola sede).

**Vistas / componentes:** `apps/core/views.py::DashboardView`, `templates/dashboard_medico.html`, `templates/atlas/hub_medico.html`, `explore_agenda_medico.html`, `explore_espera_medico.html`, `explore_historia_medico.html`, `apps/core/atlas_catalog.py` (área `medico`), `apps/core/atlas_explore.py`, `static/atlas-interactive/atlas-interactive.js`, `iso.js` escena `medico`.

**Interacciones y eventos:** Clic en objeto → abre panel, foco al panel, `aria-expanded` en el objeto; `Escape` cierra y devuelve el foco; acciones del panel llevan a agenda, cola de signos, pacientes y epidemiología.

**Estados (vacío, carga, error, seleccionado):** Sin citas → contadores en 0 y «Siguiente —»; sin diagnósticos → texto explícito; seleccionado = borde primario + imagen abierta; el hub se oculta si el usuario no tiene permiso de pacientes (sólo agenda y espera).

**Accesibilidad / control táctil y teclado:** Objetos `<button>` nativos, `aria-controls` al contenedor del panel, `:focus-visible` de 3 px, foco programático al panel (`tabindex="-1"`), barras con `role="img"` y `aria-label` numérico, imágenes decorativas con `alt=""`.

**Estrategia móvil y reducción de movimiento:** Rejilla `auto-fit` de 7,5 rem para objetos; estadísticas en 2 columnas en móvil; `prefers-reduced-motion` desactiva scroll suave y animaciones del panel.

**Rendimiento y presupuesto de recursos:** 3 consultas agregadas por render (citas, preclínica, consultas/diagnósticos) y 6 imágenes WebP de 4–9 KB; sin JS extra (reutiliza `atlas-interactive.js`).

**Criterios de aceptación verificables:**
- Con `interface_mode=atlas` el inicio del médico muestra hub de 3 objetos y la tabla sigue completa debajo.
- Con `?classic=1` o modo `classic` no se renderiza el hub.
- Cada objeto abre su panel; ningún módulo abre un contenedor vacío.
- El hub no muestra nombres de pacientes (verificado por test de código fuente).
- Tests: `apps.core.tests_atlas_medico` en verde.
