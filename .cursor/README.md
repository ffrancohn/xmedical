# Visual Experience Skills para Cursor

Paquete de cuatro skills personalizadas para seleccionar visualizaciones, crear decks HTML navegables, construir interfaces isométricas SVG y auditar calidad UX/UI.

## Instalación en un proyecto
Copiar la carpeta `.cursor/skills/` de este paquete en la raíz de tu repositorio (fusionar, sin borrar las skills existentes). Cursor detecta las skills automáticamente por sus archivos `SKILL.md`.

## Instalación global
Copiar cada carpeta de `.cursor/skills/` a `~/.cursor/skills/` (no reemplazar tus skills existentes).

## Uso en Cursor Agent
- `Diseña una visualización para riesgos tecnológicos y justifica si debe ser isométrica. Usa visual-design-architect.`
- `Crea un deck narrativo interactivo sobre una historia con tres decisiones. Usa interactive-deck-studio.`
- `Construye un mapa isométrico clicable de una clínica con panel lateral. Usa isometric-interface-builder.`
- `Audita la UX, rendimiento y accesibilidad del deck existente usando visual-quality-auditor y corrige los fallos.`

Cursor puede decidir cargar las skills según su descripción. Puedes mencionarlas explícitamente si quieres asegurar la selección.

## Demostraciones listas para abrir
- `.cursor/skills/interactive-deck-studio/assets/minimal-deck/index.html`
- `.cursor/skills/isometric-interface-builder/assets/isometric-demo/index.html`

Se pueden abrir directamente en el navegador. No requieren npm ni librerías externas.

## Arquitectura y alcance
Las skills son instrucciones para agentes, no plugins ejecutables ni motores de render autónomos. Los ejemplos HTML son demostraciones independientes. Para usar estas técnicas en React, Vue, Flutter o React Native, el agente debe integrarlas en la arquitectura específica; en Flutter/React Native no se debe asumir que DOM/HTML corre como componente nativo.

## Validación
El archivo `scripts/validate_package.py` revisa existencia de carpetas, metadatos mínimos, nombres y recursos. No sustituye pruebas visuales en navegador ni una validación oficial completa de Agent Skills.

## Estándar de referencia
https://cursor.com/docs/skills
https://agentskills.io/specification
