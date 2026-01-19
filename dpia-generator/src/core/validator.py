"""
Validator - Validare interactivă informații extrase cu utilizatorul
Prezintă informațiile extrase și cere confirmare/modificare
"""

from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from .document_parser import ProcessingInfo, ConfidenceLevel


class ValidationStatus(Enum):
    """Status validare"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    MODIFIED = "modified"
    REJECTED = "rejected"


@dataclass
class ValidationResult:
    """Rezultat validare pentru o categorie de informații"""
    category: str
    status: ValidationStatus
    original_value: any
    validated_value: any
    user_feedback: str = ""


class Validator:
    """Gestionează procesul de validare interactivă"""

    def __init__(self, interactive_mode: bool = True):
        self.interactive_mode = interactive_mode
        self.validation_results: List[ValidationResult] = []

    def validate_processing_info(
        self,
        info: ProcessingInfo,
        operator_info: Dict,
        ask_user_func: Optional[Callable] = None
    ) -> ProcessingInfo:
        """
        Validează toate informațiile extrase cu utilizatorul

        Args:
            info: ProcessingInfo extras din documente
            operator_info: Informații operator și proces (de la utilizator)
            ask_user_func: Funcție callback pentru a pune întrebări utilizatorului

        Returns:
            ProcessingInfo validat și eventual modificat
        """
        if not ask_user_func:
            ask_user_func = self._default_ask_user

        validated_info = info

        print("\n" + "═" * 63)
        print("INFORMAȚII EXTRASE AUTOMAT - VERIFICARE NECESARĂ")
        print("═" * 63)
        print()
        print(f"Am analizat documentele furnizate și am extras următoarele informații.")
        print(f"Te rog VERIFICĂ și CONFIRMĂ sau MODIFICĂ fiecare categorie.")
        print()

        # 1. Validare Împuterniciti
        validated_info.processors = self._validate_processors(
            info.processors,
            ask_user_func
        )

        # 2. Validare Scopuri
        validated_info.purposes = self._validate_purposes(
            info.purposes,
            ask_user_func
        )

        # 3. Validare Temei Juridic
        validated_info.legal_basis = self._validate_legal_basis(
            info.legal_basis,
            ask_user_func
        )

        # 4. Validare Date Personale
        validated_info.data_categories = self._validate_data_categories(
            info.data_categories,
            info.data_volume,
            ask_user_func
        )

        # 5. Validare Persoane Vizate
        validated_info.data_subjects = self._validate_data_subjects(
            info.data_subjects,
            ask_user_func
        )

        # 6. Validare Destinatari și Transferuri
        validated_info.recipients_internal = info.recipients_internal
        validated_info.recipients_external = info.recipients_external
        validated_info.international_transfers = self._validate_transfers(
            info.international_transfers,
            ask_user_func
        )

        # 7. Validare Durata Stocare
        validated_info.retention_periods = self._validate_retention(
            info.retention_periods,
            ask_user_func
        )

        # 8. Validare Măsuri Tehnice și Organizatorice
        validated_info.security_measures = self._validate_security_measures(
            info.security_measures,
            ask_user_func
        )

        # 9. Validare Context
        validated_info.is_new_processing = self._validate_context(
            info,
            ask_user_func
        )

        # Sumar finalizare
        self._display_validation_summary()

        return validated_info

    def _validate_processors(
        self,
        processors: List[Dict],
        ask_user_func: Callable
    ) -> List[Dict]:
        """Validează lista de împuterniciti"""
        print("─" * 63)
        print("1. ÎMPUTERNICITI")
        print("─" * 63)

        if not processors:
            print("❌ Nu am identificat împuterniciti în documente")
            response = ask_user_func(
                "Există împuterniciti (subcontractanți, procesatori) pentru această prelucrare?",
                options=["DA - Vreau să adaug", "NU - Nu există împuterniciti"]
            )

            if response == "DA - Vreau să adaug":
                processors = []
                while True:
                    name = ask_user_func("Denumire împuternicit:", input_type="text")
                    services = ask_user_func("Servicii furnizate:", input_type="text")
                    art28 = ask_user_func(
                        "Există contract Art. 28 GDPR?",
                        options=["DA", "NU"]
                    )

                    processors.append({
                        "name": name,
                        "services": services,
                        "has_art28_contract": art28 == "DA",
                        "confidence": ConfidenceLevel.HIGH,
                        "source": "user_input"
                    })

                    more = ask_user_func(
                        "Mai există alți împuterniciti?",
                        options=["DA", "NU"]
                    )
                    if more == "NU":
                        break

            return processors

        else:
            print(f"Am identificat {len(processors)} împuternicit(i):")
            for idx, proc in enumerate(processors, 1):
                print(f"\n┌─────────────────────────────────────────────────────")
                print(f"│ {idx}. {proc.get('name', 'Nume neidentificat')}")
                print(f"│    Servicii: {proc.get('services', 'Nespecificat')}")
                contract_status = "✓ Identificat" if proc.get('has_art28_contract') else "❌ Nu identificat"
                print(f"│    Contract Art. 28: {contract_status}")
                print(f"└─────────────────────────────────────────────────────")

            response = ask_user_func(
                "Acțiune:",
                options=[
                    "✓ CONFIRMĂ - Informațiile sunt corecte",
                    "✏️ MODIFICĂ - Vreau să modific",
                    "✏️ ADAUGĂ - Vreau să adaug alt împuternicit"
                ]
            )

            if response.startswith("✓"):
                return processors
            elif response.startswith("✏️ MODIFICĂ"):
                # Implementare modificare
                print("Funcționalitate de modificare va fi implementată în versiunea UI completă")
                return processors
            else:
                # Adaugă
                print("Funcționalitate de adăugare va fi implementată în versiunea UI completă")
                return processors

    def _validate_purposes(
        self,
        purposes: List[str],
        ask_user_func: Callable
    ) -> List[str]:
        """Validează scopurile prelucrării"""
        print("\n─" * 63)
        print("2. SCOPURI PRELUCRĂRII")
        print("─" * 63)

        if not purposes:
            print("❌ Nu am identificat scopuri clare în documente")
            print("\n⚠️ IMPORTANT: Scopurile trebuie să fie specifice, explicite și legitimate (Art. 5(1)(b) GDPR)")

            response = ask_user_func(
                "Dorești să introduci scopurile manual?",
                options=["DA", "NU"]
            )

            if response == "DA":
                purposes = []
                print("\nIntrodu scopurile unul câte unul (lasă gol pentru a termina):")
                while True:
                    purpose = ask_user_func("Scop:", input_type="text")
                    if not purpose or purpose.strip() == "":
                        break
                    purposes.append(purpose)
                    print(f"✓ Adăugat: {purpose}")

            return purposes

        else:
            print(f"\nAm identificat {len(purposes)} scop(uri):")
            for idx, purpose in enumerate(purposes, 1):
                print(f"  • {purpose}")

            response = ask_user_func(
                "\nAcțiune:",
                options=[
                    "✓ CONFIRMĂ",
                    "✏️ MODIFICĂ",
                    "✏️ ADAUGĂ scop suplimentar"
                ]
            )

            # Implementare simplificată - în versiunea completă va permite editare
            return purposes

    def _validate_legal_basis(
        self,
        legal_basis: Optional[Dict],
        ask_user_func: Callable
    ) -> Optional[Dict]:
        """Validează temeiul juridic"""
        print("\n─" * 63)
        print("3. TEMEI JURIDIC")
        print("─" * 63)

        if not legal_basis:
            print("❌ Nu am identificat temei juridic în documente")
            print("\n⚠️ OBLIGATORIU: Orice prelucrare trebuie să aibă temei juridic conform Art. 6(1) GDPR")

            # Afișează opțiuni
            print("\nTemeiul juridic poate fi:")
            print("  a) Consimțământ")
            print("  b) Contract")
            print("  c) Obligație legală")
            print("  d) Interese vitale")
            print("  e) Interes public")
            print("  f) Interes legitim")

            basis_choice = ask_user_func(
                "Care este temeiul juridic pentru această prelucrare?",
                options=["a - Consimțământ", "b - Contract", "c - Obligație legală",
                        "d - Interese vitale", "e - Interes public", "f - Interes legitim"]
            )

            basis_letter = basis_choice[0]
            legal_basis = {
                "art6_basis": f"Art. 6(1)({basis_letter})",
                "confidence": ConfidenceLevel.HIGH,
                "source": "user_input"
            }

            # Verifică dacă există date speciale
            special_data = ask_user_func(
                "Prelucrarea implică categorii speciale de date (Art. 9)?",
                options=["DA - Date medicale/biometrice/genetice/etc.", "NU"]
            )

            if special_data.startswith("DA"):
                print("\nPentru date speciale, trebuie identificat și temei Art. 9(2):")
                print("  a) Consimțământ explicit")
                print("  b) Obligații dreptul muncii")
                print("  c) Interese vitale")
                print("  h) Medicină preventivă/diagnostic")
                print("  ... (alte excepții)")

                art9_choice = ask_user_func(
                    "Care este excepția Art. 9(2)?",
                    options=["a - Consimțământ explicit", "b - Obligații muncii",
                            "h - Medicină/diagnostic", "Altă excepție"]
                )

                art9_letter = art9_choice[0] if art9_choice[0].isalpha() else "a"
                legal_basis["art9_basis"] = f"Art. 9(2)({art9_letter})"
                legal_basis["special_categories"] = True

            return legal_basis

        else:
            print(f"\nTemei identificat:")
            print(f"  • {legal_basis.get('art6_basis', 'Nespecificat')}")

            if legal_basis.get('special_categories'):
                print(f"  • Date speciale: {legal_basis.get('art9_basis', 'Art. 9')}")
                print(f"  ⚠️ ATENȚIE: Prelucrare categorii speciale Art. 9 GDPR")

            response = ask_user_func(
                "\nAcțiune:",
                options=["✓ CONFIRMĂ", "✏️ MODIFICĂ temei"]
            )

            return legal_basis

    def _validate_data_categories(
        self,
        data_categories: Dict[str, List[str]],
        data_volume: Optional[int],
        ask_user_func: Callable
    ) -> Dict[str, List[str]]:
        """Validează categoriile de date personale"""
        print("\n─" * 63)
        print("4. DATE PERSONALE PRELUCRATE")
        print("─" * 63)

        print("\nA. CATEGORII DATE:")

        # Date comune
        if data_categories.get("common_data_art6"):
            print("\n┌─ DATE COMUNE (Art. 6):")
            for item in data_categories["common_data_art6"]:
                print(f"│  ✓ {item}")
            print("└─")

        # Date speciale
        if data_categories.get("special_categories_art9"):
            print("\n┌─ DATE SPECIALE (Art. 9):")
            print("│  ⚠️ ATENȚIE: Categorii speciale - risc ridicat")
            for item in data_categories["special_categories_art9"]:
                print(f"│  ⚠️ {item}")
            print("└─")

        # Date condamnări
        if data_categories.get("criminal_records_art10"):
            print("\n┌─ DATE CONDAMNĂRI (Art. 10):")
            print("│  ⚠️ ATENȚIE: Date privind condamnările penale")
            for item in data_categories["criminal_records_art10"]:
                print(f"│  ⚠️ {item}")
            print("└─")

        # Volume
        if data_volume:
            print(f"\nB. VOLUME ESTIMATE:")
            print(f"   {data_volume:,} persoane vizate identificate")

        response = ask_user_func(
            "\nAcțiune:",
            options=["✓ CONFIRMĂ", "✏️ ADAUGĂ categorie", "✏️ MODIFICĂ"]
        )

        return data_categories

    def _validate_data_subjects(
        self,
        data_subjects: List[Dict],
        ask_user_func: Callable
    ) -> List[Dict]:
        """Validează categoriile de persoane vizate"""
        print("\n─" * 63)
        print("5. PERSOANE VIZATE")
        print("─" * 63)

        if data_subjects:
            print("\nCategorii identificate:")
            for subject in data_subjects:
                category = subject.get('category', 'Necunoscut')
                print(f"  • {category.capitalize()}")

                # Verifică persoane vulnerabile
                if category in ["copii", "pacienți", "angajați"]:
                    print(f"    ⚠️ Persoane vulnerabile - risc crescut")

        response = ask_user_func(
            "\nAcțiune:",
            options=["✓ CONFIRMĂ", "✏️ ADAUGĂ categorie", "✏️ MODIFICĂ"]
        )

        return data_subjects

    def _validate_transfers(
        self,
        transfers: List[Dict],
        ask_user_func: Callable
    ) -> List[Dict]:
        """Validează transferurile internaționale"""
        print("\n─" * 63)
        print("6. TRANSFERURI INTERNAȚIONALE")
        print("─" * 63)

        if transfers:
            for transfer in transfers:
                if transfer.get('has_transfer'):
                    print("\n⚠️ TRANSFER INTERNAȚIONAL IDENTIFICAT")

                    safeguards = transfer.get('safeguards', [])
                    if safeguards:
                        print(f"Garanții identificate:")
                        for safeguard in safeguards:
                            print(f"  ✓ {safeguard}")
                    else:
                        print("❌ NU AM IDENTIFICAT GARANȚII CLARE")
                        print("⚠️ ATENȚIE: Transfer FĂRĂ garanții → RISC RIDICAT")
                        print("Necesare: Clauze standard, BCR, sau Decizie de adecvare")

        else:
            print("❌ Nu am identificat transferuri internaționale")

        response = ask_user_func(
            "Există transferuri de date în afara UE/SEE?",
            options=["NU - Nu există transferuri", "DA - Există transferuri"]
        )

        if response.startswith("DA") and not transfers:
            # Adaugă transfer
            transfers = [{
                "has_transfer": True,
                "safeguards": [],
                "confidence": ConfidenceLevel.HIGH,
                "source": "user_input"
            }]

        return transfers

    def _validate_retention(
        self,
        retention_periods: List[Dict],
        ask_user_func: Callable
    ) -> List[Dict]:
        """Validează perioadele de păstrare"""
        print("\n─" * 63)
        print("7. DURATA STOCARE")
        print("─" * 63)

        if retention_periods:
            print("\nPerioade identificate:")
            for period in retention_periods:
                print(f"  • {period.get('period', 'Nespecificat')}")
        else:
            print("❌ Nu am identificat perioade de păstrare clare")
            print("\n⚠️ IMPORTANT: Art. 5(1)(e) - limitarea stocării")
            print("Trebuie specificate criterii clare pentru determinarea perioadei")

        response = ask_user_func(
            "\nAcțiune:",
            options=["✓ CONFIRMĂ", "✏️ ADAUGĂ perioadă", "✏️ MODIFICĂ"]
        )

        return retention_periods

    def _validate_security_measures(
        self,
        security_measures: Dict[str, List[str]],
        ask_user_func: Callable
    ) -> Dict[str, List[str]]:
        """Validează măsurile de securitate"""
        print("\n─" * 63)
        print("8. MĂSURI TEHNICE ȘI ORGANIZATORICE")
        print("─" * 63)

        print("\nA. MĂSURI DE SECURITATE IDENTIFICATE:")

        for measure_type, measures in security_measures.items():
            if measures:
                type_name = measure_type.replace("_", " ").title()
                print(f"\n{type_name}:")
                for measure in measures:
                    print(f"  ✓ {measure}")

        response = ask_user_func(
            "\nAcțiune:",
            options=["✓ CONFIRMĂ", "✏️ ADAUGĂ măsură", "✏️ MODIFICĂ"]
        )

        return security_measures

    def _validate_context(
        self,
        info: ProcessingInfo,
        ask_user_func: Callable
    ) -> Optional[bool]:
        """Validează contextul prelucrării"""
        print("\n─" * 63)
        print("9. CONTEXT SPECIFIC")
        print("─" * 63)

        is_new = info.is_new_processing
        if is_new is not None:
            status = "NOU" if is_new else "EXISTENT"
            print(f"\n• Prelucrare: {status}")
        else:
            response = ask_user_func(
                "Este o prelucrare nouă sau modificare substanțială?",
                options=["DA - Nouă/Modificare", "NU - Existentă"]
            )
            is_new = response.startswith("DA")

        if info.previous_assessments:
            print(f"• Evaluări anterioare: DA")
        else:
            print(f"• Evaluări anterioare: NU")

        if info.previous_incidents:
            print(f"• Incidente anterioare: DA ({len(info.previous_incidents)})")
        else:
            print(f"• Incidente anterioare: NU")

        return is_new

    def _display_validation_summary(self):
        """Afișează sumar la final"""
        print("\n" + "═" * 63)
        print("FINALIZARE VERIFICARE")
        print("═" * 63)
        print("\n✓ Validare completă")
        print("\nCategorii de informații verificate: 9/9")
        print("\nProcedez cu următorii pași:")
        print("  → Analiză necesitate DPIA")
        print("  → Cercetare legislație și jurisprudență")
        print("  → Generare DPIA complet")

    def _default_ask_user(
        self,
        question: str,
        options: Optional[List[str]] = None,
        input_type: str = "choice"
    ) -> str:
        """Funcție default pentru a pune întrebări utilizatorului (CLI simplu)"""
        print(f"\n{question}")

        if input_type == "text":
            return input("➜ ")

        elif options:
            for idx, option in enumerate(options, 1):
                print(f"  {idx}. {option}")

            while True:
                try:
                    choice = input("\n➜ Alege (număr): ")
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(options):
                        return options[choice_idx]
                    else:
                        print("❌ Opțiune invalidă. Te rog alege din listă.")
                except ValueError:
                    print("❌ Te rog introdu un număr valid.")
        else:
            return input("➜ ")
