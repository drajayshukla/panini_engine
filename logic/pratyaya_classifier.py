"""
FILE: logic/pratyaya_classifier.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Pratyaya-Adhikara (3.1.1)
LOGIC: Maps specific suffix strings to one of the 7 Paninian categories.
"""

from logic.pratyaya_types import PratyayaCategory


class PratyayaClassifier:
    # --- STATIC DATASETS (Based on the Sutra Ranges provided) ---

    # 3.4.78 (18 Tiṅ Suffixes)
    _TING_SET = {
        "तिप्", "तस्", "झि", "सिप्", "थस्", "थ", "मिप्", "वस्", "मस्",
        "त", "आताम्", "झ", "थास्", "आथाम्", "ध्वम्", "इड्", "वहि", "महिङ्"
    }

    # 4.1.2 (21 Sup Suffixes)
    _SUP_SET = {
        "सुँ", "औ", "जस्",
        "अम्", "औट्", "शस्",
        "टा", "भ्याम्", "भिस्",
        "ङे", "भ्याम्", "भ्यस्",
        "ङसिँ", "भ्याम्", "भ्यस्",
        "ङस्", "ओस्", "आम्",
        "ङि", "ओस्", "सुप्"
    }

    # 3.1.33 - 3.1.86 (Common Vikaranas)
    _VIKARANA_SET = {
        "शप्", "श्यन्", "श्नु", "श", "श्नम्", "उ", "श्ना", "यक्", "चिण्",
        "स्य", "तासि", "सिच्", "चङ्", "अङ्"
    }

    # 3.1.5 - 3.1.31 (Common Sanadi)
    _SANADI_SET = {
        "सन्", "क्यच्", "काम्यच्", "क्यङ्", "क्यष्", "क्विप्", "णिच्", "यङ्"
    }

    # 4.1.4 - 4.1.81 (Common Stri Pratyayas)
    _STRI_SET = {
        "टाप्", "डाप्", "चाप्", "ङीप्", "ङीष्", "ङीन्", "ऊङ्", "ति"
    }

    # Common Krt (Primary) vs Taddhita (Secondary)
    # Note: In a full engine, this requires context (Dhatu vs Pratipadika).
    # Here we define common unambiguous ones.
    _COMMON_KRT = {"घञ्", "ण्वुल्", "तृच्", "अण्", "क्त", "क्तवतु", "शतृ", "शानच्", "तुमुन्", "क्त्वा", "ल्युट्"}
    _COMMON_TADDHITA = {"अण्", "ढक्", "ख", "यत्", "छ", "मयट्", "मात्रच्", "तरप्", "तमप्", "इष्ठन्", "इयसुन्"}

    @classmethod
    def classify(cls, pratyaya_text):
        """
        Determines the specific type of Pratyaya based on 3.1.1 classification.
        Returns: (PratyayaCategory, Sutra_Reference_Hint)
        """
        p = pratyaya_text.strip()

        # 1. Check Finite Sets (Closed Lists)
        if p in cls._SUP_SET:
            return PratyayaCategory.SUP, "४.१.२ स्वौजस्..."

        if p in cls._TING_SET:
            return PratyayaCategory.TING, "३.४.७८ तिप्तस्..."

        if p in cls._VIKARANA_SET:
            return PratyayaCategory.VIKARANA, "३.१.३३ - ३.१.८६"

        if p in cls._SANADI_SET:
            return PratyayaCategory.SANADI, "३.१.५ - ३.१.३१"

        if p in cls._STRI_SET:
            return PratyayaCategory.STRI, "४.१.४ - ४.१.८१"

        # 2. Check Infinite/Open Sets (Krt vs Taddhita)
        if p in cls._COMMON_KRT:
            return PratyayaCategory.KRT, "३.१.९१ धातोः (कृत्)"

        if p in cls._COMMON_TADDHITA:
            return PratyayaCategory.TADDHITA, "४.१.७६ तद्धिताः"

        # Default fallback (Ambiguous 'aN', etc. usually default to Krt in Dhatu context)
        # For safety, we return Generic Pratyaya if unknown
        return "Generic Pratyaya", "३.१.१ प्रत्ययः"