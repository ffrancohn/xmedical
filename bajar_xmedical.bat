@echo off
setlocal

cd /d "%~dp0"

echo Deteniendo servicios Docker de XMedical...
docker compose down

echo.
echo Servicios detenidos.
echo Los datos de PostgreSQL NO se eliminan porque se conserva el volumen docker "postgres_data".
echo No uses "docker compose down -v" salvo que quieras borrar la base de datos.

endlocal
