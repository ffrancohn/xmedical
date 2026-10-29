# Contrato visual — Dashboard especialista (hub Atlas)

**Objetivo y usuario:** Médico especialista de segundo nivel; decidir qué derivación atender primero y cómo va su agenda del día.

**Decisión o tarea que habilita:** Priorizar la bandeja de referencias por prioridad y antigüedad, y abrir la agenda o la bandeja completa sin perder el resumen.

**Contenido y estructura de datos:** Agregados por institución y profesional: citas de hoy por estado (`agenda_exploracion`), presión de sala con signos y tiempos (`espera_exploracion`) y bandeja de derivaciones por prioridad, especialidad destino y espera media en días (`referencias_exploracion`). Sin nombres de pacientes ni diagnósticos.

**Representación principal y alternativa:** Primaria = **tablas de referencias y agenda** (`dashboards/especialista.html`). Complemento Atlas = **hub isométrico de 3 módulos** (`atlas/hub_especialista.html`) con panel de exploración y acciones.

**Por qué no usar otras representaciones:** Un kanban de referencias añadiría estados que el modelo no tiene (sólo pendiente/aceptada/rechazada/completada); el grafo no aporta relaciones útiles; la tabla sigue siendo superior para decidir caso por caso.

**Vistas / componentes:** `apps/dashboards/views.py::EspecialistaDashboardView`, `templates/dashboards/especialista.html`, `templates/atlas/hub_especialista.html`, `explore_derivaciones.html`, reutiliza `explore_agenda_medico.html` y `explore_espera_medico.html`, `apps/core/atlas_catalog.py` (área `especialista`), `apps/core/atlas_explore.py::referencias_exploracion`, `atlas-interactive.js`, `iso.js` escena `especialista`.

**Interacciones y eventos:** Clic en objeto → panel con foco, `aria-expanded`, imagen abierta; `Escape` cierra y devuelve el foco; acciones del panel: revisar bandeja, mi agenda, cola de signos.

**Estados (vacío, carga, error, seleccionado):** Sin pendientes → contadores en 0 y barras al 0 %; sin especialidad destino → se omite el bloque; prioridad alta usa la barra de alerta; con `?classic=1` no se renderiza el hub.

**Accesibilidad / control táctil y teclado:** Botones nativos, `aria-controls`, `:focus-visible`, foco programático al panel, barras con `role="img"` y `aria-label` («Alta: 4 de 7 pendientes»), imágenes decorativas con `alt=""`. El decimal respeta el locale (`2,4 d`).

**Estrategia móvil y reducción de movimiento:** Misma rejilla `auto-fit` que el hub del médico; estadísticas en 2 columnas; `prefers-reduced-motion` desactiva scroll y animaciones.

**Rendimiento y presupuesto de recursos:** 3 agregados por render (citas, preclínica, referencias con `AVG(now - creado_en)`); imágenes WebP de 4–9 KB; sin JS adicional.

**Criterios de aceptación verificables:**
- Con `interface_mode=atlas`, el inicio del especialista muestra hub de 3 objetos y las tablas completas debajo.
- Con `?classic=1` o modo `classic` no se renderiza el hub.
- «Derivaciones» abre su panel; ningún módulo abre contenedor vacío.
- El hub no muestra nombres de pacientes ni diagnósticos (test de código fuente).
- Tests: `apps.core.tests_atlas_especialista` en verde.
