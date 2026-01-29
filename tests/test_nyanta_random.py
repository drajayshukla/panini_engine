"""
FILE: tests/test_nyanta_random.py
TOPIC: णिजन्त-प्रक्रिया (Causative Derivations)
SCENARIO: Randomly tests 5 roots similar to 'Nī + Ṇic -> Nāyi'.
          Verifies Vriddhi (7.2.115) + Ayadi (6.1.78).
"""

import pytest
import random
from core.phonology import ad, sanskrit_varna_samyoga
from logic.it_engine import ItEngine
from logic.vidhi_engine import VidhiEngine
from core.upadesha_registry import UpadeshaType


# --- DERIVATION LOGIC ---
def derive_nyanta_form(dhatu_text):
    """
    Derives Root + Ṇic (Causative).
    Steps:
    1. Clean Suffix (Ṇic -> i)
    2. Apply Vriddhi (7.2.115): i/ī -> ai, u/ū -> au
    3. Apply Ayadi (6.1.78): ai -> āy, au -> āv
    4. Synthesis
    """
    # 1. Prepare Suffix
    suffix_varnas = ad("णिच्")
    clean_suffix, _ = ItEngine.run_it_prakaran(suffix_varnas, UpadeshaType.PRATYAYA)

    # [SIMULATION]: Force 'Nit' tag as 1.3.7 removes 'N'
    if clean_suffix:
        clean_suffix[0].sanjnas.add("ṇit")

    # 2. Prepare Root
    anga_varnas = ad(dhatu_text)

    # 3. Vriddhi (7.2.115)
    # E.g. Bhū -> Bhau
    anga_varnas, _ = VidhiEngine.apply_vṛddhi_7_2_115(anga_varnas, clean_suffix)

    # 4. Ayadi Sandhi (6.1.78)
    # E.g. Bhau -> Bhāv
    # Note: We check if rule applies. If root was 'Kṛ' -> 'Kār', Ayadi wouldn't fire.
    # But for i/u roots, it must fire.
    anga_varnas, _ = VidhiEngine.apply_ayadi_6_1_78(anga_varnas, clean_suffix)

    # 5. Synthesis
    final_varnas = anga_varnas + clean_suffix
    return sanskrit_varna_samyoga(final_varnas)


# --- TEST RUNNER ---
def test_random_nyanta_examples():
    """
    Selects 5 random roots that follow the Nayi pattern.
    """
    # Dictionary of Root -> Expected Causative Stem
    # Logic:
    # i/ī -> ai -> āy
    # u/ū -> au -> āv
    nyanta_db = {
        "भू": "भावि",  # Bhū -> Bhau -> Bhāv + i -> Bhāvi (To cause to be)
        "जि": "जायि",  # Ji -> Jai -> Jāy + i -> Jāyi (To cause to win)
        "श्रु": "श्रावि",  # Śru -> Śrau -> Śrāv + i -> Śrāvi (To cause to hear)
        "चि": "चायि",  # Chi -> Chai -> Chāy + i -> Chāyi (To cause to collect)
        "स्तु": "स्तावि",  # Stu -> Stau -> Stāv + i -> Stāvi (To cause to praise)
        "लु": "लावि",  # Lu -> Lau -> Lāv + i -> Lāvi (To cause to cut)
        "पु": "पावि",  # Pu -> Pau -> Pāv + i -> Pāvi (To cause to purify)
        "द्रु": "द्रावि",  # Dru -> Drau -> Drāv + i -> Drāvi (To cause to run)
        "हु": "हावि",  # Hu -> Hau -> Hāv + i -> Hāvi (To cause to sacrifice)
        "भी": "भायि"  # Bhī -> Bhai -> Bhāy + i -> Bhāyi (To cause to fear)
    }

    # Select 5 unique random roots
    selected_roots = random.sample(list(nyanta_db.keys()), 5)

    print(f"\n🎲 Selected Random Roots: {selected_roots}")

    for root in selected_roots:
        expected = nyanta_db[root]
        print(f"\n➡️ Testing: {root} + णिच्")

        actual = derive_nyanta_form(root)

        assert actual == expected, f"Failed on {root}: Expected '{expected}', Got '{actual}'"
        print(f"   ✅ Success: {actual}")


if __name__ == "__main__":
    test_random_nyanta_examples()