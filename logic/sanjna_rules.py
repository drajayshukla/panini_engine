"""
FILE: logic/sanjna_rules.py
PAS-v2.0: 5.0 (Siddha)
ORDER: Strictly Aṣṭādhyāyī Order (1.1.x -> 1.3.x -> 1.4.x)
REFERENCE: Brahmadutt Jigyasu (Prathamavritti) & Ashtadhyayi.com
"""

from core.upadesha_registry import UpadeshaType
from core.pratyahara_engine import PratyaharaEngine

# Initialize the Pratyahara Engine (Pillar: Algebra)
pe = PratyaharaEngine()


def get_sutra_link(sutra_num):
    """Generates precise documentation links for the UI."""
    return f"https://ashtadhyayi.com/sutraani/{sutra_num.replace('.', '/')}"


# =============================================================================
# CHAPTER 1, SECTION 1: Foundational Definitions (संज्ञा प्रकरण)
# =============================================================================

def apply_1_1_1_vriddhi(varna_list):
    """
    [SUTRA]: वृद्धिरादैच् (१.१.१)
    [VRITTI]: आदैच्च वृद्धिसंज्ञः स्यात्।
    """
    vriddhi_set = {"आ"}.union(set(pe.get_varnas("ऐच्")))
    for v in varna_list:
        if v.char in vriddhi_set:
            v.sanjnas.add("वृद्धि")
            v.trace.append(f"[१.१.१]({get_sutra_link('1.1.1')})")
    return varna_list


def apply_1_1_2_guna(varna_list):
    """
    [SUTRA]: अदेङ्गुणः (१.१.२)
    [VRITTI]: अत एङ् च गुणसंज्ञः स्यात्।
    """
    guna_set = {"अ"}.union(set(pe.get_varnas("एङ्")))
    for v in varna_list:
        if v.char in guna_set:
            v.sanjnas.add("गुण")
            v.trace.append(f"[१.१.२]({get_sutra_link('1.1.2')})")
    return varna_list


def apply_1_1_7_samyoga(varna_list):
    """
    [SUTRA]: हलोऽनन्तराः संयोगः (१.१.७)
    [VRITTI]: अज्भिरव्यवहिता हलः संयोगसंज्ञाः स्युः।
    """
    for i in range(len(varna_list)):
        if not varna_list[i].is_vowel:
            prev_hal = i > 0 and not varna_list[i - 1].is_vowel
            next_hal = i < len(varna_list) - 1 and not varna_list[i + 1].is_vowel
            if prev_hal or next_hal:
                varna_list[i].sanjnas.add("संयोग")
                varna_list[i].trace.append(f"[१.१.७]({get_sutra_link('1.1.7')})")
    return varna_list


# =============================================================================
# CHAPTER 1, SECTION 3: It-Markers (इत्-संज्ञा प्रकरण)
# =============================================================================

def apply_1_3_2_ajanunasika(varna_list):
    """[SUTRA]: उपदेशेऽजनुनासिक इत् (१.३.२)"""
    it_indices = []
    for i, v in enumerate(varna_list):
        if v.is_anunasika:
            it_indices.append(i)
            # If the nasal marker is on a vowel, both are marked (Anuvritti logic)
            if i > 0 and varna_list[i - 1].is_vowel:
                it_indices.append(i - 1)
    return list(set(it_indices))


def apply_1_3_3_halantyam(varna_list, blocked_indices=None):
    """
    [SUTRA]: हलन्त्यम् (१.३.३)
    Logic: Final consonant in Upadesha is 'It'. 
    """
    if not varna_list: return []
    blocked = blocked_indices or []
    last_idx = len(varna_list) - 1

    if last_idx in blocked: return []

    # Pillar: Pratyahara (Checking if it's a 'Hal')
    if varna_list[last_idx].char in pe.get_varnas("हल्"):
        return [last_idx]
    return []


def apply_1_3_4_na_vibhaktau(varna_list, source_type):
    """[SUTRA]: न विभक्तौ तुस्माः (१.३.४) - Exception to 1.3.3"""
    if source_type != UpadeshaType.VIBHAKTI or not varna_list:
        return []

    last_char = varna_list[-1].char
    tu_s_m = pe.get_varnas("तु") + ['स्', 'म्']  # 'tu' = t, th, d, dh, n
    if last_char in tu_s_m:
        return [len(varna_list) - 1]
    return []


def apply_1_3_5_adir_nitudavah(varna_list):
    """[SUTRA]: आदिर्ञिटुडवः (१.३.५) - Initial markers in Dhatu"""
    if len(varna_list) < 2: return []

    # Logic: Joining chars to match Upadesha patterns like 'ञि', 'टु', 'डु'
    start = varna_list[0].char + varna_list[1].char
    if start in ['ञ्इ', 'ट्उ', 'ड्उ']:
        return [0, 1]
    return []


def apply_1_3_8_lashakva(varna_list, source_type, is_taddhita=False):
    """[SUTRA]: लशक्वतद्धिते (१.३.८)"""
    if source_type != UpadeshaType.PRATYAYA or is_taddhita:
        return []

    first = varna_list[0].char
    # 'ku' = k, kh, g, gh, n
    targets = ['ल्', 'श्'] + pe.get_varnas("कु")
    if first in targets:
        return [0]
    return []


# =============================================================================
# CHAPTER 1, SECTION 4: Pada Definitions
# =============================================================================

def apply_1_4_14_pada(varna_list, source_type):
    """[SUTRA]: सुप्तिङन्तं पदम् (१.४.१४)"""
    # Logic: If derivation has reached a final Vibhakti/Pratyaya stage
    if source_type in [UpadeshaType.VIBHAKTI, UpadeshaType.PRATYAYA]:
        return True
    return False