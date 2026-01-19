"""
Document Parser - Extragere automată informații din documente pentru DPIA
Suportă: DOCX, PDF, TXT, MD
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import json


@dataclass
class ConfidenceLevel:
    """Nivel de încredere pentru informații extrase"""
    HIGH = "high"  # ✓
    MEDIUM = "medium"  # ⚠️
    LOW = "low"  # ❌


@dataclass
class ExtractedInfo:
    """Informație extrasă din document"""
    category: str
    value: any
    confidence: str
    source_document: str
    source_location: str = ""  # pagină, linie, etc.
    context: str = ""  # text din jur pentru verificare


@dataclass
class ProcessingInfo:
    """Informații despre prelucrarea de date extrase din documente"""
    # Împuterniciti
    processors: List[Dict] = field(default_factory=list)

    # Scopuri
    purposes: List[str] = field(default_factory=list)

    # Temei juridic
    legal_basis: Optional[Dict] = None

    # Date personale
    data_categories: Dict[str, List[str]] = field(default_factory=dict)
    data_volume: Optional[int] = None
    data_sources: List[str] = field(default_factory=list)

    # Persoane vizate
    data_subjects: List[Dict] = field(default_factory=list)

    # Destinatari
    recipients_internal: List[str] = field(default_factory=list)
    recipients_external: List[str] = field(default_factory=list)

    # Transferuri internaționale
    international_transfers: List[Dict] = field(default_factory=list)

    # Durata stocare
    retention_periods: List[Dict] = field(default_factory=list)

    # Măsuri tehnice și organizatorice
    security_measures: Dict[str, List[str]] = field(default_factory=dict)

    # Context
    is_new_processing: Optional[bool] = None
    previous_assessments: List[str] = field(default_factory=list)
    previous_incidents: List[str] = field(default_factory=list)

    # Metadata extragere
    extraction_metadata: List[ExtractedInfo] = field(default_factory=list)


class DocumentParser:
    """Parser pentru extragere automată informații din documente"""

    def __init__(self):
        self.patterns = self._init_patterns()

    def _init_patterns(self) -> Dict:
        """Inițializare pattern-uri regex pentru extragere"""
        return {
            # Împuterniciti
            "processors": {
                "keywords": [
                    r"împuternicit[ă-ț]*",
                    r"subcontractant[ă-ț]*",
                    r"processor[s]?",
                    r"furnizor[ă-ț]?\s+(?:de\s+)?servicii",
                    r"prestator[ă-ț]?"
                ],
                "art28_contract": r"(?:contract|acord).*?(?:art\.?\s*28|articol(?:ul)?\s+28)",
            },

            # Scopuri
            "purposes": {
                "keywords": [
                    r"scop(?:ul|uri)?[:\s]+(.*?)(?:\.|;|\n)",
                    r"finalitate[a]?[:\s]+(.*?)(?:\.|;|\n)",
                    r"pentru(?:\s+a)?\s+(.*?)(?:\.|;|\n)",
                    r"în vederea\s+(.*?)(?:\.|;|\n)"
                ]
            },

            # Temei juridic
            "legal_basis": {
                "art6": r"art\.?\s*6\s*\(\s*1\s*\)\s*\(\s*([a-f])\s*\)",
                "art9": r"art\.?\s*9\s*\(\s*2\s*\)\s*\(\s*([a-j])\s*\)",
                "consent": r"consim[țt][ăâ]m[âă]nt",
                "contract": r"contract|executare\s+contract",
                "legal_obligation": r"obliga[țt]ie\s+legal[ăâ]",
                "legitimate_interest": r"interes\s+legitim"
            },

            # Categorii date personale
            "data_categories": {
                "identification": [
                    r"\bnume\b",
                    r"\bprenume\b",
                    r"\bCNP\b",
                    r"cod\s+numeric\s+personal",
                    r"serie\s+[șs]i\s+num[ăâ]r\s+(?:CI|BI|pa[șs]aport)",
                    r"\bemail\b",
                    r"\be-mail\b",
                    r"adres[ăâ]\s+(?:de\s+)?e-?mail",
                    r"telefon",
                    r"mobil"
                ],
                "special_categories_art9": [
                    r"date\s+medicale?",
                    r"date\s+(?:privind|despre)\s+s[ăâ]n[ăâ]tate",
                    r"date\s+biometrice",
                    r"date\s+genetice",
                    r"origine\s+rasia[lă]",
                    r"opini[iae]\s+politic[eă]",
                    r"convingeri\s+religioase",
                    r"apartenen[țt][ăâ]\s+sindical[ăâ]",
                    r"via[țt][ăâ]\s+sexual[ăâ]",
                    r"orientare\s+sexual[ăâ]"
                ],
                "criminal_records_art10": [
                    r"condamn[ăâ]ri\s+penale?",
                    r"cazier\s+(?:judiciar|penal)",
                    r"infrac[țt]iuni"
                ]
            },

            # Persoane vizate
            "data_subjects": {
                "keywords": [
                    r"(?:perso[ao]ne\s+vizate?|subiec[țt]i)",
                    r"categorii\s+(?:de\s+)?persoane"
                ],
                "categories": {
                    "angajați": r"angaja[țt]i",
                    "candidați": r"candida[țt]i|aplican[țt]i",
                    "clienți": r"clien[țt]i|consumatori",
                    "copii": r"copii|minori|sub\s+18\s+ani",
                    "pacienți": r"pacien[țt]i",
                    "elevi": r"elevi|studen[țt]i"
                }
            },

            # Volume
            "volumes": {
                "numbers": r"(\d+[\.,]?\d*)\s*(?:persoane|înregistr[ăâ]ri|subiec[țt]i|utilizatori)",
                "scale": r"scar[ăâ]\s+(?:larg[ăâ]|extins[ăâ]|mare)"
            },

            # Destinatari
            "recipients": {
                "keywords": [
                    r"destinatar[ă-ț]*",
                    r"comunicare\s+(?:c[ăâ]tre|către)",
                    r"divulgare\s+(?:c[ăâ]tre|către)",
                    r"transmitere\s+(?:c[ăâ]tre|către)"
                ]
            },

            # Transferuri internaționale
            "international_transfers": {
                "keywords": r"transfer(?:uri)?\s+(?:interna[țt]ional[eă]?|în\s+afara\s+(?:UE|SEE)|[țt][ăâ]r[ăâ]\s+ter[țt][ăâ])",
                "safeguards": [
                    r"clauze\s+(?:contractuale\s+)?standard",
                    r"SCC",
                    r"BCR",
                    r"Binding\s+Corporate\s+Rules",
                    r"decizie\s+de\s+adecvare",
                    r"art\.?\s*45",
                    r"art\.?\s*46"
                ]
            },

            # Durata stocare
            "retention": {
                "periods": [
                    r"(\d+)\s*(?:ani?|luni?|zile?|ore?)",
                    r"p[ăâ]nă\s+la\s+(.*?)(?:\.|;|\n)",
                    r"(?:perioad[ăâ]|durată)\s+(?:de\s+)?p[ăâ]strare[:\s]+(.*?)(?:\.|;|\n)",
                    r"(?:perioad[ăâ]|durată)\s+(?:de\s+)?stocare[:\s]+(.*?)(?:\.|;|\n)"
                ]
            },

            # Măsuri de securitate
            "security": {
                "encryption": [
                    r"criptare",
                    r"encryption",
                    r"AES[-\s]?\d+",
                    r"TLS\s+[\d\.]+",
                    r"SSL"
                ],
                "access_control": [
                    r"control\s+acces",
                    r"autentificare",
                    r"2FA",
                    r"MFA",
                    r"autentificare\s+(?:cu\s+)?doi\s+factori",
                    r"RBAC",
                    r"parole\s+puternice"
                ],
                "backup": [
                    r"backup",
                    r"copie\s+de\s+siguran[țt][ăâ]",
                    r"restaurare"
                ],
                "pseudonymization": [
                    r"pseudonimizare",
                    r"anonimizare",
                    r"tokenizare"
                ]
            },

            # Context
            "context": {
                "new_processing": [
                    r"(?:operațiune|prelucrare)\s+nou[ăâ]",
                    r"implementare\s+(?:nou[ăâ]|recent[ăâ])"
                ],
                "dpia_previous": [
                    r"DPIA\s+(?:anterior|precedent)",
                    r"evaluare\s+(?:anterioar[ăâ]|precedent[ăâ])"
                ],
                "incidents": [
                    r"incident",
                    r"breach",
                    r"încălcare\s+(?:de\s+)?securitate",
                    r"raportare\s+ANSPDCP"
                ]
            }
        }

    def parse_document(self, file_path: Path) -> ProcessingInfo:
        """
        Parsează un document și extrage informații relevante pentru DPIA

        Args:
            file_path: Cale către document

        Returns:
            ProcessingInfo cu informații extrase
        """
        content = self._read_document(file_path)
        if not content:
            return ProcessingInfo()

        info = ProcessingInfo()
        doc_name = file_path.name

        # Extragere împuterniciti
        info.processors = self._extract_processors(content, doc_name)

        # Extragere scopuri
        info.purposes = self._extract_purposes(content, doc_name)

        # Extragere temei juridic
        info.legal_basis = self._extract_legal_basis(content, doc_name)

        # Extragere categorii date
        info.data_categories = self._extract_data_categories(content, doc_name)

        # Extragere volume
        info.data_volume = self._extract_volume(content, doc_name)

        # Extragere persoane vizate
        info.data_subjects = self._extract_data_subjects(content, doc_name)

        # Extragere destinatari
        info.recipients_internal, info.recipients_external = self._extract_recipients(content, doc_name)

        # Extragere transferuri
        info.international_transfers = self._extract_international_transfers(content, doc_name)

        # Extragere perioade păstrare
        info.retention_periods = self._extract_retention(content, doc_name)

        # Extragere măsuri securitate
        info.security_measures = self._extract_security_measures(content, doc_name)

        # Extragere context
        info.is_new_processing = self._extract_is_new(content)
        info.previous_assessments = self._extract_previous_assessments(content)
        info.previous_incidents = self._extract_incidents(content)

        return info

    def _read_document(self, file_path: Path) -> Optional[str]:
        """Citește conținut document (suport pentru multiple formate)"""
        try:
            if file_path.suffix.lower() in ['.txt', '.md']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()

            elif file_path.suffix.lower() == '.docx':
                return self._read_docx(file_path)

            elif file_path.suffix.lower() == '.pdf':
                return self._read_pdf(file_path)

            else:
                print(f"⚠️ Format nesuportat: {file_path.suffix}")
                return None

        except Exception as e:
            print(f"❌ Eroare citire {file_path}: {e}")
            return None

    def _read_docx(self, file_path: Path) -> str:
        """Citește document DOCX (placeholder - necesită python-docx)"""
        try:
            from docx import Document
            doc = Document(file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except ImportError:
            print("⚠️ python-docx nu este instalat. Instalează cu: pip install python-docx")
            return ""
        except Exception as e:
            print(f"❌ Eroare citire DOCX: {e}")
            return ""

    def _read_pdf(self, file_path: Path) -> str:
        """Citește document PDF (placeholder - necesită pdfplumber)"""
        try:
            import pdfplumber
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
            return text
        except ImportError:
            print("⚠️ pdfplumber nu este instalat. Instalează cu: pip install pdfplumber")
            return ""
        except Exception as e:
            print(f"❌ Eroare citire PDF: {e}")
            return ""

    def _extract_processors(self, content: str, doc_name: str) -> List[Dict]:
        """Extrage informații despre împuterniciti"""
        processors = []
        content_lower = content.lower()

        for keyword_pattern in self.patterns["processors"]["keywords"]:
            matches = re.finditer(keyword_pattern, content_lower, re.IGNORECASE)
            for match in matches:
                # Extrage context (100 caractere înainte și după)
                start = max(0, match.start() - 100)
                end = min(len(content), match.end() + 100)
                context = content[start:end]

                # Încearcă să extragă nume împuternicit
                processor_info = {
                    "name": self._extract_entity_name(context),
                    "services": "",
                    "has_art28_contract": self._check_art28_contract(content),
                    "confidence": ConfidenceLevel.MEDIUM,
                    "source": doc_name,
                    "context": context.strip()
                }
                processors.append(processor_info)

        return processors if processors else []

    def _extract_purposes(self, content: str, doc_name: str) -> List[str]:
        """Extrage scopurile prelucrării"""
        purposes = []

        for pattern in self.patterns["purposes"]["keywords"]:
            matches = re.finditer(pattern, content, re.IGNORECASE | re.DOTALL)
            for match in matches:
                if match.groups():
                    purpose = match.group(1).strip()
                    if purpose and len(purpose) > 5:  # Evită matches prea scurte
                        purposes.append(purpose)

        return list(set(purposes))  # Remove duplicates

    def _extract_legal_basis(self, content: str, doc_name: str) -> Optional[Dict]:
        """Extrage temeiul juridic"""
        legal_basis = {}

        # Caută Art. 6(1)
        art6_match = re.search(self.patterns["legal_basis"]["art6"], content, re.IGNORECASE)
        if art6_match:
            letter = art6_match.group(1).lower()
            legal_basis["art6_basis"] = f"Art. 6(1)({letter})"
            legal_basis["confidence"] = ConfidenceLevel.HIGH

        # Caută Art. 9(2) pentru date speciale
        art9_match = re.search(self.patterns["legal_basis"]["art9"], content, re.IGNORECASE)
        if art9_match:
            letter = art9_match.group(1).lower()
            legal_basis["art9_basis"] = f"Art. 9(2)({letter})"
            legal_basis["special_categories"] = True

        # Dacă nu găsim articol explicit, inferăm din keywords
        if not legal_basis:
            if re.search(self.patterns["legal_basis"]["consent"], content, re.IGNORECASE):
                legal_basis["art6_basis"] = "Art. 6(1)(a) - Consimțământ (inferred)"
                legal_basis["confidence"] = ConfidenceLevel.MEDIUM

            elif re.search(self.patterns["legal_basis"]["contract"], content, re.IGNORECASE):
                legal_basis["art6_basis"] = "Art. 6(1)(b) - Contract (inferred)"
                legal_basis["confidence"] = ConfidenceLevel.MEDIUM

        return legal_basis if legal_basis else None

    def _extract_data_categories(self, content: str, doc_name: str) -> Dict[str, List[str]]:
        """Extrage categorii de date personale"""
        categories = {
            "common_data_art6": [],
            "special_categories_art9": [],
            "criminal_records_art10": []
        }

        content_lower = content.lower()

        # Date comune
        for pattern in self.patterns["data_categories"]["identification"]:
            if re.search(pattern, content_lower, re.IGNORECASE):
                categories["common_data_art6"].append(pattern.replace(r"\b", "").replace(r"\s+", " "))

        # Date speciale Art. 9
        for pattern in self.patterns["data_categories"]["special_categories_art9"]:
            if re.search(pattern, content_lower, re.IGNORECASE):
                match_text = re.search(pattern, content_lower, re.IGNORECASE).group(0)
                categories["special_categories_art9"].append(match_text)

        # Date condamnări Art. 10
        for pattern in self.patterns["data_categories"]["criminal_records_art10"]:
            if re.search(pattern, content_lower, re.IGNORECASE):
                match_text = re.search(pattern, content_lower, re.IGNORECASE).group(0)
                categories["criminal_records_art10"].append(match_text)

        return categories

    def _extract_volume(self, content: str, doc_name: str) -> Optional[int]:
        """Extrage volume/număr persoane vizate"""
        numbers_match = re.search(self.patterns["volumes"]["numbers"], content, re.IGNORECASE)
        if numbers_match:
            number_str = numbers_match.group(1).replace(".", "").replace(",", "")
            try:
                return int(number_str)
            except ValueError:
                return None
        return None

    def _extract_data_subjects(self, content: str, doc_name: str) -> List[Dict]:
        """Extrage categorii persoane vizate"""
        subjects = []

        for category, pattern in self.patterns["data_subjects"]["categories"].items():
            if re.search(pattern, content, re.IGNORECASE):
                subjects.append({
                    "category": category,
                    "confidence": ConfidenceLevel.MEDIUM
                })

        return subjects

    def _extract_recipients(self, content: str, doc_name: str) -> Tuple[List[str], List[str]]:
        """Extrage destinatari interni și externi"""
        # Placeholder - implementare simplificată
        internal = []
        external = []
        return internal, external

    def _extract_international_transfers(self, content: str, doc_name: str) -> List[Dict]:
        """Extrage informații despre transferuri internaționale"""
        transfers = []

        # Verifică dacă există mențiune de transfer
        if re.search(self.patterns["international_transfers"]["keywords"], content, re.IGNORECASE):
            transfer_info = {
                "has_transfer": True,
                "safeguards": [],
                "confidence": ConfidenceLevel.MEDIUM
            }

            # Verifică garanții
            for safeguard_pattern in self.patterns["international_transfers"]["safeguards"]:
                if re.search(safeguard_pattern, content, re.IGNORECASE):
                    transfer_info["safeguards"].append(
                        re.search(safeguard_pattern, content, re.IGNORECASE).group(0)
                    )

            transfers.append(transfer_info)

        return transfers

    def _extract_retention(self, content: str, doc_name: str) -> List[Dict]:
        """Extrage perioade de păstrare"""
        periods = []

        for pattern in self.patterns["retention"]["periods"]:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                period_text = match.group(0) if not match.groups() else match.group(1)
                periods.append({
                    "period": period_text,
                    "confidence": ConfidenceLevel.MEDIUM,
                    "source": doc_name
                })

        return periods

    def _extract_security_measures(self, content: str, doc_name: str) -> Dict[str, List[str]]:
        """Extrage măsuri tehnice și organizatorice"""
        measures = {
            "encryption": [],
            "access_control": [],
            "backup": [],
            "pseudonymization": []
        }

        content_lower = content.lower()

        for measure_type, patterns in self.patterns["security"].items():
            for pattern in patterns:
                if re.search(pattern, content_lower, re.IGNORECASE):
                    match_text = re.search(pattern, content_lower, re.IGNORECASE).group(0)
                    measures[measure_type].append(match_text)

        return measures

    def _extract_is_new(self, content: str) -> Optional[bool]:
        """Verifică dacă este prelucrare nouă"""
        for pattern in self.patterns["context"]["new_processing"]:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        return None

    def _extract_previous_assessments(self, content: str) -> List[str]:
        """Extrage mențiuni despre DPIA-uri anterioare"""
        assessments = []
        for pattern in self.patterns["context"]["dpia_previous"]:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                assessments.append(match.group(0))
        return assessments

    def _extract_incidents(self, content: str) -> List[str]:
        """Extrage mențiuni despre incidente"""
        incidents = []
        for pattern in self.patterns["context"]["incidents"]:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                incidents.append(match.group(0))
        return incidents

    def _check_art28_contract(self, content: str) -> bool:
        """Verifică existența contractului Art. 28"""
        return bool(re.search(self.patterns["processors"]["art28_contract"], content, re.IGNORECASE))

    def _extract_entity_name(self, context: str) -> str:
        """Încearcă să extragă nume entitate din context"""
        # Pattern pentru companii: SC ... SRL, SA, etc.
        company_pattern = r"S\.?C\.?\s+([A-Z][A-Za-z0-9\s]+)\s+(?:SRL|S\.R\.L\.|SA|S\.A\.)"
        match = re.search(company_pattern, context)
        if match:
            return f"SC {match.group(1).strip()} SRL/SA"

        # Altfel returnează placeholder
        return "Nume extras din context"


def merge_processing_info(info_list: List[ProcessingInfo]) -> ProcessingInfo:
    """
    Combină informații extrase din multiple documente

    Args:
        info_list: Listă de ProcessingInfo din documente diferite

    Returns:
        ProcessingInfo combinat
    """
    merged = ProcessingInfo()

    for info in info_list:
        # Merge processors
        merged.processors.extend(info.processors)

        # Merge purposes
        merged.purposes.extend(info.purposes)

        # Legal basis - ia primul găsit cu highest confidence
        if info.legal_basis and not merged.legal_basis:
            merged.legal_basis = info.legal_basis

        # Data categories - combine
        for category_type in ["common_data_art6", "special_categories_art9", "criminal_records_art10"]:
            if category_type in info.data_categories:
                if category_type not in merged.data_categories:
                    merged.data_categories[category_type] = []
                merged.data_categories[category_type].extend(info.data_categories[category_type])

        # Volume - ia maximul
        if info.data_volume:
            if not merged.data_volume or info.data_volume > merged.data_volume:
                merged.data_volume = info.data_volume

        # Data subjects
        merged.data_subjects.extend(info.data_subjects)

        # Recipients
        merged.recipients_internal.extend(info.recipients_internal)
        merged.recipients_external.extend(info.recipients_external)

        # Transfers
        merged.international_transfers.extend(info.international_transfers)

        # Retention
        merged.retention_periods.extend(info.retention_periods)

        # Security measures
        for measure_type, measures in info.security_measures.items():
            if measure_type not in merged.security_measures:
                merged.security_measures[measure_type] = []
            merged.security_measures[measure_type].extend(measures)

        # Context
        if info.is_new_processing is not None:
            merged.is_new_processing = info.is_new_processing

        merged.previous_assessments.extend(info.previous_assessments)
        merged.previous_incidents.extend(info.previous_incidents)

        # Metadata
        merged.extraction_metadata.extend(info.extraction_metadata)

    # Remove duplicates
    merged.purposes = list(set(merged.purposes))
    for category in merged.data_categories:
        merged.data_categories[category] = list(set(merged.data_categories[category]))

    return merged
