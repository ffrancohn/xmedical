@echo off
title XMedical - Sistema de Asistencia Médica Inteligente
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    XMEDICAL SYSTEM                          ║
echo ║              Sistema de Asistencia Médica Inteligente       ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🚀 Iniciando sistema XMedical...
echo.

REM Verificar que Python esté instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado
    echo 🔧 Instala Python desde: https://python.org/
    pause
    exit /b 1
)

REM Verificar que Node.js esté instalado
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js no está instalado
    echo 🔧 Instala Node.js desde: https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Dependencias básicas verificadas
echo.

REM Verificar PostgreSQL
echo 🔍 Verificando PostgreSQL...
echo    Asegúrate de que PostgreSQL esté instalado y ejecutándose
echo    en el puerto 5432
echo.

REM Iniciar backend
echo 🖥️  Iniciando Backend...
echo.
cd server

REM Activar entorno virtual
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✅ Entorno virtual activado
) else (
    echo ❌ Entorno virtual no encontrado
    echo 🔧 Ejecuta: python -m venv venv
    pause
    exit /b 1
)

REM Verificar base de datos
echo 🔍 Verificando base de datos...
python test_db.py
if errorlevel 1 (
    echo.
    echo ⚠️  Problemas con la base de datos
    echo 🔧 Verifica que PostgreSQL esté ejecutándose
    echo 🔧 Verifica las credenciales en config.env
    echo.
    pause
)

REM Inicializar base de datos si es necesario
echo 🔍 Inicializando base de datos...
python init_db.py

echo.
echo 🚀 Iniciando servidor backend...
echo    Puerto: 8000
echo    Documentación: http://localhost:8000/docs
echo.

REM Iniciar servidor backend en segundo plano
start "XMedical Backend" cmd /k "venv\Scripts\activate.bat && python start_server.py"

REM Esperar un momento para que el backend inicie
timeout /t 5 /nobreak >nul

REM Volver al directorio raíz
cd ..

REM Iniciar frontend
echo 🌐 Iniciando Frontend...
echo    Puerto: 3000
echo    URL: http://localhost:3000
echo.

REM Iniciar frontend en segundo plano
start "XMedical Frontend" cmd /k "cd client && npm run dev"

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    SISTEMA INICIADO                         ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo 🎯 URLs del sistema:
echo    Frontend: http://localhost:3000
echo    Backend:  http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
echo 📋 Credenciales por defecto:
echo    Usuario: admin
echo    Contraseña: admin123
echo.
echo ⚠️  IMPORTANTE: Cambia la contraseña del administrador
echo.
echo 🛑 Para detener el sistema, cierra las ventanas de comandos
echo.
pause 