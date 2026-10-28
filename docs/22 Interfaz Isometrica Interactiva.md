# Interfaz isométrica interactiva (Atlas hub)

Especificación operativa y mapa de carpetas. Complementa [doc 18](18%20Interfaz%20Atlas%20Despliegue%20Produccion.md) y [doc 21](21%20Arquitectura%20Visual%20Pantallas.md).

## Principio de layout (modo Atlas)

- **Navegación:** menú lateral en escritorio y drawer en móvil (`base.html`) — **sin cambios**, no duplicar menú isométrico.
- **Área principal:** escena isométrica a pantalla (`xm-atlas-viewport`): objeto + exploración.
- **Datos operativos:** solo en **panel de escritorio** integrado (`xm-atlas-desk-panel`), abierto con `?ver=datos` (pacientes) o `?ver=agenda` (citas), no como segunda “pantalla clásica” debajo del hub.

Modo **classic** no cambia. Modo **Atlas** sustituye el contenido central por la escena; listas/tablas clásicas solo con `?classic=1` o modo classic.

## Carpetas

| Ruta | Uso |
|------|-----|
| [`designs/atlas-interactive/`](../designs/atlas-interactive/) | Diseños fuente (WebP/SVG) — pendiente de artes finales |
| [`static/atlas-interactive/`](../static/atlas-interactive/) | CSS, JS, `catalog.json`, assets optimizados |
| [`templates/atlas/`](../templates/atlas/) | Partials Django hub y exploración |
| [`deck/atlas-interactive/`](../deck/atlas-interactive/) | Prototipo estático sin backend |
| [`apps/core/atlas_catalog.py`](../apps/core/atlas_catalog.py) | Metáforas y visibilidad por rol |
| [`apps/core/atlas_explore.py`](../apps/core/atlas_explore.py) | Agregados pacientes/citas |

## Configuración grupos de edad

En `Institucion.configuracion`:

```json
{
  "pacientes_grupos_edad": {
    "buckets": [
      {"id": "ninos", "label": "Niños", "min_years": 0, "max_years": 11}
    ]
  }
}
```

Si falta, se usan defaults en `atlas_explore.DEFAULT_AGE_BUCKETS`.

## Integración actual

- **Recepción** (`dashboards/recepcion`): hub con módulos Pacientes, Citas, Atención del día.
- **Pacientes** (`pacientes_lista`): solo archivador hasta `?ver=datos` (búsqueda, grupo); `?classic=1` omite hub.
- **Citas** (`citas_lista`): solo agenda isométrica hasta `?ver=agenda`; `?classic=1` vista clásica completa.
- **Formularios recepción** (nuevo/editar paciente, agendar cita, ficha): cabecera isométrica + **panel de formulario legible** (`atlas/stage_begin.html`); enlace **Vista clásica** con `?classic=1`.

## Próximos pasos

1. Sustituir placeholders emoji por WebP desde `designs/`.
2. Animaciones CSS de apertura (`open` state).
3. Módulos Consultas, Historia, Medicamentos según catálogo.
4. PixiJS solo si los assets lo exigen.
