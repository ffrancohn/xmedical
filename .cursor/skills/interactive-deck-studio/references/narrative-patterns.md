# Patrones narrativos

## Paginado
Para exposiciones y clases con momentos discretos. Teclas, botones, contador y foco al cambiar de escena.

## Scroll narrativo
Para relatos cronológicos, investigaciones y formación inmersiva. Escenas desarrolladas gradualmente; indicador de avance; contenido visible si JS falla.

## Guiado con elección
Para escenarios educativos con decisiones y consecuencias. Modelar estados, volver atrás, rutas alternativas y resumen.

## Híbrido
Secciones con scroll y escenas con opciones. Evitar bloquear scroll sin alternativa táctil y de teclado.

## Contrato de escena
`id`, `heading`, `objective`, `narrative`, `media`, `visualizationType`, `interaction`, `transition`, `accessibilityLabel`, `sources`.

## Narrativa
Apertura con contexto, tensión, sucesión causal, puntos de decisión, conclusión y transferencia al usuario. En contenido histórico, separar hechos documentados de dramatización.

## SVG / medios
Usar `viewBox`, `<title>` o descripciones accesibles cuando aportan significado, elementos interactivos con controles HTML, rutas relativas, créditos/licencias de recursos y fallback cuando la imagen falle. No atribuir imágenes generadas a hechos reales.
