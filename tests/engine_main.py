"""
FILE: tests/test_sarva_vs_rama.py
DESCRIPTION: Verifies that the Engine distinguishes between
             Standard Nouns (Rama) and Pronouns (Sarva).
"""
from logic.subanta_engine import SubantaEngine

def test_plural_distinction():
    engine = SubantaEngine()

    print("\n==================================================")
    print("  TEST 1: RAMA (Standard Noun) - Case 1.3")
    print("  Expected: Ramah (Purvasavarna Dirgha)")
    print("==================================================")
    # Rama + Jas -> Rama + as -> Ramah
    log_rama = engine.derive_detailed("राम", 1, 3)
    log_rama.render()

    print("\n==================================================")
    print("  TEST 2: SARVA (Pronoun) - Case 1.3")
    print("  Expected: Sarve (Jasah Shi -> Guna)")
    print("==================================================")
    # Sarva + Jas -> Sarva + Shi (7.1.17) -> Sarva + i -> Sarve (6.1.87)
    log_sarva = engine.derive_detailed("सर्व", 1, 3)
    log_sarva.render()

if __name__ == "__main__":
    test_plural_distinction()