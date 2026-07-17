@echo off
setlocal
where uv >nul 2>&1
if errorlevel 1 (
  echo.
  echo [ERROR] uv no esta instalado.
  echo.
  echo Instale uv en Windows con PowerShell:
  echo   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  echo.
  echo O con pip: pip install uv
  echo Luego cierre y vuelva a abrir la terminal.
  echo.
  exit /b 1
)
exit /b 0
