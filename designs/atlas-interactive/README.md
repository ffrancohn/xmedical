# Diseños — interfaz isométrica interactiva (Atlas)

Carpeta para **artes finales** antes de exportar a `static/atlas-interactive/assets/`.

## Estructura

| Carpeta | Contenido esperado |
|---------|-------------------|
| `recepcion/` | Hub mostrador: idle, hover, estados de módulos |
| `pacientes/archivador/` | Archivador: cerrado, destacado, abierto |
| `citas/agenda/` | Agenda sobre escritorio |
| `exports/` | WebP @1x/@2x, SVG de apoyo, sprites |

## Convención de nombres

```
{modulo}-{estado}@{escala}.webp
```

Ejemplos: `archivador-idle@1x.webp`, `archivador-open@2x.webp`.

## Estados por objeto

- `idle` — reposo
- `focus` — teclado / selección
- `active` — seleccionado
- `open` — animación de apertura (exploración)

Documentar en cada subcarpeta un `NOTES.md` con medidas y puntos de anclaje para hotspots.

## Integración

Tras aprobar diseños, copiar optimizados a:

`static/atlas-interactive/assets/<modulo>/`

Y registrar en `static/atlas-interactive/catalog.json`.
