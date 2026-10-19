@echo off
setlocal
title Instalador de TranscribeNext
cd /d "%~dp0"

echo =========================================================
echo          INSTALADOR DE TRANSCRIBENEXT
echo =========================================================
echo.
echo Instalando TranscribeNext en tu equipo...
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0installer\instalar.ps1"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Ocurrio un inconveniente al ejecutar el instalador.
    pause
)
exit /b 0
