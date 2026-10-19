# Script de instalación de acceso directo para TranscribeNext
$ErrorActionPreference = "SilentlyContinue"

$carpeta = Split-Path -Parent $MyInvocation.MyCommand.Definition
$targetExe = Join-Path $carpeta "Transcriptor.exe"
if (-not (Test-Path $targetExe)) {
    $targetExe = Join-Path $carpeta "app.pyw"
}

$icono = Join-Path $carpeta "icono.ico"
if (-not (Test-Path $icono)) {
    $icono = $targetExe
}

$ws = New-Object -ComObject WScript.Shell

# 1. Acceso directo en el Escritorio
$desktopPath = [Environment]::GetFolderPath([Environment+SpecialFolder]::Desktop)
$shortcutDesktop = $ws.CreateShortcut((Join-Path $desktopPath "TranscribeNext.lnk"))
$shortcutDesktop.TargetPath = $targetExe
$shortcutDesktop.WorkingDirectory = $carpeta
$shortcutDesktop.Description = "TranscribeNext - Transcriptor inteligente de audios con IA local"
$shortcutDesktop.IconLocation = "$icono,0"
$shortcutDesktop.Save()

# 2. Acceso directo en el Menú Inicio (Programas)
$programsPath = [Environment]::GetFolderPath([Environment+SpecialFolder]::Programs)
$shortcutProg = $ws.CreateShortcut((Join-Path $programsPath "TranscribeNext.lnk"))
$shortcutProg.TargetPath = $targetExe
$shortcutProg.WorkingDirectory = $carpeta
$shortcutProg.Description = "TranscribeNext - Transcriptor inteligente de audios con IA local"
$shortcutProg.IconLocation = "$icono,0"
$shortcutProg.Save()

Write-Host "OK"
