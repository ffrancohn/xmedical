---
name: visual-quality-auditor
description: Audita y mejora la calidad visual y técnica de aplicaciones, decks HTML, SVG e interfaces isométricas. Úsala para revisar UX, accesibilidad, responsive, rendimiento, animación, navegación y mantenimiento; corrige fallos demostrables y verifica resultados.
---
# Visual Quality Auditor

## Auditoría basada en evidencia
1. Inspecciona código, stack, diseño existente y objetivos del usuario. No reemplaces componentes buenos para imponer gustos.
2. Usa `references/audit-checklist.md` para verificar jerarquía, contraste, tipografía, espaciado, consistencia, densidad, controles táctiles, teclado, semántica, estados y responsive.
3. Revisa navegación de decks (progreso, avance, retroceso, scroll, foco y movimiento reducido) e interacciones SVG/isométricas (selección, hit target, equivalente textual, panel de detalle).
4. Mide o comprueba lo que puedas en entorno disponible. No afirmar que ejecutaste pruebas reales si no tienes navegador/test runner. Diferencia verificado, inspeccionado y pendiente.
5. Prioriza hallazgos por gravedad: bloqueo, alto, medio, bajo. Explica impacto y archivo/línea relevante.
6. Si se solicitan correcciones, aplica cambios mínimos, mantiene el diseño funcional y agrega pruebas apropiadas.
7. Entrega resumen antes/después, cambios y pruebas realizadas/pendientes.

## No hacer
No añadir bibliotecas para resolver detalles simples; no sustituir contrastes accesibles por estética; no convertir todas las pantallas a cards; no incluir animación decorativa sin considerar rendimiento y reduced motion; no ocultar problemas móviles detrás de hover.

## Resultado
Matriz de hallazgos, recomendaciones concretas, correcciones y validación documentada. Revisar `assets/audit-report.template.md`.
