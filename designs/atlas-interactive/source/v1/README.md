# XMedical Visual Assets 1.0

Paquete de recursos individuales para la interfaz isométrica 2.5D de XMedical.

## Directorios
- `modulos/`: recepción, archivador de pacientes cerrado/abierto, agenda cerrada/abierta, consultorio, historia, medicamentos, laboratorio, administración y sala de espera.
- `avatares/`: personajes genéricos agrupados por niños, adolescentes, adultos jóvenes, adultos y personas mayores.
- `documentos/`: carpetas, receta, resultados, documento y estudios.
- `estados/`: iconos de citas.
- `profesionales/`: médico, enfermera, recepcionista, administrativo.
- `manifest.json`: identificadores, rutas y dimensiones.

## Uso
Estos archivos WebP tienen canal alfa y pueden mostrarse con `<img>` o como sprites. Las variantes abierto/cerrado se pueden intercambiar con CSS/JS; no son modelos 3D.

**Nota de diseño:** recursos recortados y separados de una lámina generativa maestra. Revisar bordes y consistencia antes de uso en producción, especialmente para animaciones de continuidad exacta; se recomienda conservar un rótulo de texto y no usar imágenes como único elemento de navegación. Ningún avatar corresponde a pacientes reales.
