# Checklist de auditoría

| Área | Criterios |
|---|---|
| Claridad | Objetivo de pantalla evidente; jerarquía visual; contenido comprensible |
| Consistencia | Tokens; espaciamiento; tipografía; iconografía; patrones de botones |
| Accesibilidad | Navegación teclado; foco visible; nombres accesibles; contraste; etiquetas; no solo color |
| Móvil | Viewports pequeños; zoom; scroll; targets táctiles; ausencia de hover obligatorio |
| Estados | Carga, vacío, error, éxito, deshabilitado y selección |
| Deck | Avance/retroceso, orientación, progreso, foco, scroll, salto a escenas, reduced motion |
| SVG/isometría | viewBox, semántica, orden de capas, alternativa textual, pan/zoom sin bloqueo |
| Rendimiento | Tamaño de imágenes; lazy load; animaciones; scroll listeners; DOM excesivo |
| Seguridad | No exponer tokens; escape de contenido; dependencias justificadas; enlaces seguros |
| Integración | Componentes reutilizables; estilos acotados; embebido responsive; rutas relativas |

## Clasificación
Bloqueante: impide completar la tarea. Alto: rompe funciones clave o acceso. Medio: perjudica significativamente experiencia. Bajo: mejora puntual. Priorizar evidencia y reproducibilidad.

## Verificación
Registrar las pruebas realmente ejecutadas (nombre, comando, resultado), la revisión manual y las limitaciones. Probar anchos de móvil/escritorio y reduced motion cuando el entorno lo permita.
