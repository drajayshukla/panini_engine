"""
FILE: core/upadesha_registry.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Upadeśa (Instructional Source Registry)
UPDATED: Added robust type-checking to prevent AttributeErrors on dirty JSON data.
"""

import json
import os
from core.phonology import Varna

class UpadeshaType:
    """
    Registry of Source Types (Yoni) in Paninian Grammar.
    Acts as the central authority for identifying input types.
    """
    # --- CONSTANTS ---
    DHATU = "dhatu"             # Root (e.g. Bhaj, Pac)
    PRATYAYA = "pratyaya"       # Suffix (e.g. Ghanj, Shap)
    VIBHAKTI = "vibhakti"       # Case Ending
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
        Returns: (UpadeshaType, Is_Taddhita, Origin_Sutra/Source)
        """
        if not text:
            return cls.PRATIPADIKA, False, "Empty Input"

        # --- 1. CHECK DHATUPATHA (Roots) ---
        dhatus = cls._load_data("dhatupatha.json")

        # Normalization: Ensure we have a list to iterate over
        dhatu_list = []
        if isinstance(dhatus, dict):
            dhatu_list = dhatus.get('dhatus', [])
        elif isinstance(dhatus, list):
            dhatu_list = dhatus

        # Robust Scan: Handles both Dicts and Strings
        for d in dhatu_list:
            # Case A: Dictionary Object (Standard)
            if isinstance(d, dict):
                if d.get("dhatu") == text or d.get("mula_dhatu") == text:
                    return cls.DHATU, False, "Dhatupatha"
            # Case B: Simple String (Legacy/Simple JSON)
            elif isinstance(d, str):
                if d == text:
                    return cls.DHATU, False, "Dhatupatha (String)"

        # --- 2. CHECK PRATYAYAS (Suffixes) ---
        fallback_pratyayas = {
            "घञ्", "अण्", "यत्", "ण्वुल्", "तृच्", "शप्", "स्य", "सिच्",
            "सुँ", "औ", "जस्", "अम्", "औट्", "शस्", "टा", "भ्याम्", "भिस्",
            "ङे", "भ्यस्", "ङसिँ", "ङस्", "ओस्", "आम्", "ङि", "सुप्",
            "तिप्", "तस्", "झि", "सिप्", "थस्", "थ", "मिप्", "वस्", "मस्"
        }

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

        if text in fallback_pratyayas or is_pratyaya_db:
            return cls.PRATYAYA, False, "Pratyaya Kosha"

        # --- 3. CHECK SHABDA (Pratipadika) ---
        shabdas = cls._load_data("shabdroop.json")
        if isinstance(shabdas, list):
            for s in shabdas:
                if isinstance(s, dict) and s.get("word") == text:
                    return cls.PRATIPADIKA, False, "Shabda Kosha"
                elif isinstance(s, str) and s == text:
                    return cls.PRATIPADIKA, False, "Shabda List"

        # Default: Treat unknown as Pratipadika
        return cls.PRATIPADIKA, False, "User Input"

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