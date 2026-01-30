"""
FILE: logic/vidhi/engine_base.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Vidhi-Foundation (Base Utilities)
REFERENCE: General Computational Linguistics Helpers
"""
from core.phonology import Varna, sanskrit_varna_samyoga
from core.paribhasha_manager import ParibhashaManager


class VidhiEngineBase:
    """
    Base utilities shared across all Vidhi sub-modules.
    Provides common logic for stem analysis and transformation.
    """

    @staticmethod
    def get_stem_string(varnas):
        """Helper to get joined string for identity checks."""
        return sanskrit_varna_samyoga(varnas)

    @staticmethod
    def find_penultimate_vowel(varnas):
        """Helper to locate the Upadhā vowel for Guna/Vriddhi."""
        if len(varnas) < 2:
            return None, -1
        # Typically penultimate is at index -2 for consonant-ending stems
        idx = len(varnas) - 2
        if idx >= 0 and varnas[idx].is_vowel:
            return varnas[idx], idx
        return None, -1

    @staticmethod
    def apply_substitution(varna_list, index, new_chars, rule_code):
        """
        Generic helper to replace a varna with one or more new varnas.
        Handles the 'trace' and 'sanjna' stamping automatically.
        """
        if index < 0 or index >= len(varna_list):
            return varna_list

        old_char = varna_list[index].char
        varna_list.pop(index)

        new_varnas = []
        for c in new_chars:
            v = Varna(c)
            v.trace.append(f"{rule_code} ({old_char}->{c})")
            new_varnas.append(v)

        # Re-insert at the same position
        for i, v in enumerate(new_varnas):
            varna_list.insert(index + i, v)

        return varna_list