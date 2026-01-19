"""
Diagram Generator - Generare diagrame Mermaid pentru DPIA
Creează: DFD, Lifecycle, Risk Matrix, Architecture, Roles, Timeline
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class DiagramConfig:
    """Configurare pentru diagrame"""
    include_dfd: bool = True
    include_lifecycle: bool = True
    include_risk_matrix: bool = True
    include_architecture: bool = False
    include_roles: bool = False
    include_timeline: bool = False


class DiagramGenerator:
    """Generator diagrame Mermaid pentru DPIA"""

    def __init__(self):
        self.diagrams = {}

    def generate_all_diagrams(
        self,
        processing_info: Dict,
        risks: List,
        config: DiagramConfig = DiagramConfig()
    ) -> Dict[str, str]:
        """
        Generează toate diagramele necesare

        Args:
            processing_info: Informații despre prelucrare
            risks: Listă riscuri evaluate
            config: Configurare ce diagrame să genereze

        Returns:
            Dict cu diagrame {nume: cod_mermaid}
        """
        diagrams = {}

        if config.include_dfd:
            diagrams["dfd"] = self.generate_data_flow_diagram(processing_info)

        if config.include_lifecycle:
            diagrams["lifecycle"] = self.generate_lifecycle_diagram(processing_info)

        if config.include_risk_matrix:
            diagrams["risk_matrix"] = self.generate_risk_heatmap(risks)

        if config.include_architecture:
            diagrams["architecture"] = self.generate_architecture_diagram(processing_info)

        if config.include_roles:
            diagrams["roles"] = self.generate_roles_diagram(processing_info)

        if config.include_timeline:
            diagrams["timeline"] = self.generate_timeline_diagram(processing_info)

        self.diagrams = diagrams
        return diagrams

    def generate_data_flow_diagram(self, processing_info: Dict) -> str:
        """
        Generează Diagrama Fluxului de Date (DFD)

        Figura 1: Diagrama fluxului de date
        """
        # Extrage informații
        operator_name = processing_info.get('operator', {}).get('name', 'Operator')
        processors = processing_info.get('processors', [])
        recipients = processing_info.get('recipients_external', [])
        transfers = processing_info.get('international_transfers', [])
        data_subjects = processing_info.get('data_subjects', [])
        data_categories = processing_info.get('data_categories', {})

        # Construiește lista date
        common_data = data_categories.get('common_data_art6', [])
        special_data = data_categories.get('special_categories_art9', [])

        data_list = ", ".join(common_data[:3]) if common_data else "Date personale"
        if special_data:
            data_list += f" + Date speciale Art. 9"

        # Construiește lista persoane vizate
        subjects_list = ", ".join([s.get('category', '') for s in data_subjects[:3]]) if data_subjects else "Persoane vizate"

        mermaid = "```mermaid\n"
        mermaid += "flowchart TB\n"

        # Subgraph Surse
        mermaid += '    subgraph Surse["📊 SURSE DATE"]\n'
        mermaid += f'        PV1["👤 Persoane vizate<br/>Categorii: {subjects_list}<br/>Date: {data_list}"]\n'
        mermaid += '    end\n\n'

        # Subgraph Operator
        mermaid += f'    subgraph Operator["🏢 OPERATOR - {operator_name}"]\n'
        mermaid += '        SYS1["💾 Sistem prelucrare<br/>Bază de date<br/>Aplicații"]\n'
        mermaid += '    end\n\n'

        # Subgraph Împuterniciti (dacă există)
        if processors:
            mermaid += '    subgraph Imputerniciti["⚙️ ÎMPUTERNICITI"]\n'
            for idx, proc in enumerate(processors[:3], 1):  # Max 3 pentru vizibilitate
                proc_name = proc.get('name', f'Împuternicit {idx}')[:30]
                proc_services = proc.get('services', 'Servicii')[:30]
                mermaid += f'        IMP{idx}["🔧 {proc_name}<br/>Servicii: {proc_services}<br/>Contract Art. 28"]\n'
            mermaid += '    end\n\n'

        # Subgraph Destinatari (dacă există)
        if recipients:
            mermaid += '    subgraph Destinatari["📤 DESTINATARI"]\n'
            for idx, recip in enumerate(recipients[:2], 1):
                mermaid += f'        DEST{idx}["🏛️ {recip}<br/>Scop: Conform temei"]\n'
            mermaid += '    end\n\n'

        # Subgraph Transferuri (dacă există)
        if transfers and transfers[0].get('has_transfer'):
            mermaid += '    subgraph Transfer["🌍 TRANSFERURI INTERNAȚIONALE"]\n'
            safeguards = ", ".join(transfers[0].get('safeguards', ['SCC']))[:40] if transfers[0].get('safeguards') else "Necesare garanții"
            mermaid += f'        TRANS1["🌍 Țară terță<br/>Garanții: {safeguards}"]\n'
            mermaid += '    end\n\n'

        # Fluxuri de date
        mermaid += '    PV1 -->|Colectare date| SYS1\n'

        if processors:
            for idx in range(1, min(len(processors) + 1, 4)):
                mermaid += f'    SYS1 -->|Procesare| IMP{idx}\n'

        if recipients:
            for idx in range(1, min(len(recipients) + 1, 3)):
                mermaid += f'    SYS1 -->|Comunicare| DEST{idx}\n'

        if transfers and transfers[0].get('has_transfer'):
            mermaid += '    SYS1 -.->|Transfer SCCs| TRANS1\n'

        # Stiluri
        mermaid += '\n    style PV1 fill:#e1f5ff,stroke:#0288d1\n'
        mermaid += '    style SYS1 fill:#fff4e1,stroke:#f57c00\n'

        if processors:
            for idx in range(1, min(len(processors) + 1, 4)):
                mermaid += f'    style IMP{idx} fill:#ffe1f5,stroke:#c2185b\n'

        if recipients:
            for idx in range(1, min(len(recipients) + 1, 3)):
                mermaid += f'    style DEST{idx} fill:#e1ffe1,stroke:#388e3c\n'

        if transfers and transfers[0].get('has_transfer'):
            mermaid += '    style TRANS1 fill:#ffe1e1,stroke:#d32f2f\n'

        mermaid += "```\n"

        return mermaid

    def generate_lifecycle_diagram(self, processing_info: Dict) -> str:
        """
        Generează Ciclul de Viață al Datelor

        Figura 2: Ciclul de viață al datelor
        """
        retention = processing_info.get('retention_periods', [])
        retention_text = retention[0].get('period', 'Conform politicii') if retention else 'Conform politicii'

        legal_basis = processing_info.get('legal_basis', {}).get('art6_basis', 'Art. 6(1)')
        purposes = processing_info.get('purposes', ['Scopuri definite'])
        purpose_text = purposes[0][:40] if purposes else "Scopuri definite"

        recipients = processing_info.get('recipients_external', [])
        has_recipients = len(recipients) > 0

        mermaid = "```mermaid\n"
        mermaid += "flowchart LR\n"

        # Colectare
        mermaid += f'    A["📥 COLECTARE<br/>Sursă: Persoane vizate<br/>Temei: {legal_basis}<br/>Măsuri: Informare Art. 13"]\n'

        # Stocare
        mermaid += f'    B["💾 STOCARE<br/>Durată: {retention_text}<br/>Locație: Bază date securizată<br/>Măsuri: Criptare, Control acces"]\n'

        # Utilizare
        mermaid += f'    C["⚙️ UTILIZARE<br/>Scop: {purpose_text}<br/>Acces: Personal autorizat"]\n'

        # Decizie comunicare
        if has_recipients:
            mermaid += '    D{"📤 Comunicare?"}\n'
            mermaid += f'    E["📤 COMUNICARE<br/>Către: Destinatari terți<br/>Temei: {legal_basis}"]\n'
        else:
            mermaid += '    D["⏭️ Fără comunicare"]\n'

        # Arhivare
        mermaid += f'    F["📦 ARHIVARE<br/>Durată: {retention_text}<br/>Acces restricționat"]\n'

        # Decizie termen
        mermaid += '    G{"⏰ Termen?"}\n'

        # Ștergere
        mermaid += '    H["🗑️ ȘTERGERE<br/>Metodă: Ștergere securizată<br/>Verificare: Audit"]\n'

        # Solicitare ștergere
        mermaid += '    I["👤 Solicitare ștergere<br/>Art. 17 GDPR"]\n'
        mermaid += '    J{"✅ Valid?"}\n'
        mermaid += '    K["📧 Refuz justificat<br/>Art. 17(3)"]\n'

        # Fluxuri
        mermaid += '    A --> B --> C\n'

        if has_recipients:
            mermaid += '    C --> D\n'
            mermaid += '    D -->|DA| E --> F\n'
            mermaid += '    D -->|NU| F\n'
        else:
            mermaid += '    C --> D --> F\n'

        mermaid += '    F --> G\n'
        mermaid += '    G -->|NU| F\n'
        mermaid += '    G -->|DA| H\n'

        mermaid += '    I -.->|Oricând| J\n'
        mermaid += '    J -->|DA| H\n'
        mermaid += '    J -->|NU| K\n'

        # Stiluri
        mermaid += '\n    style A fill:#e3f2fd\n'
        mermaid += '    style B fill:#fff3e0\n'
        mermaid += '    style C fill:#f3e5f5\n'
        mermaid += '    style H fill:#ffebee\n'

        mermaid += "```\n"

        return mermaid

    def generate_risk_heatmap(self, risks: List) -> str:
        """
        Generează Matrice Heat Map Riscuri

        Figura 3: Matrice evaluare risc
        """
        if not risks:
            return "Nu există riscuri evaluate."

        # Construiește tabelul markdown
        table = "## Matrice Evaluare Risc\n\n"
        table += "| ID | Risc | Prob. Inițială | Severitate | Nivel Inerent | Măsuri | Prob. Reziduală | Nivel Rezidual |\n"
        table += "|:---|:-----|:--------------:|:----------:|:-------------:|:------:|:---------------:|:--------------:|\n"

        for risk in risks:
            # Emoji pentru nivel
            inherent_emoji = self._get_risk_emoji(risk.inherent_level.value)
            residual_emoji = self._get_risk_emoji(risk.residual_level.value)

            # Nume risc trunchiat
            risk_name = risk.name[:35] + "..." if len(risk.name) > 35 else risk.name

            table += f"| {risk.risk_id} | {risk_name} | "
            table += f"{risk.inherent_probability.value} | {risk.inherent_severity.value} | "
            table += f"{inherent_emoji} {risk.inherent_score} | "
            table += f"{len(risk.mitigation_measures)} | "
            table += f"{risk.residual_probability.value} | "
            table += f"{residual_emoji} {risk.residual_score} |\n"

        table += "\n**Legendă:**\n"
        table += "- 🟢 Risc scăzut (1-4): Acceptabil\n"
        table += "- 🟡 Risc mediu (5-8): Necesită măsuri suplimentare\n"
        table += "- 🟠 Risc ridicat (9-12): Necesită măsuri imediate\n"
        table += "- 🔴 Risc critic (13-16): INACCEPTABIL - Consultare ANSPDCP\n"

        return table

    def generate_architecture_diagram(self, processing_info: Dict) -> str:
        """
        Generează Arhitectură Sisteme IT (opțional)

        Figura 4: Arhitectură sisteme IT
        """
        mermaid = "```mermaid\n"
        mermaid += "flowchart TB\n"

        mermaid += '    subgraph Internet["🌐 INTERNET"]\n'
        mermaid += '        USER["👤 Utilizatori<br/>Browser HTTPS"]\n'
        mermaid += '    end\n\n'

        mermaid += '    subgraph Security["🛡️ SECURITATE"]\n'
        mermaid += '        FW["🛡️ Firewall<br/>Filtrare trafic"]\n'
        mermaid += '        WAF["🛡️ WAF<br/>Web Application Firewall"]\n'
        mermaid += '    end\n\n'

        mermaid += '    subgraph AppLayer["💻 APLICAȚIE"]\n'
        mermaid += '        WEB["🖥️ Server Web<br/>Nginx/Apache<br/>TLS 1.3"]\n'
        mermaid += '        APP["⚙️ Server Aplicație<br/>Autentificare 2FA<br/>RBAC"]\n'
        mermaid += '    end\n\n'

        mermaid += '    subgraph DataLayer["💾 DATE"]\n'
        mermaid += '        DB[("💾 Bază date<br/>Criptare AES-256<br/>Backup zilnic")]\n'
        mermaid += '        BACKUP[("💾 Backup<br/>Stocare off-site<br/>Criptat")]\n'
        mermaid += '    end\n\n'

        mermaid += '    USER -->|HTTPS| FW\n'
        mermaid += '    FW --> WAF\n'
        mermaid += '    WAF --> WEB\n'
        mermaid += '    WEB --> APP\n'
        mermaid += '    APP --> DB\n'
        mermaid += '    DB -.->|Backup zilnic| BACKUP\n'

        mermaid += '\n    style USER fill:#e3f2fd\n'
        mermaid += '    style FW fill:#ffebee\n'
        mermaid += '    style DB fill:#fff3e0\n'

        mermaid += "```\n"

        return mermaid

    def generate_roles_diagram(self, processing_info: Dict) -> str:
        """
        Generează Diagrama Roluri și Responsabilități

        Figura 5: Roluri și responsabilități
        """
        operator = processing_info.get('operator', {}).get('name', 'Operator')
        dpo_name = processing_info.get('dpo', {}).get('name', 'DPO')
        processors = processing_info.get('processors', [])

        mermaid = "```mermaid\n"
        mermaid += "flowchart TB\n"

        mermaid += f'    OP["🏢 OPERATOR<br/>{operator}"]\n'
        mermaid += f'    DPO["👤 DPO<br/>{dpo_name}"]\n\n'

        mermaid += '    OP -.->|Desemnează și consultă| DPO\n\n'

        mermaid += '    subgraph Responsabilitati_OP["📋 Responsabilități Operator"]\n'
        mermaid += '        R1["📋 Determină scopuri și mijloace<br/>Art. 24 GDPR"]\n'
        mermaid += '        R2["🛡️ Măsuri securitate<br/>Art. 32 GDPR"]\n'
        mermaid += '        R3["📊 Registru activități<br/>Art. 30 GDPR"]\n'
        mermaid += '        R4["⚠️ Notificare incidente<br/>Art. 33-34 GDPR"]\n'
        mermaid += '        R5["📄 DPIA<br/>Art. 35 GDPR"]\n'
        mermaid += '    end\n\n'

        mermaid += '    OP --> R1 & R2 & R3 & R4 & R5\n\n'

        if processors:
            mermaid += '    subgraph Imputerniciti["⚙️ Împuterniciti"]\n'
            for idx, proc in enumerate(processors[:3], 1):
                proc_name = proc.get('name', f'Împuternicit {idx}')[:25]
                mermaid += f'        IMP{idx}["⚙️ {proc_name}"]\n'
            mermaid += '    end\n\n'

            for idx in range(1, min(len(processors) + 1, 4)):
                mermaid += f'    OP -->|Contract Art. 28| IMP{idx}\n'

        mermaid += '\n    style OP fill:#e3f2fd\n'
        mermaid += '    style DPO fill:#fff3e0\n'

        mermaid += "```\n"

        return mermaid

    def generate_timeline_diagram(self, processing_info: Dict) -> str:
        """
        Generează Timeline Implementare Măsuri (opțional)

        Figura 6: Timeline implementare
        """
        mermaid = "```mermaid\n"
        mermaid += "gantt\n"
        mermaid += "    title Plan implementare măsuri DPIA\n"
        mermaid += "    dateFormat YYYY-MM-DD\n"
        mermaid += "    section Măsuri tehnice\n"
        mermaid += "    Criptare AES-256        :done, m1, 2024-01-15, 30d\n"
        mermaid += "    Autentificare 2FA       :active, m2, 2024-02-15, 45d\n"
        mermaid += "    Backup automat          :m3, 2024-04-01, 15d\n"
        mermaid += "    Monitoring și logging   :m4, 2024-04-15, 20d\n"
        mermaid += "    section Măsuri organizatorice\n"
        mermaid += "    Politică securitate     :done, m5, 2024-01-01, 20d\n"
        mermaid += "    Training GDPR personal  :active, m6, 2024-02-01, 60d\n"
        mermaid += "    Procedură incidente     :m7, 2024-03-15, 30d\n"
        mermaid += "    Proceduri drepturi      :m8, 2024-04-01, 25d\n"
        mermaid += "    section Conformitate\n"
        mermaid += "    Finalizare DPIA         :milestone, done, 2024-01-30, 0d\n"
        mermaid += "    Consultare DPO          :done, 2024-02-05, 5d\n"
        mermaid += "    Actualizare Registru    :m10, 2024-03-01, 10d\n"
        mermaid += "    section Audit\n"
        mermaid += "    Audit implementare      :m11, 2024-06-01, 10d\n"
        mermaid += "    Revizuire DPIA          :m12, 2025-01-30, 15d\n"
        mermaid += "```\n"

        return mermaid

    def _get_risk_emoji(self, level: str) -> str:
        """Returnează emoji pentru nivel risc"""
        emoji_map = {
            "low": "🟢",
            "medium": "🟡",
            "high": "🟠",
            "critical": "🔴"
        }
        return emoji_map.get(level, "⚪")

    def save_diagrams_to_files(self, output_dir: str) -> Dict[str, str]:
        """
        Salvează diagramele în fișiere separate

        Args:
            output_dir: Director unde să salveze fișierele

        Returns:
            Dict cu {nume: path_fisier}
        """
        from pathlib import Path

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        saved_files = {}

        for diagram_name, diagram_content in self.diagrams.items():
            file_path = output_path / f"{diagram_name}.md"
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"# {diagram_name.upper()}\n\n")
                f.write(diagram_content)

            saved_files[diagram_name] = str(file_path)

        return saved_files
