"""
FILE: tests/test_taddhita_aupagava.py
TOPIC: तद्धित-प्रक्रिया (Secondary Derivatives)
SCENARIO: उपगु + अण् -> औपगव (Upagu + Aṇ -> Aupagava)
RULES: 7.2.117 (Adi Vriddhi), 6.4.146 (Orgunah), 6.1.78 (Ayadi)
"""

import pytest
from logic.prakriya_engine import PrakriyaEngine


def test_aupagava_derivation():
    print("\n🔬 Testing Taddhita Logic (Upagu + Aṇ)...")

    # 1. Setup Engine
    engine = PrakriyaEngine()

    # 2. Run Recipe
    # Input: Pratipadika "Upagu", Suffix "Aṇ"
    result = engine.derive_taddhita("उपगु", "अण्")

    print(f"   Result: {result}")

    # 3. Assertions
    expected = "औपगव"
    assert result == expected, f"Expected '{expected}', got '{result}'"

    # 4. Verify Steps in History (Optional but good for debugging)
    history = engine.get_history()

    # Check if Adi Vriddhi happened (Step 2)
    step_vriddhi = next((h for h in history if "७.२.११७" in h['rule']), None)
    assert step_vriddhi is not None, "Rule 7.2.117 (Adi Vriddhi) missed"
    print(f"   ✅ Vriddhi Applied: {step_vriddhi['description']}")

    # Check if Orgunah happened (Step 3)
    step_guna = next((h for h in history if "६.४.१४६" in h['rule']), None)
    assert step_guna is not None, "Rule 6.4.146 (Orgunah) missed"
    print(f"   ✅ Guna Applied: {step_guna['description']}")


@pytest.mark.parametrize("base, suffix, expected", [
    ("उपगु", "अण्", "औपगव"),  # Upagu -> Aupagava
    ("कुरु", "अण्", "कौरव"),  # Kuru -> Kaurava (Similar Logic)
    ("भृगु", "अण्", "भार्गव"),  # Bhrgu -> Bhargava (Adi Vriddhi on Ṛ -> Ār)
])
def test_similar_taddhitas(base, suffix, expected):
    """
    Tests other words that follow the exact same Upagu pattern.
    """
    engine = PrakriyaEngine()
    res = engine.derive_taddhita(base, suffix)
    assert res == expected, f"Failed on {base}: Expected {expected}, got {res}"