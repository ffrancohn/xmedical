@echo off
setlocal

cd /d "%~dp0"

echo Iniciando servicios Docker de XMedical...
docker compose up -d db redis

echo.
echo Servicios iniciados.
echo PostgreSQL: localhost:5432
echo Redis: localhost:6379
echo.
echo Para iniciar Django localmente:
echo   venv\Scripts\activate
echo   python manage.py runserver

endlocal
