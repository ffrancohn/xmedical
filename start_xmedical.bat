@echo off
title XMedical - Sistema de Gestion Clinica
color 0A

echo.
echo ================================================================
echo                    XMEDICAL - Django
echo              Sistema de Gestion Clinica Multi-tenant
echo ================================================================
echo.

cd /d "%~dp0"

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no esta instalado
    echo Instala Python 3.11+ desde https://python.org/
    pause
    exit /b 1
)

REM Verificar Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker no esta instalado
    echo Instala Docker Desktop desde https://docker.com/
    pause
    exit /b 1
)

echo [1/4] Levantando PostgreSQL y Redis...
docker compose up -d db redis
if errorlevel 1 (
    echo [ERROR] No se pudieron iniciar los servicios Docker
    pause
    exit /b 1
)

echo.
echo [2/4] Activando entorno virtual...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo Creando entorno virtual...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
)

echo.
echo [3/4] Aplicando migraciones y cargando datos de prueba...
python manage.py migrate
python manage.py loaddata fixtures/initial_data.json

echo.
echo [4/4] Iniciando servidor Django...
echo.
echo   URL:      http://localhost:8000
echo   Login:    http://localhost:8000/auth/login/
echo   Usuarios: ver USUARIOS_PRUEBA.md
echo.

start "XMedical Django" cmd /k "cd /d %~dp0 && venv\Scripts\activate.bat && python manage.py runserver"

echo.
echo ================================================================
echo                    SISTEMA INICIADO
echo ================================================================
echo.
echo Para detener: cierra la ventana de Django y ejecuta bajar_xmedical.bat
echo.
pause
