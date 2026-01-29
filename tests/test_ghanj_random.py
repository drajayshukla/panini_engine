# tests/test_ghanj_random.py
import pytest
import random
from core.phonology import ad, sanskrit_varna_samyoga
from logic.it_engine import ItEngine
from logic.vidhi_engine import VidhiEngine
from core.upadesha_registry import UpadeshaType


def derive_ghanj_logic(dhatu_text):
    print(f"\n🎲 Deriving: {dhatu_text} + घञ्")

    # 1. PROCESS DHATU (Root)
    dhatu_varnas = ad(dhatu_text)

    # [LOGIC]: 1.3.2 now automatically removes "Vowel + Nasal Marker"
    # Example: 'Paca~' -> 'Pac' (Halanta)
    dhatu_clean, _ = ItEngine.run_it_prakaran(dhatu_varnas, UpadeshaType.DHATU)

    # 2. PROCESS PRATYAYA (Suffix)
    suffix_varnas = ad("घञ्")
    suffix_clean, suffix_trace = ItEngine.run_it_prakaran(suffix_varnas, UpadeshaType.PRATYAYA)

    # 3. TAG TRANSFER
    if suffix_clean:
        for v in suffix_clean:
            v.sanjnas.add("ghit")
            v.sanjnas.add("ñit")

            # 4. COMBINE (Anga + Suffix)
    combined = dhatu_clean + suffix_clean
    split_idx = len(dhatu_clean)

    # 5. APPLY VIDHI RULES

    # A. 7.2.116 Ata Upadhaya (Vriddhi)
    # Since 'Pac' is now Halanta, 'a' is correctly seen as Upadha.
    combined, s116 = VidhiEngine.apply_ata_upadhayah_7_2_116(combined, manual_range=(0, split_idx))

    # B. 7.3.52 Chajo Ku (Kutva)
    combined, s52 = VidhiEngine.apply_chajo_ku_7_3_52(combined, manual_range=(0, split_idx))

    final_form = sanskrit_varna_samyoga(combined)
    return final_form


def test_random_ghanj_derivations():
    """
    Randomly selects 3 roots and verifies derivation.
    """
    valid_roots = {
        "यजँ": "याग",
        "भजँ": "भाग",
        "त्यजँ": "त्याग",
        "पठँ": "पाठ",
        "तपँ": "ताप",
        "पचँ": "पाक",
        "वचँ": "वाक",
        "सचँ": "साक"
    }

    selected_roots = random.sample(list(valid_roots.keys()), 3)
    print(f"\n🔍 Testing {selected_roots}...")

    for root in selected_roots:
        expected = valid_roots[root]
        actual = derive_ghanj_logic(root)

        assert actual == expected, f"Failed on {root}: Expected {expected}, got {actual}"
        print(f"✅ Pass: {root} -> {actual}")


if __name__ == "__main__":
    test_random_ghanj_derivations()