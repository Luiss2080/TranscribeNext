# TranscribeNext - Instalador para Windows
# Instala la aplicacion permanentemente en el equipo del usuario

$ErrorActionPreference = "Stop"

try {
    Add-Type -AssemblyName System.Windows.Forms
} catch {}

$repoDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
$installDir = Join-Path $env:LOCALAPPDATA "Programs\TranscribeNext"

Write-Host "Instalando TranscribeNext en tu computadora..." -ForegroundColor Cyan
Write-Host "Directorio destino: $installDir" -ForegroundColor Gray

# 1. Crear carpeta destino limpia
if (-not (Test-Path $installDir)) {
    New-Item -ItemType Directory -Path $installDir -Force | Out-Null
}

# 2. Copiar archivos del programa
$compiledDir = Join-Path $repoDir "dist\Transcriptor"
if (Test-Path (Join-Path $compiledDir "Transcriptor.exe")) {
    Write-Host "Copiando binarios y modelos compilados..." -ForegroundColor Cyan
    Copy-Item -Path "$compiledDir\*" -Destination $installDir -Recurse -Force
} else {
    Write-Host "Copiando codigo fuente y dependencias..." -ForegroundColor Cyan
    $filesToCopy = @("app.pyw", "transcribir.py", "requirements.txt", "icono.ico", "logo.png")
    foreach ($f in $filesToCopy) {
        $src = Join-Path $repoDir $f
        if (Test-Path $src) {
            Copy-Item -Path $src -Destination $installDir -Force
        }
    }
    # Copiar modelos si existen
    $modelosSrc = Join-Path $repoDir "modelos"
    if (Test-Path $modelosSrc) {
        Copy-Item -Path $modelosSrc -Destination $installDir -Recurse -Force
    }
}

# Copiar icono para accesos directos
$iconSrc = Join-Path $repoDir "icono.ico"
$iconDest = Join-Path $installDir "icono.ico"
if (Test-Path $iconSrc) {
    Copy-Item -Path $iconSrc -Destination $iconDest -Force
}

# 3. Determinar ejecutable principal
$targetExe = Join-Path $installDir "Transcriptor.exe"
if (-not (Test-Path $targetExe)) {
    $targetExe = Join-Path $installDir "app.pyw"
}

# 4. Crear accesos directos (Escritorio y Menu Inicio)
$ws = New-Object -ComObject WScript.Shell

$desktop = [Environment]::GetFolderPath([Environment+SpecialFolder]::Desktop)
$scDesktop = $ws.CreateShortcut((Join-Path $desktop "TranscribeNext.lnk"))
$scDesktop.TargetPath = $targetExe
$scDesktop.WorkingDirectory = $installDir
$scDesktop.Description = "TranscribeNext - Transcriptor inteligente de audios con IA local"
if (Test-Path $iconDest) {
    $scDesktop.IconLocation = "$iconDest,0"
}
$scDesktop.Save()

$programs = [Environment]::GetFolderPath([Environment+SpecialFolder]::Programs)
$scProg = $ws.CreateShortcut((Join-Path $programs "TranscribeNext.lnk"))
$scProg.TargetPath = $targetExe
$scProg.WorkingDirectory = $installDir
$scProg.Description = "TranscribeNext - Transcriptor inteligente de audios con IA local"
if (Test-Path $iconDest) {
    $scProg.IconLocation = "$iconDest,0"
}
$scProg.Save()

# 5. Crear script de desinstalacion
$uninstallScript = @"
@echo off
setlocal
echo Desinstalando TranscribeNext...
del "%USERPROFILE%\Desktop\TranscribeNext.lnk" 2>nul
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\TranscribeNext.lnk" 2>nul
cd /d "%LOCALAPPDATA%\Programs"
rmdir /s /q "TranscribeNext" 2>nul
echo TranscribeNext ha sido desinstalado.
pause
"@
[System.IO.File]::WriteAllText((Join-Path $installDir "desinstalar.bat"), $uninstallScript, [System.Text.Encoding]::ASCII)

Write-Host "Instalacion completada con exito." -ForegroundColor Green

# 6. Mostrar mensaje amigable al usuario
try {
    [System.Windows.Forms.MessageBox]::Show(
        "¡TranscribeNext se ha instalado correctamente en tu computadora!`n`nA partir de ahora puedes abrirlo en cualquier momento desde el acceso directo en tu Escritorio o desde el Menú Inicio.",
        "TranscribeNext - Instalación Exitosa",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Information
    ) | Out-Null
} catch {}

# 7. Iniciar la aplicacion instalada
Start-Process -FilePath $targetExe -WorkingDirectory $installDir
