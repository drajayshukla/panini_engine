"""
FILE: logic/sanjna_rules.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Sanjñā-Prakaraṇam (Definitions)
EXPANDED: Includes 1.1 (General), 1.3 (It-Markers), and 1.4 (Morphology)
"""

from core.pratyahara_engine import PratyaharaEngine
from core.upadesha_registry import UpadeshaType

# Initialize engine for query checks
pe = PratyaharaEngine()

# =============================================================================
# SECTION 1.1: Foundation Definitions (Vriddhi, Guna, Samyoga, Sarvanama)
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

def is_sarvanama_1_1_27(word_str):
    """
    [SUTRA]: सर्वादीनि सर्वनामानि (१.१.२७)
    [LOGIC]: Checks against the Sarvadi Gana (List of Pronouns).
    """
    # In a full production app, load 'ganapatha.json'.
    # For now, we hardcode the most common ones for Subanta.
    sarvadi_gana = {
        "सर्व", "विश्व", "उभ", "उभय", "डतर", "डतम", "अन्य", "अन्यतर",
        "इतर", "त्वत्", "त्व", "नेम", "सम", "सिम", "पूर्व", "पर",
        "अवर", "दक्षिण", "उत्तर", "अपर", "अधर", "स्व", "अन्तर",
        "त्यद्", "तद्", "यद्", "एतद्", "इदम्", "अदस्", "एक", "द्वि",
        "युष्मद्", "अस्मद्", "भवतु", "किम्"
    }
    return word_str in sarvadi_gana

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
    # Strict check usually involves splitting 'Ñi' -> 'Ñ' + 'i'

    indices = set()
    if char in ['ञ्', 'ट्', 'ड्']:
        # We assume the user inputs 'Ñi' as 'Ñ' + 'i'
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
# SECTION 1.4: Morphological Definitions (Nadi, Ghi, Bha, Pada)
# =============================================================================

def is_nadi_1_4_3(varna_list):
    """
    [SUTRA]: यू स्त्र्याख्यौ नदी (१.४.३)
    [LOGIC]: Long 'ī' and 'ū' ending feminine words are Nadi.
    Example: 'Nadi', 'Vadhu'.
    """
    if not varna_list: return False
    last_char = varna_list[-1].char
    # Check 1: Must end in Long I or Long U
    if last_char not in ['ई', 'ऊ']:
        return False
    # Check 2: Must be Feminine (Simplistic check for now)
    return True

def is_ghi_1_4_7(varna_list):
    """
    [SUTRA]: शेषो घ्यसखि (१.४.७)
    [LOGIC]: Short 'i' and 'u' ending words (except Sakhi) are Ghi.
    Example: 'Mati', 'Bhanu'.
    """
    if not varna_list: return False

    word_str = "".join([v.char for v in varna_list])
    if word_str == "सखि": return False # Exception

    last_char = varna_list[-1].char
    if last_char in ['इ', 'उ']:
        return True
    return False

def check_pada_sanjna_1_4_14(varna_list, source_type):
    """
    [SUTRA]: सुप्तिङन्तं पदम् (१.४.१४)
    [LOGIC]: Ends in Sup (Case) or Ting (Verb).
    """
    is_pada = False
    msg = ""

    if source_type == UpadeshaType.VIBHAKTI:
        is_pada = True
        msg = "१.४.१४ (सुबन्तम्)"
    return is_pada, msg

# Alias for compatibility with other files (FIXES IMPORT ERROR)
apply_1_4_14_pada = check_pada_sanjna_1_4_14

def is_bha_1_4_18(varna_list, suffix_varna_list):
    """
    [SUTRA]: यचि भम् (१.४.१८)
    [LOGIC]: Stem is 'Bha' before a suffix starting with 'Y' or 'Ac'.
    """
    if not suffix_varna_list: return False
    first_char = suffix_varna_list[0].char

    # Check: Starts with Y or Vowel?
    is_y_or_ac = first_char == 'य्' or pe.is_in(first_char, "अच्")

    if is_y_or_ac:
        return True
    return False