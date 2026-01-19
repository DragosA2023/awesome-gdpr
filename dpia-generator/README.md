# 🎯 DPIA Generator System

**Sistem profesional de generare DPIA (Data Protection Impact Assessment) conform Art. 35 GDPR**

Generează automat documentații DPIA complete, conforme cu legislația GDPR și ANSPDCP (România), în limba română.

---

## 📋 Caracteristici

### ✅ Funcționalități principale:

- **Extragere automată** informații din documente (DOCX, PDF, TXT)
- **Validare interactivă** cu utilizatorul pentru acuratețe maximă
- **Evaluare riscuri** conform metodologia WP29 Guidelines
- **Generare diagrame** (Mermaid): fluxuri date, lifecycle, matrici risc
- **Cercetare legislație** din baza de cunoștințe GDPR actualizată
- **Export multiple formate**: Markdown, JSON metadata

### 📚 Conformitate legislativă:

- ✅ **Art. 35 GDPR** - Evaluarea impactului asupra protecției datelor
- ✅ **WP29 Guidelines WP248rev.01** - Metodologie oficială DPIA
- ✅ **EDPB Guidelines** recente (2024-2025)
- ✅ **Decizia ANSPDCP 174/2018** - Listă operațiuni DPIA obligatorii (România)
- ✅ **Jurisprudență CJUE** relevantă (Schrems II, etc.)

### 🎨 Output generat:

1. **Document DPIA complet** (Markdown) cu 7 secțiuni obligatorii:
   - Identificarea părților
   - Descrierea sistematică a operațiunii
   - Evaluarea necesității și proporționalității
   - Evaluarea riscurilor
   - Măsuri tehnice și organizatorice
   - Consultări
   - Concluzii și aprobare

2. **Diagrame vizuale** (Mermaid):
   - Data Flow Diagram (DFD)
   - Ciclul de viață al datelor
   - Matrice heat map riscuri
   - Arhitectură sisteme (opțional)
   - Roluri și responsabilități (opțional)

3. **Anexe**:
   - Referințe legislative și jurisprudență
   - Metadata document

---

## 🚀 Instalare

### Cerințe sistem:

- Python 3.10 sau mai recent
- pip (package manager Python)

### Pași instalare:

```bash
# 1. Clonează sau descarcă repository-ul
cd awesome-gdpr/dpia-generator

# 2. Creează virtual environment (recomandat)
python -m venv venv

# 3. Activează virtual environment
# Pe Linux/Mac:
source venv/bin/activate
# Pe Windows:
venv\Scripts\activate

# 4. Instalează dependințele
pip install -r requirements.txt
```

### Dependințe instalate:

- `python-docx` - Citire/scriere documente DOCX
- `pdfplumber` - Citire documente PDF
- `rich` - Interfață CLI frumoasă
- `pyyaml` - Fișiere configurare
- `jinja2` - Template engine
- Altele (vezi `requirements.txt`)

---

## 💻 Utilizare

### Modul interactiv (recomandat):

```bash
# Rulează sistemul în mod interactiv
python -m src.main
```

Sistemul va ghida utilizatorul prin următorii pași:

#### **PASUL 0: Identificare operator și proces**
- Denumire operator, CUI, adresă
- Date contact
- DPO (dacă există)
- Denumire proces/operațiune prelucrare

#### **PASUL 1: Extragere automată informații**
- Încarcă documente din director (DOCX, PDF, TXT)
- Sistemul extrage automat:
  - Împuterniciti
  - Scopuri prelucrării
  - Temei juridic
  - Categorii date personale
  - Persoane vizate
  - Destinatari
  - Transferuri internaționale
  - Durata stocare
  - Măsuri de securitate

- **Validare interactivă** - confirmi/modifici fiecare categorie

#### **PASUL 2: Verificare necesitate DPIA**
- Sistemul analizează dacă DPIA este obligatorie
- Pe baza: categorii speciale, scară largă, monitorizare, etc.

#### **PASUL 3: Cercetare legislație**
- Sistemul încarcă automat:
  - Articole GDPR relevante
  - Guidelines EDPB/WP29
  - Jurisprudență CJUE
  - Decizii ANSPDCP

#### **PASUL 4: Evaluare riscuri**
- Identificare riscuri pe baza caracteristicilor prelucrării
- Evaluare severitate și probabilitate
- Propunere măsuri de atenuare
- Calcul risc rezidual

#### **PASUL 5: Generare diagrame**
- Data Flow Diagram
- Ciclul de viață al datelor
- Matrice risc (heat map)

#### **PASUL 6: Generare document DPIA**
- Generare conținut complet conform Art. 35(7)
- Include toate secțiunile obligatorii
- Limbă română profesională

#### **PASUL 7: Export**
- Salvare fișiere în folder `output/`
- Format Markdown pentru editare ușoară
- Metadata JSON

---

## 📁 Structură proiect

```
dpia-generator/
├── src/
│   ├── core/
│   │   ├── document_parser.py      # Extragere info din documente
│   │   ├── validator.py            # Validare interactivă
│   │   ├── risk_assessor.py        # Evaluare riscuri GDPR
│   │   └── dpia_generator.py       # Generator principal DPIA
│   ├── modules/
│   │   ├── web_research.py         # Cercetare legislație
│   │   └── diagram_generator.py    # Generare diagrame Mermaid
│   ├── utils/
│   │   └── gdpr_knowledge.py       # Bază cunoștințe GDPR
│   └── main.py                     # Entry point
├── data/
│   ├── models/                     # Modele DPIA (template-uri)
│   ├── completed_dpias/            # DPIA-uri completate (exemple)
│   ├── expert_dpias/               # DPIA-uri experți
│   └── legislation/                # Cache legislație
├── output/                         # Fișiere generate
├── requirements.txt
└── README.md
```

---

## 📄 Exemplu utilizare

### 1. Pregătire documente

Creează un folder cu documentele tale:
```
my-documents/
├── Registru_Art30.docx
├── Contract_Impuiternicire_CloudProvider.pdf
├── Politica_Securitate.docx
└── Procedura_Drepturi_Persoane_Vizate.pdf
```

### 2. Rulează sistemul

```bash
python -m src.main
```

### 3. Urmează pașii interactivi

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║            🎯 DPIA GENERATOR SYSTEM v1.0                  ║
║                                                           ║
║   Generare DPIA conform Art. 35 GDPR                      ║
║   Legislație română - ANSPDCP                            ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════
PASUL 0: IDENTIFICARE OPERATOR ȘI PROCES
═══════════════════════════════════════════════════════════

➜ Denumire completă operator: SC Example SRL
➜ Forma juridică (SRL/SA/PFA/etc.): SRL
➜ CUI/CIF: RO12345678
...
```

### 4. Rezultat

```
output/
├── DPIA_SC_Example_SRL_20260119.md          # Document principal
├── DPIA_SC_Example_SRL_20260119_Referinte.md  # Referințe
├── DPIA_SC_Example_SRL_20260119_metadata.json # Metadata
└── diagrams/
    ├── dfd.md                                # Data flow diagram
    ├── lifecycle.md                          # Lifecycle
    └── risk_matrix.md                        # Matrice risc
```

---

## 🎓 Concepte GDPR folosite

### Baza de cunoștințe include:

#### Articole GDPR:
- **Art. 5** - Principii prelucrare (legalitate, minimizare, etc.)
- **Art. 6** - Temeiuri juridice (consimțământ, contract, interes legitim, etc.)
- **Art. 9** - Categorii speciale de date
- **Art. 32** - Securitatea prelucrării
- **Art. 35** - DPIA
- **Art. 36** - Consultare prealabilă autoritate

#### Metodologie evaluare risc:
- **Severitate** (1-4): Impact asupra persoanelor vizate
- **Probabilitate** (1-4): Cât de probabil este riscul
- **Nivel risc** = Severitate × Probabilitate
  - 🟢 1-4: Scăzut (acceptabil)
  - 🟡 5-8: Mediu (măsuri suplimentare)
  - 🟠 9-12: Ridicat (măsuri imediate)
  - 🔴 13-16: Critic (INACCEPTABIL - consultare ANSPDCP)

#### Catalog riscuri:
- Acces neautorizat
- Data breach (încălcare securitate)
- Prelucrare ilicită
- Colectare excesivă (încălcare minimizare)
- Date inexacte
- Păstrare excesivă
- Lipsa transparenței
- Imposibilitate exercitare drepturi
- Risc transferuri internaționale
- Neconformitate împuternicit
- Discriminare prin profilare
- Expunere date speciale (Art. 9)
- Risc specific copii
- Impact monitorizare/supraveghere

---

## 🔧 Configurare avansată

### Modificare catalog riscuri

Editează `src/utils/gdpr_knowledge.py`:

```python
# Adaugă risc personalizat
"custom_risk": {
    "name": "Denumire risc personalizat",
    "description": "Descriere detaliată",
    "sources": ["Sursă 1", "Sursă 2"],
    "typical_severity": RiskSeverity.SIGNIFICANT,
    "affects_principles": ["Art. X GDPR"]
}
```

### Adăugare legislație nouă

Editează `src/modules/web_research.py`:

```python
# Adaugă referință nouă
LegalReference(
    type="gdpr_article",
    reference="Art. X GDPR",
    title="Titlu articol",
    url="https://...",
    relevance="De ce e relevant",
    key_points=["Punct cheie 1", "Punct cheie 2"]
)
```

---

## 🤝 Contribuții

Sistemul este open-source. Contribuțiile sunt binevenite!

### Cum să contribui:

1. Fork repository
2. Creează branch pentru feature (`git checkout -b feature/NovaFunctionalitate`)
3. Commit modificări (`git commit -m 'Adaugă funcționalitate X'`)
4. Push la branch (`git push origin feature/NovaFunctionalitate`)
5. Creează Pull Request

---

## ⚖️ Licență

MIT License - vezi fișierul LICENSE pentru detalii

---

## 📞 Contact și suport

Pentru întrebări, sugestii sau raportare probleme:
- 📧 Email: [contact]
- 🐛 Issues: GitHub Issues

---

## ⚠️ Disclaimer

Acest software generează documentații DPIA ca instrument de asistență. **Nu înlocuiește consultanța juridică profesională.**

Recomandări:
- ✅ Verificați întotdeauna DPIA-ul generat cu un expert GDPR
- ✅ Adaptați conținutul la specificul organizației
- ✅ Consultați DPO-ul (dacă există)
- ✅ Pentru cazuri complexe, solicitați asistență juridică specializată

---

## 📚 Resurse adiționale

### Legislație:
- [GDPR - Text oficial EUR-Lex](https://eur-lex.europa.eu/legal-content/RO/TXT/?uri=CELEX:32016R0679)
- [Legea 190/2018 - Măsuri punere în aplicare GDPR](https://legislatie.just.ro/Public/DetaliiDocument/203870)
- [ANSPDCP - Decizia 174/2018 - Listă DPIA](https://www.dataprotection.ro/)

### Guidelines:
- [WP29 Guidelines on DPIA (WP248rev.01)](https://ec.europa.eu/newsroom/article29/items/611236)
- [EDPB Guidelines & Recommendations](https://edpb.europa.eu/our-work-tools/general-guidance/gdpr-guidelines-recommendations-best-practices_en)
- [ICO - Guide to DPIA](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/data-protection-impact-assessments-dpias/)

### Jurisprudență:
- [CJUE - Toate cazurile GDPR](https://curia.europa.eu/)
- [GDPRhub - Wiki GDPR](https://gdprhub.eu/)

### Tools:
- [CNIL - Open Source DPIA Software](https://www.cnil.fr/en/open-source-pia-software-helps-carry-out-data-protection-impact-assesment)
- [awesome-gdpr - Resurse GDPR](https://github.com/bakke92/awesome-gdpr)

---

## 🎯 Roadmap viitor

### Versiunea 1.1 (planificat):
- [ ] Export DOCX nativ (cu formatare)
- [ ] Export PDF
- [ ] Interfață web (Flask/FastAPI)
- [ ] Integrare AI pentru analiză documentație avansată
- [ ] Support limbă engleză
- [ ] Template-uri industrie specifice (healthcare, fintech, etc.)
- [ ] Import DPIA-uri existente pentru actualizare

### Versiunea 2.0 (concept):
- [ ] Platformă SaaS completă
- [ ] Colaborare multi-utilizator
- [ ] Istoric versiuni DPIA
- [ ] Dashboard analytics riscuri
- [ ] Integrare cu tool-uri GRC (Governance, Risk, Compliance)

---

**Versiune:** 1.0.0
**Data ultimei actualizări:** Ianuarie 2026
**Autor:** GDPR Expert System
**Licență:** MIT

---

**Mulțumim că folosești DPIA Generator System! 🎯**

*Pentru un viitor conform GDPR și respectuos cu privacitatea.*
