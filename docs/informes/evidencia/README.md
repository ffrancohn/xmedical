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
├── 07-cobertura-html/         ← cobertura en navegador (index.html)
├── 08-seguridad-estatica.txt  ← SEC-S* (bandit, pip-audit)
├── 09-seguridad-headers.txt   ← SEC-08* (headers prod)
├── 11-django-security-tests.txt ← SEC-* Django
└── 10-seguridad-zap.html      ← ZAP mensual (verify_security_zap.sh)
```

## Warnings aceptados

- **W008:** `SECURE_SSL_REDIRECT=False` — Apache redirige HTTP→HTTPS.
- **W021:** `SECURE_HSTS_PRELOAD=False` — preload opcional.
- **SEC-06:** rate limiting pendiente (API futura).

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

## Cron mensual (ZAP)

```cron
0 3 1 * *  /var/www/xmedical/scripts/verify_security_zap.sh >> /var/log/xmedical/zap-scan.log 2>&1
```
