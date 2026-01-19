"""
Risk Assessor - Evaluare riscuri GDPR pentru DPIA
Implementează metodologia WP29 pentru evaluare impact
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

from ..utils.gdpr_knowledge import GDPRKnowledge


class RiskSeverity(Enum):
    """Severitate risc (impact asupra persoanelor)"""
    NEGLIGIBLE = 1  # Neglijabilă
    LIMITED = 2  # Limitată
    SIGNIFICANT = 3  # Semnificativă
    MAXIMUM = 4  # Maximă


class RiskProbability(Enum):
    """Probabilitate risc"""
    NEGLIGIBLE = 1  # Neglijabilă
    LIMITED = 2  # Limitată
    SIGNIFICANT = 3  # Semnificativă
    MAXIMUM = 4  # Maximă


class RiskLevel(Enum):
    """Nivel risc (după matricea Severitate × Probabilitate)"""
    LOW = "low"  # 1-4: Scăzut
    MEDIUM = "medium"  # 5-8: Mediu
    HIGH = "high"  # 9-12: Ridicat
    CRITICAL = "critical"  # 13-16: Critic


@dataclass
class Risk:
    """Reprezentare risc GDPR"""
    risk_id: str
    name: str
    description: str
    source: str  # Sursa riscului
    threat_scenarios: List[str] = field(default_factory=list)

    # Evaluare risc inerent (înainte de măsuri)
    inherent_severity: RiskSeverity = RiskSeverity.NEGLIGIBLE
    inherent_severity_justification: str = ""
    inherent_probability: RiskProbability = RiskProbability.NEGLIGIBLE
    inherent_probability_justification: str = ""
    inherent_level: RiskLevel = RiskLevel.LOW
    inherent_score: int = 0

    # Măsuri de atenuare
    mitigation_measures: List[str] = field(default_factory=list)

    # Risc rezidual (după măsuri)
    residual_probability: RiskProbability = RiskProbability.NEGLIGIBLE
    residual_level: RiskLevel = RiskLevel.LOW
    residual_score: int = 0

    # Metadata
    affects_data_subjects: List[str] = field(default_factory=list)  # Categorii afectate
    gdpr_principles_affected: List[str] = field(default_factory=list)  # Art. 5 principles
    rights_affected: List[str] = field(default_factory=list)  # Drepturi afectate


class RiskAssessor:
    """Evaluare sistematică riscuri pentru DPIA"""

    # Riscuri comune pentru diferite tipuri de prelucrări
    COMMON_RISKS_CATALOG = {
        "unauthorized_access": {
            "name": "Acces neautorizat la date personale",
            "description": "Persoane neautorizate (interne sau externe) pot accesa datele personale",
            "sources": ["Vulnerabilități tehnice", "Control acces inadecvat", "Atac cibernetic"],
            "typical_severity": RiskSeverity.SIGNIFICANT,
            "affects_principles": ["Confidențialitate (Art. 5(1)(f))", "Integritate", "Securitate (Art. 32)"]
        },
        "data_breach": {
            "name": "Încălcare de securitate (data breach)",
            "description": "Pierdere, distrugere, modificare, divulgare neautorizată a datelor",
            "sources": ["Atac ransomware", "Phishing", "Eroare umană", "Vulnerabilități sistem"],
            "typical_severity": RiskSeverity.MAXIMUM,
            "affects_principles": ["Confidențialitate", "Integritate", "Disponibilitate"]
        },
        "unlawful_processing": {
            "name": "Prelucrare ilicită sau excesivă",
            "description": "Prelucrare fără temei juridic valid sau depășirea scopului inițial",
            "sources": ["Lipsă consimțământ", "Scope creep", "Temei juridic inadecvat"],
            "typical_severity": RiskSeverity.SIGNIFICANT,
            "affects_principles": ["Legalitate (Art. 5(1)(a))", "Limitare scop (Art. 5(1)(b))"]
        },
        "excessive_data_collection": {
            "name": "Colectare excesivă de date (încălcare minimizare)",
            "description": "Colectare mai multe date decât necesar pentru scop",
            "sources": ["Formulare excesive", "Cerințe nejustificate", "Lipsă analiză necesitate"],
            "typical_severity": RiskSeverity.LIMITED,
            "affects_principles": ["Minimizare date (Art. 5(1)(c))"]
        },
        "inaccurate_data": {
            "name": "Date inexacte sau învechite",
            "description": "Lipsa procedurilor de actualizare și verificare corectitudine date",
            "sources": ["Proces verificare inadecvat", "Date învechite", "Erori introducere"],
            "typical_severity": RiskSeverity.LIMITED,
            "affects_principles": ["Exactitate (Art. 5(1)(d))"],
            "affects_rights": ["Drept rectificare (Art. 16)"]
        },
        "excessive_retention": {
            "name": "Păstrare excesivă date (încălcare limitare stocare)",
            "description": "Păstrare date mai mult decât necesar",
            "sources": ["Lipsa politici ștergere", "Arhivare nedefinită", "Criterii neclare"],
            "typical_severity": RiskSeverity.LIMITED,
            "affects_principles": ["Limitare stocare (Art. 5(1)(e))"]
        },
        "lack_transparency": {
            "name": "Lipsa transparenței față de persoanele vizate",
            "description": "Persoanele vizate nu sunt informate corespunzător despre prelucrare",
            "sources": ["Clauze informare incomplete", "Limbaj complex", "Informare absentă"],
            "typical_severity": RiskSeverity.LIMITED,
            "affects_principles": ["Transparență (Art. 5(1)(a))", "Informare (Art. 13-14)"]
        },
        "rights_obstruction": {
            "name": "Imposibilitatea exercitării drepturilor",
            "description": "Persoanele vizate nu pot exercita drepturile GDPR (acces, ștergere, etc.)",
            "sources": ["Lipsa proceduri", "Termene nerespectate", "Proces complicat"],
            "typical_severity": RiskSeverity.SIGNIFICANT,
            "affects_rights": ["Art. 15-22 - Toate drepturile persoanelor vizate"]
        },
        "international_transfer_risk": {
            "name": "Risc la transferuri internaționale",
            "description": "Transfer date în țări fără nivel adecvat protecție, fără garanții",
            "sources": ["Lipsă SCCs", "Țară fără decizie adecvare", "Legi supraveghere terță țară"],
            "typical_severity": RiskSeverity.MAXIMUM,
            "affects_principles": ["Art. 44-50 - Transferuri", "Schrems II compliance"]
        },
        "processor_noncompliance": {
            "name": "Neconformitate împuternicit",
            "description": "Împuternicit nu respectă obligațiile Art. 28 sau are securitate slabă",
            "sources": ["Contract Art. 28 absent/incomplet", "Audit neefectuat", "Măsuri securitate slabe"],
            "typical_severity": RiskSeverity.SIGNIFICANT,
            "affects_principles": ["Art. 28 - Împuternicit", "Art. 32 - Securitate"]
        },
        "profiling_discrimination": {
            "name": "Discriminare prin profilare/decizie automată",
            "description": "Algoritmi pot produce decizii discriminatorii sau eronate",
            "sources": ["Bias în algoritmi", "Lipsă intervenție umană", "Date antrenare biased"],
            "typical_severity": RiskSeverity.MAXIMUM,
            "affects_principles": ["Art. 22 - Decizie automată", "Non-discriminare"],
            "affects_rights": ["Drept contestare decizie automată"]
        },
        "special_categories_exposure": {
            "name": "Expunere date speciale (Art. 9)",
            "description": "Divulgare neautorizată date medicale, biometrice, genetice, etc.",
            "sources": ["Securitate inadecvată", "Acces necontrolat", "Breach"],
            "typical_severity": RiskSeverity.MAXIMUM,
            "affects_principles": ["Art. 9 - Categorii speciale", "Confidențialitate sporită"]
        },
        "children_data_risk": {
            "name": "Risc specific pentru copii",
            "description": "Prelucrare date copii fără consimțământ părinți sau măsuri inadecvate",
            "sources": ["Lipsa verificare vârstă", "Consimțământ părinți absent", "Limbaj neadaptat"],
            "typical_severity": RiskSeverity.SIGNIFICANT,
            "affects_principles": ["Art. 8 - Consimțământ copii", "Protecție sporită"]
        },
        "surveillance_privacy_impact": {
            "name": "Impact prin supraveghere/monitorizare",
            "description": "Monitorizare sistematică poate afecta libertăți și autonomie personală",
            "sources": ["Camere video", "Tracking comportamental", "Monitorizare angajați"],
            "typical_severity": RiskSeverity.SIGNIFICANT,
            "affects_principles": ["Art. 35(3)(c) - Monitorizare sistematică", "Drept viață privată"]
        }
    }

    def __init__(self):
        self.identified_risks: List[Risk] = []

    def assess_risks(
        self,
        processing_info: Dict,
        existing_measures: Dict[str, List[str]]
    ) -> List[Risk]:
        """
        Evaluează riscurile pentru o prelucrare dată

        Args:
            processing_info: Informații despre prelucrare (din ProcessingInfo)
            existing_measures: Măsuri existente de securitate

        Returns:
            Listă de riscuri identificate și evaluate
        """
        risks = []

        # 1. Identificare riscuri pe baza caracteristicilor prelucrării
        risks.extend(self._identify_risks_by_characteristics(processing_info))

        # 2. Evaluare severitate și probabilitate pentru fiecare risc
        for risk in risks:
            self._assess_inherent_risk(risk, processing_info)
            self._propose_mitigation_measures(risk, existing_measures)
            self._assess_residual_risk(risk)

        self.identified_risks = risks
        return risks

    def _identify_risks_by_characteristics(
        self,
        processing_info: Dict
    ) -> List[Risk]:
        """Identifică riscuri pe baza caracteristicilor prelucrării"""
        risks = []
        risk_counter = 1

        # Risc comun: Acces neautorizat (aproape universal)
        risks.append(self._create_risk_from_catalog(
            f"R{risk_counter:02d}",
            "unauthorized_access",
            processing_info
        ))
        risk_counter += 1

        # Risc comun: Data breach (universal)
        risks.append(self._create_risk_from_catalog(
            f"R{risk_counter:02d}",
            "data_breach",
            processing_info
        ))
        risk_counter += 1

        # Dacă există date speciale (Art. 9)
        if processing_info.get('has_special_categories'):
            risks.append(self._create_risk_from_catalog(
                f"R{risk_counter:02d}",
                "special_categories_exposure",
                processing_info
            ))
            risk_counter += 1

        # Dacă există copii
        if processing_info.get('includes_children'):
            risks.append(self._create_risk_from_catalog(
                f"R{risk_counter:02d}",
                "children_data_risk",
                processing_info
            ))
            risk_counter += 1

        # Dacă există transferuri internaționale
        if processing_info.get('has_international_transfers'):
            risks.append(self._create_risk_from_catalog(
                f"R{risk_counter:02d}",
                "international_transfer_risk",
                processing_info
            ))
            risk_counter += 1

        # Dacă există împuterniciti
        if processing_info.get('has_processors'):
            risks.append(self._create_risk_from_catalog(
                f"R{risk_counter:02d}",
                "processor_noncompliance",
                processing_info
            ))
            risk_counter += 1

        # Dacă există profilare/decizie automată
        if processing_info.get('has_profiling') or processing_info.get('has_automated_decision'):
            risks.append(self._create_risk_from_catalog(
                f"R{risk_counter:02d}",
                "profiling_discrimination",
                processing_info
            ))
            risk_counter += 1

        # Dacă există monitorizare sistematică
        if processing_info.get('has_systematic_monitoring'):
            risks.append(self._create_risk_from_catalog(
                f"R{risk_counter:02d}",
                "surveillance_privacy_impact",
                processing_info
            ))
            risk_counter += 1

        # Risc privind transparența
        if not processing_info.get('has_privacy_notice'):
            risks.append(self._create_risk_from_catalog(
                f"R{risk_counter:02d}",
                "lack_transparency",
                processing_info
            ))
            risk_counter += 1

        # Risc privind drepturile
        if not processing_info.get('has_rights_procedures'):
            risks.append(self._create_risk_from_catalog(
                f"R{risk_counter:02d}",
                "rights_obstruction",
                processing_info
            ))
            risk_counter += 1

        # Risc minimizare date
        if processing_info.get('risk_excessive_data'):
            risks.append(self._create_risk_from_catalog(
                f"R{risk_counter:02d}",
                "excessive_data_collection",
                processing_info
            ))
            risk_counter += 1

        # Risc păstrare excesivă
        if not processing_info.get('has_retention_policy'):
            risks.append(self._create_risk_from_catalog(
                f"R{risk_counter:02d}",
                "excessive_retention",
                processing_info
            ))
            risk_counter += 1

        return risks

    def _create_risk_from_catalog(
        self,
        risk_id: str,
        catalog_key: str,
        processing_info: Dict
    ) -> Risk:
        """Creează obiect Risk din catalogul de riscuri"""
        catalog_risk = self.COMMON_RISKS_CATALOG[catalog_key]

        return Risk(
            risk_id=risk_id,
            name=catalog_risk["name"],
            description=catalog_risk["description"],
            source=", ".join(catalog_risk["sources"]),
            threat_scenarios=self._generate_threat_scenarios(catalog_key, processing_info),
            inherent_severity=catalog_risk["typical_severity"],
            gdpr_principles_affected=catalog_risk.get("affects_principles", []),
            rights_affected=catalog_risk.get("affects_rights", [])
        )

    def _generate_threat_scenarios(
        self,
        risk_type: str,
        processing_info: Dict
    ) -> List[str]:
        """Generează scenarii amenințătoare specifice pentru context"""
        scenarios = []

        if risk_type == "data_breach":
            scenarios.append("Atacator extern obține acces prin vulnerabilitate și exfiltrează date")
            scenarios.append("Angajat malițios copiază date și le divulgă")
            scenarios.append("Ransomware criptează datele și solicită plată")

        elif risk_type == "unauthorized_access":
            scenarios.append("Utilizator cu privilegii excesive accesează date fără justificare")
            scenarios.append("Parole slabe permit acces neautorizat")
            scenarios.append("Lipsa autentificare multiplă factor permite acces ușor")

        elif risk_type == "international_transfer_risk":
            scenarios.append("Autorități țară terță solicită acces la date fără garanții GDPR")
            scenarios.append("Furnizor cloud din SUA supus CLOUD Act sau FISA 702")
            scenarios.append("Date transferate fără SCCs sau măsuri suplimentare")

        # Generic fallback
        if not scenarios:
            scenarios.append(f"Scenarii specifice pentru {risk_type}")

        return scenarios

    def _assess_inherent_risk(
        self,
        risk: Risk,
        processing_info: Dict
    ) -> None:
        """Evaluează riscul inerent (înainte de măsuri)"""

        # Severitatea rămâne cea din catalog (poate fi ajustată)
        # Evaluăm probabilitatea pe baza contextului

        # Factori care cresc probabilitatea:
        high_probability_factors = 0

        if not processing_info.get('has_encryption'):
            high_probability_factors += 1

        if not processing_info.get('has_access_control'):
            high_probability_factors += 1

        if not processing_info.get('has_security_training'):
            high_probability_factors += 1

        if processing_info.get('has_internet_facing_systems'):
            high_probability_factors += 1

        if processing_info.get('has_special_categories'):
            high_probability_factors += 1  # Mai atractive pentru atacatori

        # Mapare factori -> probabilitate
        if high_probability_factors >= 4:
            risk.inherent_probability = RiskProbability.MAXIMUM
            risk.inherent_probability_justification = "Măsuri de securitate insuficiente, multiple vulnerabilități"
        elif high_probability_factors == 3:
            risk.inherent_probability = RiskProbability.SIGNIFICANT
            risk.inherent_probability_justification = "Unele măsuri lipsesc, vulnerabilități prezente"
        elif high_probability_factors == 2:
            risk.inherent_probability = RiskProbability.LIMITED
            risk.inherent_probability_justification = "Măsuri parțiale implementate"
        else:
            risk.inherent_probability = RiskProbability.NEGLIGIBLE
            risk.inherent_probability_justification = "Măsuri multiple de securitate implementate"

        # Justificare severitate
        severity_descriptions = {
            RiskSeverity.NEGLIGIBLE: "Impact minim asupra persoanelor vizate",
            RiskSeverity.LIMITED: "Impact minor, posibile nemulțumiri sau inconveniente",
            RiskSeverity.SIGNIFICANT: "Impact important, posibile prejudicii financiare sau discriminare",
            RiskSeverity.MAXIMUM: "Impact sever, consecințe grave: riscuri fizice, furt identitate, prejudicii majore"
        }
        risk.inherent_severity_justification = severity_descriptions[risk.inherent_severity]

        # Calculare nivel risc inerent
        risk.inherent_score = risk.inherent_severity.value * risk.inherent_probability.value
        risk.inherent_level = self._calculate_risk_level(risk.inherent_score)

    def _propose_mitigation_measures(
        self,
        risk: Risk,
        existing_measures: Dict[str, List[str]]
    ) -> None:
        """Propune măsuri de atenuare pentru risc"""

        measures = []

        # Măsuri specifice pe tip de risc
        if "acces neautorizat" in risk.name.lower():
            if not existing_measures.get('access_control'):
                measures.append("Implementare control acces bazat pe roluri (RBAC)")
                measures.append("Autentificare cu doi factori (2FA/MFA) pentru toate conturile")
            if not existing_measures.get('encryption'):
                measures.append("Criptare date în repaus (AES-256)")
            measures.append("Monitorizare și audit log-uri acces")
            measures.append("Politică parole puternice și expirare periodică")

        elif "breach" in risk.name.lower() or "încălcare" in risk.name.lower():
            if not existing_measures.get('backup'):
                measures.append("Backup regulat (zilnic) cu testare restaurare")
            if not existing_measures.get('encryption'):
                measures.append("Criptare end-to-end pentru toate datele sensibile")
            measures.append("Firewall și segmentare rețea")
            measures.append("Sistem detectare intruziuni (IDS/IPS)")
            measures.append("Plan de răspuns la incidente cu responsabili definiți")
            measures.append("Procedură raportare breach în 72h către ANSPDCP")

        elif "transfer" in risk.name.lower():
            measures.append("Implementare Clauze Contractuale Standard (SCCs) Comisia Europeană")
            measures.append("Transfer Impact Assessment (TIA) conform Schrems II")
            measures.append("Măsuri tehnice suplimentare: criptare end-to-end")
            measures.append("Clauze contractuale privind solicitări autorități terțe")

        elif "împuternicit" in risk.name.lower() or "processor" in risk.name.lower():
            measures.append("Contract Art. 28 GDPR cu toate obligațiile operatorului")
            measures.append("Audit periodic al împuternicitului (anual)")
            measures.append("Verificare certificate securitate (ISO 27001, SOC 2)")
            measures.append("Clauze contractuale privind sub-împuternicirea")

        elif "profilare" in risk.name.lower() or "automată" in risk.name.lower():
            measures.append("Implementare intervenție umană semnificativă în decizie")
            measures.append("Transparență: explicare logică algoritm către persoane vizate")
            measures.append("Testing pentru bias și discriminare în algoritm")
            measures.append("Procedură contestare decizie automată (Art. 22)")
            measures.append("Impact assessment pentru algoritmi")

        elif "date speciale" in risk.name.lower() or "art. 9" in risk.name.lower():
            measures.append("Criptare sporită pentru categorii speciale (end-to-end)")
            measures.append("Separare fizică/logică date speciale de alte date")
            measures.append("Control acces restrictiv (need-to-know basis)")
            measures.append("Pseudonimizare date medicale/biometrice")
            measures.append("Audit trail complet pentru acces la date speciale")

        elif "copii" in risk.name.lower():
            measures.append("Sistem verificare vârstă conform Art. 8 GDPR")
            measures.append("Obținere consimțământ de la părinți pentru sub-16 ani")
            measures.append("Interfață adaptată copiilor cu limbaj clar")
            measures.append("Protecție sporită: opt-in implicit, nu opt-out")

        elif "transparență" in risk.name.lower():
            measures.append("Clauză informare Art. 13/14 completă și clară")
            measures.append("Politică de confidențialitate cu limbaj accesibil")
            measures.append("Privacy notice stratificat (layered)")
            measures.append("Informare proactivă la colectare date")

        elif "drepturi" in risk.name.lower():
            measures.append("Proceduri documentate pentru toate drepturile (Art. 15-22)")
            measures.append("Formular online pentru solicitări drepturi")
            measures.append("Proces răspuns în 1 lună (cu posibilitate extindere 2 luni)")
            measures.append("Training personal privind gestionare solicitări")

        elif "păstrare" in risk.name.lower() or "retention" in risk.name.lower():
            measures.append("Politică de păstrare cu perioade clare per categorie date")
            measures.append("Procedură ștergere automată la expirare perioadă")
            measures.append("Revizie anuală necesitate păstrare date")
            measures.append("Criterii clare pentru determinare perioadă păstrare")

        # Măsuri generice dacă nu s-a identificat specific
        if not measures:
            measures.append("Implementare măsuri tehnice și organizatorice Art. 32 GDPR")
            measures.append("Proceduri de minimizare risc specifice acestei amenințări")

        risk.mitigation_measures = measures

    def _assess_residual_risk(
        self,
        risk: Risk
    ) -> None:
        """Evaluează riscul rezidual (după aplicarea măsurilor)"""

        # După implementarea măsurilor, probabilitatea scade semnificativ
        # Severitatea rămâne aceeași (impactul potențial nu se schimbă)

        # Reducere probabilitate cu 1-2 niveluri în funcție de măsuri
        num_measures = len(risk.mitigation_measures)

        if num_measures >= 5:
            # Măsuri comprehensiv → reducere 2 niveluri
            new_prob_value = max(1, risk.inherent_probability.value - 2)
        elif num_measures >= 3:
            # Măsuri bune → reducere 1 nivel
            new_prob_value = max(1, risk.inherent_probability.value - 1)
        else:
            # Măsuri minime → fără reducere semnificativă
            new_prob_value = risk.inherent_probability.value

        risk.residual_probability = RiskProbability(new_prob_value)

        # Calculare risc rezidual
        risk.residual_score = risk.inherent_severity.value * risk.residual_probability.value
        risk.residual_level = self._calculate_risk_level(risk.residual_score)

    def _calculate_risk_level(self, score: int) -> RiskLevel:
        """Calculează nivelul de risc din scor"""
        if 1 <= score <= 4:
            return RiskLevel.LOW
        elif 5 <= score <= 8:
            return RiskLevel.MEDIUM
        elif 9 <= score <= 12:
            return RiskLevel.HIGH
        else:  # 13-16
            return RiskLevel.CRITICAL

    def generate_risk_matrix(self) -> str:
        """Generează matrice heat map pentru riscuri"""
        matrix = []

        matrix.append("| ID | Risc | Prob. Inițială | Severitate | Nivel Inerent | Măsuri | Prob. Reziduală | Nivel Rezidual |")
        matrix.append("|----|----|----|----|----|----|----|----|")

        for risk in self.identified_risks:
            level_colors = {
                RiskLevel.LOW: "🟢",
                RiskLevel.MEDIUM: "🟡",
                RiskLevel.HIGH: "🟠",
                RiskLevel.CRITICAL: "🔴"
            }

            inherent_color = level_colors[risk.inherent_level]
            residual_color = level_colors[risk.residual_level]

            matrix.append(
                f"| {risk.risk_id} | {risk.name[:40]} | {risk.inherent_probability.value} | "
                f"{risk.inherent_severity.value} | {inherent_color} {risk.inherent_score} | "
                f"{len(risk.mitigation_measures)} măsuri | {risk.residual_probability.value} | "
                f"{residual_color} {risk.residual_score} |"
            )

        return "\n".join(matrix)

    def check_prior_consultation_needed(self) -> bool:
        """
        Verifică dacă este necesară consultare prealabilă ANSPDCP (Art. 36)

        Returns:
            True dacă riscul rezidual rămâne ridicat după măsuri
        """
        for risk in self.identified_risks:
            if risk.residual_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]:
                return True

        return False
