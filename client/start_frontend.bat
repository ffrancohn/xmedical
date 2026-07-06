@echo off
echo 🚀 Iniciando Frontend XMedical...
echo.

REM Verificar que Node.js esté instalado
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js no está instalado
    echo 🔧 Instala Node.js desde: https://nodejs.org/
    pause
    exit /b 1
)

REM Verificar que npm esté instalado
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm no está instalado
    pause
    exit /b 1
)

REM Verificar que las dependencias estén instaladas
if not exist "node_modules" (
    echo 📦 Instalando dependencias...
    npm install
    if errorlevel 1 (
        echo ❌ Error al instalar dependencias
        pause
        exit /b 1
    )
)

REM Copiar archivo de configuración si no existe
if not exist ".env.local" (
    echo 📋 Copiando configuración...
    copy env.local .env.local >nul 2>&1
)

echo ✅ Dependencias verificadas
echo.
echo 🎯 Configuración del frontend:
echo    URL: http://localhost:3000
echo    Backend: http://localhost:8000
echo    Modo: Desarrollo
echo.
echo 🚀 Iniciando servidor de desarrollo...
echo    Presiona Ctrl+C para detener
echo.

REM Iniciar servidor de desarrollo
npm run dev 