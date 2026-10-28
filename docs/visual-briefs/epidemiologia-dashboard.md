# Contrato visual — Dashboard epidemiológico

**Objetivo y usuario:** Administrador / epidemiólogo interno; detectar brotes y revisar tendencias CIE-10.

**Decisión o tarea que habilita:** Decidir vigilancia o comunicación ante umbral de casos.

**Contenido y estructura de datos:** Alertas de brote (tabla), totales 30 días, configuración ventana/umbral, tendencias por mes (datos agregados).

**Representación principal y alternativa:** Primaria = **stat cards + tablas** (`dashboards/epidemiologia.html`). Complemento = **gráfico SVG de líneas** (`components/epidemiologia_trend_chart.html`) + barras CSS en top 30 días. **Sin capa Atlas / isometría.**

**Por qué no usar otras representaciones:** Datos cuantitativos y exportables; isometría no mejora comparación de casos; heatmap opcional secundario.

**Vistas / componentes:** `epidemiologia.html`, `institution_filter.html`, sin `atlas_scene_banner`.

**Interacciones y eventos:** Filtro institución; lectura tabla; enlaces a detalle si se añaden.

**Estados (vacío, carga, error, seleccionado):** Tabla vacía con mensaje; stats en cero.

**Accesibilidad / control táctil y teclado:** Tabla semántica `<table>`; contraste en alertas; no depender de color solo.

**Estrategia móvil y reducción de movimiento:** `overflow-x-auto` en tablas; sin animaciones.

**Rendimiento y presupuesto de recursos:** Agregaciones en servidor; gráficos lazy si se añaden.

**Criterios de aceptación verificables:**
- Modo Atlas no inserta banner isométrico en esta ruta.
- KPIs y alertas legibles en móvil.
- Gráfico SVG visible cuando hay series; tabla mensual en «Ver datos tabulares».
