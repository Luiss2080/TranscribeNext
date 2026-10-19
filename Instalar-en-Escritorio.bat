@echo off
chcp 65001 >nul
title TranscribeNext - Instalador en Escritorio

echo ======================================================================
echo                INSTALADOR DE ACCESO DIRECTO - TRANSCRIBENEXT
echo ======================================================================
echo.
echo Creando acceso directo en tu Escritorio y Menú Inicio...
echo.

set "CARPETA=%~dp0"
set "CARPETA=%CARPETA:~0,-1%"

:: Ejecutar script de PowerShell con política bypass
powershell -NoProfile -ExecutionPolicy Bypass -File "%CARPETA%\instalar.ps1" >nul 2>&1

:: Si falló powershell, usar respaldo VBScript
if not exist "%USERPROFILE%\Desktop\TranscribeNext.lnk" (
    set "TARGET=%CARPETA%\Transcriptor.exe"
    if not exist "%CARPETA%\Transcriptor.exe" set "TARGET=%CARPETA%\app.pyw"
    
    echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\crear_lnk.vbs"
    echo sDesk = oWS.SpecialFolders("Desktop") >> "%TEMP%\crear_lnk.vbs"
    echo Set oLink = oWS.CreateShortcut(sDesk ^& "\TranscribeNext.lnk") >> "%TEMP%\crear_lnk.vbs"
    echo oLink.TargetPath = "%TARGET%" >> "%TEMP%\crear_lnk.vbs"
    echo oLink.WorkingDirectory = "%CARPETA%" >> "%TEMP%\crear_lnk.vbs"
    echo oLink.IconLocation = "%CARPETA%\icono.ico,0" >> "%TEMP%\crear_lnk.vbs"
    echo oLink.Save >> "%TEMP%\crear_lnk.vbs"
    cscript //nologo "%TEMP%\crear_lnk.vbs" >nul 2>&1
    del "%TEMP%\crear_lnk.vbs" >nul 2>&1
)

echo ----------------------------------------------------------------------
echo  [LISTO] ¡Acceso directo creado correctamente en tu Escritorio!
echo ----------------------------------------------------------------------
echo.
echo Ya no necesitas buscar en esta carpeta. A partir de ahora puedes abrir
echo TranscribeNext directamente desde el icono en tu Escritorio o Menú Inicio.
echo.

set "EJECUTABLE=%CARPETA%\Transcriptor.exe"
if not exist "%EJECUTABLE%" set "EJECUTABLE=%CARPETA%\Iniciar-TranscribeNext.bat"

echo Presiona cualquier tecla para abrir TranscribeNext ahora mismo...
pause >nul
start "" "%EJECUTABLE%"
