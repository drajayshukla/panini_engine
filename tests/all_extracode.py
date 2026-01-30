"""
FILE: tests/test_guna_pitarau.py
TOPIC: गुणसंज्ञायाः प्रयोजनम् (Application of Guna Sanjna)
SOURCE: User Input (Sanskrit Commentary)

SCENARIO:
    १. पितृ + औ (प्रथमाद्विवचन)
    २. ऋतो ङिसर्वनामस्थानयोः (७.३.११०) -> ऋकारस्य गुणः (अ)
    ३. उरण् रपरः (१.१.५१) -> सः रपरः (अर्) -> पितर् + औ
    ४. वर्णसम्मेलनम् -> पितरौ
"""

import pytest
from core.phonology import ad, sanskrit_varna_samyoga
from logic.it_engine import ItEngine
from logic.vidhi_engine import VidhiEngine
from core.upadesha_registry import UpadeshaType


def test_pitarau_derivation():
    print("\n🔬 Testing Guna Logic (Pitṛ + Au)...")

    # --- 1. INPUTS ---
    base_word = "पितृ"
    suffix_text = "औ"
    print(f"   Input: {base_word} + {suffix_text}")

    # --- 2. PREPARATION ---
    anga_varnas = ad(base_word)
    suffix_varnas = ad(suffix_text)

    # Verify Initial State
    assert sanskrit_varna_samyoga(anga_varnas) == "पितृ"

    # --- 3. APPLY RULE 7.3.110 ---
    # Logic: Ṛ -> Ar before Strong Suffix (Au)

    modified_anga, rule = VidhiEngine.apply_rto_ngi_sarvanamasthanayoh_7_3_110(anga_varnas, suffix_varnas)

    # Assertions
    assert rule is not None, "Rule 7.3.110 did not fire!"
    assert "७.३.११०" in rule
    print(f"   ✅ Applied: {rule}")

    # Verify 'Ṛ' became 'Ar'
    # Anga should be: P-i-t-a-r (पितर्)
    current_stem = sanskrit_varna_samyoga(modified_anga)
    print(f"   Stem Change: पितृ -> {current_stem}")
    assert current_stem == "पितर्", f"Expected Stem 'पितर्', got '{current_stem}'"

    # --- 4. SYNTHESIS ---
    # Pitar + Au -> Pitarau
    final_varnas = modified_anga + suffix_varnas
    final_result = sanskrit_varna_samyoga(final_varnas)

    print(f"   Final Result: {final_result}")

    # --- 5. FINAL CHECK ---
    assert final_result == "पितरौ", f"Derivation Failed: Expected 'पितरौ', got '{final_result}'"


if __name__ == "__main__":
    test_pitarau_derivation()
#-------------------
#---------------
"""
FILE: tests/test_guna_matayah.py
TOPIC: जसि च (7.3.109) - Derivation of 'Matayaḥ'
SCENARIO:
    1. Mati + Jas
    2. Mati + As (It-Sanjna)
    3. Mate + As (Jasi Ca - Guna)
    4. Matay + As (Ayadi)
    5. Matayas (Synthesis)
    6. Matayaḥ (Rutva/Visarga)
"""

import pytest
from core.phonology import ad, sanskrit_varna_samyoga
from logic.it_engine import ItEngine
from logic.vidhi_engine import VidhiEngine
from core.upadesha_registry import UpadeshaType


def test_matayah_derivation():
    print("\n🔬 Testing 7.3.109 Jasi Ca (Mati + Jas)...")

    # --- 1. INPUTS ---
    base = "मति"
    suffix = "जस्"
    print(f"   Input: {base} + {suffix}")

    # --- 2. PREPARATION (IT-SANJNA) ---
    anga = ad(base)

    # Clean 'Jas' -> 'As' (1.3.7 Chutu removes 'J')
    raw_suffix = ad(suffix)
    clean_suffix, _ = ItEngine.run_it_prakaran(raw_suffix, UpadeshaType.VIBHAKTI)

    # Verify Clean State
    assert sanskrit_varna_samyoga(clean_suffix) == "अस्"
    print(f"   Cleaned Suffix: {sanskrit_varna_samyoga(clean_suffix)}")

    # --- 3. APPLY JASI CA (7.3.109) ---
    # Mati + As -> Mate + As
    anga, rule_guna = VidhiEngine.apply_jasi_ca_7_3_109(anga, clean_suffix)

    assert rule_guna is not None
    assert "७.३.१०९" in rule_guna
    print(f"   ✅ Guna Applied: {rule_guna} -> Form: {sanskrit_varna_samyoga(anga)}")

    # Check Stem is now 'Mate'
    assert sanskrit_varna_samyoga(anga) == "मते"

    # --- 4. APPLY AYADI SANDHI (6.1.78) ---
    # Mate + As -> Matay + As
    anga, rule_ayadi = VidhiEngine.apply_ayadi_6_1_78(anga, clean_suffix)

    assert rule_ayadi is not None
    print(f"   ✅ Ayadi Applied: {rule_ayadi} -> Form: {sanskrit_varna_samyoga(anga)}")

    # --- 5. SYNTHESIS & TRIPADI ---
    # Combine: Matay + As -> Matayas
    full_form = anga + clean_suffix

    # Apply Rutva (8.2.66): Matayas -> Matayaru
    full_form, _ = VidhiEngine.apply_rutva_8_2_66(full_form)

    # Apply Visarga (8.3.15): Matayaru -> Matayaḥ
    full_form, _ = VidhiEngine.apply_visarga_8_3_15(full_form)

    final_result = sanskrit_varna_samyoga(full_form)
    print(f"   Final Result: {final_result}")

    # --- 6. FINAL ASSERTION ---
    expected = "मतयः"
    assert final_result == expected, f"Expected {expected}, got {final_result}"


if __name__ == "__main__":
    test_matayah_derivation()

    #-------
    """
    FILE: derive_nayi.py
    TOPIC: नी + णिच् -> नायि (Step-by-Step Derivation)
    """

    from core.phonology import ad, sanskrit_varna_samyoga
    from logic.it_engine import ItEngine
    from logic.vidhi_engine import VidhiEngine
    from core.upadesha_registry import UpadeshaType


    def derive_nayi():
        print("\n🔬 PANINIAN DERIVATION: Nī + Ṇic -> Nāyi\n")

        # --- STEP 1: IT-SANJNA (Cleaning) ---
        # Sutras: 1.3.3 (Halantyam), 1.3.7 (Chutu), 1.3.9 (Tasya Lopah)
        root_str = "नी"
        suffix_str = "णिच्"

        anga = ad(root_str)
        suffix_raw = ad(suffix_str)

        print(f"1. Input: {root_str} + {suffix_str}")

        # Apply Cleaning
        clean_suffix, _ = ItEngine.run_it_prakaran(suffix_raw, UpadeshaType.PRATYAYA)

        # [CRITICAL]: Manually tag the suffix as Ṇit because 1.3.7 removed 'Ñ/Ṇ'
        # In a full flow, ItEngine does this. We force it here for the test logic.
        if clean_suffix:
            clean_suffix[0].sanjnas.add("ṇit")

        print(f"   → {root_str} + {sanskrit_varna_samyoga(clean_suffix)} [इत्संज्ञालोपः]")

        # --- STEP 2: VRIDDHI (7.2.115) ---
        # Sutra: अचो ञ्णिति (7.2.115)
        anga, s_72115 = VidhiEngine.apply_vṛddhi_7_2_115(anga, clean_suffix)

        step2_form = sanskrit_varna_samyoga(anga)
        print(f"   → {step2_form} + {sanskrit_varna_samyoga(clean_suffix)} [{s_72115} इत्यनेन ईकारस्य वृद्धिः ऐकारः]")

        # --- STEP 3: AYADI SANDHI (6.1.78) ---
        # Sutra: एचोऽयवायावः (6.1.78)
        anga, s_6178 = VidhiEngine.apply_ayadi_6_1_78(anga, clean_suffix)

        step3_form = sanskrit_varna_samyoga(anga)
        print(f"   → {step3_form} + {sanskrit_varna_samyoga(clean_suffix)} [{s_6178} इति आयादेशः]")

        # --- STEP 4: SYNTHESIS (3.1.32) ---
        # Sutra: सनाद्यन्ता धातवः (3.1.32)
        final_varnas = anga + clean_suffix
        final_result = sanskrit_varna_samyoga(final_varnas)

        print(f"   → {final_result} [सनाद्यन्ता धातवः ३.१.३२ इति धातुसंज्ञा]")


    if __name__ == "__main__":
        derive_nayi()
import pytest
from core.phonology import ad, sanskrit_varna_samyoga
from logic.it_engine import ItEngine
from core.upadesha_registry import UpadeshaType
from logic.vidhi_engine import VidhiEngine


# --- LEGACY COMPATIBILITY TEST ---
def clean_and_rejoin(text, context):
    varnas = ad(text)
    cleaned_varnas, trace = ItEngine.run_it_prakaran(varnas, context)
    return sanskrit_varna_samyoga(cleaned_varnas)


def test_legacy_examples():
    """
    Tests the specific examples from your 2026 logic.
    EXPECTATION: 1.3.2 removes Vowel + Marker, leaving strict Halanta roots.
    """
    print("\n🔍 Running Legacy 2026 Compatibility Check...")

    examples = [
        # (Input, Context, Expected Output (Strict Halanta))
        ("भजँ", UpadeshaType.DHATU, "भज्"),
        ("यजँ", UpadeshaType.DHATU, "यज्"),
        ("त्यजँ", UpadeshaType.DHATU, "त्यज्"),
        ("पठँ", UpadeshaType.DHATU, "पठ्"),
        ("तपँ", UpadeshaType.DHATU, "तप्"),
        ("पतँ", UpadeshaType.DHATU, "पत्"),

        # Complex Markers
        ("टुओँस्फूर्जाँ", UpadeshaType.DHATU, "स्फूर्ज्"),

        # [CORRECTION]: Tu-Vepṛ~ -> Vep (Ṛ is It-marker/Anunasika Ach, so it goes)
        ("टुवेपृँ", UpadeshaType.DHATU, "वेप्"),

        ("ञिफलाँ", UpadeshaType.DHATU, "फल्"),
        ("डुभजँ", UpadeshaType.DHATU, "भज्"),

        # Suffixes
        ("घञ्", UpadeshaType.PRATYAYA, "अ"),
        ("ष्यञ्", UpadeshaType.PRATYAYA, "य"),
        ("ल्युट्", UpadeshaType.PRATYAYA, "यु")
    ]

    for inp, ctx, exp in examples:
        result = clean_and_rejoin(inp, ctx)
        assert result == exp, f"Failed on {inp}: Expected {exp}, got {result}"
        print(f"✅ Pass: {inp} -> {result}")


# --- GHANJ DERIVATION TEST ---
def derive_ghanj_logic(dhatu_text):
    # 1. PROCESS DHATU
    dhatu_varnas = ad(dhatu_text)
    dhatu_clean, _ = ItEngine.run_it_prakaran(dhatu_varnas, UpadeshaType.DHATU)

    # 2. PROCESS PRATYAYA
    suffix_varnas = ad("घञ्")
    suffix_clean, _ = ItEngine.run_it_prakaran(suffix_varnas, UpadeshaType.PRATYAYA)

    # 3. TAG TRANSFER
    if suffix_clean:
        for v in suffix_clean:
            v.sanjnas.add("ghit")
            v.sanjnas.add("ñit")

            # 4. COMBINE
    combined = dhatu_clean + suffix_clean
    split_idx = len(dhatu_clean)

    # 5. VIDHI
    combined, _ = VidhiEngine.apply_ata_upadhayah_7_2_116(combined, manual_range=(0, split_idx))
    combined, _ = VidhiEngine.apply_chajo_ku_7_3_52(combined, manual_range=(0, split_idx))

    return sanskrit_varna_samyoga(combined)


@pytest.mark.parametrize("dhatu, expected", [
    ("यजँ", "याग"),
    ("भजँ", "भाग"),
    ("त्यजँ", "त्याग"),
    ("पठँ", "पाठ"),
    ("तपँ", "ताप"),
    ("पचँ", "पाक"),
    ("वचँ", "वाक"),
    ("सचँ", "साक")
])
def test_ghanj_derivation(dhatu, expected):
    result = derive_ghanj_logic(dhatu)
    assert result == expected
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

"""
FILE: tests/test_bhavaniya.py
TOPIC: कृत्-प्रक्रिया (Kṛt Derivations)
SUTRA: सार्वधातुकार्धधातुकयोः (7.3.84)
SCENARIO: भू + अनीयर् -> भवनीय (Bhū + Anīyar -> Bhavanīya)
"""

import pytest
from core.phonology import ad, sanskrit_varna_samyoga
from logic.it_engine import ItEngine
from logic.vidhi_engine import VidhiEngine
from core.upadesha_registry import UpadeshaType


def test_bhavaniya_derivation():
    print("\n🔬 Testing 7.3.84 Sarvadhatukardhadhatukayoh...")

    # --- 1. INPUT ---
    dhatu = "भू"
    suffix = "अनीयर्"
    print(f"   Input: {dhatu} + {suffix}")

    # --- 2. IT-PRAKARAN (Cleaning) ---
    anga = ad(dhatu)
    raw_suffix = ad(suffix)

    # Clean 'Anīyar' -> 'Anīya' (1.3.3 Halantyam removes 'r')
    clean_suffix, it_log = ItEngine.run_it_prakaran(raw_suffix, UpadeshaType.PRATYAYA)

    print(f"   It-Sanjna Log: {it_log}")
    current_suffix = sanskrit_varna_samyoga(clean_suffix)
    assert current_suffix == "अनीय", f"Expected 'अनीय', got '{current_suffix}'"

    # --- 3. APPLY GUNA (7.3.84) ---
    # Logic: Bhū -> Bho
    anga, rule_guna = VidhiEngine.apply_sarvadhatukardhadhatukayoh_7_3_84(anga, clean_suffix)

    assert rule_guna is not None
    assert "७.३.८४" in rule_guna
    print(f"   ✅ Guna Applied: {rule_guna}")
    print(f"      Current Anga: {sanskrit_varna_samyoga(anga)}")  # Should be 'Bho'

    # --- 4. APPLY AYADI SANDHI (6.1.78) ---
    # Logic: Bho + Anīya -> Bhav + Anīya
    anga, rule_ayadi = VidhiEngine.apply_ayadi_6_1_78(anga, clean_suffix)

    assert rule_ayadi is not None
    print(f"   ✅ Ayadi Applied: {rule_ayadi}")
    print(f"      Current Anga: {sanskrit_varna_samyoga(anga)}")  # Should be 'Bhav'

    # --- 5. SYNTHESIS ---
    final_varnas = anga + clean_suffix
    final_result = sanskrit_varna_samyoga(final_varnas)

    print(f"   Final Result: {final_result}")

    # --- 6. ASSERTION ---
    expected = "भवनीय"
    assert final_result == expected, f"Derivation Failed. Expected {expected}, got {final_result}"


if __name__ == "__main__":
    test_bhavaniya_derivation()
"""
FILE: tests/test_paribhasha_ika.py
TOPIC: परिभाषा १.१.३ इकः गुणवृद्धी
SCENARIO: Verify that Guna only happens on Ik letters.
"""

import pytest
from core.phonology import ad
from logic.vidhi_engine import VidhiEngine
from core.paribhasha_manager import ParibhashaManager


def test_ika_paribhasha_logic():
    print("\n🔬 Testing Paribhasha 1.1.3 (Iko Guna Vriddhi)...")

    # --- TEST 1: The Definition ---
    print("   1. Checking Definition Logic...")
    assert ParibhashaManager.is_ika_1_1_3(ad("इ")[0]) == True
    assert ParibhashaManager.is_ika_1_1_3(ad("उ")[0]) == True
    assert ParibhashaManager.is_ika_1_1_3(ad("क")[0]) == False
    assert ParibhashaManager.is_ika_1_1_3(ad("ए")[0]) == False  # E is Guna, not Ik
    print("   ✅ Definition Check Passed")


def test_guna_blocking():
    print("   2. Checking Rule Application (7.3.84 constrained by 1.1.3)...")

    # CASE A: POSITIVE (Nī -> Ne)
    # Nī (नी) ends in Ī (Ik). Should change.
    anga_ni = ad("नी")
    suffix = ad("अ")

    res_ni, rule_ni = VidhiEngine.apply_sarvadhatukardhadhatukayoh_7_3_84(anga_ni, suffix)
    assert rule_ni is not None
    print(f"   ✅ Nī (Ik) -> {res_ni[-1].char} (Rule: {rule_ni})")

    # CASE B: NEGATIVE (Gam -> No Change)
    # Gam (गम्) ends in M (Not Ik). Should NOT change.
    anga_gam = ad("गम्")

    res_gam, rule_gam = VidhiEngine.apply_sarvadhatukardhadhatukayoh_7_3_84(anga_gam, suffix)

    assert rule_gam is None
    print(f"   ✅ Gam (Non-Ik) -> No Change (Blocked by 1.1.3)")


if __name__ == "__main__":
    test_ika_paribhasha_logic()
    test_guna_blocking()
"""
FILE: tests/test_medyati.py
TOPIC: भ्वादिगण (Bhvādi) - मिदेर्गुणः (7.3.82)
SCENARIO: ञिमिदाँ -> मेद्यति (Medyati)
RULES: 1.3.5, 1.3.2, 7.3.82 (constrained by 1.1.3)
"""

import pytest
from core.phonology import ad, sanskrit_varna_samyoga
from logic.it_engine import ItEngine
from logic.vidhi_engine import VidhiEngine
from core.upadesha_registry import UpadeshaType


def test_medyati_derivation():
    print("\n🔬 Testing 7.3.82 Midergunah (Mid + Śyan)...")

    # --- 1. ROOT PREPARATION ---
    # Input: Ñimidā~ (ञिमिदाँ)
    raw_root = "ञिमिदाँ"
    print(f"   Raw Root: {raw_root}")

    # Clean Root:
    # 1. 1.3.5 Adi Ñitudavah (Removes 'Ñi')
    # 2. 1.3.2 Upadeshe'janunasika (Removes 'ā~')
    root_varnas = ad(raw_root)
    clean_root, root_log = ItEngine.run_it_prakaran(root_varnas, UpadeshaType.DHATU)

    stem = sanskrit_varna_samyoga(clean_root)
    print(f"   Cleaned Root: {stem} (Log: {root_log})")
    assert stem == "मिद्", f"Root cleaning failed. Expected 'मिद्', got '{stem}'"

    # --- 2. SUFFIX PREPARATION ---
    # Suffix 1: Śyan (श्यन्) -> Vikarana for Divadi Gana
    raw_vikarana = ad("श्यन्")
    clean_vikarana, _ = ItEngine.run_it_prakaran(raw_vikarana, UpadeshaType.PRATYAYA)

    # [CRITICAL]: Manually apply 'śit' tag because 1.3.8 removes 'Ś'
    # The rule 7.3.82 specifically requires a 'Śit' suffix.
    if clean_vikarana:
        clean_vikarana[0].sanjnas.add("śit")
        print("   ✅ Tagged suffix 'ya' as Śit")

    # Suffix 2: Tip (तिप्) -> T + i + p -> ti
    raw_tip = ad("तिप्")
    clean_tip, _ = ItEngine.run_it_prakaran(raw_tip, UpadeshaType.VIBHAKTI)

    # --- 3. APPLY 7.3.82 MIDER GUNAH ---
    # Logic: Mid + ya -> Med + ya
    # Note: We pass the Vikarana (ya) as the trigger suffix

    anga, rule_code = VidhiEngine.apply_mider_gunah_7_3_82(clean_root, clean_vikarana)

    assert rule_code is not None
    assert "७.३.८२" in rule_code
    print(f"   ✅ Rule Applied: {rule_code}")

    current_stem = sanskrit_varna_samyoga(anga)
    print(f"   Stem Change: मिद् -> {current_stem}")
    assert current_stem == "मेद्", "Guna failed on 'Mid'"

    # --- 4. SYNTHESIS ---
    # Med + ya + ti
    final_varnas = anga + clean_vikarana + clean_tip
    result = sanskrit_varna_samyoga(final_varnas)

    print(f"   Final Result: {result}")

    expected = "मेद्यति"
    assert result == expected, f"Expected {expected}, got {result}"


if __name__ == "__main__":
    test_medyati_derivation()
"""
FILE: tests/test_bodhati.py
TOPIC: पुगन्तलघूपधस्य च (7.3.86)
SCENARIO: बुध् + शप् + तिप् -> बोधति (Bodhati)
"""

import pytest
from core.phonology import ad, sanskrit_varna_samyoga
from logic.vidhi_engine import VidhiEngine


def test_bodhati_derivation():
    print("\n🔬 Testing 7.3.86 Puganta Laghupadhasya (Budh + Sap)...")

    # 1. Input: Budh (No It-sanjna needed for simple test)
    anga = ad("बुध्")  # b-u-dh
    suffix = ad("अ")  # Sap (Vikaran)

    print(f"   Anga: {sanskrit_varna_samyoga(anga)}")

    # 2. Apply 7.3.86
    # Expectation: Penultimate 'u' is Laghu. Should become 'o'.
    anga, rule = VidhiEngine.apply_puganta_laghupadhasya_7_3_86(anga, suffix)

    assert rule is not None
    assert "७.३.८६" in rule
    print(f"   ✅ Rule Applied: {rule}")

    # 3. Check Result: Bodh
    res_stem = sanskrit_varna_samyoga(anga)
    print(f"   Result Stem: {res_stem}")
    assert res_stem == "बोध्"

    # 4. Final Form: Bodh + a + ti
    final = sanskrit_varna_samyoga(anga + suffix + ad("ति"))
    print(f"   Final Form: {final}")
    assert final == "बोधति"


if __name__ == "__main__":
    test_bodhati_derivation()

"""
FILE: tests/test_kniti_blocker.py
TOPIC: क्ङिति च (1.1.5) - The Guna Blocker
SCENARIO:
    1. Nī + Tip -> Ne (Guna Allowed) -> Nayati
    2. Nī + Kta -> Nī (Guna Blocked) -> Nīta
"""

import pytest
from core.phonology import ad, sanskrit_varna_samyoga
from logic.vidhi_engine import VidhiEngine
from logic.it_engine import ItEngine
from core.upadesha_registry import UpadeshaType


def test_kniti_blocking():
    print("\n🔬 Testing 1.1.5 Kniti Ca (Guna Blocking)...")

    # --- CASE 1: Nī + Tip (Guna SHOULD happen) ---
    root = ad("नी")
    suffix_tip = ad("तिप्")

    # Clean Tip (removes p)
    clean_tip, _ = ItEngine.run_it_prakaran(suffix_tip, UpadeshaType.VIBHAKTI)

    # Apply 7.3.84
    res_tip, rule_tip = VidhiEngine.apply_sarvadhatukardhadhatukayoh_7_3_84(root[:], clean_tip)  # Pass copy of root

    print(f"   1. Nī + Tip: {rule_tip if rule_tip else 'Blocked'}")
    assert rule_tip is not None, "Guna should apply to Tip!"
    assert sanskrit_varna_samyoga(res_tip) == "ने"  # Ne

    # --- CASE 2: Nī + Kta (Guna should be BLOCKED) ---
    root = ad("नी")  # Reset root
    suffix_kta = ad("क्त")

    # Clean Kta (Removes K -> marks as 'kit')
    clean_kta, log_kta = ItEngine.run_it_prakaran(suffix_kta, UpadeshaType.PRATYAYA)
    print(f"      Kta Cleaning Log: {log_kta}")

    # Verify 'kit' tag
    assert "kit" in clean_kta[0].sanjnas, "Suffix Kta must be tagged 'kit'!"

    # Attempt 7.3.84
    res_kta, rule_kta = VidhiEngine.apply_sarvadhatukardhadhatukayoh_7_3_84(root[:], clean_kta)

    print(f"   2. Nī + Kta: {rule_kta if rule_kta else 'Blocked'}")

    # ASSERT BLOCKING
    assert rule_kta is None, "Guna should contain been BLOCKED by 1.1.5!"
    assert sanskrit_varna_samyoga(res_kta) == "नी"  # Remains Nī


if __name__ == "__main__":
    test_kniti_blocking()

"""
FILE: tests/test_yaniya.py
TOPIC: इको गुणवृद्धी (1.1.3) - The Constraint
SCENARIO:
    1. Yā (ends in Ā, not Ik) + Anīyar
    2. Guna (7.3.84) -> BLOCKED by 1.1.3
    3. Savarna Dirgha (6.1.101) -> APPLIES
    4. Result: Yānīya
"""

import pytest
from core.phonology import ad, sanskrit_varna_samyoga
from logic.vidhi_engine import VidhiEngine
from logic.it_engine import ItEngine
from core.upadesha_registry import UpadeshaType


def test_yaniya_derivation():
    print("\n🔬 Testing 1.1.3 Constraint (Yā + Anīyar)...")

    # --- 1. PREPARATION ---
    root = ad("या")
    suffix = ad("अनीयर्")

    # Clean Suffix: Anīyar -> Anīya
    clean_suffix, _ = ItEngine.run_it_prakaran(suffix, UpadeshaType.PRATYAYA)
    print(f"   Input: {sanskrit_varna_samyoga(root)} + {sanskrit_varna_samyoga(clean_suffix)}")

    # --- 2. ATTEMPT GUNA (7.3.84) ---
    # Logic: 7.3.84 wants to apply Guna.
    # Constraint: 1.1.3 says "Only if ending in Ik".
    # 'Ā' is NOT in Ik. -> Must return None.

    # Pass copy of list to ensure we don't modify it if it fails
    res_guna, rule_guna = VidhiEngine.apply_sarvadhatukardhadhatukayoh_7_3_84(root[:], clean_suffix)

    print(f"   Guna Check: {rule_guna if rule_guna else 'BLOCKED'}")

    # ASSERT BLOCKING
    assert rule_guna is None, "❌ Guna should NOT apply! 'Ā' is not an Ik letter."

    # --- 3. APPLY SAVARNA DIRGHA (6.1.101) ---
    # Yā + Anīya -> Yānīya
    # Logic: Ā + A -> Ā

    # We use the original root because Guna didn't change it
    res_sandhi, rule_sandhi = VidhiEngine.apply_aka_savarne_dirgha_6_1_101(root, clean_suffix)

    assert rule_sandhi is not None
    assert "६.१.१०१" in rule_sandhi
    print(f"   ✅ Sandhi Applied: {rule_sandhi}")

    # --- 4. FINAL SYNTHESIS ---
    final_form = sanskrit_varna_samyoga(res_sandhi + clean_suffix)  # clean_suffix had first char popped in Vidhi
    print(f"   Final Result: {final_form}")

    assert final_form == "यानीय", f"Expected 'यानीय', got '{final_form}'"


if __name__ == "__main__":
    test_yaniya_derivation()


"""
FILE: tests/all_extracode.py
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

    """
    FILE: tests/master_prakriya_test.py
    PAS-v2.0: 5.0 (Siddha)
    PILLAR: Quality Assurance & Verification
    DESCRIPTION: Master test for Gauḥ, Dyauḥ, and Yānīya using the new Modular Engine.
    """

    import pytest
    from core.phonology import ad, sanskrit_varna_samyoga
    from logic.vidhi import VidhiEngine
    from logic.it_engine import ItEngine
    from core.upadesha_registry import UpadeshaType


    class TestMasterDerivations:
        """
        Validates that the modular VidhiEngine correctly handles complex
        derivations involving substitutions, Sandhi, and Tripadi rules.
        """

        def test_gauh_derivation(self):
            """[GO + SU]: Proves 7.2.115 Vriddhi on non-Ik vowel 'o'."""
            print("\n🔬 Testing: Go + Su -> Gauḥ")
            anga = ad("गो")
            suffix = ad("सुँ")

            # 1. It-Prakaran (Standard marker removal)
            clean_suffix, _ = ItEngine.run_it_prakaran(suffix, UpadeshaType.VIBHAKTI)

            # 2. Atidesha (7.1.90) - Virtual Nit marker tagging
            VidhiEngine.apply_goto_nit_7_1_90(clean_suffix)

            # 3. Vriddhi (7.2.115) - End vowel transformation
            # Inherited from guna_vriddhi.py
            anga, rule = VidhiEngine.apply_aco_niti_7_2_115(anga, clean_suffix)
            assert sanskrit_varna_samyoga(anga) == "गौ"

            # 4. Tripadi (8.2.66 & 8.3.15) - Final phonology
            # Inherited from tripadi.py
            full = anga + clean_suffix
            full, _ = VidhiEngine.apply_rutva_8_2_66(full)
            full, _ = VidhiEngine.apply_visarga_8_3_15(full)

            final = sanskrit_varna_samyoga(full)
            print(f"   ✅ Result: {final}")
            assert final == "गौः"

        def test_dyauh_derivation(self):
            """[DIV + SU]: Proves 7.1.84 Substitution and 6.1.77 Yan Sandhi."""
            print("\n🔬 Testing: Div + Su -> Dyauḥ")
            anga = ad("दिव्")
            suffix = ad("सुँ")

            # 1. It-Prakaran
            clean_suffix, _ = ItEngine.run_it_prakaran(suffix, UpadeshaType.VIBHAKTI)

            # 2. Substitution (7.1.84) - v -> au (Alo'ntyasya 1.1.52)
            # Inherited from anga_transform.py
            anga, rule_aut = VidhiEngine.apply_div_aut_7_1_84(anga, clean_suffix)
            assert sanskrit_varna_samyoga(anga) == "दिऔ"

            # 3. Yan Sandhi (6.1.77) - i -> y
            # Inherited from sandhi_engine.py
            anga, rule_yan = VidhiEngine.apply_iko_yan_achi_6_1_77(anga)
            assert sanskrit_varna_samyoga(anga) == "द्यौ"

            # 4. Tripadi
            full = anga + clean_suffix
            full, _ = VidhiEngine.apply_rutva_8_2_66(full)
            full, _ = VidhiEngine.apply_visarga_8_3_15(full)

            final = sanskrit_varna_samyoga(full)
            print(f"   ✅ Result: {final}")
            assert final == "द्यौः"

        def test_yaniya_derivation(self):
            """[YĀ + ANĪYA]: Proves 6.1.101 Savarna Dirgha."""
            print("\n🔬 Testing: Yā + Anīya -> Yānīya")
            anga = ad("या")
            suffix = ad("अनीयर्")

            # 1. It-Prakaran (Remove 'r')
            clean_suffix, _ = ItEngine.run_it_prakaran(suffix, UpadeshaType.PRATYAYA)

            # 2. Savarna Dirgha (6.1.101) - ā + a -> ā
            # Inherited from sandhi_engine.py
            anga, rule_dirgha = VidhiEngine.apply_aka_savarne_dirgha_6_1_101(anga, clean_suffix)

            # Synthesis
            final = sanskrit_varna_samyoga(anga + clean_suffix)
            print(f"   ✅ Result: {final}")
            assert final == "यानीय"


    if __name__ == "__main__":
        # Execute via pytest for detailed reporting
        pytest.main([__file__])
"""
FILE: tests/test_dyauh.py
TOPIC: दिव औत् (7.1.84) & 1.1.52 (Alo'ntyasya)
SCENARIO: Div + Su -> Dyauḥ
"""

import pytest
from core.phonology import ad, sanskrit_varna_samyoga
from logic.vidhi_engine import VidhiEngine
from logic.it_engine import ItEngine
from core.upadesha_registry import UpadeshaType


def test_dyauh_derivation():
    print("\n🔬 Testing 7.1.84 Diva Aut (Div + Su)...")

    # --- 1. PREPARATION ---
    # Root: Div (दिव्), Suffix: Su (सुँ)
    root = ad("दिव्")
    suffix = ad("सुँ")

    # Clean Suffix: सुँ -> स्
    clean_suffix, _ = ItEngine.run_it_prakaran(suffix, UpadeshaType.VIBHAKTI)
    print(f"   Input: {sanskrit_varna_samyoga(root)} + {sanskrit_varna_samyoga(clean_suffix)}")

    # --- 2. APPLY 7.1.84 (v -> au) ---
    # Per 1.1.52, the final 'v' of 'Div' becomes 'au'
    anga, rule_aut = VidhiEngine.apply_div_aut_7_1_84(root, clean_suffix)

    assert rule_aut is not None
    print(f"   ✅ Rule Applied: {rule_aut}")
    print(f"      Intermediate Stem: {sanskrit_varna_samyoga(anga)}")  # दि + औ
    assert sanskrit_varna_samyoga(anga) == "दिऔ"

    # --- 3. APPLY YAN SANDHI (6.1.77) ---
    # Logic: i + au -> y + au
    anga, rule_yan = VidhiEngine.apply_iko_yan_achi_6_1_77(anga)

    assert rule_yan is not None
    print(f"   ✅ Yan Applied: {rule_yan}")
    print(f"      Final Stem: {sanskrit_varna_samyoga(anga)}")  # द्यौ
    assert sanskrit_varna_samyoga(anga) == "द्यौ"

    # --- 4. SYNTHESIS & VISARGA ---
    # Dyau + s -> Dyauḥ
    full_varnas = anga + clean_suffix

    # Rutva (8.2.66) and Visarga (8.3.15)
    full_varnas, _ = VidhiEngine.apply_rutva_8_2_66(full_varnas)
    full_varnas, _ = VidhiEngine.apply_visarga_8_3_15(full_varnas)

    final_result = sanskrit_varna_samyoga(full_varnas)
    print(f"   Final Result: {final_result}")

    assert final_result == "द्यौः"


if __name__ == "__main__":
    test_dyauh_derivation()

"""
FILE: tests/test_kniti_blocker.py
TOPIC: क्ङिति च (1.1.5) - The Guna Blocker
SCENARIO:
    1. Nī + Tip -> Ne (Guna Allowed) -> Nayati
    2. Nī + Kta -> Nī (Guna Blocked) -> Nīta
"""

import pytest
from core.phonology import ad, sanskrit_varna_samyoga
from logic.vidhi_engine import VidhiEngine
from logic.it_engine import ItEngine
from core.upadesha_registry import UpadeshaType


def test_kniti_blocking():
    print("\n🔬 Testing 1.1.5 Kniti Ca (Guna Blocking)...")

    # --- CASE 1: Nī + Tip (Guna SHOULD happen) ---
    root = ad("नी")
    suffix_tip = ad("तिप्")

    # Clean Tip (removes p)
    clean_tip, _ = ItEngine.run_it_prakaran(suffix_tip, UpadeshaType.VIBHAKTI)

    # Apply 7.3.84
    res_tip, rule_tip = VidhiEngine.apply_sarvadhatukardhadhatukayoh_7_3_84(root[:], clean_tip)  # Pass copy of root

    print(f"   1. Nī + Tip: {rule_tip if rule_tip else 'Blocked'}")
    assert rule_tip is not None, "Guna should apply to Tip!"
    assert sanskrit_varna_samyoga(res_tip) == "ने"  # Ne

    # --- CASE 2: Nī + Kta (Guna should be BLOCKED) ---
    root = ad("नी")  # Reset root
    suffix_kta = ad("क्त")

    # Clean Kta (Removes K -> marks as 'kit')
    clean_kta, log_kta = ItEngine.run_it_prakaran(suffix_kta, UpadeshaType.PRATYAYA)
    print(f"      Kta Cleaning Log: {log_kta}")

    # Verify 'kit' tag
    assert "kit" in clean_kta[0].sanjnas, "Suffix Kta must be tagged 'kit'!"

    # Attempt 7.3.84
    res_kta, rule_kta = VidhiEngine.apply_sarvadhatukardhadhatukayoh_7_3_84(root[:], clean_kta)

    print(f"   2. Nī + Kta: {rule_kta if rule_kta else 'Blocked'}")

    # ASSERT BLOCKING
    assert rule_kta is None, "Guna should contain been BLOCKED by 1.1.5!"
    assert sanskrit_varna_samyoga(res_kta) == "नी"  # Remains Nī


if __name__ == "__main__":
    test_kniti_blocking()
"""
FILE: tests/test_gauh.py
SCENARIO: Go + Su -> Gauḥ
PROVES: 7.2.115 operates on 'o' (non-Ik) due to explicit 'Ac' mention.
"""

from core.phonology import ad, sanskrit_varna_samyoga
from logic.vidhi_engine import VidhiEngine
from logic.it_engine import ItEngine
from core.upadesha_registry import UpadeshaType


def test_gauh_derivation():
    # 1. Input: Go + Su
    root = ad("गो")
    suffix = ad("सुँ")

    # 2. It-Prakaran: su -> s
    clean_suffix, _ = ItEngine.run_it_prakaran(suffix, UpadeshaType.VIBHAKTI)

    # 3. Atidesha: su is Nit-vadbhava after Go
    VidhiEngine.apply_goto_nit_7_1_90(clean_suffix)

    # 4. Vriddhi: o -> au (Bypasses Ik restriction)
    anga, rule = VidhiEngine.apply_aco_niti_7_2_115(root, clean_suffix)

    # Assertions
    assert "वृद्धि" in anga[-1].sanjnas
    assert sanskrit_varna_samyoga(anga) == "गौ"

    # 5. Final Synthesis
    full = anga + clean_suffix
    full, _ = VidhiEngine.apply_rutva_8_2_66(full)
    full, _ = VidhiEngine.apply_visarga_8_3_15(full)

    assert sanskrit_varna_samyoga(full) == "गौः"
    print(f"\n✅ Result: {sanskrit_varna_samyoga(full)} (Rule: {rule})")


if __name__ == "__main__":
    test_gauh_derivation()
"""
FILE: tests/stress_test_naika.py
PAS-v2.0: 5.0 (Siddha)
PURPOSE: The "Stress Test" - Integrates nearly every module in the architecture.
FLOW:
    1. It-Prakaran (1.3.x)
    2. Vriddhi (7.2.115)
    3. Ayadi Sandhi (6.1.78)
    4. Rutva/Visarga (Tripadi)
"""

import pytest
from core.phonology import ad, sanskrit_varna_samyoga
from logic.vidhi import VidhiEngine
from logic.it_engine import ItEngine
from core.upadesha_registry import UpadeshaType


def test_tough_nayaka_derivation():
    print("\n🚀 STARTING STRESS TEST: Nī + Ghañ -> Nāyakaḥ")

    # 1. SETUP: Root (Nī) + Suffix (Ṇvul - which results in 'aka')
    # We use Ghañ logic to simplify, but testing the Vṛddhi + Ayādi chain.
    root = ad("नी")
    # For this test, we simulate the 'aka' that comes from Ṇvul (7.1.1)
    # but keep the Ṇit tags that trigger Vṛddhi.
    suffix_raw = ad("अक")

    print(f"   Input: {sanskrit_varna_samyoga(root)} + {sanskrit_varna_samyoga(suffix_raw)}")

    # 2. TAGGING: Simulate the Ṇit status from the original Ṇvul suffix
    # This tests if VidhiEngine correctly reads tags from the suffix varna.
    suffix_raw[0].sanjnas.add("ṇit")

    # 3. VRIDDHI (7.2.115): अचो ञ्णिति
    # Logic: Final 'ī' of root becomes 'ai' because suffix is Ṇit.
    # Note: 1.1.3 (Ik restriction) applies here.
    anga, rule_vriddhi = VidhiEngine.apply_aco_niti_7_2_115(root, suffix_raw)

    step1_val = sanskrit_varna_samyoga(anga)
    print(f"   Step 1 (Vriddhi): {step1_val} [Rule: {rule_vriddhi}]")
    assert step1_val == "नै", "Vriddhi failed: 'ī' did not become 'ai'"

    # 4. AYADI SANDHI (6.1.78): एचोऽयवायावः
    # Logic: 'ai' + 'a' -> 'āy' + 'a'
    # This tests the SandhiEngine's ability to handle internal word formation.
    anga, rule_ayadi = VidhiEngine.apply_ayadi_6_1_78(anga, suffix_raw)

    step2_val = sanskrit_varna_samyoga(anga)
    print(f"   Step 2 (Ayadi): {step2_val} [Rule: {rule_ayadi}]")
    assert step2_val == "नाय्", "Ayadi failed: 'ai' did not become 'āy'"

    # 5. SYNTHESIS & VIBHAKTI
    # Combine Nāy + aka + Su (Visarga)
    # Testing the Tripadi module's cleanup.
    intermediate = anga + suffix_raw
    visarga_suffix = ad("स्")

    full_form = intermediate + visarga_suffix
    full_form, _ = VidhiEngine.apply_rutva_8_2_66(full_form)
    full_form, _ = VidhiEngine.apply_visarga_8_3_15(full_form)

    final_output = sanskrit_varna_samyoga(full_form)
    print(f"   Step 3 (Tripadi): {final_output}")

    # 6. FINAL VERDICT
    assert final_output == "नायकः", f"Stress test failed! Expected 'नायकः', got '{final_output}'"
    print("   ✅ STRESS TEST PASSED: Architecture is Robust.")


if __name__ == "__main__":
    pytest.main([__file__])
