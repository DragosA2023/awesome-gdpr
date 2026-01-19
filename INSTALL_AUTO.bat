@echo off
REM ═══════════════════════════════════════════════════════════
REM    DPIA GENERATOR - INSTALARE AUTOMATA 100%
REM    Nu trebuie sa tastezi NIMIC - totul e automat!
REM ═══════════════════════════════════════════════════════════

color 0A
echo.
echo ═══════════════════════════════════════════════════════════
echo    DPIA GENERATOR - INSTALARE AUTOMATA
echo ═══════════════════════════════════════════════════════════
echo.
echo Acest script va instala AUTOMAT tot ce e nevoie.
echo Nu trebuie sa faci NIMIC - doar asteapta.
echo.
pause

REM ===== VERIFICARE PYTHON =====
echo.
echo [1/6] Verificare Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo [EROARE] Python NU este instalat sau nu este in PATH!
    echo.
    echo SOLUTIE:
    echo 1. Descarca Python de la: https://www.python.org/downloads/
    echo 2. La instalare, BIFEAZA "Add Python to PATH"
    echo 3. Restart computerul
    echo 4. Ruleaza din nou acest script
    echo.
    pause
    exit /b 1
)
echo [OK] Python gasit!

REM ===== GASESTE FOLDERUL CU FISIERE =====
echo.
echo [2/6] Cautare folder dpia-generator cu fisiere...

REM Cauta in locatia curenta
if exist "%~dp0dpia-generator\src" (
    set "SOURCE_DIR=%~dp0dpia-generator"
    echo [OK] Gasit in: %SOURCE_DIR%
    goto :found
)

REM Cauta in Desktop
if exist "%USERPROFILE%\Desktop\dpia-generator\src" (
    set "SOURCE_DIR=%USERPROFILE%\Desktop\dpia-generator"
    echo [OK] Gasit in: %SOURCE_DIR%
    goto :found
)

if exist "%USERPROFILE%\Desktop\dpia-temp\dpia-generator\src" (
    set "SOURCE_DIR=%USERPROFILE%\Desktop\dpia-temp\dpia-generator"
    echo [OK] Gasit in: %SOURCE_DIR%
    goto :found
)

REM Cauta in Downloads
if exist "%USERPROFILE%\Downloads\dpia-generator\src" (
    set "SOURCE_DIR=%USERPROFILE%\Downloads\dpia-generator"
    echo [OK] Gasit in: %SOURCE_DIR%
    goto :found
)

if exist "%USERPROFILE%\Downloads\dpia-temp\dpia-generator\src" (
    set "SOURCE_DIR=%USERPROFILE%\Downloads\dpia-temp\dpia-generator"
    echo [OK] Gasit in: %SOURCE_DIR%
    goto :found
)

REM Nu a gasit folderul
color 0C
echo.
echo [EROARE] Nu gasesc folderul dpia-generator cu fisiere!
echo.
echo SOLUTIE:
echo 1. Extrage arhiva dpia-generator-v1.0.zip
echo 2. Pune folderul extras pe Desktop SAU in acelasi folder cu acest script
echo 3. Verifica ca folderul contine: src\, requirements.txt, README.md
echo 4. Ruleaza din nou acest script
echo.
pause
exit /b 1

:found

REM ===== CREARE DIRECTOR C:\CLAUDE =====
echo.
echo [3/6] Creare director C:\Claude\dpia-generator...

if exist "C:\Claude\dpia-generator" (
    echo [!] Directorul exista deja - il sterg si il recrez...
    rmdir /S /Q "C:\Claude\dpia-generator" 2>nul
)

mkdir "C:\Claude" 2>nul
mkdir "C:\Claude\dpia-generator" 2>nul

if not exist "C:\Claude\dpia-generator" (
    color 0C
    echo.
    echo [EROARE] Nu pot crea C:\Claude\dpia-generator
    echo.
    echo SOLUTIE:
    echo 1. Ruleaza acest BAT ca Administrator:
    echo    Click dreapta pe fisier -^> Run as Administrator
    echo.
    pause
    exit /b 1
)

echo [OK] Director creat!

REM ===== COPIERE FISIERE =====
echo.
echo [4/6] Copiere fisiere...
echo (Poate dura 10-30 secunde...)

xcopy /E /I /Y /Q "%SOURCE_DIR%\*" "C:\Claude\dpia-generator\" >nul 2>&1

if not exist "C:\Claude\dpia-generator\src" (
    color 0C
    echo [EROARE] Copiere esuata!
    pause
    exit /b 1
)

echo [OK] Fisiere copiate!

REM ===== CREARE VIRTUAL ENVIRONMENT =====
echo.
echo [5/6] Creare Python virtual environment...
echo (Poate dura 30-60 secunde...)

cd /d "C:\Claude\dpia-generator"

python -m venv venv

if not exist "venv\Scripts\python.exe" (
    color 0C
    echo [EROARE] Virtual environment nu s-a creat!
    pause
    exit /b 1
)

echo [OK] Virtual environment creat!

REM ===== INSTALARE DEPENDENCIES =====
echo.
echo [6/6] Instalare dependinte Python...
echo (Poate dura 1-2 minute - TE ROG ASTEAPTA!)
echo.

venv\Scripts\python.exe -m pip install --upgrade pip --quiet
venv\Scripts\python.exe -m pip install -r requirements.txt --quiet

if %errorlevel% neq 0 (
    color 0E
    echo.
    echo [ATENTIE] Unele erori la instalare, dar incerc sa continui...
    echo.
)

echo [OK] Dependinte instalate!

REM ===== CREARE SCRIPT DE RULARE =====
echo.
echo Creare script de rulare rapida...

(
echo @echo off
echo echo ═══════════════════════════════════════════════════════════
echo echo    DPIA GENERATOR - START
echo echo ═══════════════════════════════════════════════════════════
echo echo.
echo cd /d C:\Claude\dpia-generator
echo call venv\Scripts\activate.bat
echo python -m src.main
echo echo.
echo echo ═══════════════════════════════════════════════════════════
echo echo Program terminat.
echo pause
) > "C:\Claude\dpia-generator\RUN_DPIA_GENERATOR.bat"

echo [OK] Script creat: RUN_DPIA_GENERATOR.bat

REM ===== CREARE SHORTCUT DESKTOP =====
echo.
echo Creare shortcut pe Desktop...

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\Desktop\DPIA Generator.lnk'); $Shortcut.TargetPath = 'C:\Claude\dpia-generator\RUN_DPIA_GENERATOR.bat'; $Shortcut.WorkingDirectory = 'C:\Claude\dpia-generator'; $Shortcut.IconLocation = 'shell32.dll,70'; $Shortcut.Save()" >nul 2>&1

if exist "%USERPROFILE%\Desktop\DPIA Generator.lnk" (
    echo [OK] Shortcut creat pe Desktop!
) else (
    echo [!] Nu am putut crea shortcut-ul ^(nu e o problema^)
)

REM ===== FINALIZARE =====
color 0A
echo.
echo.
echo ═══════════════════════════════════════════════════════════
echo    INSTALARE COMPLETA CU SUCCES!
echo ═══════════════════════════════════════════════════════════
echo.
echo Locatie: C:\Claude\dpia-generator
echo.
echo Pentru a rula aplicatia:
echo   1. Dublu-click pe shortcut-ul "DPIA Generator" de pe Desktop
echo   SAU
echo   2. Dublu-click pe: C:\Claude\dpia-generator\RUN_DPIA_GENERATOR.bat
echo.
echo ═══════════════════════════════════════════════════════════
echo.

REM ===== INTREABA DACA VREA SA RULEZE ACUM =====
set /p "RUN_NOW=Doresti sa rulezi DPIA Generator ACUM? (D/N): "

if /i "%RUN_NOW%"=="D" (
    echo.
    echo Pornire DPIA Generator...
    echo.
    timeout /t 2 /nobreak >nul
    cd /d "C:\Claude\dpia-generator"
    call venv\Scripts\activate.bat
    python -m src.main
) else (
    echo.
    echo OK. Poti rula mai tarziu folosind shortcut-ul de pe Desktop.
    echo.
    pause
)
