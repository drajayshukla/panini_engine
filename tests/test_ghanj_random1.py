"""
FILE: tests/test_ghanj_random.py
TOPIC: कृत्-प्रक्रिया (Kṛt Derivations) - घञ् प्रत्ययः
SCENARIO: Randomly tests 5 roots to verify Vriddhi (7.2.116) and Kutva (7.3.52).
"""

import pytest
import random
from core.phonology import ad, sanskrit_varna_samyoga
from logic.it_engine import ItEngine
from logic.vidhi_engine import VidhiEngine
from core.upadesha_registry import UpadeshaType


def derive_ghanj_form(dhatu_text):
    """
    Helper function to derive Root + Ghañ.
    Pipeline:
    1. Clean Suffix (Ghañ -> a)
    2. Clean Root (Vichhed)
    3. Apply Vriddhi (7.2.116)
    4. Apply Kutva (7.3.52) [Necessary for Pac -> Paka, etc.]
    5. Synthesis
    """
    # --- 1. PREPARE SUFFIX (घञ् -> अ) ---
    suffix_varnas = ad("घञ्")
    clean_suffix, _ = ItEngine.run_it_prakaran(suffix_varnas, UpadeshaType.PRATYAYA)

    # --- 2. PREPARE ROOT ---
    anga_varnas = ad(dhatu_text)

    # --- 3. APPLY VRIDDHI (7.2.116) ---
    # अत उपधायाः (Penultimate 'a' -> 'ā')
    anga_varnas, rule_vriddhi = VidhiEngine.apply_ata_upadhayah_7_2_116(anga_varnas)

    # --- 4. APPLY KUTVA (7.3.52) ---
    # चजोः कु घिण्ण्यतोः (Palatal -> Velar because suffix was Ghit)
    # This transforms 'c'->'k' (Pāc -> Pāk) and 'j'->'g' (Yāj -> Yāg)
    anga_varnas, rule_kutva = VidhiEngine.apply_chajo_ku_7_3_52(anga_varnas)

    # --- 5. SYNTHESIS ---
    final_varnas = anga_varnas + clean_suffix
    return sanskrit_varna_samyoga(final_varnas)


def test_random_ghanj_examples():
    """
    Randomly selects 5 roots from a database and verifies their Ghañ derivation.
    """
    # Database of Roots (Halanta) -> Expected Output (Subanta Stem)
    # Includes roots requiring only Vriddhi (Vad->Vāda) and Vriddhi+Kutva (Pac->Pāka)
    root_db = {
        "वद्": "वाद",  # Vad -> Vāda (Dispute/Theory)
        "चर्": "चार",  # Char -> Chāra (Spy/Movement)
        "ज्वल्": "ज्वाल",  # Jval -> Jvāla (Flame)
        "पच्": "पाक",  # Pac -> Pāka (Cooking) [Requires 7.3.52]
        "त्यज्": "त्याग",  # Tyaj -> Tyāga (Renunciation) [Requires 7.3.52]
        "यज्": "याग",  # Yaj -> Yāga (Sacrifice) [Requires 7.3.52]
        "भज्": "भाग",  # Bhaj -> Bhāga (Portion) [Requires 7.3.52]
        "पठ्": "पाठ",  # Paṭh -> Pāṭha (Reading)
        "तप्": "ताप"  # Tap -> Tāpa (Heat)
    }

    # Select 5 unique random roots
    selected_roots = random.sample(list(root_db.keys()), 5)

    print(f"\n🎲 Selected Random Roots: {selected_roots}")

    for root in selected_roots:
        expected = root_db[root]
        print(f"\n➡️ Testing: {root} + घञ्")

        actual = derive_ghanj_form(root)

        # assertions
        assert actual == expected, f"Failed on {root}: Expected '{expected}', Got '{actual}'"
        print(f"   ✅ Success: {actual}")


if __name__ == "__main__":
    test_random_ghanj_examples()