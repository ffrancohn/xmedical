# Catálogo CIE-10 (dato de terceros)

Esta carpeta es el destino por defecto de `manage.py import_cie10`. El CSV **no se
versiona** (está en `.gitignore`).

## Origen

`cie-10.csv` de [verasativa/CIE-10](https://github.com/verasativa/CIE-10): listado
jerarquizado de ~14.500 entradas construido a partir de icdcode.info y completado con
el `cie10.xls` de deis.cl (Chile, actualización 2013).

```powershell
Invoke-WebRequest `
  https://raw.githubusercontent.com/verasativa/CIE-10/master/cie-10.csv `
  -OutFile data/cie10/cie-10.csv
```

## Carga

```powershell
python manage.py import_cie10                 # crea/actualiza sin borrar
python manage.py import_cie10 --truncate      # vacía y recarga
python manage.py import_cie10 --csv otra/ruta.csv
```

Es idempotente: sólo escribe lo que cambia e informa de nuevos, actualizados y sin cambios.

## Formato

```
code,code_0,code_1,code_2,code_3,code_4,description,level,source
A00-B99,,,,,,Ciertas enfermedades infecciosas y parasitarias,0,icdcode.info
I10,I00-I99,I10-I15,,,,Hipertensión esencial (primaria),2,icdcode.info
```

- `level` 0 = capítulo, 1 = bloque, 2 = categoría, 3–5 = subcategorías.
- `code_0` = capítulo, `code_1` = bloque.
- Sólo `level >= 2` se marca `es_hoja` y aparece en el buscador.

## Licencia

El repositorio de origen **no declara licencia**. La CIE-10 es de la OMS/OPS; su uso
clínico y docente está permitido, pero antes de redistribuir el archivo conviene
confirmar los términos con la representación OPS/OMS local. Por eso el CSV queda fuera
del control de versiones: cada entorno lo descarga desde el origen.
