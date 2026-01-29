"""
FILE: logic/pratipadika_engine.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Prātipadika-Saṃjñā (Noun Stem Definition)
REFERENCE: १.२.४५ अर्थवदधातुरप्रत्ययः प्रातिपदिकम् & १.२.४६ कृत्तद्धितसमासाश्च
"""

from core.upadesha_registry import UpadeshaType

class PratipadikaEngine:
    """
    प्रातिपदिक-सञ्चालक: (The Noun Stem Validator)
    Certifies a base word as eligible for Su-au-jas (4.1.2) application.
    """

    @staticmethod
    def identify_base(text):
        """
        [VERIFICATION PIPELINE]:
        1. Registry Scan: Checks if it's a Dhatu/Pratyaya (Conflict Check).
        2. 1.2.46 Check: Is it a Taddhita (Derived Noun)?
        3. 1.2.45 Check: Is it a valid dictionary word (Arthavat)?
        """
        if not text:
            return {"is_pratipadika": False, "reason": "रिक्त इनपुट (No input)."}

        # --- PHASE 1: REGISTRY SCAN (Auto-Detect) ---
        # Unpacking 3 values as per Core PAS-5.0 update
        detected_type, is_taddhita, origin = UpadeshaType.auto_detect(text)

        # A. EXCLUSION CHECK (1.2.45: Adhātuḥ Apratyayaḥ)
        # If it is a Dhatu, it is NOT a Pratipadika.
        if detected_type == UpadeshaType.DHATU:
            return {
                "is_pratipadika": False,
                "detected_as": "Dhatu",
                "reason": f"Conflict (1.2.45): '{text}' is a Root ({origin}), hence Adhātu rule blocks it.",
                "sutra_applied": None
            }

        # If it is a bare Pratyaya (and NOT a Taddhita derivative), it is excluded.
        if detected_type == UpadeshaType.PRATYAYA and not is_taddhita:
            return {
                "is_pratipadika": False,
                "detected_as": "Pratyaya",
                "reason": f"Conflict (1.2.45): '{text}' is a Suffix ({origin}), hence Apratyaya rule blocks it.",
                "sutra_applied": None
            }

        # B. INCLUSION CHECK (1.2.46: Kṛt-Taddhita-Samāsāśca)
        # If it is a Taddhita (Secondary Derivative), it IS a Pratipadika.
        if is_taddhita:
            return {
                "is_pratipadika": True,
                "text": text,
                "type": "Taddhita",
                "sutra_applied": "१.२.४६ कृत्तद्धितसमासाश्च",
                "description": f"Derived Noun (Taddhita) validated via {origin}.",
                "link": "https://ashtadhyayi.com/sutraani/1/2/46"
            }

        # --- PHASE 2: DICTIONARY CHECK (1.2.45: Arthavat) ---
        # Look for established nouns in shabdroop.json
        try:
            shabda_data = UpadeshaType._load_data('shabdroop.json')
            if shabda_data and isinstance(shabda_data, list):
                match = next((item for item in shabda_data if item.get('word') == text), None)
                if match:
                    return {
                        "is_pratipadika": True,
                        "text": text,
                        "type": "Siddha",
                        "sutra_applied": "१.२.४५ अर्थवदधातुरप्रत्ययः प्रातिपदिकम्",
                        "description": f"Dictionary Match: {match.get('artha_hin') or match.get('artha')}",
                        "link": "https://ashtadhyayi.com/sutraani/1/2/45",
                        "metadata": match
                    }
        except Exception:
            # Fail gracefully if JSON missing, proceed to default Arthavat assumption
            pass

        # --- PHASE 3: DEFAULT INCLUSION (1.2.45) ---
        # If it passed the Exclusion check (not Dhatu/Pratyaya) and has no specific match,
        # we assume it is a valid Arthavat word (User input confidence).
        return {
            "is_pratipadika": True,
            "text": text,
            "type": "Arthavat",
            "sutra_applied": "१.२.४५ अर्थवदधातुरप्रत्ययः प्रातिपदिकम्",
            "description": "User-defined meaningful base (Arthavat).",
            "link": "https://ashtadhyayi.com/sutraani/1/2/45"
        }

    @staticmethod
    def get_sup_vibhakti_map():
        """
        [SUTRA]: स्वौजसमौट्छष्टा... (४.१.२)
        Returns the 21 Sup-Pratyayas for Subanta derivation.
        """
        return {
            "1. प्रथमा":  {"एक": "सुँ",  "द्वि": "औ",     "बहु": "जस्"},
            "2. द्वितीया": {"एक": "अम्",  "द्वि": "औट्",    "बहु": "शस्"},
            "3. तृतीया":  {"एक": "टा",   "द्वि": "भ्याम्", "बहु": "भिस्"},
            "4. चतुर्थी":  {"एक": "ङे",   "द्वि": "भ्याम्", "बहु": "भ्यस्"},
            "5. पञ्चमी":  {"एक": "ङसिँ", "द्वि": "भ्याम्", "बहु": "भ्यस्"},
            "6. षष्ठी":   {"एक": "ङस्",  "द्वि": "ओस्",    "बहु": "आम्"},
            "7. सप्तमी":  {"एक": "ङि",   "द्वि": "ओस्",    "बहु": "सुप्"},
            "8. सम्बोधन": {"एक": "सुँ",   "द्वि": "औ",     "बहु": "जस्"}
        }