@echo off
setlocal

cd /d "%~dp0"

echo Reiniciando servicios Docker de XMedical...
docker compose down
docker compose up -d db redis

echo.
echo Servicios reiniciados. Los datos se conservan.

endlocal
