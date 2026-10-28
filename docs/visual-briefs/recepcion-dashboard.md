# Contrato visual — Dashboard recepción

**Objetivo y usuario:** Recepcionista; situación operativa del día (llegadas, sala, pendientes).

**Decisión o tarea que habilita:** Priorizar a quién atender y abrir acciones (paciente, cita, check-in).

**Contenido y estructura de datos:** Estaciones del flujo clínico (`hilo.stations`), conteos por estación, acciones rápidas en hero.

**Representación principal y alternativa:** Primaria = **diagrama de flujo horizontal** (`components/hilo.html`). Complemento Atlas = **hero isométrico** (`atlas_hero` + escena `recepcion`).

**Por qué no usar otras representaciones:** Tabla sola no muestra el recorrido; isometría completa no sustituye paneles del hilo; mapa geográfico no aplica.

**Vistas / componentes:** `dashboards/recepcion.html`, `hilo.html`, `recepcion_hero_actions.html`, `iso.js` escena `recepcion`.

**Interacciones y eventos:** Clic estación hilo → panel; hero decorativo + enlaces acción; sidebar navegación módulos.

**Estados (vacío, carga, error, seleccionado):** Hilo con estaciones `done`/`mine`/`open`; classic usa `xm-page-header` equivalente.

**Accesibilidad / control táctil y teclado:** Botones estación con `aria-expanded`; hero SVG `role="presentation"`; acciones en HTML.

**Estrategia móvil y reducción de movimiento:** Hilo scroll horizontal; hero acotado en altura; sin animación obligatoria.

**Rendimiento y presupuesto de recursos:** Un SVG iso por hero; hilo DOM ligero.

**Criterios de aceptación verificables:**
- Modo classic y Atlas muestran el mismo hilo funcional.
- Atlas muestra hero + hint de activación si usuario en classic en otras rutas.
- Acciones rápidas alcanzables sin interactuar con SVG.
