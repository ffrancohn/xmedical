# Catálogo CIE-10

Esta carpeta contiene el catálogo que carga `manage.py import_cie10`.

| Archivo | Descripción |
|---|---|
| `cie-10.csv` | **Versionado en el repo** (1,43 MB, 14.498 filas). Es la fuente del importador |
| `README.md` | Este documento |

## Origen

`cie-10.csv` de [verasativa/CIE-10](https://github.com/verasativa/CIE-10): listado
jerarquizado de ~14.500 entradas construido a partir de icdcode.info y completado con
el `cie10.xls` de deis.cl (Chile, actualización 2013).

Se versiona para que el despliegue no dependa de descargas ni de pasos manuales: tras
un `git pull`, el catálogo ya está en el servidor y sólo hay que importarlo a la base.

## Carga

```bash
python manage.py import_cie10                 # crea/actualiza sin borrar (ruta por defecto)
python manage.py import_cie10 --truncate      # vacía y recarga
python manage.py import_cie10 --csv otra/ruta.csv
```

Es idempotente: sólo escribe lo que cambia e informa de nuevos, actualizados y sin cambios.
Resultado esperado en una base nueva:

```
CIE-10 importado: 14498 nuevos, 0 actualizados, 0 sin cambios.
Catálogo: 14498 códigos (14268 consultables).
```

Si la tabla está vacía, el buscador del wizard cae al listado MVP de 10 códigos: no se
rompe nada, pero la búsqueda pierde cobertura.

## Formato

```
code,code_0,code_1,code_2,code_3,code_4,description,level,source
A00-B99,,,,,,Ciertas enfermedades infecciosas y parasitarias,0,icdcode.info
I10,I00-I99,I10-I15,,,,Hipertensión esencial (primaria),2,icdcode.info
```

- `level` 0 = capítulo, 1 = bloque, 2 = categoría, 3–5 = subcategorías.
- `code_0` = capítulo, `code_1` = bloque.
- Sólo `level >= 2` se marca `es_hoja` y aparece en el buscador.
- El importador agrega a cada fila un campo `busqueda` normalizado (minúsculas, sin
  tildes) que es el que consulta el autocompletado.

## Actualizar el catálogo

1. Descargar la versión nueva del origen y reemplazar `cie-10.csv`.
2. `python manage.py import_cie10` (sin `--truncate`): actualiza descripciones y
   jerarquía, y da de alta los códigos nuevos.
3. Commit del CSV para que el resto de entornos reciba el cambio.

## Licencia

El repositorio de origen **no declara licencia**. La CIE-10 es de la OMS/OPS; su uso
clínico, docente y de sistemas de información está extendido, pero la redistribución
del archivo conviene confirmarla con la representación OPS/OMS local antes de publicar
el repositorio fuera del ámbito de la institución. Se mantiene la atribución al origen
en este documento.
