# Cursor — reglas y skills (XMedical)

Configuración del agente en este repositorio: **reglas**, **skills** de experiencia visual y scripts de validación.

## Skills del proyecto (`.cursor/skills/`)

| Skill | Cuándo usarla |
|-------|----------------|
| [visual-design-architect](skills/visual-design-architect/SKILL.md) | Elegir tipo de visualización (isometría, grafo, tablas, timeline) **antes** de implementar. |
| [interactive-deck-studio](skills/interactive-deck-studio/SKILL.md) | Decks HTML navegables; alinea con `deck/` y presentaciones del producto. |
| [isometric-interface-builder](skills/isometric-interface-builder/SKILL.md) | Mapas isométricos SVG + panel de detalle; alinea con **modo Atlas**, `deck/prototipo/` y `static/js/iso.js`. |
| [visual-quality-auditor](skills/visual-quality-auditor/SKILL.md) | Auditar UX, accesibilidad, responsive y correcciones tras cambios visuales. |

Cursor carga cada skill por su `SKILL.md` (frontmatter `name` + `description`). Puedes invocarlas en el chat, por ejemplo:

- *«Extiende la interfaz Atlas de recepción; usa **isometric-interface-builder** y audita con **visual-quality-auditor**.»*
- *«¿Debe ser isométrico el dashboard de citas? Usa **visual-design-architect**.»*
- *«Mejora el deck en `deck/` con **interactive-deck-studio**.»*

### Demos en el navegador (sin npm)

- `skills/interactive-deck-studio/assets/minimal-deck/index.html`
- `skills/isometric-interface-builder/assets/isometric-demo/index.html`

### Validación

Desde la raíz del repo:

```bash
python3 .cursor/scripts/validate_package.py
```

Comprueba las cuatro skills, frontmatter y rutas. No sustituye prueba manual en navegador.

## Reglas (`.cursor/rules/`)

| Regla | Alcance |
|-------|---------|
| [graphify.mdc](rules/graphify.mdc) | Grafo de código: usar `graphify query` cuando la CLI esté instalada; ver `graphify-out/GRAPH_REPORT.md`. |

## Atlas isométrico en la app Django

- Modo usuario: **Preferencias** → **Atlas** (`UserPreference.interface_mode`).
- Código: `static/js/iso.js`, `static/css/atlas.css`, `apps/core/atlas_ui.py`.
- Prototipo estático: `deck/prototipo/`.
- Despliegue: [docs/18 Interfaz Atlas Despliegue Produccion.md](../docs/18%20Interfaz%20Atlas%20Despliegue%20Produccion.md).

Para nuevas pantallas isométricas en Django, combinar **isometric-interface-builder** (diseño) con el motor existente `iso.js` (no reescribir desde cero salvo necesidad).

## Instalación en otro clone

Las skills ya viven en `.cursor/skills/` en git; basta con clonar el repo. Para copiar solo skills a otro proyecto, fusiona esa carpeta sin borrar skills ajenas.

Instalación global opcional: copiar cada carpeta de `skills/` a `~/.cursor/skills/`.

## Referencias

- [Cursor Skills](https://cursor.com/docs/skills)
- [Agent Skills specification](https://agentskills.io/specification)
- [AGENTS.md](../AGENTS.md) — entorno cloud y cuándo leer cada skill
