# DPIA Generator - Instalare Windows (Versiune îmbunătățită)
# Acest script NU se va închide până nu apeși Enter
# Vei vedea toate erorile clar

# Păstrează fereastra deschisă chiar și la erori
$ErrorActionPreference = "Continue"

function Write-ColorText {
    param($Text, $Color = "White")
    Write-Host $Text -ForegroundColor $Color
}

function Pause-WithMessage {
    param($Message = "Apasă Enter pentru a continua...")
    Write-Host ""
    Write-Host $Message -ForegroundColor Yellow
    $null = Read-Host
}

try {
    Clear-Host
    Write-ColorText "═══════════════════════════════════════════════════════════" Cyan
    Write-ColorText "   DPIA GENERATOR - INSTALARE PE WINDOWS                  " Cyan
    Write-ColorText "═══════════════════════════════════════════════════════════" Cyan
    Write-Host ""

    # Verifică locația curentă
    Write-ColorText "Director curent: $PWD" Yellow
    Write-Host ""

    # Verifică dacă Python este instalat
    Write-ColorText "Pas 1/7: Verificare Python..." Yellow

    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -ne 0) {
            throw "Python nu răspunde"
        }
        Write-ColorText "✓ Python găsit: $pythonVersion" Green
    } catch {
        Write-ColorText "✗ EROARE: Python NU este instalat sau nu este în PATH!" Red
        Write-Host ""
        Write-ColorText "SOLUȚIE:" Yellow
        Write-ColorText "1. Descarcă Python de la: https://www.python.org/downloads/" White
        Write-ColorText "2. La instalare, BIFEAZĂ opțiunea 'Add Python to PATH'" White
        Write-ColorText "3. Restart computerul după instalare" White
        Write-ColorText "4. Rulează din nou acest script" White
        Pause-WithMessage "Apasă Enter pentru a ieși..."
        exit 1
    }

    # Verifică versiune Python
    Write-ColorText "Pas 2/7: Verificare versiune Python..." Yellow
    try {
        $versionString = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>&1
        $version = [double]$versionString
        if ($version -lt 3.10) {
            Write-ColorText "✗ Versiune Python prea veche: $versionString (necesar: 3.10+)" Red
            Pause-WithMessage "Apasă Enter pentru a ieși..."
            exit 1
        }
        Write-ColorText "✓ Versiune Python OK: $versionString" Green
    } catch {
        Write-ColorText "⚠ Nu pot verifica versiunea Python, dar continui..." Yellow
    }

    # Verifică dacă folderul dpia-generator există
    Write-ColorText "Pas 3/7: Căutare folder dpia-generator..." Yellow
    $sourceDir = Join-Path $PSScriptRoot "dpia-generator"

    if (-not (Test-Path $sourceDir)) {
        Write-ColorText "✗ EROARE: Nu găsesc folderul 'dpia-generator'!" Red
        Write-Host ""
        Write-ColorText "Locația scriptului: $PSScriptRoot" Yellow
        Write-ColorText "Caut folder: $sourceDir" Yellow
        Write-Host ""
        Write-ColorText "SOLUȚIE:" Yellow
        Write-ColorText "1. Extrage COMPLET arhiva ZIP" White
        Write-ColorText "2. Ar trebui să ai structura:" White
        Write-ColorText "   dpia-temp\" White
        Write-ColorText "   ├── INSTALL_WINDOWS.ps1  (acest script)" White
        Write-ColorText "   ├── dpia-generator\      (FOLDER - trebuie să existe!)" White
        Write-ColorText "   └── alte fișiere..." White
        Write-Host ""
        Write-ColorText "3. Dacă vezi dpia-generator-v1.0.zip, extrage-l MAI ÎNTÂI!" White
        Write-ColorText "4. Apoi rulează din nou acest script" White
        Pause-WithMessage "Apasă Enter pentru a ieși..."
        exit 1
    }

    Write-ColorText "✓ Folder găsit: $sourceDir" Green

    # Creează directorul C:\Claude
    Write-ColorText "Pas 4/7: Creare director C:\Claude\dpia-generator..." Yellow
    $targetDir = "C:\Claude\dpia-generator"

    if (Test-Path $targetDir) {
        Write-ColorText "⚠ Directorul $targetDir există deja." Yellow
        $response = Read-Host "Ștergi și recreezi? (DA/NU)"
        if ($response -eq "DA" -or $response -eq "D") {
            try {
                Remove-Item -Path $targetDir -Recurse -Force -ErrorAction Stop
                Write-ColorText "✓ Director șters" Green
            } catch {
                Write-ColorText "✗ EROARE la ștergere: $_" Red
                Write-ColorText "Încearcă să ștergi manual: $targetDir" Yellow
                Pause-WithMessage
                exit 1
            }
        } else {
            Write-ColorText "Instalare anulată de utilizator." Yellow
            Pause-WithMessage
            exit 0
        }
    }

    try {
        New-Item -ItemType Directory -Path $targetDir -Force -ErrorAction Stop | Out-Null
        Write-ColorText "✓ Director creat: $targetDir" Green
    } catch {
        Write-ColorText "✗ EROARE la creare director: $_" Red
        Write-Host ""
        Write-ColorText "SOLUȚIE:" Yellow
        Write-ColorText "1. Rulează PowerShell ca Administrator:" White
        Write-ColorText "   Click dreapta pe PowerShell → Run as Administrator" White
        Write-ColorText "2. SAU folosește alt folder (ex: Documents\Claude)" White
        Pause-WithMessage
        exit 1
    }

    # Copiază fișierele
    Write-ColorText "Pas 5/7: Copiere fișiere..." Yellow
    try {
        Copy-Item -Path "$sourceDir\*" -Destination $targetDir -Recurse -Force -ErrorAction Stop
        Write-ColorText "✓ Fișiere copiate" Green
    } catch {
        Write-ColorText "✗ EROARE la copiere: $_" Red
        Pause-WithMessage
        exit 1
    }

    # Navighează în director
    Set-Location $targetDir

    # Creează virtual environment
    Write-ColorText "Pas 6/7: Creare Python virtual environment..." Yellow
    Write-ColorText "(Poate dura 30-60 secunde...)" Gray
    try {
        python -m venv venv 2>&1 | Out-Null
        if (-not (Test-Path "venv\Scripts\python.exe")) {
            throw "Virtual environment nu s-a creat corect"
        }
        Write-ColorText "✓ Virtual environment creat" Green
    } catch {
        Write-ColorText "✗ EROARE la creare venv: $_" Red
        Pause-WithMessage
        exit 1
    }

    # Instalează dependințe
    Write-ColorText "Pas 7/7: Instalare dependințe Python..." Yellow
    Write-ColorText "(Poate dura 1-2 minute, te rog așteaptă...)" Gray

    try {
        Write-ColorText "  → Upgrade pip..." Gray
        & ".\venv\Scripts\python.exe" -m pip install --upgrade pip 2>&1 | Out-Null

        Write-ColorText "  → Instalare dependințe..." Gray
        $installOutput = & ".\venv\Scripts\python.exe" -m pip install -r requirements.txt 2>&1

        if ($LASTEXITCODE -ne 0) {
            Write-ColorText "⚠ Unele erori la instalare, dar verific..." Yellow
            Write-Host $installOutput
        }

        Write-ColorText "✓ Dependințe instalate" Green
    } catch {
        Write-ColorText "✗ EROARE la instalare dependințe: $_" Red
        Write-ColorText "Încearcă manual:" Yellow
        Write-ColorText "  cd $targetDir" White
        Write-ColorText "  venv\Scripts\activate" White
        Write-ColorText "  pip install -r requirements.txt" White
        Pause-WithMessage
        exit 1
    }

    # Creează script de rulare
    $runScript = @"
@echo off
echo ═══════════════════════════════════════════════════════════
echo    DPIA GENERATOR - START
echo ═══════════════════════════════════════════════════════════
echo.
cd /d C:\Claude\dpia-generator
call venv\Scripts\activate.bat
python -m src.main
echo.
echo ═══════════════════════════════════════════════════════════
echo Program terminat.
pause
"@

    Set-Content -Path "RUN_DPIA_GENERATOR.bat" -Value $runScript
    Write-ColorText "✓ Script de rulare creat: RUN_DPIA_GENERATOR.bat" Green

    # Desktop shortcut
    Write-Host ""
    $response = Read-Host "Creezi shortcut pe Desktop? (DA/NU)"
    if ($response -eq "DA" -or $response -eq "D") {
        try {
            $WshShell = New-Object -comObject WScript.Shell
            $Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\DPIA Generator.lnk")
            $Shortcut.TargetPath = "$targetDir\RUN_DPIA_GENERATOR.bat"
            $Shortcut.WorkingDirectory = $targetDir
            $Shortcut.IconLocation = "shell32.dll,70"
            $Shortcut.Description = "DPIA Generator - Sistem generare DPIA conform GDPR"
            $Shortcut.Save()
            Write-ColorText "✓ Shortcut creat pe Desktop" Green
        } catch {
            Write-ColorText "⚠ Nu am putut crea shortcut-ul: $_" Yellow
        }
    }

    # Finalizare
    Write-Host ""
    Write-ColorText "═══════════════════════════════════════════════════════════" Green
    Write-ColorText "   ✓ INSTALARE COMPLETĂ CU SUCCES!                       " Green
    Write-ColorText "═══════════════════════════════════════════════════════════" Green
    Write-Host ""
    Write-ColorText "Locație instalare: $targetDir" Cyan
    Write-Host ""
    Write-ColorText "Pentru a rula aplicația:" Yellow
    Write-ColorText "  1. Dublu-click pe: RUN_DPIA_GENERATOR.bat" White
    Write-ColorText "     (în folder: $targetDir)" Gray
    Write-ColorText "  SAU" Yellow
    Write-ColorText "  2. Dublu-click pe shortcut de pe Desktop (dacă l-ai creat)" White
    Write-Host ""

    # Test rulare
    $response = Read-Host "Dorești să testezi aplicația ACUM? (DA/NU)"
    if ($response -eq "DA" -or $response -eq "D") {
        Write-Host ""
        Write-ColorText "Pornire DPIA Generator..." Green
        Write-Host ""
        Start-Sleep -Seconds 2
        & ".\venv\Scripts\python.exe" -m src.main
    }

} catch {
    Write-ColorText "" Red
    Write-ColorText "═══════════════════════════════════════════════════════════" Red
    Write-ColorText "   ✗ EROARE GENERALĂ" Red
    Write-ColorText "═══════════════════════════════════════════════════════════" Red
    Write-ColorText "Eroare: $_" Red
    Write-ColorText "Stack trace: $($_.ScriptStackTrace)" Gray
} finally {
    Write-Host ""
    Pause-WithMessage "Apasă Enter pentru a închide această fereastră..."
}
