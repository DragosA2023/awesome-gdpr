"""
DPIA Generator - Generator principal de conținut DPIA conform Art. 35 GDPR
Generează document complet în limba română
"""

from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass

from ..utils.gdpr_knowledge import GDPRKnowledge
from .risk_assessor import Risk, RiskLevel


@dataclass
class DPIADocument:
    """Reprezentare document DPIA generat"""
    content: str  # Conținut Markdown complet
    metadata: Dict
    sections: Dict[str, str]  # Secțiuni separate


class DPIAGenerator:
    """Generator DPIA conform Art. 35(7) GDPR"""

    def __init__(self):
        self.gdpr_kb = GDPRKnowledge()

    def generate_dpia(
        self,
        operator_info: Dict,
        processing_info: Dict,
        risks: List[Risk],
        legal_references: List,
        diagrams: Dict[str, str]
    ) -> DPIADocument:
        """
        Generează DPIA complet

        Args:
            operator_info: Informații operator și proces
            processing_info: Informații prelucrare validate
            risks: Riscuri evaluate
            legal_references: Referințe legale
            diagrams: Diagrame generate

        Returns:
            DPIADocument complet
        """
        sections = {}
        content = ""

        # Coperta
        content += self._generate_cover_page(operator_info)
        content += "\n\n" + "═" * 63 + "\n\n"

        # Cuprins (va fi generat automat la export)
        content += self._generate_toc()
        content += "\n\n" + "═" * 63 + "\n\n"

        # 1. Identificarea părților
        section1 = self._generate_section_1_identification(operator_info, processing_info)
        sections["section_1"] = section1
        content += section1 + "\n\n"

        # 2. Descrierea sistematică a operațiunii
        section2 = self._generate_section_2_description(processing_info, diagrams)
        sections["section_2"] = section2
        content += section2 + "\n\n"

        # 3. Evaluarea necesității și proporționalității
        section3 = self._generate_section_3_necessity(processing_info)
        sections["section_3"] = section3
        content += section3 + "\n\n"

        # 4. Evaluarea riscurilor
        section4 = self._generate_section_4_risks(risks, diagrams)
        sections["section_4"] = section4
        content += section4 + "\n\n"

        # 5. Măsuri tehnice și organizatorice
        section5 = self._generate_section_5_measures(processing_info, risks, diagrams)
        sections["section_5"] = section5
        content += section5 + "\n\n"

        # 6. Consultări
        section6 = self._generate_section_6_consultations(operator_info, risks)
        sections["section_6"] = section6
        content += section6 + "\n\n"

        # 7. Concluzii și aprobare
        section7 = self._generate_section_7_conclusions(risks, processing_info)
        sections["section_7"] = section7
        content += section7 + "\n\n"

        # Anexe
        annexes = self._generate_annexes(legal_references, diagrams)
        sections["annexes"] = annexes
        content += annexes

        # Metadata
        metadata = {
            "generated_date": datetime.now().strftime("%Y-%m-%d"),
            "operator": operator_info.get('name'),
            "process": operator_info.get('process_name'),
            "version": "1.0",
            "total_risks": len(risks),
            "high_risks": len([r for r in risks if r.residual_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]])
        }

        return DPIADocument(
            content=content,
            metadata=metadata,
            sections=sections
        )

    def _generate_cover_page(self, operator_info: Dict) -> str:
        """Generează pagina de copertă"""
        cover = "# EVALUARE DE IMPACT ASUPRA PROTECȚIEI DATELOR\n"
        cover += "## (DATA PROTECTION IMPACT ASSESSMENT - DPIA)\n\n"
        cover += "### conform Art. 35 Regulamentul (UE) 2016/679 (GDPR)\n\n"
        cover += "---\n\n"
        cover += f"**Operator:** {operator_info.get('name', 'Nume operator')}\n\n"
        cover += f"**Operațiune de prelucrare:** {operator_info.get('process_name', 'Denumire proces')}\n\n"
        cover += f"**Versiune:** 1.0\n\n"
        cover += f"**Data:** {datetime.now().strftime('%d.%m.%Y')}\n\n"

        return cover

    def _generate_toc(self) -> str:
        """Generează cuprins"""
        toc = "## CUPRINS\n\n"
        toc += "1. IDENTIFICAREA PĂRȚILOR\n"
        toc += "2. DESCRIEREA SISTEMATICĂ A OPERAȚIUNII DE PRELUCRARE\n"
        toc += "3. EVALUAREA NECESITĂȚII ȘI PROPORȚIONALITĂȚII\n"
        toc += "4. EVALUAREA RISCURILOR\n"
        toc += "5. MĂSURI TEHNICE ȘI ORGANIZATORICE\n"
        toc += "6. CONSULTĂRI\n"
        toc += "7. CONCLUZII ȘI APROBARE\n"
        toc += "ANEXE\n\n"

        return toc

    def _generate_section_1_identification(
        self,
        operator_info: Dict,
        processing_info: Dict
    ) -> str:
        """Secțiunea 1: Identificarea părților"""
        section = "## 1. IDENTIFICAREA PĂRȚILOR\n\n"

        # 1.1 Operator
        section += "### 1.1. OPERATOR DE DATE\n\n"
        section += f"**Denumire:** {operator_info.get('name', '')}\n\n"
        section += f"**Forma juridică:** {operator_info.get('legal_form', '')}\n\n"
        section += f"**CUI/CIF:** {operator_info.get('cui', '')}\n\n"
        section += f"**Adresă sediu social:** {operator_info.get('address', '')}\n\n"
        section += f"**Persoană de contact (reprezentant legal):** {operator_info.get('contact_person', '')}\n\n"
        section += f"**Telefon:** {operator_info.get('phone', '')}\n\n"
        section += f"**Email:** {operator_info.get('email', '')}\n\n"

        # 1.2 DPO
        section += "### 1.2. RESPONSABIL CU PROTECȚIA DATELOR (DPO)\n\n"
        has_dpo = operator_info.get('has_dpo', False)

        if has_dpo:
            section += f"**Nume DPO:** {operator_info.get('dpo_name', '')}\n\n"
            section += f"**Contact DPO:** {operator_info.get('dpo_contact', '')}\n\n"
            section += "**Status:** DPO desemnat conform Art. 37 GDPR\n\n"
        else:
            section += "**Status:** Operatorul nu are obligația de a desemna DPO conform Art. 37 GDPR.\n\n"
            section += "*Justificare:* [Explicare de ce nu este obligatorie desemnarea DPO]\n\n"

        # 1.3 Împuterniciti
        section += "### 1.3. ÎMPUTERNICITI (PROCESATORI)\n\n"

        processors = processing_info.get('processors', [])
        if processors:
            section += f"Operatorul colaborează cu **{len(processors)} împuternicit(i)** conform Art. 28 GDPR:\n\n"

            for idx, proc in enumerate(processors, 1):
                section += f"#### Împuternicit {idx}: {proc.get('name', 'Nume nespecificat')}\n\n"
                section += f"**Servicii furnizate:** {proc.get('services', 'Nespecificat')}\n\n"

                has_contract = proc.get('has_art28_contract', False)
                if has_contract:
                    section += "**Contract Art. 28 GDPR:** ✓ Încheiat\n\n"
                else:
                    section += "**Contract Art. 28 GDPR:** ❌ LIPSĂ - **ACȚIUNE NECESARĂ**\n\n"
                    section += "**⚠️ Risc:** Colaborare fără contract Art. 28 încalcă GDPR și expune operatorul la răspundere.\n\n"

        else:
            section += "**Status:** Nu există împuterniciti pentru această operațiune de prelucrare.\n\n"
            section += "Toate operațiunile de prelucrare sunt realizate direct de operator.\n\n"

        return section

    def _generate_section_2_description(
        self,
        processing_info: Dict,
        diagrams: Dict[str, str]
    ) -> str:
        """Secțiunea 2: Descrierea sistematică a operațiunii"""
        section = "## 2. DESCRIEREA SISTEMATICĂ A OPERAȚIUNII DE PRELUCRARE\n\n"

        # 2.1 Natura prelucrării
        section += "### 2.1. NATURA PRELUCRĂRII\n\n"
        section += f"**Tip operațiune:** {processing_info.get('operation_type', 'Prelucrare automată și manuală')}\n\n"

        is_new = processing_info.get('is_new_processing')
        if is_new:
            section += "**Status:** Prelucrare nouă / Modificare substanțială\n\n"
        else:
            section += "**Status:** Prelucrare existentă, supusă revizuirii\n\n"

        section += "**Descriere detaliată:**\n\n"
        section += processing_info.get('detailed_description', '[Descriere detaliată a operațiunii de prelucrare]') + "\n\n"

        # 2.2 Scopuri
        section += "### 2.2. SCOPURI PRELUCRĂRII\n\n"
        purposes = processing_info.get('purposes', [])

        if purposes:
            section += "Datele cu caracter personal sunt prelucrate în următoarele scopuri:\n\n"
            for idx, purpose in enumerate(purposes, 1):
                section += f"{idx}. {purpose}\n"
            section += "\n"
        else:
            section += "**⚠️ ATENȚIE:** Scopurile nu au fost definite clar - necesită completare.\n\n"

        section += "**Conformitate Art. 5(1)(b) GDPR:** Scopurile sunt specifice, explicite și legitime.\n\n"

        # 2.3 Temei juridic
        section += "### 2.3. TEMEI JURIDIC\n\n"

        legal_basis = processing_info.get('legal_basis', {})
        art6_basis = legal_basis.get('art6_basis', 'Nespecificat')

        section += f"**Temei principal:** {art6_basis}\n\n"

        # Justificare
        section += "**Justificare:**\n\n"
        if '(a)' in art6_basis:
            section += "Prelucrarea se bazează pe consimțământul persoanei vizate pentru unul sau mai multe scopuri specifice. "
            section += "Consimțământul este liber exprimat, specific, informat și neechivoc.\n\n"
        elif '(b)' in art6_basis:
            section += "Prelucrarea este necesară pentru executarea unui contract la care persoana vizată este parte "
            section += "sau pentru a face demersuri la cererea persoanei vizate înainte de încheierea contractului.\n\n"
        elif '(c)' in art6_basis:
            section += "Prelucrarea este necesară pentru îndeplinirea unei obligații legale care îi revine operatorului.\n\n"
        elif '(f)' in art6_basis:
            section += "Prelucrarea este necesară în scopul intereselor legitime urmărite de operator sau de o parte terță, "
            section += "cu excepția cazului în care prevalează interesele sau drepturile și libertățile fundamentale ale persoanei vizate.\n\n"
            section += "*Notă: Pentru acest temei, a fost efectuată o Evaluare a Interesului Legitim (LIA) - vezi Secțiunea 3.5.*\n\n"

        # Date speciale Art. 9
        if legal_basis.get('special_categories'):
            section += "**⚠️ CATEGORII SPECIALE DE DATE (Art. 9 GDPR)**\n\n"
            art9_basis = legal_basis.get('art9_basis', 'Nespecificat')
            section += f"**Temei Art. 9(2):** {art9_basis}\n\n"
            section += "Prelucrarea categoriilor speciale de date se realizează în conformitate cu excepțiile prevăzute de Art. 9(2) GDPR.\n\n"

        # 2.4 Categorii de date personale
        section += self._generate_data_categories_subsection(processing_info)

        # 2.5 Categorii de persoane vizate
        section += self._generate_data_subjects_subsection(processing_info)

        # 2.6 Destinatari
        section += self._generate_recipients_subsection(processing_info)

        # 2.7 Transferuri internaționale
        section += self._generate_transfers_subsection(processing_info)

        # 2.8 Durata de stocare
        section += self._generate_retention_subsection(processing_info)

        # 2.9 Descriere funcțională și diagrame
        section += "### 2.9. DESCRIERE FUNCȚIONALĂ - FLUXUL DE DATE\n\n"

        if 'dfd' in diagrams:
            section += "#### Figura 1: Diagrama fluxului de date\n\n"
            section += diagrams['dfd'] + "\n\n"

        if 'lifecycle' in diagrams:
            section += "#### Figura 2: Ciclul de viață al datelor\n\n"
            section += diagrams['lifecycle'] + "\n\n"

        section += "**Explicație flux:**\n\n"
        section += "Datele cu caracter personal sunt colectate direct de la persoanele vizate, "
        section += "prelucrate în sistemele operatorului conform scopurilor definite, "
        section += "și eventual comunicate către destinatari în baza temeiului juridic.\n\n"

        return section

    def _generate_data_categories_subsection(self, processing_info: Dict) -> str:
        """Subsecțiune 2.4: Categorii de date personale"""
        subsection = "### 2.4. CATEGORII DE DATE CU CARACTER PERSONAL\n\n"

        data_categories = processing_info.get('data_categories', {})

        # Date comune
        common_data = data_categories.get('common_data_art6', [])
        if common_data:
            subsection += "#### A. Date comune (Art. 6 GDPR):\n\n"
            for data_item in common_data:
                subsection += f"- {data_item}\n"
            subsection += "\n"

        # Date speciale Art. 9
        special_data = data_categories.get('special_categories_art9', [])
        if special_data:
            subsection += "#### B. Categorii speciale de date (Art. 9 GDPR):\n\n"
            subsection += "**⚠️ ATENȚIE: RISC RIDICAT**\n\n"
            for data_item in special_data:
                subsection += f"- ⚠️ {data_item}\n"
            subsection += "\n"
            subsection += "*Conform Art. 9 GDPR, aceste date necesită măsuri de securitate sporite.*\n\n"

        # Date condamnări Art. 10
        criminal_data = data_categories.get('criminal_records_art10', [])
        if criminal_data:
            subsection += "#### C. Date privind condamnările penale (Art. 10 GDPR):\n\n"
            for data_item in criminal_data:
                subsection += f"- {data_item}\n"
            subsection += "\n"

        # Volume
        volume = processing_info.get('data_volume')
        if volume:
            subsection += f"**Volume estimate:** {volume:,} persoane vizate\n\n"

            if volume > 10000:
                subsection += "*Notă: Prelucrare la scară largă conform WP29 Guidelines*\n\n"

        # Surse
        sources = processing_info.get('data_sources', [])
        if sources:
            subsection += "**Surse date:**\n\n"
            for source in sources:
                subsection += f"- {source}\n"
            subsection += "\n"

        return subsection

    def _generate_data_subjects_subsection(self, processing_info: Dict) -> str:
        """Subsecțiune 2.5: Persoane vizate"""
        subsection = "### 2.5. CATEGORII DE PERSOANE VIZATE\n\n"

        data_subjects = processing_info.get('data_subjects', [])

        if data_subjects:
            subsection += "Prelucrarea vizează următoarele categorii de persoane:\n\n"

            for subject in data_subjects:
                category = subject.get('category', 'Necunoscut')
                subsection += f"- **{category.capitalize()}**"

                # Flag pentru persoane vulnerabile
                if category.lower() in ['copii', 'minori', 'pacienți', 'angajați']:
                    subsection += " ⚠️ *Persoane vulnerabile - risc crescut*"

                subsection += "\n"

            subsection += "\n"

            # Verifică copii
            has_children = any('copii' in s.get('category', '').lower() or 'minori' in s.get('category', '').lower()
                             for s in data_subjects)
            if has_children:
                subsection += "**⚠️ ATENȚIE: PRELUCRARE DATE COPII**\n\n"
                subsection += "Conform Art. 8 GDPR, pentru copii sub 16 ani este necesar consimțământul titularului "
                subsection += "responsabilității părintești.\n\n"

        else:
            subsection += "**⚠️ ATENȚIE:** Categoriile de persoane vizate nu au fost definite - necesită completare.\n\n"

        return subsection

    def _generate_recipients_subsection(self, processing_info: Dict) -> str:
        """Subsecțiune 2.6: Destinatari"""
        subsection = "### 2.6. DESTINATARI\n\n"

        recipients_internal = processing_info.get('recipients_internal', [])
        recipients_external = processing_info.get('recipients_external', [])

        if recipients_internal:
            subsection += "#### A. Destinatari interni:\n\n"
            for recip in recipients_internal:
                subsection += f"- {recip}\n"
            subsection += "\n"

        if recipients_external:
            subsection += "#### B. Destinatari externi (terți):\n\n"
            for recip in recipients_external:
                subsection += f"- {recip}\n"
            subsection += "\n"
            subsection += "*Comunicarea către terți se realizează conform temeiului juridic și cu respectarea Art. 6 GDPR.*\n\n"

        if not recipients_internal and not recipients_external:
            subsection += "**Status:** Datele nu sunt comunicate către alți destinatari.\n\n"
            subsection += "Prelucrarea este realizată exclusiv de operator (și împuterniciți, dacă este cazul).\n\n"

        return subsection

    def _generate_transfers_subsection(self, processing_info: Dict) -> str:
        """Subsecțiune 2.7: Transferuri internaționale"""
        subsection = "### 2.7. TRANSFERURI INTERNAȚIONALE DE DATE\n\n"

        transfers = processing_info.get('international_transfers', [])

        if transfers and transfers[0].get('has_transfer'):
            subsection += "**⚠️ EXISTĂ TRANSFERURI DE DATE ÎN AFARA UE/SEE**\n\n"

            subsection += "**Țări destinație:** [Specifică țările]\n\n"

            safeguards = transfers[0].get('safeguards', [])
            if safeguards:
                subsection += "**Garanții implementate (Art. 46 GDPR):**\n\n"
                for safeguard in safeguards:
                    subsection += f"- {safeguard}\n"
                subsection += "\n"
            else:
                subsection += "**❌ RISC CRITIC: NU EXISTĂ GARANȚII IDENTIFICATE**\n\n"
                subsection += "**ACȚIUNE OBLIGATORIE:** Implementare Clauze Contractuale Standard (SCCs) și/sau "
                subsection += "efectuare Transfer Impact Assessment conform Schrems II.\n\n"

            subsection += "**Conformitate Schrems II:**\n\n"
            subsection += "Conform jurisprudenței CJUE (C-311/18 Schrems II), transferurile către țări terțe necesită:\n\n"
            subsection += "1. Evaluare nivel protecție țară destinație\n"
            subsection += "2. Măsuri suplimentare tehnice/organizatorice (ex: criptare end-to-end)\n"
            subsection += "3. SCCs actualizate conform Decizia UE 2021/914\n\n"

        else:
            subsection += "**Status:** NU există transferuri de date personale în afara Uniunii Europene/Spațiului Economic European.\n\n"
            subsection += "Toate datele sunt procesate și stocate exclusiv în UE/SEE.\n\n"

        return subsection

    def _generate_retention_subsection(self, processing_info: Dict) -> str:
        """Subsecțiune 2.8: Durata de stocare"""
        subsection = "### 2.8. DURATA DE STOCARE (LIMITARE STOCARE - Art. 5(1)(e))\n\n"

        retention_periods = processing_info.get('retention_periods', [])

        if retention_periods:
            subsection += "**Perioade de păstrare:**\n\n"
            subsection += "| Categorie date | Perioadă păstrare | Justificare |\n"
            subsection += "|----------------|-------------------|-------------|\n"

            for period in retention_periods:
                period_text = period.get('period', 'Nespecificat')
                subsection += f"| Date generale | {period_text} | Conform scopului și legislației aplicabile |\n"

            subsection += "\n"
        else:
            subsection += "**⚠️ ATENȚIE:** Perioadele de păstrare nu sunt definite clar.\n\n"
            subsection += "**ACȚIUNE NECESARĂ:** Definire perioade clare conform Art. 5(1)(e) GDPR.\n\n"

        subsection += "**Criterii pentru determinarea perioadei:**\n\n"
        subsection += "- Durata necesară pentru îndeplinirea scopurilor prelucrării\n"
        subsection += "- Obligații legale de păstrare (ex: legislație fiscală, contabilă)\n"
        subsection += "- Termene de prescripție legale\n"
        subsection += "- Dreptul persoanelor vizate la ștergere (Art. 17)\n\n"

        subsection += "**Procedură ștergere/anonimizare:**\n\n"
        subsection += "La expirarea perioadei de păstrare, datele sunt:\n"
        subsection += "- Șterse definitiv din sistemele operatorului, SAU\n"
        subsection += "- Anonimizate ireversibil (astfel încât să nu mai fie date personale)\n\n"

        return subsection

    def _generate_section_3_necessity(self, processing_info: Dict) -> str:
        """Secțiunea 3: Evaluarea necesității și proporționalității"""
        section = "## 3. EVALUAREA NECESITĂȚII ȘI PROPORȚIONALITĂȚII\n\n"

        section += "Conform Art. 35(7)(b) GDPR, DPIA trebuie să includă o evaluare a necesității și proporționalității "
        section += "operațiunilor de prelucrare în raport cu scopurile.\n\n"

        # 3.1 Justificare temei
        section += "### 3.1. JUSTIFICAREA TEMEIULUI JURIDIC\n\n"

        legal_basis = processing_info.get('legal_basis', {})
        art6_basis = legal_basis.get('art6_basis', '')

        section += f"Prelucrarea se bazează pe **{art6_basis}**.\n\n"

        section += "**Analiză conformitate:**\n\n"
        section += "Temeiul juridic ales este adecvat deoarece:\n"
        section += "- Corespunde naturii și scopului prelucrării\n"
        section += "- Este în conformitate cu legislația aplicabilă\n"
        section += "- Nu există temeiuri mai puțin intruzive disponibile\n\n"

        # 3.2 Test necesitate
        section += "### 3.2. TESTUL NECESITĂȚII\n\n"

        section += "**Întrebare:** Este prelucrarea datelor cu caracter personal necesară pentru îndeplinirea scopurilor declarate?\n\n"

        section += "**Răspuns:** DA\n\n"

        section += "**Justificare:**\n\n"
        purposes = processing_info.get('purposes', [])
        if purposes:
            section += f"Pentru îndeplinirea scopului principal (\"{purposes[0]}\"), "
            section += "prelucrarea datelor personale este strict necesară și nu poate fi realizată prin mijloace alternative.\n\n"

        section += "**Alternative evaluate:**\n\n"
        section += "Au fost evaluate următoarele alternative:\n"
        section += "- Colectare date anonime: ❌ Nu permite îndeplinirea scopului\n"
        section += "- Reducere volum date: ✓ Implementat - se colectează doar minimul necesar\n"
        section += "- Pseudonimizare: ✓ Implementată unde posibil\n\n"

        # 3.3 Test proporționalitate
        section += "### 3.3. TESTUL PROPORȚIONALITĂȚII\n\n"

        section += "**Întrebare:** Este prelucrarea proporțională cu scopul urmărit?\n\n"

        section += "**Răspuns:** DA\n\n"

        section += "**Analiză:**\n\n"
        section += "1. **Minimizare date (Art. 5(1)(c)):**\n"
        section += "   - Sunt colectate DOAR categoriile de date strict necesare\n"
        section += "   - Nu există date excesive sau irelevante\n\n"

        section += "2. **Limitare scop (Art. 5(1)(b)):**\n"
        section += "   - Datele sunt folosite exclusiv pentru scopurile declarate\n"
        section += "   - Nu există prelucrare ulterioară incompatibilă\n\n"

        section += "3. **Limitare stocare (Art. 5(1)(e)):**\n"
        section += "   - Perioade de păstrare definite și justificate\n"
        section += "   - Ștergere automată la expirare\n\n"

        # 3.4 Analiză alternative
        section += "### 3.4. ANALIZĂ ALTERNATIVE MAI PUȚIN INTRUZIVE\n\n"

        section += "Au fost evaluate următoarele metode alternative de prelucrare, mai puțin intruzive:\n\n"

        section += "| Alternativă | Fezabilitate | Decizie |\n"
        section += "|-------------|--------------|----------|\n"
        section += "| Anonimizare completă | ❌ Nu permite identificare persoane | Respinsă |\n"
        section += "| Pseudonimizare | ✓ Posibilă pentru anumite scopuri | **Adoptată** |\n"
        section += "| Agregare date | ⚠️ Parțial posibilă | Adoptată unde aplicabil |\n"
        section += "| Criptare end-to-end | ✓ Tehnică disponibilă | **Adoptată** |\n\n"

        # 3.5 LIA (dacă e cazul)
        if '(f)' in art6_basis:
            section += "### 3.5. LEGITIMATE INTEREST ASSESSMENT (LIA) - Art. 6(1)(f)\n\n"

            section += "Întrucât prelucrarea se bazează pe interes legitim, conform Guidelines EDPB 1/2024, "
            section += "este necesară o evaluare în trei pași:\n\n"

            section += "#### Pasul 1: Test legitimitate interes\n\n"
            section += "**Interesul legitim urmărit:** [Descrie interesul]\n\n"
            section += "**Este interesul legitim?** DA - interesul este:\n"
            section += "- Legal (nu încalcă legea)\n"
            section += "- Clar articulat\n"
            section += "- Reprezentând un beneficiu real pentru operator/terți\n\n"

            section += "#### Pasul 2: Test necesitate\n\n"
            section += "**Este prelucrarea necesară pentru interes?** DA\n\n"
            section += "Nu există mijloace mai puțin intruzive de a atinge același scop.\n\n"

            section += "#### Pasul 3: Test balansare\n\n"
            section += "**Balansare interese operator vs. drepturi persoane vizate:**\n\n"

            section += "| Factor | Analiză |\n"
            section += "|--------|----------|\n"
            section += "| Așteptări rezonabile | Persoanele vizate pot anticipa în mod rezonabil această prelucrare |\n"
            section += "| Impact asupra persoanelor | Impact limitat, măsuri de protecție implementate |\n"
            section += "| Categorie date | Date comune, fără categorii speciale |\n"
            section += "| Transparență | Informare clară prin clauză de informare |\n\n"

            section += "**Concluzie LIA:** Interesul legitim este valid și prevalează, cu condiția implementării măsurilor de atenuare.\n\n"

        return section

    def _generate_section_4_risks(self, risks: List[Risk], diagrams: Dict[str, str]) -> str:
        """Secțiunea 4: Evaluarea riscurilor"""
        section = "## 4. EVALUAREA RISCURILOR PENTRU DREPTURILE ȘI LIBERTĂȚILE PERSOANELOR VIZATE\n\n"

        section += "Conform Art. 35(7)(c) GDPR, DPIA trebuie să includă evaluarea riscurilor pentru drepturile "
        section += "și libertățile persoanelor vizate.\n\n"

        # 4.1 Metodologie
        section += "### 4.1. METODOLOGIE EVALUARE RISC\n\n"

        section += "Evaluarea riscurilor se realizează conform metodologiei WP29 Guidelines (WP248rev.01), "
        section += "bazată pe o matrice Probabilitate × Severitate.\n\n"

        section += "**Scala severitate (impact asupra persoanelor):**\n\n"
        section += "| Nivel | Descriere | Exemple |\n"
        section += "|-------|-----------|----------|\n"
        section += "| 1 - Neglijabilă | Impact minim, inconvenient minor | Email marketing nesolicitat ușor dezabonat |\n"
        section += "| 2 - Limitată | Impact minor, posibile nemulțumiri | Întârziere răspuns solicitări |\n"
        section += "| 3 - Semnificativă | Impact important, prejudicii posibile | Discriminare, pierdere oportunități |\n"
        section += "| 4 - Maximă | Impact sever, consecințe grave | Riscuri fizice, furt identitate, daune majore |\n\n"

        section += "**Scala probabilitate:**\n\n"
        section += "| Nivel | Descriere | Exemple |\n"
        section += "|-------|-----------|----------|\n"
        section += "| 1 - Neglijabilă | Foarte improbabil | Toate măsurile de securitate funcționează |\n"
        section += "| 2 - Limitată | Posibil dar puțin probabil | Măsuri bune cu vulnerabilități minore |\n"
        section += "| 3 - Semnificativă | Probabil în anumite condiții | Măsuri parțiale, unele controale lipsesc |\n"
        section += "| 4 - Maximă | Foarte probabil sau aproape sigur | Fără măsuri adecvate |\n\n"

        section += "**Niveluri risc (Severitate × Probabilitate):**\n\n"
        section += "- 🟢 **Risc scăzut (1-4):** Acceptabil\n"
        section += "- 🟡 **Risc mediu (5-8):** Necesită măsuri suplimentare\n"
        section += "- 🟠 **Risc ridicat (9-12):** Necesită măsuri imediate\n"
        section += "- 🔴 **Risc critic (13-16):** INACCEPTABIL - Consultare prealabilă ANSPDCP obligatorie\n\n"

        # 4.2 Riscuri identificate
        section += "### 4.2. RISCURI IDENTIFICATE ȘI EVALUATE\n\n"

        section += f"Au fost identificate **{len(risks)} riscuri** pentru această operațiune de prelucrare.\n\n"

        for risk in risks:
            section += f"#### RISC #{risk.risk_id}: {risk.name.upper()}\n\n"

            section += f"**Descriere:** {risk.description}\n\n"

            section += f"**Sursa riscului:** {risk.source}\n\n"

            if risk.threat_scenarios:
                section += "**Scenarii amenințătoare:**\n\n"
                for idx, scenario in enumerate(risk.threat_scenarios, 1):
                    section += f"{idx}. {scenario}\n"
                section += "\n"

            # Evaluare risc inerent
            section += "**EVALUARE RISC INERENT (înainte de măsuri):**\n\n"

            severity_emoji = self._get_severity_emoji(risk.inherent_severity.value)
            prob_emoji = self._get_severity_emoji(risk.inherent_probability.value)

            section += f"- **Severitate (impact):** {severity_emoji} **Nivel {risk.inherent_severity.value}** - {risk.inherent_severity.name}\n"
            section += f"  - *Justificare:* {risk.inherent_severity_justification}\n\n"

            section += f"- **Probabilitate:** {prob_emoji} **Nivel {risk.inherent_probability.value}** - {risk.inherent_probability.name}\n"
            section += f"  - *Justificare:* {risk.inherent_probability_justification}\n\n"

            level_emoji = self._get_risk_level_emoji(risk.inherent_level.value)
            section += f"- **Nivel risc inerent:** {level_emoji} **Scor {risk.inherent_score}** - {risk.inherent_level.value.upper()}\n\n"

            section += "---\n\n"

        # 4.3 Matrice risc
        section += "### 4.3. MATRICE GENERALĂ DE RISC\n\n"

        if 'risk_matrix' in diagrams:
            section += diagrams['risk_matrix'] + "\n\n"

        return section

    def _generate_section_5_measures(
        self,
        processing_info: Dict,
        risks: List[Risk],
        diagrams: Dict[str, str]
    ) -> str:
        """Secțiunea 5: Măsuri tehnice și organizatorice"""
        section = "## 5. MĂSURI TEHNICE ȘI ORGANIZATORICE (Art. 32 GDPR)\n\n"

        section += "Conform Art. 35(7)(d) GDPR, DPIA trebuie să includă măsurile preconizate pentru "
        section += "a trata riscurile, inclusiv garanții, măsuri și mecanisme de securitate.\n\n"

        # 5.1 Măsuri de securitate existente și propuse
        section += "### 5.1. MĂSURI DE SECURITATE\n\n"

        security_measures = processing_info.get('security_measures', {})

        # 5.1.1 Măsuri tehnice
        section += "#### 5.1.1. Măsuri tehnice\n\n"

        section += "**Criptare (Art. 32(1)(a)):**\n\n"
        encryption = security_measures.get('encryption', [])
        if encryption:
            for measure in encryption:
                section += f"- ✓ {measure}\n"
        else:
            section += "- ❌ **ACȚIUNE NECESARĂ:** Implementare criptare AES-256 pentru date în repaus\n"
            section += "- ❌ **ACȚIUNE NECESARĂ:** Implementare TLS 1.3 pentru date în tranzit\n"
        section += "\n"

        section += "**Control acces și autentificare:**\n\n"
        access_control = security_measures.get('access_control', [])
        if access_control:
            for measure in access_control:
                section += f"- ✓ {measure}\n"
        else:
            section += "- ❌ **ACȚIUNE NECESARĂ:** Implementare control acces bazat pe roluri (RBAC)\n"
            section += "- ❌ **ACȚIUNE NECESARĂ:** Autentificare cu doi factori (2FA/MFA)\n"
        section += "\n"

        section += "**Backup și recuperare (Art. 32(1)(c)):**\n\n"
        backup = security_measures.get('backup', [])
        if backup:
            for measure in backup:
                section += f"- ✓ {measure}\n"
        else:
            section += "- ❌ **ACȚIUNE NECESARĂ:** Implementare backup automat zilnic\n"
            section += "- ❌ **ACȚIUNE NECESARĂ:** Stocare backup off-site criptat\n"
        section += "\n"

        # 5.1.2 Măsuri organizatorice
        section += "#### 5.1.2. Măsuri organizatorice\n\n"

        section += "**Politici și proceduri:**\n\n"
        section += "- ✓ Politică de confidențialitate a datelor\n"
        section += "- ✓ Proceduri de securitate a informațiilor\n"
        section += "- ✓ Politică clean desk / clear screen\n\n"

        section += "**Instruire personal (Art. 32(4)):**\n\n"
        section += "- ✓ Training GDPR anual pentru tot personalul\n"
        section += "- ✓ Training securitate cibernetică\n"
        section += "- ✓ Campanii awareness (ex: phishing simulation)\n\n"

        # 5.2 Măsuri pentru fiecare risc
        section += "### 5.2. MĂSURI DE ATENUARE PENTRU FIECARE RISC\n\n"

        for risk in risks:
            section += f"#### Măsuri pentru Risc #{risk.risk_id}: {risk.name}\n\n"

            if risk.mitigation_measures:
                for idx, measure in enumerate(risk.mitigation_measures, 1):
                    section += f"{idx}. {measure}\n"
                section += "\n"

            # Risc rezidual
            residual_emoji = self._get_risk_level_emoji(risk.residual_level.value)
            section += f"**Risc rezidual (după măsuri):** {residual_emoji} **Scor {risk.residual_score}** - {risk.residual_level.value.upper()}\n\n"

            if risk.residual_level in [RiskLevel.LOW, RiskLevel.MEDIUM]:
                section += "✓ Riscul rezidual este acceptabil.\n\n"
            else:
                section += "⚠️ **ATENȚIE:** Risc rezidual ridicat - consultare prealabilă ANSPDCP necesară.\n\n"

            section += "---\n\n"

        # 5.3 Drepturi persoane vizate
        section += "### 5.3. PROCEDURI PENTRU DREPTURILE PERSOANELOR VIZATE (Art. 12-22)\n\n"

        section += "Operatorul a implementat proceduri pentru facilitarea exercitării drepturilor:\n\n"

        section += "| Drept | Procedură | Termen răspuns |\n"
        section += "|-------|-----------|----------------|\n"
        section += "| Drept acces (Art. 15) | Formular solicitare online + email | 1 lună |\n"
        section += "| Drept rectificare (Art. 16) | Procedură corectare date | 1 lună |\n"
        section += "| Drept ștergere (Art. 17) | Procedură ștergere automată | 1 lună |\n"
        section += "| Drept restricționare (Art. 18) | Marcare temporară date | 1 lună |\n"
        section += "| Drept portabilitate (Art. 20) | Export format CSV/JSON | 1 lună |\n"
        section += "| Drept opoziție (Art. 21) | Procedură stop procesare | Imediat |\n\n"

        section += "*Notă: Termenul poate fi extins cu 2 luni suplimentare în cazuri complexe, cu informare persoanei vizate.*\n\n"

        # 5.4 Gestionare incidente
        section += "### 5.4. PROCEDURĂ GESTIONARE INCIDENTE DE SECURITATE (Art. 33-34)\n\n"

        section += "**Plan de răspuns la incidente:**\n\n"
        section += "1. **Detectare și raportare:**\n"
        section += "   - Orice angajat detectează incident → raportare imediată către responsabil securitate\n"
        section += "   - Evaluare preliminară în 24 ore\n\n"

        section += "2. **Investigare și containment:**\n"
        section += "   - Echipă de răspuns activată\n"
        section += "   - Izolare sistem afectat\n"
        section += "   - Investigare cauză și extent\n\n"

        section += "3. **Notificare ANSPDCP (Art. 33):**\n"
        section += "   - **Termen: 72 ore** de la conștientizare\n"
        section += "   - Responsabil: [Nume DPO / Responsabil]\n"
        section += "   - Procedură: Formular ANSPDCP + dovezi\n\n"

        section += "4. **Notificare persoane vizate (Art. 34):**\n"
        section += "   - DOAR dacă riscul este ridicat pentru persoane\n"
        section += "   - Limbaj clar, non-tehnic\n"
        section += "   - Recomandări măsuri protecție\n\n"

        section += "5. **Remediere și lessons learned:**\n"
        section += "   - Corectare vulnerabilitate\n"
        section += "   - Raport post-incident\n"
        section += "   - Actualizare proceduri\n\n"

        # 5.5 Plan implementare (dacă există timeline)
        if 'timeline' in diagrams:
            section += "### 5.5. PLAN IMPLEMENTARE MĂSURI\n\n"
            section += diagrams['timeline'] + "\n\n"

        return section

    def _generate_section_6_consultations(self, operator_info: Dict, risks: List[Risk]) -> str:
        """Secțiunea 6: Consultări"""
        section = "## 6. CONSULTĂRI\n\n"

        # 6.1 Consultare DPO
        section += "### 6.1. CONSULTARE RESPONSABIL PROTECȚIE DATE (DPO) - Art. 35(2)\n\n"

        has_dpo = operator_info.get('has_dpo', False)

        if has_dpo:
            section += f"**Status:** ✓ DPO consultat\n\n"
            section += f"**DPO:** {operator_info.get('dpo_name', '')}\n\n"
            section += f"**Data consultării:** {datetime.now().strftime('%d.%m.%Y')}\n\n"

            section += "**Recomandări DPO:**\n\n"
            section += "DPO a revizuit DPIA-ul și a furnizat următoarele recomandări:\n\n"
            section += "1. Implementare măsurilor de securitate identificate în Secțiunea 5\n"
            section += "2. Monitorizare continuă a riscurilor reziduale\n"
            section += "3. Revizuire DPIA la schimbări substanțiale sau anual\n"
            section += "4. [Alte recomandări specifice]\n\n"

            section += "**Poziția DPO:** ✓ DPIA este conform și complet\n\n"

        else:
            section += "**Status:** Operatorul nu are obligația de a desemna DPO conform Art. 37 GDPR.\n\n"
            section += "Cu toate acestea, DPIA a fost revizuit de [Responsabil intern protecție date / Manager].\n\n"

        # 6.2 Consultare persoane vizate
        section += "### 6.2. CONSULTARE PERSOANE VIZATE - Art. 35(9)\n\n"

        section += "Conform Art. 35(9) GDPR, operatorul are obligația să consulte persoanele vizate sau "
        section += "reprezentanții acestora în legătură cu prelucrarea preconizată, **dacă este cazul**.\n\n"

        section += "**Status:** [DA / NU se aplică]\n\n"
        section += "*Motivare:* [Explicare dacă a fost efectuată consultarea sau de ce nu este aplicabilă]\n\n"

        # 6.3 Consultare prealabilă ANSPDCP
        section += "### 6.3. CONSULTARE PREALABILĂ ANSPDCP - Art. 36\n\n"

        # Verifică dacă există riscuri reziduale ridicate
        high_risks = [r for r in risks if r.residual_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]]

        if high_risks:
            section += "**⚠️ CONSULTARE PREALABILĂ OBLIGATORIE**\n\n"
            section += f"Au fost identificate **{len(high_risks)} risc(uri) rezidual(e) ridicat(e)/critic(e)** "
            section += "care rămân ridicate chiar și după implementarea măsurilor.\n\n"

            section += "Conform Art. 36(1) GDPR, operatorul are obligația de a consulta ANSPDCP **înainte** "
            section += "de a demara prelucrarea.\n\n"

            section += "**Riscuri reziduale ridicate:**\n\n"
            for risk in high_risks:
                section += f"- Risc #{risk.risk_id}: {risk.name} - Nivel rezidual: {risk.residual_level.value}\n"
            section += "\n"

            section += "**Procedură consultare:**\n\n"
            section += "1. Depunere cerere consultare prealabilă la ANSPDCP\n"
            section += "2. Documentație: acest DPIA + documente suport\n"
            section += "3. Termen răspuns ANSPDCP: 8 săptămâni (extins la 14 săptămâni dacă complex)\n"
            section += "4. **IMPORTANT:** Prelucrarea NU poate începe fără răspuns pozitiv ANSPDCP\n\n"

        else:
            section += "**Status:** ✓ Consultare prealabilă ANSPDCP NU este necesară\n\n"
            section += "Toate riscurile reziduale au fost reduse la nivel scăzut sau mediu prin măsurile implementate.\n\n"
            section += "Operatorul poate proceda cu prelucrarea, cu condiția implementării tuturor măsurilor din Secțiunea 5.\n\n"

        return section

    def _generate_section_7_conclusions(self, risks: List[Risk], processing_info: Dict) -> str:
        """Secțiunea 7: Concluzii și aprobare"""
        section = "## 7. CONCLUZII ȘI APROBARE\n\n"

        # 7.1 Nivel general de risc
        section += "### 7.1. NIVEL GENERAL DE RISC\n\n"

        # Calculează nivel general
        critical_risks = len([r for r in risks if r.residual_level == RiskLevel.CRITICAL])
        high_risks = len([r for r in risks if r.residual_level == RiskLevel.HIGH])
        medium_risks = len([r for r in risks if r.residual_level == RiskLevel.MEDIUM])
        low_risks = len([r for r in risks if r.residual_level == RiskLevel.LOW])

        section += "**Distribuție riscuri reziduale:**\n\n"
        section += f"- 🔴 Critic: {critical_risks}\n"
        section += f"- 🟠 Ridicat: {high_risks}\n"
        section += f"- 🟡 Mediu: {medium_risks}\n"
        section += f"- 🟢 Scăzut: {low_risks}\n\n"

        if critical_risks > 0 or high_risks > 0:
            overall_level = "🔴 RIDICAT"
        elif medium_risks > low_risks:
            overall_level = "🟡 MEDIU"
        else:
            overall_level = "🟢 SCĂZUT"

        section += f"**Nivel general de risc:** {overall_level}\n\n"

        # 7.2 Acceptabilitate
        section += "### 7.2. ACCEPTABILITATEA PRELUCRĂRII\n\n"

        if critical_risks > 0 or high_risks >= 2:
            section += "☐ Prelucrarea NU este acceptabilă în forma actuală\n\n"
            section += "**Motive:**\n"
            section += "- Riscuri reziduale ridicate/critice persistă\n"
            section += "- Consultare prealabilă ANSPDCP obligatorie (Art. 36)\n\n"
            acceptable = False
        elif high_risks == 1:
            section += "☑ Prelucrarea este ACCEPTABILĂ CONDIȚIONAT\n\n"
            section += "**Condiții:**\n"
            section += "- Consultare prealabilă ANSPDCP recomandată\n"
            section += "- Implementare obligatorie toate măsurile din Secțiunea 5\n"
            section += "- Monitorizare riguroasă risc rezidual ridicat\n\n"
            acceptable = True
        else:
            section += "☑ Prelucrarea este ACCEPTABILĂ\n\n"
            section += "**Condiții:**\n"
            section += "- Implementare măsurilor propuse în Secțiunea 5\n"
            section += "- Respectare principii GDPR (Art. 5)\n"
            section += "- Monitorizare și revizuire periodică\n\n"
            acceptable = True

        # 7.3 Condiții implementare
        section += "### 7.3. CONDIȚII DE IMPLEMENTARE\n\n"

        section += "Pentru ca prelucrarea să fie conformă GDPR, următoarele măsuri trebuie implementate **ÎNAINTE** de inițiere:\n\n"

        section += "**Măsuri critice (P1 - OBLIGATORII ÎNAINTE DE START):**\n\n"
        section += "1. Implementare criptare AES-256 pentru date în repaus\n"
        section += "2. Implementare autentificare 2FA pentru toate conturile\n"
        section += "3. Semnare contracte Art. 28 cu toți împuterniciti\n"

        if processing_info.get('international_transfers'):
            section += "4. Implementare SCCs pentru transferuri internaționale\n"

        section += "\n"

        section += "**Măsuri importante (P2 - în 30 zile):**\n\n"
        section += "1. Implementare proceduri drepturi persoane vizate\n"
        section += "2. Instruire personal GDPR\n"
        section += "3. Implementare procedură gestionare incidente\n\n"

        section += "**Măsuri secundare (P3 - în 90 zile):**\n\n"
        section += "1. Audit securitate de către terț\n"
        section += "2. Implementare monitorizare automată\n\n"

        # 7.4 Plan revizuire
        section += "### 7.4. PLAN REVIZUIRE DPIA\n\n"

        section += "Conform Art. 35(11) GDPR, DPIA trebuie revizuit periodic, în special la modificări.\n\n"

        section += "**Revizuire obligatorie la:**\n\n"
        section += "- ✓ Modificări substanțiale ale operațiunii de prelucrare\n"
        section += "- ✓ Schimbări în scopuri sau categorii de date\n"
        section += "- ✓ Introducere tehnologii noi\n"
        section += "- ✓ Incidente de securitate majore\n"
        section += "- ✓ Modificări legislative relevante\n\n"

        section += "**Revizuire planificată:**\n\n"
        next_year = datetime.now().year + 1
        section += f"- Următoarea revizuire: **{datetime.now().strftime('%B')} {next_year}**\n"
        section += "- Frecvență: **Anuală** (minim)\n"
        section += "- Responsabil: DPO / Responsabil protecție date\n\n"

        # 7.5 Aprobare
        section += "### 7.5. APROBARE\n\n"

        section += "Prezentul DPIA a fost elaborate în conformitate cu Art. 35 GDPR și Guidelines WP29 (WP248rev.01).\n\n"

        section += "**Aprobare:**\n\n"
        section += "```\n"
        section += "Data: _______________\n\n"
        section += "Reprezentant legal operator:\n"
        section += "Nume și funcție: _______________________________\n"
        section += "Semnătură: _______________________________\n\n"

        if processing_info.get('has_dpo'):
            section += "Responsabil protecție date (DPO):\n"
            section += f"Nume: {processing_info.get('dpo_name', '_______________________________')}\n"
            section += "Semnătură: _______________________________\n"

        section += "```\n\n"

        return section

    def _generate_annexes(self, legal_references: List, diagrams: Dict[str, str]) -> str:
        """Generează anexe"""
        annexes = "## ANEXE\n\n"

        # Anexa 1: Referințe legislative
        annexes += "### ANEXA 1: REFERINȚE LEGISLATIVE ȘI JURISPRUDENȚĂ\n\n"
        annexes += "*Vezi secțiune separată generată de modulul Web Research*\n\n"

        # Anexa 2: Diagrame suplimentare
        if 'architecture' in diagrams or 'roles' in diagrams:
            annexes += "### ANEXA 2: DIAGRAME SUPLIMENTARE\n\n"

            if 'architecture' in diagrams:
                annexes += "#### Figura: Arhitectură sisteme IT\n\n"
                annexes += diagrams['architecture'] + "\n\n"

            if 'roles' in diagrams:
                annexes += "#### Figura: Roluri și responsabilități\n\n"
                annexes += diagrams['roles'] + "\n\n"

        # Anexa 3: Metadata
        annexes += "### ANEXA 3: METADATA DOCUMENT\n\n"
        annexes += f"- **Software utilizat:** DPIA Generator System v1.0\n"
        annexes += f"- **Data generării:** {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        annexes += f"- **Metodologie:** WP29 Guidelines WP248rev.01\n"
        annexes += f"- **Conformitate:** Art. 35 GDPR\n\n"

        return annexes

    def _get_severity_emoji(self, level: int) -> str:
        """Emoji pentru severitate/probabilitate"""
        emojis = {1: "🟢", 2: "🟡", 3: "🟠", 4: "🔴"}
        return emojis.get(level, "⚪")

    def _get_risk_level_emoji(self, level: str) -> str:
        """Emoji pentru nivel risc"""
        emojis = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}
        return emojis.get(level, "⚪")
