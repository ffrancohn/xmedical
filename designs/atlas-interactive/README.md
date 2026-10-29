# Diseños — interfaz isométrica interactiva (Atlas)

## Paquete v1 (`xmedical_visual_assets_v1`)

| Ubicación | Contenido |
|-----------|-----------|
| [`exports/xmedical_visual_assets_v1.zip`](exports/xmedical_visual_assets_v1.zip) | Archivo original entregado |
| [`source/v1/`](source/v1/) | Extracción completa + `manifest.json` + README del paquete |
| [`pacientes/archivador/`](pacientes/archivador/) | Copia de referencia archivador cerrado/abierto |
| [`citas/agenda/`](citas/agenda/) | Agenda cerrada/abierta |
| [`recepcion/`](recepcion/) | Mostrador y sala de espera |

## Paquete v2 de avatares (`xmedical_avatares_completos_v2`)

Sustituye las 18 variantes numeradas del paquete v1 por **10 retratos**, uno por grupo de edad y sexo.

| Ubicación | Contenido |
|-----------|-----------|
| [`exports/xmedical_avatares_completos_v2.zip`](exports/xmedical_avatares_completos_v2.zip) | Paquete entregado |
| [`source/v1/avatares/`](source/v1/avatares/) | Los 10 WebP + `manifest.json` + `README.md` del paquete |
| `static/atlas-interactive/assets/v1/avatares/` | Copia servida por Django |
| `static/atlas-interactive/manifest.avatares.v2.json` | Metadatos del paquete (ids, dimensiones, transparencia) |

**Limitaciones declaradas por el autor del paquete:** 240×330 px, **sin canal alfa** (conservan el fondo de la lámina) y pensados para tarjetas pequeñas; no ampliar. Para producción definitiva hay que regenerar cada personaje con transparencia.

## Servidos por Django (producción)

Los WebP activos están en:

`static/atlas-interactive/assets/v1/`

- `modulos/` — metáforas por módulo (archivador, agenda, recepción, …)
- `avatares/` — 10 ilustraciones completas por grupo de edad y sexo (`ninos_masculino.webp`, …), 240×330 px y con fondo. Paquete v2; ver `avatares/README.md`.
- `estados/` — iconos de estado de cita
- `documentos/` — carpetas, recetas, estudios
- `profesionales/` — roles clínicos

Metadatos: [`static/atlas-interactive/manifest.v1.json`](../../static/atlas-interactive/manifest.v1.json) para módulos, documentos, estados y profesionales; [`manifest.avatares.v2.json`](../../static/atlas-interactive/manifest.avatares.v2.json) para los avatares.

## Convención de nombres

```
{modulo}_{estado}.webp
{grupo_edad}_{sexo}.webp      # avatares v2: masculino | femenino
```

Estados de módulo: `cerrado` / `abierto` (o `cerrada` / `abierta` en agenda).
El paquete v1 usaba `{grupo_edad}_01..04.webp`; esos archivos ya no se sirven.

## Integración

Tras actualizar artes, copiar de `source/v1/` a `static/atlas-interactive/assets/v1/` y ejecutar `collectstatic` en producción.
