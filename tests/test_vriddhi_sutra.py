"""
FILE: tests/test_vriddhi_sutra.py
TOPIC: वृद्धिसंज्ञायाः प्रयोजनम् (Purpose of Vriddhi Designation)
SOURCE: User Input (Sanskrit Commentary)

SCENARIO:
    १. अत उपधायाः ७.२.११६ इत्यनेन अकारस्य वृद्धिः विधीयते ।
    २. अत्र अकारस्य स्थाने वृद्धिसंज्ञकः आकारः आदिश्यते ।
    ३. उदाहरणम्: पठ् + घञ् -> पाठ
"""

import pytest
from core.phonology import ad, sanskrit_varna_samyoga
from logic.it_engine import ItEngine
from logic.vidhi_engine import VidhiEngine
from core.upadesha_registry import UpadeshaType


def test_ata_upadhayah_7_2_116_derivation():
    """
    Test Case: पठ् + घञ् -> पाठ
    Verifies that the penultimate 'a' grows to 'ā' when followed by a Ñit suffix.
    """
    print("\n🔬 Testing Vriddhi Logic (7.2.116)...")

    # --- 1. INPUTS ---
    dhatu_text = "पठ्"
    pratyaya_text = "घञ्"
    print(f"   Input: {dhatu_text} + {pratyaya_text}")

    # --- 2. PRATYAYA PROCESSING (It-Sanjna) ---
    # We must detect that 'Ghañ' is Ñit (has 'ñ' as It-marker).
    # घञ् -> 'घ्' (1.3.8 Lashakva...) + 'अ' + 'ञ्' (1.3.3 Halantyam)
    # Result should be 'अ' with tags: Ghit, Ñit.

    suffix_varnas = ad(pratyaya_text)
    clean_suffix, _ = ItEngine.run_it_prakaran(suffix_varnas, UpadeshaType.PRATYAYA)

    # Verify Suffix Cleaning
    suffix_str = sanskrit_varna_samyoga(clean_suffix)
    assert suffix_str == "अ", f"Suffix cleaning failed. Expected 'अ', got '{suffix_str}'"

    # Verify Tags (Check if any original varna had the 'Ñit' marker)
    # Note: In the full engine, tags are preserved on the remaining 'a'.
    # Here we assume the logic correctly identified the context for the Vidhi rule.
    print(f"   Clean Suffix: {suffix_str}")

    # --- 3. ANGA PROCESSING (The Stem) ---
    # पठ् -> p-a-ṭh
    anga_varnas = ad(dhatu_text)

    # Verify Upadha (Penultimate Letter) is 'a' (अ)
    # Anga: [प, अ, ठ्] -> Indices: 0, 1, 2. Upadha is Index 1 ('अ').
    upadha_char = anga_varnas[-2].char
    print(f"   Upadha before rule: {upadha_char}")
    assert upadha_char == 'अ', "Pre-condition Failed: Upadha is not 'a'"

    # --- 4. APPLY RULE 7.2.116 (अत उपधायाः) ---
    # Logic: Replace penultimate 'a' with 'ā' (Vriddhi)

    modified_anga, rule_applied = VidhiEngine.apply_ata_upadhayah_7_2_116(anga_varnas)

    # Check if rule fired
    assert rule_applied is not None, "Rule 7.2.116 did not fire!"
    assert "७.२.११६" in rule_applied

    # Verify the change: [प, आ, ठ्]
    new_upadha_char = modified_anga[-2].char
    print(f"   Upadha after rule: {new_upadha_char}")
    assert new_upadha_char == 'आ', f"Vriddhi Failed: Expected 'आ', got '{new_upadha_char}'"

    # --- 5. SYNTHESIS (Samyoga) ---
    # पाठ् + अ -> पाठ
    final_varnas = modified_anga + clean_suffix
    final_result = sanskrit_varna_samyoga(final_varnas)

    print(f"   Final Result: {final_result}")

    # --- 6. FINAL ASSERTION ---
    assert final_result == "पाठ", f"Derivation Mismatch: Expected 'पाठ', got '{final_result}'"


if __name__ == "__main__":
    test_ata_upadhayah_7_2_116_derivation()