@echo off
chcp 65001 >nul
set "CARPETA=%~dp0"
set "CARPETA=%CARPETA:~0,-1%"

if exist "%CARPETA%\Transcriptor.exe" (
    start "" "%CARPETA%\Transcriptor.exe" %*
) else (
    if exist "%CARPETA%\.venv\Scripts\pythonw.exe" (
        start "" "%CARPETA%\.venv\Scripts\pythonw.exe" "%CARPETA%\app.pyw" %*
    ) else (
        start "" pythonw "%CARPETA%\app.pyw" %*
    )
)
exit
