# 📦 DPIA Generator - Instalare Manuală pe Windows în C:\Claude

## 🎯 Ghid Complet Instalare Manuală

---

## Metoda 1: Instalare Automată (RECOMANDATĂ) ⚡

### Pași:

1. **Descarcă fișierele:**
   - Descarcă `dpia-generator-v1.0.zip` din repository
   - Descarcă `INSTALL_WINDOWS.ps1` (scriptul de instalare)

2. **Extrage arhiva:**
   - Click dreapta pe `dpia-generator-v1.0.zip` → Extract All
   - Extrage în orice folder temporar

3. **Rulează scriptul de instalare:**
   - Copiază `INSTALL_WINDOWS.ps1` în același folder cu `dpia-generator/`
   - Click dreapta pe `INSTALL_WINDOWS.ps1` → **Run with PowerShell**
   - SAU deschide PowerShell și rulează:
     ```powershell
     powershell -ExecutionPolicy Bypass -File INSTALL_WINDOWS.ps1
     ```

4. **Urmează instrucțiunile interactive:**
   - Scriptul va verifica Python
   - Va crea `C:\Claude\dpia-generator`
   - Va instala toate dependințele
   - Va crea shortcut pe Desktop (opțional)

5. **GATA!** Dublu-click pe shortcut sau `RUN_DPIA_GENERATOR.bat`

---

## Metoda 2: Instalare Manuală 🛠️

Dacă preferi să instalezi manual sau dacă scriptul PowerShell nu funcționează:

### Cerințe Preliminare:

✅ **Python 3.10 sau mai nou**
   - Descarcă de la: https://www.python.org/downloads/
   - **IMPORTANT:** La instalare, bifează **"Add Python to PATH"**
   - Verificare: Deschide CMD și rulează: `python --version`

✅ **Git** (opțional, pentru clonare repository)
   - Descarcă de la: https://git-scm.com/download/win

### Pașii Instalării Manuale:

#### **Pasul 1: Creează directorul C:\Claude**

Deschide **Command Prompt** (CMD) sau **PowerShell**:

```cmd
mkdir C:\Claude
cd C:\Claude
```

#### **Pasul 2: Obține codul sursă**

**Opțiunea A - Descarcă ZIP:**
```cmd
REM 1. Descarcă dpia-generator-v1.0.zip din GitHub
REM 2. Extrage în C:\Claude
REM 3. Ar trebui să ai C:\Claude\dpia-generator\
```

**Opțiunea B - Clone repository (dacă ai Git):**
```cmd
cd C:\Claude
git clone https://github.com/DragosA2023/awesome-gdpr.git
cd awesome-gdpr
git checkout claude/dpia-generator-system-CkEDL
REM Apoi copiază folderul dpia-generator în C:\Claude
xcopy /E /I awesome-gdpr\dpia-generator C:\Claude\dpia-generator
cd C:\Claude\dpia-generator
```

#### **Pasul 3: Verifică structura folderelor**

Verifică că ai:
```
C:\Claude\dpia-generator\
├── README.md
├── requirements.txt
├── src\
│   ├── main.py
│   ├── core\
│   ├── modules\
│   └── utils\
├── data\
├── config\
├── tests\
└── output\
```

#### **Pasul 4: Creează Python Virtual Environment**

```cmd
cd C:\Claude\dpia-generator

REM Creează venv
python -m venv venv

REM Activează venv
venv\Scripts\activate

REM Ar trebui să vezi (venv) în prompt
```

#### **Pasul 5: Instalează dependințele**

Cu venv activat:

```cmd
REM Upgrade pip
python -m pip install --upgrade pip

REM Instalează dependințele
pip install -r requirements.txt
```

Așteptă ~1-2 minute pentru instalare. Vei vedea:
```
Successfully installed python-docx-0.8.11 pdfplumber-0.9.0 rich-13.0.0 ...
```

#### **Pasul 6: Testează instalarea**

```cmd
python -m src.main
```

Ar trebui să vezi:
```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║            🎯 DPIA GENERATOR SYSTEM v1.0                  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

**✅ SUCCES! Instalarea este completă.**

#### **Pasul 7: Creează script de rulare rapidă (opțional)**

Creează fișier `RUN_DPIA_GENERATOR.bat` în `C:\Claude\dpia-generator\`:

```batch
@echo off
echo ═══════════════════════════════════════════════════════════
echo    DPIA GENERATOR - START
echo ═══════════════════════════════════════════════════════════
echo.
cd /d C:\Claude\dpia-generator
call venv\Scripts\activate.bat
python -m src.main
pause
```

Apoi dublu-click pe acest fișier pentru a rula aplicația rapid.

#### **Pasul 8: Creează shortcut pe Desktop (opțional)**

1. Click dreapta pe Desktop → New → Shortcut
2. Location: `C:\Claude\dpia-generator\RUN_DPIA_GENERATOR.bat`
3. Name: `DPIA Generator`
4. Click Finish

---

## 🚀 Utilizare După Instalare

### Metoda 1: Shortcut Desktop
Dublu-click pe shortcut-ul `DPIA Generator`

### Metoda 2: BAT file
Dublu-click pe `C:\Claude\dpia-generator\RUN_DPIA_GENERATOR.bat`

### Metoda 3: Manual din CMD/PowerShell
```cmd
cd C:\Claude\dpia-generator
venv\Scripts\activate
python -m src.main
```

---

## 🐛 Troubleshooting - Probleme Comune

### ❌ "Python is not recognized..."

**Problemă:** Python nu este în PATH

**Soluție:**
1. Reinstalează Python de la https://www.python.org/downloads/
2. **BIFEAZĂ opțiunea "Add Python to PATH"**
3. SAU adaugă manual în PATH:
   - Windows Search → "Environment Variables"
   - System Variables → Path → Edit
   - Add New → `C:\Users\<User>\AppData\Local\Programs\Python\Python311\`
   - Add New → `C:\Users\<User>\AppData\Local\Programs\Python\Python311\Scripts\`

### ❌ "pip install" eșuează

**Problemă:** Erori la instalare dependințe

**Soluție:**
```cmd
REM Upgrade pip mai întâi
python -m pip install --upgrade pip setuptools wheel

REM Apoi instalează din nou
pip install -r requirements.txt
```

### ❌ "No module named 'docx'"

**Problemă:** Dependințele nu s-au instalat corect

**Soluție:**
```cmd
REM Asigură-te că venv este activat (vezi (venv) în prompt)
venv\Scripts\activate

REM Instalează manual fiecare dependință
pip install python-docx
pip install pdfplumber
pip install rich
pip install click
pip install pyyaml
pip install jinja2
```

### ❌ "Access Denied" la creare C:\Claude

**Problemă:** Lipsă permisiuni administrator

**Soluție:**
1. Click dreapta pe CMD/PowerShell → **Run as Administrator**
2. SAU creează într-un folder cu permisiuni (ex: `C:\Users\<User>\Documents\Claude`)

### ❌ PowerShell script nu rulează

**Problemă:** Execution Policy restricționat

**Soluție:**
```powershell
REM Rulează PowerShell ca Administrator
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass

REM Apoi rulează scriptul
.\INSTALL_WINDOWS.ps1
```

---

## 📂 Structură Finală Instalare

După instalare, ar trebui să ai:

```
C:\Claude\
└── dpia-generator\
    ├── README.md                    (Documentație completă)
    ├── requirements.txt             (Dependințe Python)
    ├── RUN_DPIA_GENERATOR.bat       (Script rulare rapidă)
    ├── .gitignore
    ├── venv\                        (Virtual environment Python)
    │   ├── Scripts\
    │   │   ├── python.exe
    │   │   ├── activate.bat
    │   │   └── pip.exe
    │   └── Lib\
    ├── src\
    │   ├── __init__.py
    │   ├── main.py                  (Entry point)
    │   ├── core\                    (Module principale)
    │   │   ├── document_parser.py
    │   │   ├── validator.py
    │   │   ├── risk_assessor.py
    │   │   └── dpia_generator.py
    │   ├── modules\                 (Module suport)
    │   │   ├── diagram_generator.py
    │   │   └── web_research.py
    │   └── utils\
    │       └── gdpr_knowledge.py    (Bază cunoștințe GDPR)
    ├── data\
    │   ├── models\
    │   ├── completed_dpias\
    │   ├── expert_dpias\
    │   └── legislation\
    ├── config\
    ├── tests\
    └── output\                      (Fișiere DPIA generate)
```

---

## 📚 Resurse Adiționale

### Documentație:
- **README.md** - Documentație completă sistem
- **GitHub:** https://github.com/DragosA2023/awesome-gdpr

### Help:
- Rulează: `python -m src.main --help` (când va fi implementat)
- Issues: https://github.com/DragosA2023/awesome-gdpr/issues

### Python Resources:
- Python Download: https://www.python.org/downloads/
- pip Documentation: https://pip.pypa.io/en/stable/
- venv Guide: https://docs.python.org/3/library/venv.html

---

## ✅ Checklist Instalare

Verifică că ai completat:

- [ ] Python 3.10+ instalat și în PATH
- [ ] Cod sursă extras în `C:\Claude\dpia-generator`
- [ ] Virtual environment creat (`venv\` folder există)
- [ ] Dependințele instalate (pip install reușit)
- [ ] Test rulare: `python -m src.main` funcționează
- [ ] Script BAT creat (opțional)
- [ ] Shortcut Desktop creat (opțional)

---

## 🎉 Gata de Utilizare!

Odată instalat, citește **README.md** pentru:
- Tutorial complet utilizare
- Exemple
- Configurare avansată
- Best practices

**Succes la generarea DPIA-urilor conforme GDPR! 🎯**

---

**Versiune:** 1.0.0
**Data:** Ianuarie 2026
**Support:** GitHub Issues
