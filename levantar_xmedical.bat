@echo off
setlocal EnableDelayedExpansion

cd /d "%~dp0"

echo Iniciando servicios Docker de XMedical...
docker compose up -d db redis
if errorlevel 1 (
    echo Error al iniciar servicios Docker.
    exit /b 1
)

echo.
echo Servicios Docker iniciados.
echo PostgreSQL: localhost:5432
echo Redis: localhost:6379
echo.

REM Buscar el primer puerto libre para Django (8000-8099)
set START_PORT=8000
set MAX_PORT=8099
set DJANGO_PORT=

for /L %%P in (%START_PORT%,1,%MAX_PORT%) do (
    if "!DJANGO_PORT!"=="" (
        netstat -ano | findstr /R /C:":%%P " | findstr LISTENING >nul 2>&1
        if errorlevel 1 set DJANGO_PORT=%%P
    )
)

if "!DJANGO_PORT!"=="" (
    echo No hay puerto libre entre %START_PORT% y %MAX_PORT% para Django.
    exit /b 1
)

if not "!DJANGO_PORT!"=="%START_PORT%" (
    echo Puerto %START_PORT% ocupado. Django usara el puerto !DJANGO_PORT!.
) else (
    echo Puerto Django: !DJANGO_PORT!
)
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo Python no esta instalado o no esta en el PATH.
    exit /b 1
)

echo Esperando a que PostgreSQL este listo...
ping 127.0.0.1 -n 4 >nul

set "ROOT_DIR=%~dp0"
if exist "%ROOT_DIR%venv\Scripts\activate.bat" (
    set "DJANGO_CMD=cd /d "%ROOT_DIR%" && call venv\Scripts\activate.bat && python manage.py runserver 127.0.0.1:!DJANGO_PORT!"
) else (
    echo Aviso: entorno virtual no encontrado, usando Python del sistema.
    set "DJANGO_CMD=cd /d "%ROOT_DIR%" && python manage.py runserver 127.0.0.1:!DJANGO_PORT!"
)

echo Iniciando Django...
start "XMedical Django" cmd /k "!DJANGO_CMD!"

echo.
echo ========================================
echo XMedical listo
echo ========================================
echo PostgreSQL: localhost:5432
echo Redis:      localhost:6379
echo Django:     http://127.0.0.1:!DJANGO_PORT!/
echo Login:      http://127.0.0.1:!DJANGO_PORT!/auth/login/
echo.
echo Cierra la ventana "XMedical Django" para detener el servidor web.
echo.

endlocal
