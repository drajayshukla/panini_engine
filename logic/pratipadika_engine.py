#logic/pratipadika_engine.py
from core.upadesha_registry import UpadeshaType

class PratipadikaEngine:
    """
    Sutras: 1.2.45 (Arthavadadhaturapratyayah) & 1.2.46 (Krittadhitasamasashcha).
    उद्देश्य: सुबन्त-प्रक्रिया के लिए आधार की स्वचालित पहचान एवं सत्यापन।
    """

    @staticmethod
    def identify_base(text):
        """
        Verification Pipeline:
        1. Direct Inclusion: Search shabdroop.json (Pre-recorded Nouns).
        2. Derivative Inclusion: Search for Taddhita markers via 1.2.46.
        3. Exclusion: Filter out Roots (Dhatu) and Suffixes (Pratyaya) via 1.2.45.
        4. Default: Declare as primary Pratipadika (1.2.45).
        """
        if not text:
            return {"is_pratipadika": False, "reason": "रिक्त इनपुट (No input)."}

        # --- PHASE 1: DIRECT INCLUSION (shabdroop.json) ---
        # Look for established nouns already in the database
        shabda_data = UpadeshaType._load_data('shabdroop.json')
        if isinstance(shabda_data, list):
            match = next((item for item in shabda_data if item.get('word') == text), None)
            if match:
                return {
                    "is_pratipadika": True,
                    "text": text,
                    "sutra_applied": "Siddha-Shabda (सिद्ध-प्रातिपदिकम्)",
                    "description": f"Found in Master Noun List. Artha: {match.get('artha_hin') or match.get('artha')}",
                    "link": "https://ashtadhyayi.com/sutraani/1/2/45",
                    "metadata": match
                }

        # --- PHASE 2: REGISTRY CHECK (Dhatu/Pratyaya/Taddhita) ---
        # Automatic detection using the centralized registry scanner
        detected_type, is_taddhita = UpadeshaType.auto_detect(text)

        # 1.2.46 Inclusion (Derived Nouns/Taddhita)
        if is_taddhita:
            return {
                "is_pratipadika": True,
                "text": text,
                "sutra_applied": "१.२.४६ (कृत्तद्धितसमासाश्च)",
                "description": f"चूंकि '{text}' एक तद्धित प्रत्ययान्त रूप है, इसकी प्रातिपदिक संज्ञा होती है।",
                "link": "https://ashtadhyayi.com/sutraani/1/2/46"
            }

        # 1.2.45 Exclusion (Adhatur-Apratyayah)
        # If registered as Dhatu or Vibhakti, it cannot be a primary Pratipadika
        if detected_type is not None:
            return {
                "is_pratipadika": False,
                "detected_as": detected_type.value,
                "reason": f"Conflict: यह शब्द डेटाबेस में '{detected_type.value}' के रूप में दर्ज है, अतः १.२.४५ से वर्जित है।",
                "sutra_applied": None
            }

        # --- PHASE 3: DEFAULT INCLUSION (1.2.45) ---
        # Meaningful base not found in existing Dhatu/Pratyaya databases
        return {
            "is_pratipadika": True,
            "text": text,
            "sutra_applied": "१.२.४५ (अर्थवदधातुरप्रत्ययः प्रातिपदिकम्)",
            "description": "Independent meaningful base not found in Dhatu/Pratyaya databases.",
            "link": "https://ashtadhyayi.com/sutraani/1/2/45"
        }

    @staticmethod
    def get_sup_vibhakti_map():
        """
        सूत्र: स्वौजसमौट्... (४.१.२)
        २१ सुप्-प्रत्ययों का पदानुक्रमित मानचित्र।
        """
        return {
            "प्रथमा": {"एकवचन": "सुँ", "द्विवचन": "औ", "बहुवचन": "जस्"},
            "द्वितीया": {"एकवचन": "अम्", "द्विवचन": "औट्", "बहुवचन": "शस्"},
            "तृतीया": {"एकवचन": "टा", "द्विवचन": "भ्याम्", "बहुवचन": "भिस्"},
            "चतुर्थी": {"एकवचन": "ङे", "द्विवचन": "भ्याम्", "बहुवचन": "भ्यस्"},
            "पञ्चमी": {"एकवचन": "ङसिँ", "द्विवचन": "भ्याम्", "बहुवचन": "भ्यस्"},
            "षष्ठी": {"एकवचन": "ङस्", "द्विवचन": "ओस्", "बहुवचन": "आम्"},
            "सप्तमी": {"एकवचन": "ङि", "द्विवचन": "ओस्", "बहुवचन": "सुप्"}
        }