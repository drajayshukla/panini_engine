"""
FILE: core/pratyahara_engine.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Pratyāhāra (Algebraic Set Generation)
REFERENCE: १.१.७१ आदिरन्त्येन सहेता
"""

import json
import os
from core.phonology import ad

class PratyaharaEngine:
    """
    प्रत्याहार-निर्माता (The Algebraic Generator)
    Parses the Shiva Sutras to generate dynamic character sets.
    Includes Caching (Smṛti) for O(1) performance on repeated lookups.
    """

    def __init__(self, json_path="data/shiva_sutras.json"):
        self.sutras = self._load_sutras(json_path)
        self._cache = {}  # Internal memory to store generated Pratyaharas

    def _load_sutras(self, path):
        """
        Loads and surgically normalizes Shiva Sutras to match the 'ad' physiological standard.
        """
        if not os.path.exists(path):
            # Fallback for empty init or missing file
            return []

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f).get("shiva_sutras", [])

            # Normalization: Ensure DB matches the engine's 'halant' standards
            for sutra in data:
                # 1. Clean Varnas: Run them through 'ad' to ensure object parity
                clean_varnas = []
                for v in sutra['varnas']:
                    # ad returns a list of Varna objects, we extract .char
                    # e.g., 'क' -> 'क्' + 'अ' (if strict) or just 'क' depending on ad logic.
                    # For Shiva Sutras, we assume pure phonetic units.
                    parsed = ad(v)
                    clean_varnas.extend([p.char for p in parsed])
                sutra['varnas'] = clean_varnas

                # 2. Clean It-Marker: Ensure it has the Halant if strictly consonantal
                it_marker = sutra['it_varna']
                if not it_marker.endswith('्'):
                    it_marker += '्'
                sutra['it_varna'] = it_marker

            return data

    def get_varnas(self, name: str) -> list:
        """
        [SUTRA]: आदिरन्त्येन सहेता (१.१.७१)
        Decodes a Pratyahara name (e.g., 'अच्', 'झल्') into a list of characters.
        """
        # 1. Check Smṛti (Cache)
        if name in self._cache:
            return self._cache[name]

        # 2. Parse Input (e.g., "अच्" -> Adi "अ", It "च््")
        parsed = ad(name)
        if len(parsed) < 2:
            return []

        adi = parsed[0].char
        antya_it = parsed[-1].char

        # Ensure parity with normalized JSON It-markers
        if not antya_it.endswith('्'):
            antya_it += '्'

        pratyahara_list = []
        start_collecting = False

        # 3. Scan the Shiva Sutras
        for sutra in self.sutras:
            current_varnas = sutra["varnas"]
            current_it = sutra["it_varna"]

            # A. Adi Search (Finding the start)
            if not start_collecting and adi in current_varnas:
                start_idx = current_varnas.index(adi)
                # Collect from the start index onwards
                pratyahara_list.extend(current_varnas[start_idx:])
                start_collecting = True

                # Immediate check: If the start block's It matches the target
                if current_it == antya_it:
                    self._cache[name] = pratyahara_list
                    return pratyahara_list
                continue

            # B. Continuation (Collecting intermediate varnas)
            if start_collecting:
                pratyahara_list.extend(current_varnas)

                # C. Boundary Check (Stop at the It-Marker)
                if current_it == antya_it:
                    self._cache[name] = pratyahara_list
                    return pratyahara_list

        return []

    def is_in(self, char: str, pratyahara_name: str) -> bool:
        """
        [SUTRA]: अणुदित् सवर्णस्य चाप्रत्ययः (१.१.६९)
        Checks if 'char' belongs to 'pratyahara_name', considering Savarna (homogeneity).
        """
        # Get the strict Pratyahara set (e.g., 'अक्' -> अ, इ, उ, ऋ, ऌ)
        base_range = set(self.get_varnas(pratyahara_name))

        # Immediate Match
        if char in base_range:
            return True

        # Savarna Expansion Logic (PAS-5.0)
        # Maps surface forms (Long/Pluta) back to their Shiva Sutra roots (Hrasva).
        # This allows 'आ' to be recognized as part of 'अक्'.
        savarna_map = {
            # Ak (Vowels)
            'आ': 'अ', 'ा': 'अ', 'इ': 'इ', 'ई': 'इ', 'ी': 'इ',
            'उ': 'उ', 'ऊ': 'उ', 'ू': 'उ',
            'ऋ': 'ऋ', 'ॠ': 'ऋ', 'ृ': 'ऋ', 'ॄ': 'ऋ',
            'ऌ': 'ऌ', 'ॡ': 'ऌ', 'ॢ': 'ऌ',
            # Yan (Semivowels - Nasalized variants usually map to self)
            'यँ': 'य्', 'वँ': 'व्', 'लँ': 'ल्'
        }

        # Normalize the input char
        # Note: If input is 'ग्', we check 'ग्'. If 'गा', we check 'ग' + 'आ'.
        # This function expects atomic chars (output of ad).
        normalized_char = savarna_map.get(char, char)

        # Special Handling for Consonants (removing Halant for sloppy checks if needed)
        # But strictly, 'क' in Shiva Sutra is 'क' (pronounced) but technically 'क्'.
        # Our engine uses strict Halant parity.

        return normalized_char in base_range