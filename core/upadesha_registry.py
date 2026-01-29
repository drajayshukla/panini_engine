"""
FILE: core/upadesha_registry.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Upadeśa (Instructional Source Registry)
UPDATED: Integrated 3.1.1 Pratyaya Classification + Robust Type Checking.
"""

import json
import os
from core.phonology import Varna
from logic.pratyaya_classifier import PratyayaClassifier

class UpadeshaType:
    """
    Registry of Source Types (Yoni) in Paninian Grammar.
    Acts as the central authority for identifying input types.
    """
    # --- CONSTANTS ---
    DHATU = "dhatu"             # Root (e.g. Bhaj, Pac)
    PRATYAYA = "pratyaya"       # Suffix (e.g. Ghanj, Shap)
    VIBHAKTI = "vibhakti"       # Case Ending (Subset of Pratyaya: Su, Au, Jas)
    AGAMA = "agama"             # Augment
    ADESHA = "adesha"           # Substitute
    PRATIPADIKA = "pratipadika" # Nominal Stem
    UNADI = "unadi"             # Irregular affix
    NIPATA = "nipata"           # Particle

    @classmethod
    def _load_data(cls, filename):
        """Helper to load JSON data safely."""
        try:
            path = os.path.join("data", filename)
            if not os.path.exists(path):
                return []
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if data is not None else []
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return []

    @classmethod
    def auto_detect(cls, text):
        """
        Scans all databases to guess the type of the input string.
        Returns: (UpadeshaType, SubCategory, Origin_Sutra)
        """
        if not text:
            return cls.PRATIPADIKA, None, "Empty Input"

        # --- 1. DHATU CHECK (Robust) ---
        dhatus = cls._load_data("dhatupatha.json")

        # Ensure list structure
        dhatu_list = dhatus.get('dhatus', []) if isinstance(dhatus, dict) else dhatus
        if not isinstance(dhatu_list, list): dhatu_list = []

        # Robust Scan: Handles both Dicts and Strings
        for d in dhatu_list:
            if isinstance(d, dict):
                if d.get("dhatu") == text or d.get("mula_dhatu") == text:
                    return cls.DHATU, None, "Dhatupatha"
            elif isinstance(d, str):
                if d == text:
                    return cls.DHATU, None, "Dhatupatha (String)"

        # --- 2. PRATYAYA CHECK (Enhanced with 3.1.1 Logic) ---
        # Step A: Use the Classifier first for high-precision identification
        # This handles Sup, Ting, Vikarana, Sanadi, etc.
        category, sutra_hint = PratyayaClassifier.classify(text)

        if category != "Generic Pratyaya":
            # [CRITICAL]: Map 'sup' category to VIBHAKTI type for the engine
            if category == "sup":
                return cls.VIBHAKTI, "Sup", sutra_hint

            # All others (Ting, Krt, Taddhita) return as PRATYAYA with sub-cat
            return cls.PRATYAYA, category, sutra_hint

        # Step B: Fallback to JSON check (Pratyaya Kosha)
        # Only needed if PratyayaClassifier returned "Generic"
        pratyayas = cls._load_data("pratyaya_defs.json")
        is_pratyaya_db = False

        if pratyayas and isinstance(pratyayas, list):
            for p in pratyayas:
                if isinstance(p, dict) and p.get("pratyaya") == text:
                    is_pratyaya_db = True
                    break
                elif isinstance(p, str) and p == text:
                    is_pratyaya_db = True
                    break

        if is_pratyaya_db:
            return cls.PRATYAYA, "General", "Pratyaya Kosha"

        # --- 3. SHABDA CHECK (Robust) ---
        shabdas = cls._load_data("shabdroop.json")
        if isinstance(shabdas, list):
            for s in shabdas:
                if isinstance(s, dict) and s.get("word") == text:
                    return cls.PRATIPADIKA, None, "Shabda Kosha"
                elif isinstance(s, str) and s == text:
                    return cls.PRATIPADIKA, None, "Shabda List"

        # --- 4. DEFAULT ---
        # Treat unknown inputs as user-defined Pratipadikas
        return cls.PRATIPADIKA, None, "User Input"


class Upadesha(Varna):
    """
    [PAS-5.0] The Siddha Upadesha Object.
    Wraps the phoneme with its Legal Identity (Adhikara).
    Inherits from Varna to prevent 'AttributeError: is_vowel'.
    """
    def __init__(self, char, source_rule=None):
        super().__init__(char)
        self.source_rule = source_rule
        self.sanjnas = set()
        self.trace.append(f"Origin: {source_rule}")

    def __repr__(self):
        return f"{self.char}"