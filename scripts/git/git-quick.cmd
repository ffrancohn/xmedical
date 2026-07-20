@echo off
REM Atajos directos (misma carpeta, cualquier repo).
setlocal
set "SCRIPT_DIR=%~dp0"
set "ACT=%~1"
if "%ACT%"=="" (
    echo Uso: git-quick.cmd [status^|diff^|commit^|fetch^|pull^|push^|sync^|log^|help]
    exit /b 1
)
if not "%~2"=="" (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%git-helper.ps1" -RepoPath "%~2" -Action %ACT%
) else (
    powershell -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%git-helper.ps1" -Action %ACT%
)
endlocal
