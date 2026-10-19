@echo off
setlocal
title Desinstalador de TranscribeNext
cd /d "%~dp0"

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0installer\desinstalar.ps1"
exit /b 0
