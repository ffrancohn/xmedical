# Diseños — interfaz isométrica interactiva (Atlas)

## Paquete v1 (`xmedical_visual_assets_v1`)

| Ubicación | Contenido |
|-----------|-----------|
| [`exports/xmedical_visual_assets_v1.zip`](exports/xmedical_visual_assets_v1.zip) | Archivo original entregado |
| [`source/v1/`](source/v1/) | Extracción completa + `manifest.json` + README del paquete |
| [`pacientes/archivador/`](pacientes/archivador/) | Copia de referencia archivador cerrado/abierto |
| [`citas/agenda/`](citas/agenda/) | Agenda cerrada/abierta |
| [`recepcion/`](recepcion/) | Mostrador y sala de espera |

## Servidos por Django (producción)

Los WebP activos están en:

`static/atlas-interactive/assets/v1/`

- `modulos/` — metáforas por módulo (archivador, agenda, recepción, …)
- `avatares/` — genéricos por grupo de edad (`ninos_01.webp`, …)
- `estados/` — iconos de estado de cita
- `documentos/` — carpetas, recetas, estudios
- `profesionales/` — roles clínicos

Metadatos: [`static/atlas-interactive/manifest.v1.json`](../../static/atlas-interactive/manifest.v1.json)

## Convención de nombres

```
{modulo}_{estado}.webp
{grupo_edad}_{variante}.webp
```

Estados de módulo: `cerrado` / `abierto` (o `cerrada` / `abierta` en agenda).

## Integración

Tras actualizar artes, copiar de `source/v1/` a `static/atlas-interactive/assets/v1/` y ejecutar `collectstatic` en producción.
