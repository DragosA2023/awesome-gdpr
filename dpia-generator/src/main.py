"""
DPIA Generator - Main Entry Point
Orchestrează întreg procesul de generare DPIA

Usage:
    python -m src.main --interactive
    python -m src.main --config config.yaml
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Import module proprii
from .core.document_parser import DocumentParser, ProcessingInfo, merge_processing_info
from .core.validator import Validator
from .core.risk_assessor import RiskAssessor
from .core.dpia_generator import DPIAGenerator
from .modules.diagram_generator import DiagramGenerator, DiagramConfig
from .modules.web_research import WebResearch
from .utils.gdpr_knowledge import GDPRKnowledge


class DPIAWorkflow:
    """Workflow complet pentru generare DPIA"""

    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.document_parser = DocumentParser()
        self.validator = Validator(interactive_mode=True)
        self.risk_assessor = RiskAssessor()
        self.diagram_generator = DiagramGenerator()
        self.dpia_generator = DPIAGenerator()
        self.web_research = WebResearch()
        self.gdpr_kb = GDPRKnowledge()

        # Data storage
        self.operator_info = {}
        self.processing_info = ProcessingInfo()
        self.risks = []
        self.legal_references = []
        self.diagrams = {}

    def run(self):
        """Execută workflow complet"""
        print("\n" + "═" * 63)
        print("🎯 SISTEM DPIA GENERATOR - START")
        print("═" * 63)
        print()
        print("Generare DPIA complet, profesional, conform GDPR.")
        print()
        print("Pași:")
        print("0. ✓ Identificare operator și proces")
        print("1. ✓ Extragere automată informații")
        print("2. ✓ Analiză necesitate DPIA")
        print("3. ✓ Consultare baze de date")
        print("4. ✓ Cercetare legislație")
        print("5. ✓ Generare DPIA text")
        print("6. ✓ Generare diagrame")
        print("7. ✓ Export document final")
        print()

        # STEP 0: Get operator and process info
        print("═" * 63)
        print("PASUL 0: IDENTIFICARE OPERATOR ȘI PROCES")
        print("═" * 63)
        self._step_0_operator_identification()

        # STEP 1: Parse documents and extract info
        print("\n" + "═" * 63)
        print("PASUL 1: EXTRAGERE AUTOMATĂ INFORMAȚII")
        print("═" * 63)
        self._step_1_extract_information()

        # Validate with user
        self._step_1b_validate_information()

        # STEP 2: Check DPIA necessity
        print("\n" + "═" * 63)
        print("PASUL 2: VERIFICARE NECESITATE DPIA")
        print("═" * 63)
        self._step_2_check_necessity()

        # STEP 3: Research legislation
        print("\n" + "═" * 63)
        print("PASUL 3: CERCETARE LEGISLAȚIE ȘI JURISPRUDENȚĂ")
        print("═" * 63)
        self._step_3_research_legislation()

        # STEP 4: Risk assessment
        print("\n" + "═" * 63)
        print("PASUL 4: EVALUARE RISCURI")
        print("═" * 63)
        self._step_4_assess_risks()

        # STEP 5: Generate diagrams
        print("\n" + "═" * 63)
        print("PASUL 5: GENERARE DIAGRAME")
        print("═" * 63)
        self._step_5_generate_diagrams()

        # STEP 6: Generate DPIA document
        print("\n" + "═" * 63)
        print("PASUL 6: GENERARE DOCUMENT DPIA")
        print("═" * 63)
        dpia_document = self._step_6_generate_dpia()

        # STEP 7: Save output
        print("\n" + "═" * 63)
        print("PASUL 7: EXPORT DOCUMENT FINAL")
        print("═" * 63)
        self._step_7_export(dpia_document)

        # Done!
        print("\n" + "═" * 63)
        print("✅ DPIA GENERAT CU SUCCES")
        print("═" * 63)
        print(f"\n📁 Documentul a fost salvat în: {self.output_dir}")
        print(f"📄 Fișier principal: DPIA_{self.operator_info.get('name', 'Operator').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md")
        print("\nMultumesc pentru utilizarea DPIA Generator!")

    def _step_0_operator_identification(self):
        """Step 0: Get operator and process information from user"""
        print("\nPentru a începe generarea DPIA, am nevoie de informații de bază:\n")

        # Operator info
        print("─" * 63)
        print("1. OPERATOR DE DATE")
        print("─" * 63)

        self.operator_info = {
            'name': self._ask_input("Denumire completă operator"),
            'legal_form': self._ask_input("Forma juridică (SRL/SA/PFA/etc.)"),
            'cui': self._ask_input("CUI/CIF"),
            'address': self._ask_input("Adresă sediu social"),
            'contact_person': self._ask_input("Persoană contact (reprezentant legal)"),
            'phone': self._ask_input("Telefon contact"),
            'email': self._ask_input("Email contact"),
        }

        # DPO
        has_dpo = self._ask_yes_no("Are operator DPO desemnat?")
        self.operator_info['has_dpo'] = has_dpo

        if has_dpo:
            self.operator_info['dpo_name'] = self._ask_input("Nume DPO")
            self.operator_info['dpo_contact'] = self._ask_input("Contact DPO (email/telefon)")

        # Process info
        print("\n─" * 63)
        print("2. OPERAȚIUNE/PROCES DE PRELUCRARE")
        print("─" * 63)

        self.operator_info['process_name'] = self._ask_input("Denumire operațiune/proces")
        self.operator_info['process_description'] = self._ask_input("Descriere sumară (2-3 propoziții)")

        is_new_options = ["NOU - Prelucrare nouă", "MODIFICARE - Modificare substanțială", "EXISTENT - Prelucrare existentă"]
        is_new_choice = self._ask_choice("Tip prelucrare", is_new_options)
        self.operator_info['is_new'] = is_new_choice.startswith("NOU") or is_new_choice.startswith("MODIFICARE")

        print("\n✓ Informații operator și proces primite.")

    def _step_1_extract_information(self):
        """Step 1: Extract information from documents"""
        print("\nDorești să încarci documente pentru extragere automată informații?")
        print("(Registru Art. 30, contracte împuternicire, politici, proceduri, etc.)")

        load_docs = self._ask_yes_no("Încarci documente")

        if load_docs:
            docs_dir = self._ask_input("Introdu calea către directorul cu documente")
            docs_path = Path(docs_dir)

            if docs_path.exists() and docs_path.is_dir():
                print(f"\n🔍 Scanez directorul: {docs_path}")

                # Parse all documents
                all_processing_info = []
                for doc_file in docs_path.glob("**/*"):
                    if doc_file.is_file() and doc_file.suffix.lower() in ['.txt', '.md', '.docx', '.pdf']:
                        print(f"   📄 Procesez: {doc_file.name}")
                        try:
                            info = self.document_parser.parse_document(doc_file)
                            all_processing_info.append(info)
                        except Exception as e:
                            print(f"   ⚠️ Eroare: {e}")

                # Merge all extracted info
                if all_processing_info:
                    self.processing_info = merge_processing_info(all_processing_info)
                    print(f"\n✓ Procesate {len(all_processing_info)} documente")
                else:
                    print("\n⚠️ Nu am putut extrage informații din documente")
            else:
                print(f"\n❌ Directorul nu există: {docs_path}")
        else:
            print("\n⚠️ Vei introduce informațiile manual în pasul următor")

        # Set from operator info
        self.processing_info.is_new_processing = self.operator_info.get('is_new')

    def _step_1b_validate_information(self):
        """Step 1b: Validate extracted information with user"""
        print("\n🔍 Validare informații extrase...")

        # Prepare processing info dict for validator
        processing_info_dict = {
            'processors': self.processing_info.processors,
            'purposes': self.processing_info.purposes,
            'legal_basis': self.processing_info.legal_basis,
            'data_categories': self.processing_info.data_categories,
            'data_volume': self.processing_info.data_volume,
            'data_subjects': self.processing_info.data_subjects,
            'recipients_internal': self.processing_info.recipients_internal,
            'recipients_external': self.processing_info.recipients_external,
            'international_transfers': self.processing_info.international_transfers,
            'retention_periods': self.processing_info.retention_periods,
            'security_measures': self.processing_info.security_measures,
            'is_new_processing': self.processing_info.is_new_processing,
            'has_dpo': self.operator_info.get('has_dpo'),
            'dpo_name': self.operator_info.get('dpo_name'),
        }

        # Run validator (interactive)
        validated_info = self.validator.validate_processing_info(
            self.processing_info,
            self.operator_info,
            ask_user_func=None  # Uses default CLI prompts
        )

        # Update processing info
        self.processing_info = validated_info

        print("\n✓ Validare completă")

    def _step_2_check_necessity(self):
        """Step 2: Check if DPIA is necessary"""
        print("\n📋 Verific dacă DPIA este necesară conform Art. 35 GDPR...\n")

        # Prepare characteristics
        characteristics = {
            'systematic_evaluation': False,
            'special_categories_large_scale': False,
            'systematic_monitoring': False,
            'new_technologies': False,
            'vulnerable_persons': False,
        }

        # Check special categories
        if self.processing_info.data_categories.get('special_categories_art9'):
            characteristics['special_categories_large_scale'] = True
            print("✓ Identificate categorii speciale de date (Art. 9)")

        # Check children
        if any('copii' in str(s).lower() or 'minori' in str(s).lower()
               for s in self.processing_info.data_subjects):
            characteristics['vulnerable_persons'] = True
            print("✓ Identificate persoane vulnerabile (copii)")

        # Check necessity
        result = self.gdpr_kb.check_dpia_necessity(characteristics)

        print(f"\n{'─' * 63}")
        print("REZULTAT:")
        print(f"{'─' * 63}\n")

        if result['dpia_required']:
            print("✅ DPIA ESTE NECESARĂ")
            print("\nMotive:")
            for trigger in result['triggers']:
                print(f"  • {trigger['criterion']}")
                print(f"    Sursă: {trigger['source']}")
            print("\nPrelucrarea prezintă risc ridicat conform Art. 35 GDPR.")
        else:
            print("ℹ️ DPIA nu este strict obligatorie")
            print("\nTotuși, continuăm cu generarea DPIA ca bună practică.")

        print(f"\n{'─' * 63}\n")
        print("Continuăm cu generarea DPIA complete...")

    def _step_3_research_legislation(self):
        """Step 3: Research legislation and case law"""
        print("\n🔍 Cercetez legislație și jurisprudență relevantă...\n")

        # Prepare characteristics
        characteristics = {
            'has_international_transfers': bool(self.processing_info.international_transfers),
            'has_special_categories': bool(self.processing_info.data_categories.get('special_categories_art9')),
        }

        # Research
        self.legal_references = self.web_research.research_for_dpia(characteristics)

        print(f"✓ Identificate {len(self.legal_references)} referințe legislative:")
        print(f"  • Articole GDPR: {len([r for r in self.legal_references if r.type == 'gdpr_article'])}")
        print(f"  • Guidelines EDPB/WP29: {len([r for r in self.legal_references if r.type == 'edpb_guideline'])}")
        print(f"  • Jurisprudență CJUE: {len([r for r in self.legal_references if r.type == 'cjeu_case'])}")
        print(f"  • Resurse ANSPDCP: {len([r for r in self.legal_references if r.type in ['anspdcp_decision', 'national_law']])}")

    def _step_4_assess_risks(self):
        """Step 4: Assess risks"""
        print("\n⚠️ Evaluez riscurile pentru drepturile persoanelor vizate...\n")

        # Prepare processing characteristics for risk assessment
        processing_characteristics = {
            'has_special_categories': bool(self.processing_info.data_categories.get('special_categories_art9')),
            'includes_children': any('copii' in str(s).lower() for s in self.processing_info.data_subjects),
            'has_international_transfers': bool(self.processing_info.international_transfers),
            'has_processors': bool(self.processing_info.processors),
            'has_profiling': False,  # TODO: detect from purposes
            'has_automated_decision': False,  # TODO: detect
            'has_systematic_monitoring': False,  # TODO: detect
            'has_encryption': bool(self.processing_info.security_measures.get('encryption')),
            'has_access_control': bool(self.processing_info.security_measures.get('access_control')),
            'has_security_training': False,  # TODO: detect
            'has_internet_facing_systems': True,  # Assume yes by default
            'has_privacy_notice': True,  # Assume yes
            'has_rights_procedures': True,  # Assume yes
            'risk_excessive_data': False,  # TODO: analyze
            'has_retention_policy': bool(self.processing_info.retention_periods),
        }

        # Assess
        self.risks = self.risk_assessor.assess_risks(
            processing_characteristics,
            self.processing_info.security_measures
        )

        print(f"✓ Identificate și evaluate {len(self.risks)} riscuri:")

        for risk in self.risks:
            emoji = self._get_risk_emoji(risk.residual_level.value)
            print(f"  {emoji} {risk.risk_id}: {risk.name}")
            print(f"     Inerent: {risk.inherent_score} → Rezidual: {risk.residual_score} ({len(risk.mitigation_measures)} măsuri)")

        # Check if prior consultation needed
        if self.risk_assessor.check_prior_consultation_needed():
            print("\n⚠️ ATENȚIE: Consultare prealabilă ANSPDCP necesară (Art. 36)")
            print("   Riscuri reziduale ridicate persistă după măsuri.")

    def _step_5_generate_diagrams(self):
        """Step 5: Generate diagrams"""
        print("\n📊 Generez diagrame pentru DPIA...\n")

        # Prepare info for diagrams
        processing_info_dict = {
            'operator': self.operator_info,
            'processors': self.processing_info.processors,
            'recipients_external': self.processing_info.recipients_external,
            'international_transfers': self.processing_info.international_transfers,
            'data_subjects': self.processing_info.data_subjects,
            'data_categories': self.processing_info.data_categories,
            'purposes': self.processing_info.purposes,
            'legal_basis': self.processing_info.legal_basis,
            'retention_periods': self.processing_info.retention_periods,
            'dpo': {'name': self.operator_info.get('dpo_name', 'N/A')},
        }

        # Configure which diagrams to generate
        config = DiagramConfig(
            include_dfd=True,
            include_lifecycle=True,
            include_risk_matrix=True,
            include_architecture=False,  # Optional
            include_roles=bool(self.operator_info.get('has_dpo')),  # If has DPO
            include_timeline=False  # Optional
        )

        # Generate
        self.diagrams = self.diagram_generator.generate_all_diagrams(
            processing_info_dict,
            self.risks,
            config
        )

        print(f"✓ Generate {len(self.diagrams)} diagrame:")
        for diagram_name in self.diagrams.keys():
            print(f"  • {diagram_name.upper()}")

    def _step_6_generate_dpia(self):
        """Step 6: Generate DPIA document"""
        print("\n📝 Generez documentul DPIA complet...\n")
        print("Generare secțiuni conform Art. 35(7) GDPR:")

        # Prepare all data
        processing_info_dict = {
            'operator': self.operator_info,
            'process_name': self.operator_info.get('process_name'),
            'operation_type': 'Prelucrare automată și manuală',
            'is_new_processing': self.processing_info.is_new_processing,
            'detailed_description': self.operator_info.get('process_description', ''),
            'purposes': self.processing_info.purposes,
            'legal_basis': self.processing_info.legal_basis,
            'data_categories': self.processing_info.data_categories,
            'data_volume': self.processing_info.data_volume,
            'data_sources': self.processing_info.data_sources,
            'data_subjects': self.processing_info.data_subjects,
            'processors': self.processing_info.processors,
            'recipients_internal': self.processing_info.recipients_internal,
            'recipients_external': self.processing_info.recipients_external,
            'international_transfers': self.processing_info.international_transfers,
            'retention_periods': self.processing_info.retention_periods,
            'security_measures': self.processing_info.security_measures,
            'has_dpo': self.operator_info.get('has_dpo'),
            'dpo_name': self.operator_info.get('dpo_name'),
        }

        # Generate
        dpia_doc = self.dpia_generator.generate_dpia(
            self.operator_info,
            processing_info_dict,
            self.risks,
            self.legal_references,
            self.diagrams
        )

        print("✓ Secțiune 1: Identificarea părților")
        print("✓ Secțiune 2: Descrierea operațiunii")
        print("✓ Secțiune 3: Evaluarea necesității")
        print("✓ Secțiune 4: Evaluarea riscurilor")
        print("✓ Secțiune 5: Măsuri tehnice și organizatorice")
        print("✓ Secțiune 6: Consultări")
        print("✓ Secțiune 7: Concluzii și aprobare")
        print("✓ Anexe")

        print(f"\n📄 Document generat:")
        print(f"   • Pagini: ~{len(dpia_doc.content) // 3000} (estimate)")
        print(f"   • Riscuri: {dpia_doc.metadata['total_risks']}")
        print(f"   • Versiune: {dpia_doc.metadata['version']}")

        return dpia_doc

    def _step_7_export(self, dpia_document):
        """Step 7: Export document"""
        print("\n💾 Salvez documentul...\n")

        # Generate filename
        operator_name_safe = self.operator_info.get('name', 'Operator').replace(' ', '_').replace('/', '_')
        date_str = datetime.now().strftime('%Y%m%d')
        filename_base = f"DPIA_{operator_name_safe}_{date_str}"

        # Save Markdown
        md_file = self.output_dir / f"{filename_base}.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(dpia_document.content)
        print(f"✓ Markdown: {md_file}")

        # Save legal references
        references_content = self.web_research.generate_references_section()
        ref_file = self.output_dir / f"{filename_base}_Referinte.md"
        with open(ref_file, 'w', encoding='utf-8') as f:
            f.write(references_content)
        print(f"✓ Referințe: {ref_file}")

        # Save diagrams
        diagrams_dir = self.output_dir / "diagrams"
        saved_diagrams = self.diagram_generator.save_diagrams_to_files(str(diagrams_dir))
        print(f"✓ Diagrame: {len(saved_diagrams)} fișiere în {diagrams_dir}")

        # Save metadata
        import json
        metadata_file = self.output_dir / f"{filename_base}_metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(dpia_document.metadata, f, indent=2, ensure_ascii=False)
        print(f"✓ Metadata: {metadata_file}")

        print("\n✅ Export complet!")

    # Helper methods
    def _ask_input(self, prompt: str) -> str:
        """Ask user for text input"""
        return input(f"➜ {prompt}: ")

    def _ask_yes_no(self, prompt: str) -> bool:
        """Ask user yes/no question"""
        while True:
            answer = input(f"➜ {prompt} (DA/NU): ").strip().upper()
            if answer in ['DA', 'D', 'YES', 'Y']:
                return True
            elif answer in ['NU', 'N', 'NO']:
                return False
            else:
                print("   Răspuns invalid. Te rog răspunde DA sau NU.")

    def _ask_choice(self, prompt: str, options: List[str]) -> str:
        """Ask user to choose from options"""
        print(f"\n{prompt}:")
        for idx, option in enumerate(options, 1):
            print(f"  {idx}. {option}")

        while True:
            try:
                choice = int(input("➜ Alege (număr): "))
                if 1 <= choice <= len(options):
                    return options[choice - 1]
                else:
                    print(f"   Opțiune invalidă. Alege între 1 și {len(options)}.")
            except ValueError:
                print("   Te rog introdu un număr valid.")

    def _get_risk_emoji(self, level: str) -> str:
        """Get emoji for risk level"""
        emojis = {"low": "🟢", "medium": "🟡", "high": "🟠", "critical": "🔴"}
        return emojis.get(level, "⚪")


def main():
    """Main entry point"""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║                                                           ║")
    print("║            🎯 DPIA GENERATOR SYSTEM v1.0                  ║")
    print("║                                                           ║")
    print("║   Generare DPIA conform Art. 35 GDPR                      ║")
    print("║   Legislație română - ANSPDCP                            ║")
    print("║                                                           ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print()

    # Run workflow
    workflow = DPIAWorkflow(output_dir="output")

    try:
        workflow.run()
    except KeyboardInterrupt:
        print("\n\n⚠️ Procesul a fost întrerupt de utilizator.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Eroare în timpul execuției: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
