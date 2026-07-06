# Carpeta de evidencia — XMedical

Cada ejecución de `./scripts/run_all_verifications.sh` crea una subcarpeta con **todos** los resultados:

```
docs/informes/evidencia/2026-07-06_143022/
├── LEEME.txt                  ← índice de archivos
├── INFORME.md                 ← resumen consolidado (empezar aquí)
├── 00-ejecucion.log
├── 01-infraestructura.txt     ← INF-*
├── 02-ssl.txt                 ← SSL-*
├── 03-humo-http.txt           ← SMK-*
├── 04-django-check.txt
├── 05-django-deploy-check.txt
├── 06-django-tests.txt        ← suite completa
├── 07-cobertura-report.txt
└── 07-cobertura-html/         ← cobertura en navegador (index.html)
```

## Última ejecución

Ver ruta en [`ULTIMA.txt`](ULTIMA.txt).

## Generar evidencia

```bash
cd /var/www/xmedical
./scripts/run_all_verifications.sh
```

Al terminar, la ruta de la carpeta se imprime en consola.

## Resumen por fecha

También se actualiza: [`../INFORME-VERIFICACION-YYYY-MM-DD.md`](../INFORME-VERIFICACION-2026-07-06.md) (enlace al informe del día).

## Cron semanal

```cron
0 6 * * 1  /var/www/xmedical/scripts/run_all_verifications.sh >> /var/log/xmedical/weekly-verify.log 2>&1
```
