"""
FILE: logic/stem_classifier.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Aṅga-Kārya (Stem Modification)
REFERENCE: ६.४.१ अङ्गस्य अधिकार
"""

from core.paribhasha_manager import ParibhashaManager

# Mapping for Vidhi (Transformation)
SHORT_TO_LONG = {
    'अ': 'आ', 'इ': 'ई', 'उ': 'ऊ', 'ऋ': 'ॠ', 'ऌ': 'ॡ',
    'ा': 'आ', 'ि': 'ई', 'ु': 'ऊ', 'ृ': 'ॠ'  # Matra forms
}


def _transform_to_dirgha(varna_obj, sutra_ref):
    """
    [HELPER]: Physically transforms a short vowel to long (Vidhi).
    """
    if varna_obj.char in SHORT_TO_LONG:
        old_char = varna_obj.char
        varna_obj.char = SHORT_TO_LONG[old_char]
        varna_obj.matra = 2
        varna_obj.sanjnas.add("दीर्घ")
        varna_obj.trace.append(f"{sutra_ref}: {old_char} -> {varna_obj.char}")
        return True
    return False


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
    # Use AngaEngine logic (last element)
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

    # Target list (simplified)
    targets = ["स्वसृ", "नप्तृ", "नेष्टृ", "त्वष्टृ", "क्षत्तृ", "होतृ", "पोतृ", "प्रशास्तृ"]

    # Note: In strict Prakriya, 6.4.11 runs AFTER Guna (7.3.110).
    # So 'swasṛ' becomes 'swasar'. Then 6.4.11 lengthens the 'a' in 'ar'.

    if any(text_stem.endswith(t) for t in ["स्वसर्", "नप्तर्", "नेष्टर्"]):  # Checking Guna form
        upadha_varna, _ = ParibhashaManager.get_upadha_1_1_65(anga_varnas)
        if upadha_varna and upadha_varna.char == 'अ':
            _transform_to_dirgha(upadha_varna, "६.४.११ अप्तृन्वृच्...")

    return anga_varnas