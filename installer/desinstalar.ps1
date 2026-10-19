# TranscribeNext - Desinstalador
$installDir = Join-Path $env:LOCALAPPDATA "Programs\TranscribeNext"
$desktop = [Environment]::GetFolderPath([Environment+SpecialFolder]::Desktop)
$programs = [Environment]::GetFolderPath([Environment+SpecialFolder]::Programs)

$lnkDesktop = Join-Path $desktop "TranscribeNext.lnk"
$lnkProg = Join-Path $programs "TranscribeNext.lnk"

if (Test-Path $lnkDesktop) { Remove-Item $lnkDesktop -Force }
if (Test-Path $lnkProg) { Remove-Item $lnkProg -Force }

if (Test-Path $installDir) {
    Remove-Item $installDir -Recurse -Force
}

try {
    Add-Type -AssemblyName System.Windows.Forms
    [System.Windows.Forms.MessageBox]::Show(
        "TranscribeNext ha sido desinstalado correctamente de tu computadora.",
        "Desinstalación Completa",
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Information
    ) | Out-Null
} catch {}
