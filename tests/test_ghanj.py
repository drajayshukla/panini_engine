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
