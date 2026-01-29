"""
FILE: logic/stem_classifier.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Classification (Anga Type)
UPDATED: Uses Varna properties and Halant-aware checks.
"""

from core.pratyahara_engine import PratyaharaEngine
from core.phonology import Varna
from core.paribhasha_manager import ParibhashaManager  # Added Missing Import

pe = PratyaharaEngine()


# --- HELPER FOR VOWEL LENGTHENING ---
def _transform_to_dirgha(varna_obj, rule_code):
    """
    Mutates the varna object to its long form.
    Used by 6.4.8 (Upadha Dirgha) etc.
    """
    map_dirgha = {
        'अ': 'आ',
        'इ': 'ई',
        'उ': 'ऊ',
        'ऋ': 'ॠ',
        'ऌ': 'ॡ'
    }
    if varna_obj.char in map_dirgha:
        old = varna_obj.char
        varna_obj.char = map_dirgha[varna_obj.char]
        varna_obj.sanjnas.add("दीर्घ")
        varna_obj.trace.append(f"{rule_code} ({old}->{varna_obj.char})")


def is_halanta(anga):
    """
    Checks if the Anga ends in a Consonant (Hal).
    """
    if not anga: return False
    last = anga[-1]

    # 1. Use the Varna Property (Safest - from user logic)
    if hasattr(last, 'is_consonant'):
        return last.is_consonant

    # 2. Fallback: Pratyahara Check
    return pe.is_in(last.char, "हल्")


def is_ajanta(anga):
    """
    Checks if the Anga ends in a Vowel (Ac).
    """
    if not anga: return False
    last = anga[-1]

    # 1. Use Varna Property
    if hasattr(last, 'is_vowel'):
        return last.is_vowel

    # 2. Fallback
    return pe.is_in(last.char, "अच्")


def ends_in_short_a(anga):
    """
    Checks if Anga ends in short 'a' (अ).
    """
    if not anga: return False
    return anga[-1].char == 'अ'


def classify_stem(anga):
    """
    Returns a descriptor dictionary for the stem.
    """
    return {
        "is_halanta": is_halanta(anga),
        "is_ajanta": is_ajanta(anga),
        "last_char": anga[-1].char if anga else None
    }


def apply_6_4_3_nami(anga_varnas, nimitta_text):
    """
    [SUTRA]: नामि (६.४.३)
    [LOGIC]: If the suffix is 'nām' (Nut-Agama + Am), lengthen the stem's final vowel.
    Example: vāri + nām -> vārīnām
    """
    # Check Context
    if nimitta_text != "नाम्":
        return anga_varnas

    # Target: Aṅga-Antya (Final Vowel)
    if not anga_varnas: return anga_varnas

    antya_varna = anga_varnas[-1]

    if antya_varna.is_vowel:
        _transform_to_dirgha(antya_varna, "६.४.३ नामि")

    return anga_varnas


def apply_6_4_8_sarvanamasthane(anga_varnas, is_sarvanamasthana, is_sambuddhi):
    """
    [SUTRA]: सर्वनामस्थाने चासम्बुद्धौ (६.४.८)
    [CONTEXT]: Follows 6.4.7 'Nopadhayah' (Stems ending in 'n').
    [LOGIC]: Lengthen the PENULTIMATE (Upadha) vowel if followed by strong suffix.
    Example: rājan + au -> rājānau
    """
    if not is_sarvanamasthana or is_sambuddhi:
        return anga_varnas

    # 1. Check strict condition: Stem must end in 'n' (Nopadhayah context)
    if not anga_varnas or anga_varnas[-1].char != 'न्':
        return anga_varnas

    # 2. Identify Upadha (Penultimate)
    upadha_varna, idx = ParibhashaManager.get_upadha_1_1_65(anga_varnas)

    if upadha_varna and upadha_varna.is_vowel:
        _transform_to_dirgha(upadha_varna, "६.४.८ सर्वनामस्थाने...")

    return anga_varnas


def apply_6_4_11_aptunvrich(anga_varnas, is_sarvanamasthana):
    """
    [SUTRA]: अप्तृन्वृच्... (६.४.११)
    [LOGIC]: Specific list of stems get Upadha-Dirgha in Sarvanamasthana.
    Example: swasṛ -> swasār (Logic assumes Guna happened previously to make it 'ar')
    """
    if not is_sarvanamasthana:
        return anga_varnas

    # Check Stem Identity (This would ideally use the PratipadikaEngine metadata)
    # For now, we reconstruct the string to check against the list
    text_stem = "".join([v.char.replace('्', '') for v in anga_varnas])

    # Target list (simplified checks for transformed Guna forms)
    # Note: In strict Prakriya, 6.4.11 runs AFTER Guna (7.3.110).
    # So 'swasṛ' becomes 'swasar'. Then 6.4.11 lengthens the 'a' in 'ar'.

    targets = ["स्वसर्", "नप्तर्", "नेष्टर्", "त्वष्टर्", "क्षत्तर्", "होत्र्", "पोत्र्", "प्रशास्तर्"]

    if any(text_stem.endswith(t) for t in targets):
        upadha_varna, _ = ParibhashaManager.get_upadha_1_1_65(anga_varnas)
        if upadha_varna and upadha_varna.char == 'अ':
            _transform_to_dirgha(upadha_varna, "६.४.११ अप्तृन्वृच्...")

    return anga_varnas