@echo off
REM Atajo: commit interactivo con descripción.
setlocal
set "SCRIPT_DIR=%~dp0"
if "%~1"=="" (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%git-helper.ps1" -Action commit
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%git-helper.ps1" -RepoPath "%~1" -Action commit
)
endlocal
