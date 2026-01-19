# DPIA Generator - Instalare automată Windows
# Rulare: Click dreapta pe fișier -> Run with PowerShell
# SAU: powershell -ExecutionPolicy Bypass -File INSTALL_WINDOWS.ps1

Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   DPIA GENERATOR - INSTALARE PE WINDOWS                  " -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Verifică dacă Python este instalat
Write-Host "Verificare Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python găsit: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python NU este instalat!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Te rog instalează Python 3.10+ de la: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "IMPORTANT: Bifează opțiunea 'Add Python to PATH' la instalare!" -ForegroundColor Yellow
    Read-Host "Apasă Enter pentru a ieși"
    exit 1
}

# Verifică versiune Python (trebuie 3.10+)
$versionString = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
$version = [double]$versionString
if ($version -lt 3.10) {
    Write-Host "✗ Versiune Python prea veche: $versionString (necesar: 3.10+)" -ForegroundColor Red
    Read-Host "Apasă Enter pentru a ieși"
    exit 1
}

# Creează directorul C:\Claude dacă nu există
$targetDir = "C:\Claude\dpia-generator"
Write-Host ""
Write-Host "Creare director: $targetDir" -ForegroundColor Yellow

if (Test-Path $targetDir) {
    $response = Read-Host "Directorul $targetDir există deja. Ștergi și recreezi? (DA/NU)"
    if ($response -eq "DA" -or $response -eq "D") {
        Remove-Item -Path $targetDir -Recurse -Force
        Write-Host "✓ Director șters" -ForegroundColor Green
    } else {
        Write-Host "Instalare anulată." -ForegroundColor Yellow
        Read-Host "Apasă Enter pentru a ieși"
        exit 0
    }
}

New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
Write-Host "✓ Director creat: $targetDir" -ForegroundColor Green

# Copiază fișierele (presupune că scriptul este în același folder cu dpia-generator/)
$sourceDir = Join-Path $PSScriptRoot "dpia-generator"

if (-not (Test-Path $sourceDir)) {
    Write-Host "✗ Nu găsesc folderul dpia-generator în directorul curent!" -ForegroundColor Red
    Write-Host "Script location: $PSScriptRoot" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Verifică că fișierul INSTALL_WINDOWS.ps1 este în același folder cu dpia-generator/" -ForegroundColor Yellow
    Read-Host "Apasă Enter pentru a ieși"
    exit 1
}

Write-Host ""
Write-Host "Copiere fișiere..." -ForegroundColor Yellow
Copy-Item -Path "$sourceDir\*" -Destination $targetDir -Recurse -Force
Write-Host "✓ Fișiere copiate" -ForegroundColor Green

# Navighează în director
Set-Location $targetDir

# Creează virtual environment
Write-Host ""
Write-Host "Creare Python virtual environment..." -ForegroundColor Yellow
python -m venv venv
Write-Host "✓ Virtual environment creat" -ForegroundColor Green

# Activează virtual environment și instalează dependințe
Write-Host ""
Write-Host "Instalare dependințe Python..." -ForegroundColor Yellow
& ".\venv\Scripts\python.exe" -m pip install --upgrade pip | Out-Null
& ".\venv\Scripts\python.exe" -m pip install -r requirements.txt

Write-Host "✓ Dependințe instalate" -ForegroundColor Green

# Creează script de rulare rapidă
$runScript = @"
@echo off
echo ═══════════════════════════════════════════════════════════
echo    DPIA GENERATOR - START
echo ═══════════════════════════════════════════════════════════
echo.
cd /d C:\Claude\dpia-generator
call venv\Scripts\activate.bat
python -m src.main
pause
"@

Set-Content -Path "RUN_DPIA_GENERATOR.bat" -Value $runScript
Write-Host "✓ Script de rulare creat: RUN_DPIA_GENERATOR.bat" -ForegroundColor Green

# Creează desktop shortcut (opțional)
$response = Read-Host "`nCreezi shortcut pe Desktop? (DA/NU)"
if ($response -eq "DA" -or $response -eq "D") {
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\DPIA Generator.lnk")
    $Shortcut.TargetPath = "$targetDir\RUN_DPIA_GENERATOR.bat"
    $Shortcut.WorkingDirectory = $targetDir
    $Shortcut.IconLocation = "shell32.dll,70"  # Document icon
    $Shortcut.Description = "DPIA Generator - Sistem generare DPIA conform GDPR"
    $Shortcut.Save()
    Write-Host "✓ Shortcut creat pe Desktop" -ForegroundColor Green
}

# Finalizare
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host "   ✓ INSTALARE COMPLETĂ CU SUCCES!                       " -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
Write-Host ""
Write-Host "Locație instalare: $targetDir" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pentru a rula aplicația:" -ForegroundColor Yellow
Write-Host "  1. Dublu-click pe 'RUN_DPIA_GENERATOR.bat'" -ForegroundColor White
Write-Host "  SAU" -ForegroundColor Yellow
Write-Host "  2. Shortcut de pe Desktop (dacă l-ai creat)" -ForegroundColor White
Write-Host "  SAU" -ForegroundColor Yellow
Write-Host "  3. Manual:" -ForegroundColor White
Write-Host "     cd C:\Claude\dpia-generator" -ForegroundColor Gray
Write-Host "     venv\Scripts\activate" -ForegroundColor Gray
Write-Host "     python -m src.main" -ForegroundColor Gray
Write-Host ""
Write-Host "Documentație completă: C:\Claude\dpia-generator\README.md" -ForegroundColor Cyan
Write-Host ""

# Întreabă dacă vrea să ruleze acum
$response = Read-Host "Dorești să rulezi DPIA Generator ACUM? (DA/NU)"
if ($response -eq "DA" -or $response -eq "D") {
    Write-Host ""
    Write-Host "Pornire DPIA Generator..." -ForegroundColor Green
    Write-Host ""
    Start-Sleep -Seconds 2
    & ".\venv\Scripts\python.exe" -m src.main
} else {
    Write-Host ""
    Write-Host "Instalare finalizată. La revedere!" -ForegroundColor Green
    Read-Host "`nApasă Enter pentru a ieși"
}
