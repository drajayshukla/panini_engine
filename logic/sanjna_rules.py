"""
FILE: logic/sanjna_rules.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Sanjñā-Prakaraṇam (Definitions)
UPDATED: 1.3.5 now correctly removes both parts of split markers (e.g., T+u).
"""

from core.pratyahara_engine import PratyaharaEngine
from core.upadesha_registry import UpadeshaType

# Initialize engine for query checks
pe = PratyaharaEngine()


# =============================================================================
# SECTION 1.1: Foundation Definitions
# =============================================================================

def apply_1_1_1_vriddhi(varna_list):
    """[SUTRA]: वृद्धिरादैच् (१.१.१)"""
    for v in varna_list:
        if v.char == 'आ' or pe.is_in(v.char, "ऐच्"):
            v.sanjnas.add("वृद्धि")
            v.trace.append("१.१.१ वृद्धिरादैच्")
    return varna_list


def apply_1_1_2_guna(varna_list):
    """[SUTRA]: अदेङ्गुणः (१.१.२)"""
    for v in varna_list:
        if v.char == 'अ' or pe.is_in(v.char, "एङ्"):
            v.sanjnas.add("गुण")
            v.trace.append("१.१.२ अदेङ्गुणः")
    return varna_list


def apply_1_1_7_samyoga(varna_list):
    """[SUTRA]: हलोऽनन्तराः संयोगः (१.१.७)"""
    if len(varna_list) < 2: return varna_list

    for i in range(len(varna_list) - 1):
        curr = varna_list[i]
        nxt = varna_list[i + 1]
        if pe.is_in(curr.char, "हल्") and pe.is_in(nxt.char, "हल्"):
            curr.sanjnas.add("संयोग")
            nxt.sanjnas.add("संयोग")
            if "१.१.७" not in curr.trace: curr.trace.append("१.१.७ संयोगः")
            if "१.१.७" not in nxt.trace: nxt.trace.append("१.१.७ संयोगः")
    return varna_list


def is_sarvanama_1_1_27(word_str):
    """[SUTRA]: सर्वादीनि सर्वनामानि (१.१.२७)"""
    sarvadi_gana = {
        "सर्व", "विश्व", "उभ", "उभय", "डतर", "डतम", "अन्य", "अन्यतर",
        "इतर", "त्वत्", "त्व", "नेम", "सम", "सिम", "पूर्व", "पर",
        "अवर", "दक्षिण", "उत्तर", "अपर", "अधर", "स्व", "अन्तर",
        "त्यद्", "तद्", "यद्", "एतद्", "इदम्", "अदस्", "एक", "द्वि",
        "युष्मद्", "अस्मद्", "भवतु", "किम्"
    }
    return word_str in sarvadi_gana


# =============================================================================
# SECTION 1.3: It-Sanjna (Markers)
# =============================================================================

def apply_1_3_2_ajanunasika(varna_list):
    """
    [SUTRA]: उपदेशेऽजनुनासिक इत् (१.३.२)
    """
    indices = set()
    for i, v in enumerate(varna_list):
        # Case A: Standalone Nasal Markers
        if v.char in ['ँ', 'ं']:
            indices.add(i)
            v.sanjnas.add("इत्")
            v.trace.append("१.३.२ (Nasal Symbol)")

            # Remove Preceding Vowel
            if i > 0:
                prev_v = varna_list[i - 1]
                if prev_v.is_vowel:
                    indices.add(i - 1)
                    prev_v.sanjnas.add("इत्")
                    prev_v.trace.append("१.३.२ (Nasalized Vowel)")
            continue

        # Case B: Vowel with internal nasal property
        if v.is_vowel and getattr(v, 'is_anunasika', False):
            indices.add(i)
            v.sanjnas.add("इत्")
            v.trace.append("१.३.२ (Nasal Vowel)")

    return indices


def apply_1_3_3_halantyam(varna_list, blocked_indices=None):
    """[SUTRA]: हलन्त्यम् (१.३.३)"""
    if not varna_list: return set(), []
    last_idx = len(varna_list) - 1
    if blocked_indices and last_idx in blocked_indices:
        return set(), []

    last_varna = varna_list[last_idx]
    if last_varna.is_consonant:
        last_varna.sanjnas.add("इत्")
        return {last_idx}, ["१.३.३ हलन्त्यम्"]
    return set(), []


def apply_1_3_4_na_vibhaktau(varna_list, source_type):
    """[SUTRA]: न विभक्तौ तुस्माः (१.३.४)"""
    blocked = set()
    if source_type != UpadeshaType.VIBHAKTI: return blocked
    last_idx = len(varna_list) - 1
    if last_idx < 0: return blocked

    char = varna_list[last_idx].char
    restricted = ['त्', 'थ्', 'द्', 'ध्', 'न्', 'स्', 'म्']
    if char in restricted: blocked.add(last_idx)
    return blocked


def apply_1_3_5_adir_nitudavah(varna_list):
    """
    [SUTRA]: आदिर्ञिटुडवः (१.३.५)
    [FIX]: Now correctly removes the VOWEL component of the marker as well.
    """
    if not varna_list: return set(), []
    indices = set()
    trace = []
    first = varna_list[0]

    # 1. Atomic Check (If input is 'Ñi' as one unit)
    if first.char in ['ञि', 'टु', 'डु', 'डुकृ']:
        indices.add(0)
        first.sanjnas.add("इत्")
        trace.append(f"१.३.५ आदिर्ञिटुडवः ({first.char})")
        return indices, trace

    # 2. Split Sequence Check (Your Vichhed Logic)
    if len(varna_list) > 1:
        second = varna_list[1]

        # Ñ + i
        if first.char == 'ञ्' and second.char == 'इ':
            indices.add(0)
            indices.add(1)  # Mark 'i' too
            first.sanjnas.add("इत्")
            second.sanjnas.add("इत्")
            trace.append("१.३.५ आदिर्ञिटुडवः (Initial Ñi)")

        # Ṭ + u
        elif first.char == 'ट्' and second.char == 'उ':
            indices.add(0)
            indices.add(1)  # Mark 'u' too
            first.sanjnas.add("इत्")
            second.sanjnas.add("इत्")
            trace.append("१.३.५ आदिर्ञिटुडवः (Initial Ṭu)")

        # Ḍ + u
        elif first.char == 'ड्' and second.char == 'उ':
            indices.add(0)
            indices.add(1)  # Mark 'u' too
            first.sanjnas.add("इत्")
            second.sanjnas.add("इत्")
            trace.append("१.३.५ आदिर्ञिटुडवः (Initial Ḍu)")

    return indices, trace


def apply_1_3_6_shah(varna_list, source_type):
    """[SUTRA]: षः प्रत्ययस्य (१.३.६)"""
    if source_type not in [UpadeshaType.PRATYAYA, UpadeshaType.VIBHAKTI]: return set(), []
    if varna_list and varna_list[0].char == 'ष्':
        varna_list[0].sanjnas.add("इत्")
        return {0}, ["१.३.६ षः प्रत्ययस्य"]
    return set(), []


def apply_1_3_7_chutu(varna_list, source_type):
    """[SUTRA]: चुटू (१.३.७)"""
    if source_type not in [UpadeshaType.PRATYAYA, UpadeshaType.VIBHAKTI]: return set(), []
    if not varna_list: return set(), []
    char = varna_list[0].char
    c_varga = ['च्', 'छ्', 'ज्', 'झ्', 'ञ्']
    t_varga = ['ट्', 'ठ्', 'ड्', 'ढ्', 'ण्']
    if char in c_varga or char in t_varga:
        varna_list[0].sanjnas.add("इत्")
        return {0}, ["१.३.७ चुटू"]
    return set(), []


def apply_1_3_8_lashakva(varna_list, source_type, is_taddhita=False):
    """[SUTRA]: लशक्वतद्धिते (१.३.८)"""
    if source_type not in [UpadeshaType.PRATYAYA, UpadeshaType.VIBHAKTI]: return set(), []
    if is_taddhita: return set(), []
    if not varna_list: return set(), []
    char = varna_list[0].char
    targets = ['ल्', 'श्', 'क्', 'ख्', 'ग्', 'घ्', 'ङ्']
    if char in targets:
        varna_list[0].sanjnas.add("इत्")
        return {0}, ["१.३.8 लशक्वतद्धिते"]
    return set(), []


# =============================================================================
# SECTION 1.4: Morphology Helpers
# =============================================================================

def is_nadi_1_4_3(varna_list):
    if not varna_list: return False
    return varna_list[-1].char in ['ई', 'ऊ']


def is_ghi_1_4_7(varna_list):
    if not varna_list: return False
    return varna_list[-1].char in ['इ', 'उ']


def check_pada_sanjna_1_4_14(varna_list, source_type):
    """[SUTRA]: सुप्तिङन्तं पदम् (१.४.१४)"""
    is_pada = False
    msg = ""
    if source_type == UpadeshaType.VIBHAKTI:
        is_pada = True
        msg = "१.४.१४ (सुबन्तम्)"
    return is_pada, msg


apply_1_4_14_pada = check_pada_sanjna_1_4_14


def is_bha_1_4_18(varna_list, suffix_varna_list):
    """[SUTRA]: यचि भम् (१.४.१८)"""
    if not suffix_varna_list: return False
    first_char = suffix_varna_list[0].char
    is_y_or_ac = first_char == 'य्' or pe.is_in(first_char, "अच्")
    if is_y_or_ac: return True
    return False