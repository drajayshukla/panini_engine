"""
FILE: tests/run_subanta_demo.py
TIMESTAMP: 2026-01-31 02:00:00 (IST)
DESCRIPTION: Validates that SubantaEngine11 correctly routes different word types
             (Standard, Irregular, Neuter, Pronoun) to their specific logic blocks.
"""
import sys
import os

# Add project root to path so imports work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.phonology import ad, sanskrit_varna_samyoga
from core.prakriya_logger import PrakriyaLogger
from logic.subanta.s_1_1 import SubantaEngine11


def run_test_case(stem, label, expected_hint):
    """
    Runs a derivation for Case 1.1 and checks if the log contains the expected rule/step.
    """
    print(f"\n🔹 TESTING: {stem} ({label})")

    # 1. Setup
    logger = PrakriyaLogger()
    stem_varnas = ad(stem)

    # 2. Run Strategy (The Engine Logic)
    try:
        final_varnas = SubantaEngine11.derive(stem, stem_varnas, logger)
        final_str = sanskrit_varna_samyoga(final_varnas)

        # 3. Analyze Trace
        found_expected = False
        print(f"   Final Form: {final_str}")

        # Scan history for the rule we expect
        for step in logger.history:
            rule = step['rule']
            desc = step.get('description', '')

            # Check if our expected logic block was hit
            if expected_hint in rule or expected_hint in desc:
                found_expected = True
                print(f"     -> [MATCH] Found expected rule: {rule} ({desc})")

        # 4. Final Verdict
        if found_expected:
            print(f"   ✅ PASS: Correct path taken for {label}")
        else:
            print(f"   ⚠️ FAIL: Did not find rule '{expected_hint}' in trace.")

    except Exception as e:
        print(f"   ❌ CRASH: {e}")


def test_all_strategies():
    print("==================================================")
    print("  STRATEGY TEST SUITE: SUBANTA 1.1")
    print("==================================================")

    # 1. RAMA (Standard Masculine)
    # Logic: Should go to generic Visarga finish (8.3.15)
    run_test_case("राम", "Standard Masc", "8.3.15")

    # 2. JNANAM (Standard Neuter)
    # Logic: Should hit Ato'm (7.1.24)
    run_test_case("ज्ञान", "Standard Neuter", "7.1.24")

    # 3. KROSHTU (Irregular)
    # Logic: Should hit Trijvadbhava (7.1.95)
    run_test_case("क्रोष्टु", "Irregular", "7.1.95")

    # 4. TAD (Pronoun)
    # Logic: Should hit Tyadadyatva (7.1.25) or Taddhita logic
    run_test_case("तद्", "Pronoun", "7.1.25")

    # 5. GAURI (Feminine/Halanta)
    # Logic: Should hit Hal-Nyabbhyo Lopa (6.1.68)
    run_test_case("गौरी", "Feminine", "6.1.68")

    # 6. GO (Irregular Vowel)
    # Logic: Should hit Goto Nit (7.1.90)
    run_test_case("गो", "Irregular Vowel", "7.1.90")


if __name__ == "__main__":
    test_all_strategies()