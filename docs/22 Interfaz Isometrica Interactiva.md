# Interfaz isométrica interactiva (Atlas hub)

Especificación operativa y mapa de carpetas. Complementa [doc 18](18%20Interfaz%20Atlas%20Despliegue%20Produccion.md) y [doc 21](21%20Arquitectura%20Visual%20Pantallas.md).

## Principio Objeto → Exploración → Acción

1. **Objeto:** metáfora isométrica (archivador, agenda, mostrador) — hub interactivo.
2. **Exploración:** panel HTML con agregados (sin PHI en assets gráficos).
3. **Acción:** vistas Django existentes (listas, formularios, permisos actuales).

Modo **classic** no cambia. Modo **Atlas** activa hub en recepción y exploración en pacientes.

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
- **Pacientes** (`pacientes_lista`): exploración archivador + tabla; `?grupo=<id>` filtra por edad; `?classic=1` omite hub.

## Próximos pasos

1. Sustituir placeholders emoji por WebP desde `designs/`.
2. Animaciones CSS de apertura (`open` state).
3. Módulos Consultas, Historia, Medicamentos según catálogo.
4. PixiJS solo si los assets lo exigen.
