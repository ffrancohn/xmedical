# Informes de verificación

Los informes automáticos se generan con:

```bash
./scripts/run_all_verifications.sh
```

Salida: `INFORME-VERIFICACION-YYYY-MM-DD.md` en esta carpeta.

## Cron sugerido (servidor)

```cron
0 6 * * 1  /var/www/xmedical/scripts/run_all_verifications.sh >> /var/log/xmedical/weekly-verify.log 2>&1
```

Instalar en crontab del usuario que ejecuta el servicio (p. ej. root o deploy).

## Secciones del informe

1. Resumen ejecutivo (PASS/FAIL)
2. Infraestructura (INF-*)
3. SSL (SSL-*)
4. Humo HTTP (SMK-*)
5. Tests Django
6. Deploy check
7. Comandos para reproducir
8. Incidencias abiertas

Ver también: [`INFORME-VERIFICACION-2026-07-06.md`](../INFORME-VERIFICACION-2026-07-06.md) (informe manual inicial).
