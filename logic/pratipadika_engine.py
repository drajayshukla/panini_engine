from core.upadesha_registry import UpadeshaType

class PratipadikaEngine:
    """
    Sutras: 1.2.45 (Arthavadadhaturapratyayah) & 1.2.46 (Krittadhitasamasashcha).
    Automatically verifies if a word is a Pratipadika based on Inclusion/Exclusion logic.
    """

    @staticmethod
    def identify_base(text):
        """
        Verification Pipeline:
        1. Direct Inclusion: Search shabdroop.json (Pre-recorded Nouns).
        2. Derivative Inclusion: Search for Taddhita markers via 1.2.46.
        3. Exclusion: Filter out Roots (Dhatu) and Suffixes (Pratyaya) via 1.2.45.
        4. Default: Declare as primary Pratipadika if meaningful and not found elsewhere.
        """
        if not text:
            return {"is_pratipadika": False, "reason": "रिक्त इनपुट (No input)."}

        # --- PHASE 1: DIRECT INCLUSION (shabdroop.json) ---
        shabda_data = UpadeshaType._load_data('shabdroop.json')
        if isinstance(shabda_data, list):
            match = next((item for item in shabda_data if item.get('word') == text), None)
            if match:
                return {
                    "is_pratipadika": True,
                    "text": text,
                    "sutra_applied": "Siddha-Shabda (सिद्ध-प्रातिपदिकम्)",
                    "description": f"'{text}' (अर्थ: {match.get('artha_hin') or match.get('artha')}) शब्दरूप डेटाबेस में पहले से उपलब्ध है।",
                    "link": "https://ashtadhyayi.com/sutraani/1/2/45",
                    "metadata": match
                }

        # --- PHASE 2: REGISTRY CHECK (Dhatu/Pratyaya/Taddhita) ---
        detected_type, is_taddhita = UpadeshaType.auto_detect(text)

        # 1.2.46 Inclusion (Derived Nouns)
        if is_taddhita:
            return {
                "is_pratipadika": True,
                "text": text,
                "sutra_applied": "१.२.४६ (कृत्तद्धितसमासाश्च)",
                "description": f"चूंकि '{text}' एक तद्धित प्रत्ययान्त रूप है, इसकी प्रातिपदिक संज्ञा होती है।",
                "link": "https://ashtadhyayi.com/sutraani/1/2/46"
            }

        # 1.2.45 Exclusion (Adhatur-Apratyayah)
        if detected_type is not None:
            return {
                "is_pratipadika": False,
                "detected_as": detected_type.value,
                "reason": f"यह शब्द डेटाबेस में '{detected_type.value}' के रूप में दर्ज है, अतः १.२.४५ से वर्जित है।",
                "sutra_applied": None
            }

        # --- PHASE 3: DEFAULT INCLUSION ---
        return {
            "is_pratipadika": True,
            "text": text,
            "sutra_applied": "१.२.४५ (अर्थवदधातुरप्रत्ययः प्रातिपदिकम्)",
            "description": f"'{text}' न धातु है न प्रत्यय, और अर्थवान है, अतः इसकी प्रातिपदिक संज्ञा होती है।",
            "link": "https://ashtadhyayi.com/sutraani/1/2/45"
        }

    @staticmethod
    def get_sup_vibhakti_map():
        """स्वौजसमौट्... (४.१.२) २१ प्रत्यय मानचित्र।"""
        return {
            "प्रथमा": {"एकवचन": "सुँ", "द्विवचन": "औ", "बहुवचन": "जस्"},
            "द्वितीया": {"एकवचन": "अम्", "द्विवचन": "औट्", "बहुवचन": "शस्"},
            "तृतीया": {"एकवचन": "टा", "द्विवचन": "भ्याम्", "बहुवचन": "भिस्"},
            "चतुर्थी": {"एकवचन": "ङे", "द्विवचन": "भ्याम्", "बहुवचन": "भ्यस्"},
            "पञ्चमी": {"एकवचन": "ङसिँ", "द्विवचन": "भ्याम्", "बहुवचन": "भ्यस्"},
            "षष्ठी": {"एकवचन": "ङस्", "द्विवचन": "ओस्", "बहुवचन": "आम्"},
            "सप्तमी": {"एकवचन": "ङि", "द्विवचन": "ओस्", "बहुवचन": "सुप्"}
        }