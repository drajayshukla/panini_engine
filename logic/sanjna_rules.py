"""
FILE: logic/sanjna_rules.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Sanjñā-Prakaraṇam (Definitions)
"""

from core.pratyahara_engine import PratyaharaEngine
from core.upadesha_registry import UpadeshaType

# Initialize engine for query checks
pe = PratyaharaEngine()

# =============================================================================
# SECTION 1.1: Foundation Definitions (Vriddhi, Guna, Samyoga)
# =============================================================================

def apply_1_1_1_vriddhi(varna_list):
    """
    [SUTRA]: वृद्धिरादैच् (१.१.१)
    [LOGIC]: Marks 'ā', 'ai', 'au' as Vriddhi.
    """
    for v in varna_list:
        if v.char == 'आ' or pe.is_in(v.char, "ऐच्"):
            v.sanjnas.add("वृद्धि")
            v.trace.append("१.१.१ वृद्धिरादैच्")
    return varna_list

def apply_1_1_2_guna(varna_list):
    """
    [SUTRA]: अदेङ्गुणः (१.१.२)
    [LOGIC]: Marks 'a', 'e', 'o' as Guna.
    """
    for v in varna_list:
        if v.char == 'अ' or pe.is_in(v.char, "एङ्"):
            v.sanjnas.add("गुण")
            v.trace.append("१.१.२ अदेङ्गुणः")
    return varna_list

def apply_1_1_7_samyoga(varna_list):
    """
    [SUTRA]: हलोऽनन्तराः संयोगः (१.१.७)
    [LOGIC]: Marks consecutive consonants (no vowels in between) as Samyoga.
    """
    if len(varna_list) < 2:
        return varna_list

    for i in range(len(varna_list) - 1):
        curr = varna_list[i]
        nxt = varna_list[i+1]

        # Check if both are Hal (Consonants)
        if pe.is_in(curr.char, "हल्") and pe.is_in(nxt.char, "हल्"):
            # Mark both as part of a conjunct
            curr.sanjnas.add("संयोग")
            nxt.sanjnas.add("संयोग")
            # We add trace only once per pair to avoid clutter
            if "१.१.७" not in curr.trace:
                curr.trace.append("१.१.७ संयोगः")
            if "१.१.७" not in nxt.trace:
                nxt.trace.append("१.१.७ संयोगः")

    return varna_list

# =============================================================================
# SECTION 1.3: It-Sanjna (Markers) - The Diagnosis Logic
# =============================================================================

def apply_1_3_2_ajanunasika(varna_list):
    """
    [SUTRA]: उपदेशेऽजनुनासिक इत् (१.३.२)
    [LOGIC]: Returns indices of Nasal Vowels (Anunasika Ac).
    """
    indices = set()
    for i, v in enumerate(varna_list):
        if v.is_vowel and v.is_anunasika: # Relies on Varna.is_anunasika
            indices.add(i)
            v.sanjnas.add("इत्")
    return indices

def apply_1_3_3_halantyam(varna_list, blocked_indices=None):
    """
    [SUTRA]: हलन्त्यम् (१.३.३)
    [LOGIC]: The final Hal (consonant) is It.
    """
    if not varna_list: return set(), []

    last_idx = len(varna_list) - 1
    last_varna = varna_list[last_idx]

    # 1. Check Blockage (by 1.3.4 Na Vibhaktau)
    if blocked_indices and last_idx in blocked_indices:
        return set(), []

    # 2. Check if Hal
    if pe.is_in(last_varna.char, "हल्"):
        last_varna.sanjnas.add("इत्")
        return {last_idx}, ["१.३.३ हलन्त्यम्"]

    return set(), []

def apply_1_3_4_na_vibhaktau(varna_list, source_type):
    """
    [SUTRA]: न विभक्तौ तुस्माः (१.३.४)
    [LOGIC]: Returns indices that are PROTECTED from 1.3.3.
    """
    blocked = set()
    if source_type != UpadeshaType.VIBHAKTI:
        return blocked

    last_idx = len(varna_list) - 1
    char = varna_list[last_idx].char

    # Tu (t-varga), s, m
    restricted = ['त्', 'थ्', 'द्', 'ध्', 'न्', 'स्', 'म्']

    if char in restricted:
        blocked.add(last_idx)

    return blocked

def apply_1_3_5_adir_nitudavah(varna_list):
    """
    [SUTRA]: आदिर्ञिटुडवः (१.३.५)
    [LOGIC]: Initial Ñi, Ṭu, Ḍu are It.
    """
    if not varna_list: return set(), []

    first = varna_list[0]
    char = first.char

    # Yi, Tu, Du check
    targets = ['ञि', 'टु', 'डुकृ', 'डु'] # Simplified check

    # Strict check usually involves splitting 'Ñi' -> 'Ñ' + 'i'
    # Here we assume the input might be atomic or split.
    # If split: 'Ñ' is at index 0.

    indices = set()
    if char in ['ञ्', 'ट्', 'ड्']:
        # We assume the user inputs 'Ñi' as 'Ñ' + 'i'
        # If the root is 'Ñibhī', then 'Ñ' is It.
        indices.add(0)
        first.sanjnas.add("इत्")
        return indices, ["१.३.५ आदिर्ञिटुडवः"]

    return set(), []

def apply_1_3_6_shah(varna_list, source_type):
    """
    [SUTRA]: षः प्रत्ययस्य (१.३.६)
    [LOGIC]: Initial 'Ṣ' of a suffix is It.
    """
    if source_type not in [UpadeshaType.PRATYAYA, UpadeshaType.VIBHAKTI]:
        return set(), []

    if varna_list and varna_list[0].char == 'ष्':
        varna_list[0].sanjnas.add("इत्")
        return {0}, ["१.३.६ षः प्रत्ययस्य"]
    return set(), []

def apply_1_3_7_chutu(varna_list, source_type):
    """
    [SUTRA]: चुटू (१.३.७)
    [LOGIC]: Initial C-varga or Ṭ-varga of a suffix is It.
    """
    if source_type not in [UpadeshaType.PRATYAYA, UpadeshaType.VIBHAKTI]:
        return set(), []

    if not varna_list: return set(), []

    char = varna_list[0].char
    c_varga = ['च्', 'छ्', 'ज्', 'झ्', 'ञ्']
    t_varga = ['ट्', 'ठ्', 'ड्', 'ढ्', 'ण्']

    if char in c_varga or char in t_varga:
        varna_list[0].sanjnas.add("इत्")
        return {0}, ["१.३.७ चुटू"]

    return set(), []

def apply_1_3_8_lashakva(varna_list, source_type, is_taddhita=False):
    """
    [SUTRA]: लशक्वतद्धिते (१.३.८)
    [LOGIC]: Initial L, Ś, or K-varga of non-Taddhita suffix is It.
    """
    # 1. Context: Must be Pratyaya but NOT Taddhita
    if source_type not in [UpadeshaType.PRATYAYA, UpadeshaType.VIBHAKTI]:
        return set(), []
    if is_taddhita:
        return set(), []

    if not varna_list: return set(), []

    char = varna_list[0].char
    k_varga = ['क्', 'ख्', 'ग्', 'घ्', 'ङ्']
    targets = ['ल्', 'श्'] + k_varga

    if char in targets:
        varna_list[0].sanjnas.add("इत्")
        return {0}, ["१.३.८ लशक्वतद्धिते"]

    return set(), []

# =============================================================================
# SECTION 1.4: Pada & Other Designations
# =============================================================================

def apply_1_4_14_pada(varna_list):
    """
    [SUTRA]: सुप्तिङन्तं पदम् (१.४.१४)
    [LOGIC]: Assigns 'Pada' Sanjna if the word ends in Sup (Case) or Ting (Verb).
    Used to trigger 8.x.x Tripadi rules (like Rutva).
    """
    # This is usually a 'State Check'.
    # If the process has reached the end of derivation (Subanta/Tinganta),
    # the whole list is a Pada.

    # For clinical usage, we attach the tag to the LAST Varna (the Anchor).
    if varna_list:
        varna_list[-1].sanjnas.add("पद")
        varna_list[-1].trace.append("१.४.१४ सुप्तिङन्तं पदम्")
        return True, "१.४.१४ (पद-संज्ञा)"

    return False, "Not a Pada"