@echo off
chcp 65001 >nul
title TranscribeNext - Instalador de Acceso Directo

echo ======================================================================
echo                INSTALADOR DE ACCESO DIRECTO - TRANSCRIBENEXT
echo ======================================================================
echo.
echo Creando acceso directo en tu Escritorio y Menú Inicio...
echo.

set "CARPETA=%~dp0"
set "CARPETA=%CARPETA:~0,-1%"

:: Buscar si existe el ejecutable compilado o el script de Python
set "TARGET=%CARPETA%\Transcriptor.exe"
if not exist "%TARGET%" (
    set "TARGET=%CARPETA%\app.pyw"
)

set "ICONO=%CARPETA%\icono.ico"
if not exist "%ICONO%" (
    set "ICONO=%TARGET%"
)

:: Usar PowerShell para crear los accesos directos de forma 100% nativa y segura
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$ws = New-Object -ComObject WScript.Shell;" ^
    "$desktop = [Environment]::GetFolderPath('Desktop');" ^
    "$scDesktop = $ws.CreateShortcut((Join-Path $desktop 'TranscribeNext.lnk'));" ^
    "$scDesktop.TargetPath = '%TARGET%';" ^
    "$scDesktop.WorkingDirectory = '%CARPETA%';" ^
    "$scDesktop.Description = 'TranscribeNext - Transcriptor inteligente de audios con IA local';" ^
    "$scDesktop.IconLocation = '%ICONO%,0';" ^
    "$scDesktop.Save();" ^
    "$programs = [Environment]::GetFolderPath('Programs');" ^
    "$scProg = $ws.CreateShortcut((Join-Path $programs 'TranscribeNext.lnk'));" ^
    "$scProg.TargetPath = '%TARGET%';" ^
    "$scProg.WorkingDirectory = '%CARPETA%';" ^
    "$scProg.Description = 'TranscribeNext - Transcriptor inteligente de audios con IA local';" ^
    "$scProg.IconLocation = '%ICONO%,0';" ^
    "$scProg.Save();"

echo ----------------------------------------------------------------------
echo  [LISTO] ¡Acceso directo creado correctamente en tu Escritorio!
echo ----------------------------------------------------------------------
echo.
echo Ya no necesitas buscar en esta carpeta. A partir de ahora puedes abrir
echo TranscribeNext directamente desde el icono en tu Escritorio o Menú Inicio.
echo.
echo Presiona cualquier tecla para abrir TranscribeNext ahora mismo...
pause >nul
start "" "%TARGET%"
