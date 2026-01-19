"""
GDPR Knowledge Base - Bază de cunoștințe GDPR pentru sistem DPIA Generator
Conține toate referințele legislative, criterii, și cunoștințe necesare
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class GDPRArticle:
    """Reprezentare articol GDPR"""
    number: str
    title: str
    text_ro: str
    text_en: str
    relevant_recitals: List[int]


@dataclass
class RiskCriteria:
    """Criterii evaluare risc conform GDPR"""
    name: str
    description: str
    severity_levels: Dict[str, str]
    probability_levels: Dict[str, str]


class GDPRKnowledge:
    """Bază centralizată de cunoștințe GDPR"""

    # Art. 35 GDPR - Evaluarea impactului asupra protecției datelor
    ART_35_CRITERIA = {
        "systematic_extensive_evaluation": {
            "name": "Evaluare sistematică și pe scară largă a aspectelor personale",
            "description": "Procesare automată inclusiv crearea de profiluri cu efecte juridice sau similare",
            "examples": ["credit scoring", "profilare comportamentală", "evaluare performanță"]
        },
        "large_scale_special_categories": {
            "name": "Prelucrare la scară largă a categoriilor speciale (Art. 9) sau condamnări (Art. 10)",
            "description": "Procesare volume mari date sensibile",
            "examples": ["spitale", "case de sănătate", "cercetare medicală"]
        },
        "systematic_monitoring": {
            "name": "Monitorizare sistematică la scară largă a unei zone accesibile publicului",
            "description": "Supraveghere continuă și sistematică",
            "examples": ["videosupraveghere", "tracking online", "geolocalizare"]
        }
    }

    # Lista ANSPDCP (Decizia 174/2018) - Operațiuni care necesită DPIA
    ANSPDCP_DPIA_LIST = [
        {
            "id": 1,
            "description": "Evaluarea, inclusiv crearea de profiluri, în special pe baza prelucrării automata a aspectelor personale",
            "examples": ["scoring credite", "evaluări performanță", "asigurări"]
        },
        {
            "id": 2,
            "description": "Prelucrarea la scară largă a categoriilor speciale de date sau a datelor privind condamnările penale",
            "examples": ["spitale mari", "laboratoare analize", "casiere de sănătate"]
        },
        {
            "id": 3,
            "description": "Monitorizarea sistematică la scară largă a zonelor accesibile publicului",
            "examples": ["camere video în spații publice", "orașe smart city"]
        },
        {
            "id": 4,
            "description": "Prelucrări care implică utilizarea noilor tehnologii",
            "examples": ["AI/ML", "IoT", "biometrie", "recunoaștere facială"]
        },
        {
            "id": 5,
            "description": "Prelucrări care împiedică persoanele vizate să își exercite un drept sau să utilizeze un serviciu/contract",
            "examples": ["scoring pentru acces servicii esențiale"]
        },
        {
            "id": 6,
            "description": "Prelucrare date biometrice pentru identificare unică",
            "examples": ["control acces biometric", "autentificare facială"]
        },
        {
            "id": 7,
            "description": "Prelucrare date genetice",
            "examples": ["teste ADN", "cercetare genetică"]
        },
        {
            "id": 8,
            "description": "Potrivire/combinare seturi de date",
            "examples": ["data matching", "integrare multiple surse"]
        },
        {
            "id": 9,
            "description": "Date persoane vulnerabile (copii, angajați, persoane vârstnice, pacienți)",
            "examples": ["școli", "spitale", "case de bătrâni", "HR"]
        },
        {
            "id": 10,
            "description": "Prelucrare la scară largă",
            "examples": ["peste 10.000 persoane vizate", "procesare națională/regională"]
        }
    ]

    # Temeiul juridic Art. 6(1) GDPR
    LEGAL_BASIS_ART6 = {
        "a": {
            "name": "Consimțământ",
            "text_ro": "Persoana vizată și-a dat consimțământul pentru prelucrarea datelor sale cu caracter personal pentru unul sau mai multe scopuri specifice",
            "requirements": ["specific", "informat", "liber exprimat", "neechivoc", "dovedit"],
            "risk_factors": ["posibilitate retragere", "dezechilibru putere"]
        },
        "b": {
            "name": "Contract",
            "text_ro": "Prelucrarea este necesară pentru executarea unui contract la care persoana vizată este parte sau pentru a face demersuri la cererea persoanei vizate înainte de încheierea unui contract",
            "requirements": ["necesitate obiectivă", "legătură directă cu contractul"],
            "risk_factors": ["procesare excesivă", "scopuri secundare"]
        },
        "c": {
            "name": "Obligație legală",
            "text_ro": "Prelucrarea este necesară în vederea îndeplinirii unei obligații legale care îi revine operatorului",
            "requirements": ["obligație clară din lege", "specificată în legislație"],
            "examples": ["contabilitate", "raportări legale", "păstrare documente fiscale"]
        },
        "d": {
            "name": "Interese vitale",
            "text_ro": "Prelucrarea este necesară pentru a proteja interesele vitale ale persoanei vizate sau ale altei persoane fizice",
            "requirements": ["urgență medicală", "imposibilitate consimțământ"],
            "examples": ["urgențe medicale", "salvare vieți"]
        },
        "e": {
            "name": "Interes public",
            "text_ro": "Prelucrarea este necesară pentru îndeplinirea unei sarcini care servește unui interes public sau care rezultă din exercitarea unei autorități oficiale cu care este investit operatorul",
            "requirements": ["bază în drept UE sau național", "sarcină publică clară"],
            "examples": ["autorități publice", "servicii publice"]
        },
        "f": {
            "name": "Interes legitim",
            "text_ro": "Prelucrarea este necesară în scopul intereselor legitime urmărite de operator sau de o parte terță, cu excepția cazului în care prevalează interesele sau drepturile și libertățile fundamentale ale persoanei vizate",
            "requirements": ["LIA - Legitimate Interest Assessment", "test necesitate", "test balansare"],
            "risk_factors": ["drepturile persoanei pot prevala", "necesită DPIA adesea"]
        }
    }

    # Categorii speciale Art. 9(1) GDPR
    SPECIAL_CATEGORIES_ART9 = {
        "categories": [
            "Origine rasială sau etnică",
            "Opinii politice",
            "Convingeri religioase sau filozofice",
            "Apartenență sindicală",
            "Date genetice",
            "Date biometrice pentru identificare unică",
            "Date privind sănătatea",
            "Date privind viața sexuală sau orientarea sexuală"
        ],
        "exceptions_art9_2": {
            "a": "Consimțământ explicit",
            "b": "Obligații în dreptul muncii, securitate socială, protecție socială",
            "c": "Protecție interese vitale (când persoana nu poate consimți)",
            "d": "Activități legitime fundații/ONG-uri",
            "e": "Date făcute publice manifest de persoana vizată",
            "f": "Constatare, exercitare, apărare drepturi în instanță",
            "g": "Interes public important (bază în drept UE/național)",
            "h": "Medicină preventivă, diagnostic, sănătate (profesionist medical)",
            "i": "Interes public sănătate publică",
            "j": "Arhivare interes public, cercetare științifică/statistică"
        }
    }

    # Matrice evaluare risc
    RISK_MATRIX = {
        "severity": {
            "1_negligible": {
                "name_ro": "Neglijabilă",
                "description": "Fără impact sau impact minim, inconvenient minor",
                "examples": ["Email marketing nesolicitat ușor de dezabonat"]
            },
            "2_limited": {
                "name_ro": "Limitată",
                "description": "Impact minor, inconvenient, posibile nemulțumiri",
                "examples": ["Întârziere în răspuns la solicitări", "Erori minore date"]
            },
            "3_significant": {
                "name_ro": "Semnificativă",
                "description": "Impact important, dificultăți semnificative, posibile prejudicii",
                "examples": ["Discriminare", "Pierdere oportunități", "Daune financiare moderate"]
            },
            "4_maximum": {
                "name_ro": "Maximă",
                "description": "Impact sever sau catastrofal, consecințe grave ireversibile",
                "examples": ["Riscuri fizice", "Furt identitate", "Daune financiare majore", "Prejudicii psihologice grave"]
            }
        },
        "probability": {
            "1_negligible": {
                "name_ro": "Neglijabilă",
                "description": "Foarte improbabil, aproape imposibil",
                "examples": ["Măsuri multiple securitate", "Toate controalele funcționează"]
            },
            "2_limited": {
                "name_ro": "Limitată",
                "description": "Posibil dar puțin probabil",
                "examples": ["Măsuri bune dar cu unele vulnerabilități minore"]
            },
            "3_significant": {
                "name_ro": "Semnificativă",
                "description": "Probabil să apară în anumite condiții",
                "examples": ["Măsuri parțiale", "Unele controale lipsesc"]
            },
            "4_maximum": {
                "name_ro": "Maximă",
                "description": "Foarte probabil sau aproape sigur",
                "examples": ["Fără măsuri adecvate", "Vulnerabilități cunoscute"]
            }
        },
        "risk_levels": {
            "1-4": {"level": "low", "color": "🟢", "name_ro": "Scăzut", "action": "Acceptabil"},
            "5-8": {"level": "medium", "color": "🟡", "name_ro": "Mediu", "action": "Necesită măsuri suplimentare"},
            "9-12": {"level": "high", "color": "🟠", "name_ro": "Ridicat", "action": "Necesită măsuri imediate"},
            "13-16": {"level": "critical", "color": "🔴", "name_ro": "Critic", "action": "INACCEPTABIL - Consultare ANSPDCP obligatorie"}
        }
    }

    # Măsuri tehnice și organizatorice Art. 32 GDPR
    SECURITY_MEASURES = {
        "technical": {
            "encryption": {
                "name_ro": "Criptare",
                "examples": ["AES-256", "TLS 1.3", "Criptare în repaus și în tranzit"],
                "gdpr_ref": "Art. 32(1)(a) - pseudonimizare și criptare"
            },
            "pseudonymization": {
                "name_ro": "Pseudonimizare",
                "examples": ["Tokenizare", "Hash-ing", "Separare identificatori"],
                "gdpr_ref": "Art. 32(1)(a)"
            },
            "access_control": {
                "name_ro": "Control acces",
                "examples": ["RBAC", "2FA/MFA", "Autentificare puternică", "Least privilege"],
                "gdpr_ref": "Art. 32(1)(b)"
            },
            "backup": {
                "name_ro": "Backup și recuperare",
                "examples": ["Backup regulat", "Test restaurare", "Backup off-site"],
                "gdpr_ref": "Art. 32(1)(c) - capacitate de a restabili"
            },
            "monitoring": {
                "name_ro": "Monitorizare și logging",
                "examples": ["SIEM", "Audit logs", "Detectare intruziuni"],
                "gdpr_ref": "Art. 32(1)(d) - testare și evaluare"
            }
        },
        "organizational": {
            "policies": {
                "name_ro": "Politici și proceduri",
                "examples": ["Politică confidențialitate", "Proceduri acces", "Clean desk policy"],
                "gdpr_ref": "Art. 24, Art. 32"
            },
            "training": {
                "name_ro": "Instruire personal",
                "examples": ["Training GDPR anual", "Awareness securitate", "Phishing simulation"],
                "gdpr_ref": "Art. 32(4)"
            },
            "incident_response": {
                "name_ro": "Gestionare incidente",
                "examples": ["Procedură breach notification", "Plan răspuns incidente", "72h reporting"],
                "gdpr_ref": "Art. 33, Art. 34"
            },
            "dpo": {
                "name_ro": "DPO și guvernanță",
                "examples": ["DPO desemnat", "Privacy team", "RACI matrix"],
                "gdpr_ref": "Art. 37-39"
            }
        }
    }

    # Drepturi persoane vizate Art. 12-23 GDPR
    DATA_SUBJECT_RIGHTS = {
        "art13_14": {
            "name_ro": "Dreptul la informare (transparență)",
            "articles": "Art. 13-14",
            "description": "Obligația de a informa persoanele vizate despre prelucrare",
            "requirements": ["Identitate operator", "Date contact DPO", "Scopuri", "Temei", "Destinatari", "Durata", "Drepturi"]
        },
        "art15": {
            "name_ro": "Dreptul de acces",
            "articles": "Art. 15",
            "description": "Dreptul de a obține confirmare și copie a datelor",
            "deadline": "1 lună (extins cu 2 luni dacă complex)",
            "format": "Electronic dacă solicitat electronic"
        },
        "art16": {
            "name_ro": "Dreptul la rectificare",
            "articles": "Art. 16",
            "description": "Corectarea datelor inexacte",
            "deadline": "1 lună"
        },
        "art17": {
            "name_ro": "Dreptul la ștergere (right to be forgotten)",
            "articles": "Art. 17",
            "description": "Ștergerea datelor în anumite condiții",
            "exceptions": ["Libertate exprimare", "Obligație legală", "Interes public", "Apărare în justiție"],
            "deadline": "1 lună"
        },
        "art18": {
            "name_ro": "Dreptul la restricționare",
            "articles": "Art. 18",
            "description": "Limitarea prelucrării în anumite cazuri",
            "deadline": "1 lună"
        },
        "art20": {
            "name_ro": "Dreptul la portabilitate",
            "articles": "Art. 20",
            "description": "Primire date în format structurat, utilizat frecvent, lizibil automat",
            "applies_to": ["Consimțământ sau contract", "Prelucrare automată"],
            "format": "CSV, JSON, XML",
            "deadline": "1 lună"
        },
        "art21": {
            "name_ro": "Dreptul la opoziție",
            "articles": "Art. 21",
            "description": "Opoziție la prelucrare pe bază interes legitim sau interes public",
            "applies_to": ["Art. 6(1)(e), (f)", "Marketing direct"],
            "deadline": "Fără întârziere"
        },
        "art22": {
            "name_ro": "Decizie automată și creare de profiluri",
            "articles": "Art. 22",
            "description": "Dreptul de a nu face obiectul unei decizii bazate exclusiv pe prelucrare automată",
            "exceptions": ["Necesar pentru contract", "Autorizat prin drept UE/național", "Consimțământ explicit"],
            "safeguards": ["Intervenție umană", "Exprimare punct vedere", "Contestare decizie"]
        }
    }

    # WP29 Guidelines relevante pentru DPIA
    WP29_GUIDELINES = {
        "wp248": {
            "title": "Guidelines on Data Protection Impact Assessment (DPIA) - WP248rev.01",
            "date": "2017-10-04",
            "url": "https://ec.europa.eu/newsroom/article29/items/611236",
            "key_points": [
                "Criteriile pentru DPIA obligatoriu",
                "Metodologia evaluare risc",
                "Consultare DPO și persoane vizate",
                "Consultare prealabilă autoritate"
            ]
        },
        "wp243": {
            "title": "Guidelines on Automated individual decision-making and Profiling - WP251rev.01",
            "date": "2018-02-06",
            "key_points": ["Profilare", "Decizii automate", "Art. 22"]
        }
    }

    # EDPB Guidelines recente
    EDPB_GUIDELINES = {
        "edpb_2024_01": {
            "title": "Guidelines 1/2024 on Legitimate Interest",
            "date": "2024",
            "url": "https://www.edpb.europa.eu/",
            "key_points": ["LIA methodology", "Balancing test", "Examples"]
        }
    }

    # Jurisprudență CJUE relevantă
    CJEU_CASE_LAW = {
        "schrems_ii": {
            "case_number": "C-311/18",
            "name": "Schrems II",
            "date": "2020-07-16",
            "relevance": "Transferuri internaționale, invalidare Privacy Shield",
            "key_holdings": ["SCCs trebuie evaluate case-by-case", "Măsuri suplimentare necesare"]
        },
        "c_203_22": {
            "case_number": "C-203/22",
            "date": "2025-02-27",
            "relevance": "Transparență algoritmi vs secrete comerciale, credit scoring",
            "key_holdings": ["Balansare între Art. 15 și protecție secrete comerciale"]
        }
    }

    @classmethod
    def get_risk_level(cls, severity: int, probability: int) -> Dict:
        """Calculează nivelul de risc pe baza severității și probabilității"""
        score = severity * probability

        if 1 <= score <= 4:
            return cls.RISK_MATRIX["risk_levels"]["1-4"]
        elif 5 <= score <= 8:
            return cls.RISK_MATRIX["risk_levels"]["5-8"]
        elif 9 <= score <= 12:
            return cls.RISK_MATRIX["risk_levels"]["9-12"]
        else:  # 13-16
            return cls.RISK_MATRIX["risk_levels"]["13-16"]

    @classmethod
    def check_dpia_necessity(cls, processing_characteristics: Dict) -> Dict:
        """
        Verifică dacă DPIA este necesară conform Art. 35(3) și lista ANSPDCP

        Args:
            processing_characteristics: Dict cu caracteristici prelucrare

        Returns:
            Dict cu rezultat analiză necesitate DPIA
        """
        triggers = []

        # Verifică criterii Art. 35(3)
        if processing_characteristics.get("systematic_evaluation"):
            triggers.append({
                "source": "Art. 35(3)(a) GDPR",
                "criterion": cls.ART_35_CRITERIA["systematic_extensive_evaluation"]["name"]
            })

        if processing_characteristics.get("special_categories_large_scale"):
            triggers.append({
                "source": "Art. 35(3)(b) GDPR",
                "criterion": cls.ART_35_CRITERIA["large_scale_special_categories"]["name"]
            })

        if processing_characteristics.get("systematic_monitoring"):
            triggers.append({
                "source": "Art. 35(3)(c) GDPR",
                "criterion": cls.ART_35_CRITERIA["systematic_monitoring"]["name"]
            })

        # Verifică lista ANSPDCP
        if processing_characteristics.get("new_technologies"):
            triggers.append({
                "source": "Lista ANSPDCP (Decizia 174/2018) - Criteriu 4",
                "criterion": "Prelucrări care implică utilizarea noilor tehnologii"
            })

        if processing_characteristics.get("vulnerable_persons"):
            triggers.append({
                "source": "Lista ANSPDCP - Criteriu 9",
                "criterion": "Date persoane vulnerabile"
            })

        return {
            "dpia_required": len(triggers) > 0,
            "triggers": triggers,
            "recommendation": "DPIA OBLIGATORIE" if len(triggers) > 0 else "DPIA nu este obligatorie, dar poate fi recomandată"
        }

    @classmethod
    def get_legal_basis_requirements(cls, basis: str) -> Dict:
        """Returnează cerințele pentru un temei juridic specific"""
        return cls.LEGAL_BASIS_ART6.get(basis, {})

    @classmethod
    def get_security_measures_template(cls) -> Dict:
        """Returnează template cu măsuri de securitate recomandate"""
        return cls.SECURITY_MEASURES
