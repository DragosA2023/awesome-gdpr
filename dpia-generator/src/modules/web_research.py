"""
Web Research - Căutare legislație și jurisprudență relevantă pentru DPIA
Folosește baza de date awesome-gdpr și verifică resurse online
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class LegalReference:
    """Referință legislativă sau jurisprudență"""
    type: str  # "gdpr_article", "cjeu_case", "edpb_guideline", "national_law", "anspdcp_decision"
    reference: str  # Ex: "Art. 35 GDPR", "C-311/18 Schrems II"
    title: str
    url: Optional[str] = None
    relevance: str = ""  # Relevanță pentru DPIA curent
    key_points: List[str] = field(default_factory=list)


class WebResearch:
    """Cercetare legislație și jurisprudență pentru DPIA"""

    def __init__(self, awesome_gdpr_path: Optional[Path] = None):
        """
        Args:
            awesome_gdpr_path: Path către repository awesome-gdpr
        """
        self.awesome_gdpr_path = awesome_gdpr_path or Path("/home/user/awesome-gdpr")
        self.legal_references: List[LegalReference] = []

    def research_for_dpia(
        self,
        processing_characteristics: Dict
    ) -> List[LegalReference]:
        """
        Cercetează legislație și jurisprudență relevantă

        Args:
            processing_characteristics: Caracteristici prelucrare

        Returns:
            Listă referințe legale relevante
        """
        references = []

        # 1. GDPR Articles - Obligatorii
        references.extend(self._get_gdpr_articles())

        # 2. WP29/EDPB Guidelines pentru DPIA
        references.extend(self._get_dpia_guidelines())

        # 3. Jurisprudență CJUE relevantă
        references.extend(self._get_cjeu_cases(processing_characteristics))

        # 4. ANSPDCP - Legislație și decizii naționale
        references.extend(self._get_anspdcp_resources())

        # 5. Autorități naționale (CNIL, AEPD, ICO) - Best practices
        references.extend(self._get_dpa_resources(processing_characteristics))

        self.legal_references = references
        return references

    def _get_gdpr_articles(self) -> List[LegalReference]:
        """Returnează articole GDPR esențiale pentru DPIA"""
        articles = [
            LegalReference(
                type="gdpr_article",
                reference="Art. 35 GDPR",
                title="Evaluarea impactului asupra protecției datelor",
                url="https://eur-lex.europa.eu/legal-content/RO/TXT/HTML/?uri=CELEX:32016R0679#d1e3629-1-1",
                relevance="Articol central - definește când și cum se realizează DPIA",
                key_points=[
                    "Obligația de a efectua DPIA când prelucrarea prezintă risc ridicat (Art. 35(1))",
                    "Criteriile specifice: evaluare sistematică, categorii speciale la scară largă, monitorizare sistematică (Art. 35(3))",
                    "Conținutul DPIA (Art. 35(7)): descriere operațiune, evaluare necesitate, evaluare risc, măsuri atenuare",
                    "Consultare DPO obligatorie (Art. 35(2))",
                    "Consultare prealabilă autoritate dacă risc ridicat rămâne (Art. 36)"
                ]
            ),
            LegalReference(
                type="gdpr_article",
                reference="Art. 5 GDPR",
                title="Principii privind prelucrarea datelor cu caracter personal",
                url="https://eur-lex.europa.eu/legal-content/RO/TXT/HTML/?uri=CELEX:32016R0679#d1e1802-1-1",
                relevance="Principiile fundamentale ce trebuie respectate în orice prelucrare",
                key_points=[
                    "Legalitate, echitate, transparență (5(1)(a))",
                    "Limitarea scopului (5(1)(b))",
                    "Minimizarea datelor (5(1)(c))",
                    "Exactitate (5(1)(d))",
                    "Limitarea stocării (5(1)(e))",
                    "Integritate și confidențialitate (5(1)(f))"
                ]
            ),
            LegalReference(
                type="gdpr_article",
                reference="Art. 6 GDPR",
                title="Legalitatea prelucrării",
                url="https://eur-lex.europa.eu/legal-content/RO/TXT/HTML/?uri=CELEX:32016R0679#d1e1888-1-1",
                relevance="Temeiurile juridice pentru prelucrare - esențial pentru justificare DPIA",
                key_points=[
                    "Cele 6 temeiuri: consimțământ, contract, obligație legală, interese vitale, interes public, interes legitim",
                    "Trebuie identificat temei valid înainte de prelucrare"
                ]
            ),
            LegalReference(
                type="gdpr_article",
                reference="Art. 9 GDPR",
                title="Prelucrarea unor categorii speciale de date cu caracter personal",
                url="https://eur-lex.europa.eu/legal-content/RO/TXT/HTML/?uri=CELEX:32016R0679#d1e2090-1-1",
                relevance="Relevant dacă prelucrarea include date medicale, biometrice, genetice, etc.",
                key_points=[
                    "Interdicție generală prelucrare categorii speciale (Art. 9(1))",
                    "Excepții Art. 9(2): consimțământ explicit, obligații muncă, interese vitale, medicină preventivă, etc.",
                    "Risc crescut → măsuri de securitate sporite necesare"
                ]
            ),
            LegalReference(
                type="gdpr_article",
                reference="Art. 32 GDPR",
                title="Securitatea prelucrării",
                url="https://eur-lex.europa.eu/legal-content/RO/TXT/HTML/?uri=CELEX:32016R0679#d1e3326-1-1",
                relevance="Măsurile tehnice și organizatorice obligatorii",
                key_points=[
                    "Pseudonimizare și criptare (Art. 32(1)(a))",
                    "Capacitate asigurare confidențialitate, integritate, disponibilitate (Art. 32(1)(b))",
                    "Capacitate restabilire rapidă date (Art. 32(1)(c))",
                    "Proces testare și evaluare periodică (Art. 32(1)(d))"
                ]
            ),
            LegalReference(
                type="gdpr_article",
                reference="Art. 33-34 GDPR",
                title="Notificarea unei încălcări de date cu caracter personal",
                url="https://eur-lex.europa.eu/legal-content/RO/TXT/HTML/?uri=CELEX:32016R0679#d1e3391-1-1",
                relevance="Proceduri obligatorii în caz de incident - parte din măsuri DPIA",
                key_points=[
                    "Notificare ANSPDCP în 72 ore (Art. 33)",
                    "Notificare persoane vizate dacă risc ridicat (Art. 34)"
                ]
            )
        ]

        return articles

    def _get_dpia_guidelines(self) -> List[LegalReference]:
        """Returnează Guidelines WP29/EDPB specifice pentru DPIA"""
        guidelines = [
            LegalReference(
                type="edpb_guideline",
                reference="WP248rev.01",
                title="Guidelines on Data Protection Impact Assessment (DPIA)",
                url="https://ec.europa.eu/newsroom/article29/items/611236",
                relevance="Ghid oficial WP29 pentru realizare DPIA - ESENȚIAL",
                key_points=[
                    "Metodologia completă pentru DPIA",
                    "Criterii pentru stabilire dacă DPIA este necesară (9 criterii)",
                    "Structura și conținutul DPIA",
                    "Consultare DPO și persoane vizate",
                    "Consultare prealabilă autoritate"
                ]
            ),
            LegalReference(
                type="edpb_guideline",
                reference="Guidelines 1/2024",
                title="Guidelines on Legitimate Interest Assessment",
                url="https://www.edpb.europa.eu/",
                relevance="Relevant dacă temeiul juridic este Art. 6(1)(f) - interes legitim",
                key_points=[
                    "Metodologie LIA (Legitimate Interest Assessment)",
                    "Test necesitatate, test balansare",
                    "Complementar cu DPIA pentru interes legitim"
                ]
            ),
            LegalReference(
                type="edpb_guideline",
                reference="WP251rev.01",
                title="Guidelines on Automated Decision-Making and Profiling",
                url="https://ec.europa.eu/newsroom/article29/items/612053",
                relevance="Relevant pentru prelucrări cu profilare sau decizii automate",
                key_points=[
                    "Aplicarea Art. 22 GDPR",
                    "Măsuri de protecție: intervenție umană, drept contestare",
                    "Transparență algoritmi"
                ]
            )
        ]

        return guidelines

    def _get_cjeu_cases(self, processing_characteristics: Dict) -> List[LegalReference]:
        """Returnează jurisprudență CJUE relevantă"""
        cases = []

        # Schrems II - dacă sunt transferuri internaționale
        if processing_characteristics.get('has_international_transfers'):
            cases.append(LegalReference(
                type="cjeu_case",
                reference="C-311/18",
                title="Schrems II - Data Protection Commissioner v Facebook Ireland și Maximillian Schrems",
                url="https://curia.europa.eu/juris/liste.jsf?num=C-311/18",
                relevance="ESENȚIAL pentru transferuri internaționale de date",
                key_points=[
                    "Invalidare Privacy Shield (2020)",
                    "SCCs rămân valide DAR necesită evaluare case-by-case",
                    "Obligație verificare nivel protecție țară terță",
                    "Măsuri suplimentare tehnice/contractuale necesare dacă țara nu oferă protecție adecvată"
                ]
            ))

        # Cazuri recente privind transparență
        cases.append(LegalReference(
            type="cjeu_case",
            reference="C-203/22",
            title="Transparență algoritmi vs secrete comerciale în credit scoring",
            url="https://curia.europa.eu/",
            relevance="Relevant pentru prelucrări cu scoring sau decizii automate",
            key_points=[
                "Balansare între dreptul la informare (Art. 15) și protecția secretelor comerciale",
                "Transparență algoritmi în decizii automate",
                "Limita protecției secretelor când afectează drepturi persoane vizate"
            ]
        ))

        # Adaugă alte cazuri dacă relevant...

        return cases

    def _get_anspdcp_resources(self) -> List[LegalReference]:
        """Returnează resurse ANSPDCP (România)"""
        references = [
            LegalReference(
                type="anspdcp_decision",
                reference="Decizia 174/2018",
                title="Lista operațiunilor de prelucrare pentru care se impune elaborarea unei evaluări de impact",
                url="https://www.dataprotection.ro/",
                relevance="Listă oficială ANSPDCP cu operațiuni care necesită DPIA - OBLIGATORIU în România",
                key_points=[
                    "10 criterii specifice pentru România",
                    "Include: evaluare/profilare, categorii speciale la scară largă, monitorizare sistematică, tehnologii noi, etc.",
                    "Dacă prelucrarea întrunește cel puțin un criteriu → DPIA obligatorie"
                ]
            ),
            LegalReference(
                type="national_law",
                reference="Legea 190/2018",
                title="Lege privind măsuri de punere în aplicare a GDPR",
                url="https://legislatie.just.ro/Public/DetaliiDocument/203870",
                relevance="Legislație națională complementară GDPR",
                key_points=[
                    "Sancțiuni specifice pentru România",
                    "Proceduri notificare ANSPDCP"
                ]
            ),
            LegalReference(
                type="anspdcp_decision",
                reference="ANSPDCP - Raport Anual 2024",
                title="Raport anual ANSPDCP cu statistici sancțiuni și tendințe",
                url="https://www.dataprotection.ro/",
                relevance="Înțelegere practică aplicare și tendințe enforcement",
                key_points=[
                    "Sancțiuni aplicate în România",
                    "Cazuri frecvente de neconformitate",
                    "Tendințe și arii de focus ale ANSPDCP"
                ]
            )
        ]

        return references

    def _get_dpa_resources(self, processing_characteristics: Dict) -> List[LegalReference]:
        """Returnează resurse de la alte autorități naționale (best practices)"""
        resources = []

        # CNIL - Software open-source DPIA
        resources.append(LegalReference(
            type="dpa_resource",
            reference="CNIL - Open Source DPIA Software",
            title="Software open-source pentru realizare DPIA",
            url="https://www.cnil.fr/en/open-source-pia-software-helps-carry-out-data-protection-impact-assesment",
            relevance="Tool practic și metodologie CNIL pentru DPIA",
            key_points=[
                "Software gratuit pentru DPIA",
                "Metodologie detaliată CNIL",
                "Template-uri și exemple"
            ]
        ))

        # ICO - DPIA Template
        resources.append(LegalReference(
            type="dpa_resource",
            reference="ICO - DPIA Template",
            title="Template DPIA de la ICO (UK)",
            url="https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/data-protection-impact-assessments-dpias/",
            relevance="Template practic și ghid ICO",
            key_points=[
                "Template structurat DPIA",
                "Screening questions pentru necesitate",
                "Exemple DPIA publice"
            ]
        ))

        return resources

    def generate_references_section(self) -> str:
        """
        Generează secțiunea Referințe pentru DPIA

        Returns:
            Text formatat Markdown cu toate referințele
        """
        output = "## ANEXA 1: REFERINȚE LEGISLATIVE ȘI JURISPRUDENȚĂ\n\n"

        # Grupează pe tipuri
        grouped = {}
        for ref in self.legal_references:
            if ref.type not in grouped:
                grouped[ref.type] = []
            grouped[ref.type].append(ref)

        # GDPR Articles
        if "gdpr_article" in grouped:
            output += "### A. ARTICOLE GDPR\n\n"
            for ref in grouped["gdpr_article"]:
                output += f"**{ref.reference}: {ref.title}**\n\n"
                output += f"*Relevanță:* {ref.relevance}\n\n"
                if ref.key_points:
                    output += "Puncte cheie:\n"
                    for point in ref.key_points:
                        output += f"- {point}\n"
                output += f"\n📎 Link: [{ref.url}]({ref.url})\n\n"
                output += "---\n\n"

        # EDPB Guidelines
        if "edpb_guideline" in grouped:
            output += "### B. LINII DIRECTOARE EDPB/WP29\n\n"
            for ref in grouped["edpb_guideline"]:
                output += f"**{ref.reference}: {ref.title}**\n\n"
                output += f"*Relevanță:* {ref.relevance}\n\n"
                if ref.key_points:
                    output += "Puncte cheie:\n"
                    for point in ref.key_points:
                        output += f"- {point}\n"
                output += f"\n📎 Link: [{ref.url}]({ref.url})\n\n"
                output += "---\n\n"

        # CJEU Cases
        if "cjeu_case" in grouped:
            output += "### C. JURISPRUDENȚĂ CJUE\n\n"
            for ref in grouped["cjeu_case"]:
                output += f"**Cauza {ref.reference}: {ref.title}**\n\n"
                output += f"*Relevanță:* {ref.relevance}\n\n"
                if ref.key_points:
                    output += "Puncte cheie:\n"
                    for point in ref.key_points:
                        output += f"- {point}\n"
                output += f"\n📎 Link: [{ref.url}]({ref.url})\n\n"
                output += "---\n\n"

        # ANSPDCP
        if "anspdcp_decision" in grouped or "national_law" in grouped:
            output += "### D. LEGISLAȚIE ȘI DECIZII NAȚIONALE (ROMÂNIA)\n\n"
            for ref in grouped.get("anspdcp_decision", []) + grouped.get("national_law", []):
                output += f"**{ref.reference}: {ref.title}**\n\n"
                output += f"*Relevanță:* {ref.relevance}\n\n"
                if ref.key_points:
                    output += "Puncte cheie:\n"
                    for point in ref.key_points:
                        output += f"- {point}\n"
                if ref.url:
                    output += f"\n📎 Link: [{ref.url}]({ref.url})\n\n"
                output += "---\n\n"

        # DPA Resources
        if "dpa_resource" in grouped:
            output += "### E. RESURSE AUTORITĂȚI NAȚIONALE (BEST PRACTICES)\n\n"
            for ref in grouped["dpa_resource"]:
                output += f"**{ref.reference}: {ref.title}**\n\n"
                output += f"*Relevanță:* {ref.relevance}\n\n"
                if ref.key_points:
                    output += "Puncte cheie:\n"
                    for point in ref.key_points:
                        output += f"- {point}\n"
                if ref.url:
                    output += f"\n📎 Link: [{ref.url}]({ref.url})\n\n"
                output += "---\n\n"

        return output
