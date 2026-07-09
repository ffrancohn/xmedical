@echo off
setlocal EnableDelayedExpansion

cd /d "%~dp0"
set "ROOT_DIR=%~dp0"

echo ========================================
echo XMedical - Inicio del sistema
echo ========================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo Python no esta instalado o no esta en el PATH.
    exit /b 1
)

REM Crear entorno virtual si no existe
if not exist "%ROOT_DIR%venv\Scripts\python.exe" (
    echo Creando entorno virtual...
    python -m venv "%ROOT_DIR%venv"
    if errorlevel 1 (
        echo Error al crear el entorno virtual.
        exit /b 1
    )
)

set "PY=%ROOT_DIR%venv\Scripts\python.exe"
set "PIP=%ROOT_DIR%venv\Scripts\pip.exe"

echo Actualizando pip...
"%PY%" -m pip install --upgrade pip -q
if errorlevel 1 (
    echo Error al actualizar pip.
    exit /b 1
)

echo Instalando dependencias desde requirements.txt...
"%PIP%" install -r "%ROOT_DIR%requirements.txt"
if errorlevel 1 (
    echo Error al instalar dependencias.
    exit /b 1
)

echo.
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

echo Esperando a que PostgreSQL este listo...
ping 127.0.0.1 -n 6 >nul

echo Aplicando migraciones de base de datos...
"%PY%" "%ROOT_DIR%manage.py" migrate --noinput
if errorlevel 1 (
    echo Error al aplicar migraciones. Verifica que PostgreSQL este activo.
    exit /b 1
)

echo Migraciones aplicadas correctamente.
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

echo Iniciando Django...
set "DJANGO_CMD=cd /d "%ROOT_DIR%" && call venv\Scripts\activate.bat && python manage.py runserver 127.0.0.1:!DJANGO_PORT!"
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
echo Si es la primera vez, carga datos demo con:
echo   venv\Scripts\activate
echo   python manage.py loaddata fixtures/initial_data.json
echo.
echo Cierra la ventana "XMedical Django" para detener el servidor web.
echo.

endlocal
