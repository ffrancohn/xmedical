@echo off
set "OTHER=C:\py\delivery"

mkdir "%OTHER%\.cursor\skills" 2>nul
mkdir "%OTHER%\.cursor\scripts" 2>nul

xcopy ".cursor\skills\*" "%OTHER%\.cursor\skills\" /E /I /Y

copy /Y ".cursor\scripts\validate_package.py" "%OTHER%\.cursor\scripts\"

echo Proceso finalizado.