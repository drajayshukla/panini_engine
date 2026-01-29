"""
FILE: core/upadesha_registry.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Upadeśa (Instructional Source Registry)
UPDATED: Defines PRATIPADIKA/VIBHAKTI constants and integrates Varna inheritance.
"""

import json
import os
from core.phonology import Varna

class UpadeshaType:
    """
    Registry of Source Types (Yoni) in Paninian Grammar.
    Acts as the central authority for identifying input types.
    """
    # --- CONSTANTS (Crucial for avoiding AttributeError) ---
    DHATU = "dhatu"             # Root (e.g. Bhaj, Pac)
    PRATYAYA = "pratyaya"       # Suffix (e.g. Ghanj, Shap)
    VIBHAKTI = "vibhakti"       # Case Ending (Subset of Pratyaya: Su, Au, Jas)
    AGAMA = "agama"             # Augment (e.g. Nut, It)
    ADESHA = "adesha"           # Substitute
    PRATIPADIKA = "pratipadika" # Nominal Stem (e.g. Rama, Geeta)
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
                return json.load(f)
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

        # 1. Check Dhatupatha (Roots)
        dhatus = cls._load_data("dhatupatha.json")
        # Handle dict or list structure of dhatupatha
        dhatu_list = dhatus.get('dhatus', []) if isinstance(dhatus, dict) else dhatus
        if any(d.get("dhatu") == text or d.get("mula_dhatu") == text for d in dhatu_list):
            return cls.DHATU, False, "Dhatupatha"

        # 2. Check Pratyayas (Suffixes)
        # Fallback list for common Krt/Taddhita/Sup/Ting if file is missing/incomplete
        fallback_pratyayas = {
            "घञ्", "अण्", "यत्", "ण्वुल्", "तृच्", "शप्", "स्य", "सिच्",
            "सुँ", "औ", "जस्", "अम्", "औट्", "शस्", "टा", "भ्याम्", "भिस्",
            "ङे", "भ्यस्", "ङसिँ", "ङस्", "ओस्", "आम्", "ङि", "सुप्",
            "तिप्", "तस्", "झि", "सिप्", "थस्", "थ", "मिप्", "वस्", "मस्"
        }

        pratyayas = cls._load_data("pratyaya_defs.json")
        is_pratyaya_db = False
        if pratyayas:
             is_pratyaya_db = any(p.get("pratyaya") == text for p in pratyayas)

        if text in fallback_pratyayas or is_pratyaya_db:
            # Check if Taddhita (Secondary Suffix) - simplified check
            # Real logic would check 'taddhita_master_data.json'
            is_taddhita = False
            return cls.PRATYAYA, is_taddhita, "Pratyaya Kosha"

        # 3. Check Shabda (Pratipadika)
        shabdas = cls._load_data("shabdroop.json")
        if any(s.get("word") == text for s in shabdas):
            return cls.PRATIPADIKA, False, "Shabda Kosha"

        # Default: Treat unknown as Pratipadika (User input base)
        return cls.PRATIPADIKA, False, "User Input"

class Upadesha(Varna):
    """
    A wrapper object for a Varna or String that tracks its Upadesha source.
    Useful for Atidesha (Extension) rules.
    Inherits from Varna so it has .is_vowel, .is_consonant etc.
    """
    def __init__(self, char, source_rule=None):
        # Initialize biological/phonetic layer
        super().__init__(char)

        # Add legal layer
        self.source_rule = source_rule
        self.sanjnas = set()
        # Trace is inherited from Varna, but we can append to it
        self.trace.append(f"Origin: {source_rule}")

    def __repr__(self):
        return f"{self.char}"