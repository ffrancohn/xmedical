@echo off
chcp 65001 >nul
setlocal EnableExtensions

REM Lanza el asistente Git. Copia esta carpeta scripts\git\ a cualquier sitio.
REM Uso:
REM   git-helper.cmd                  (desde la raíz de un repo)
REM   git-helper.cmd C:\ruta\al\repo

set "SCRIPT_DIR=%~dp0"
set "PS1=%SCRIPT_DIR%git-helper.ps1"

if not exist "%PS1%" (
    echo No se encuentra git-helper.ps1 en %SCRIPT_DIR%
    exit /b 1
)

if "%~1"=="" (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%PS1%"
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%PS1%" -RepoPath "%~1"
)

endlocal
