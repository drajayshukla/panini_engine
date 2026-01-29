# panini_engine/logic/sanjna_rules.py
import os
from core.upadesha_registry import UpadeshaType


def get_sutra_link(sutra_num):
    """Ashtadhyayi.com के लिए सटीक लिंक जेनरेट करता है।"""
    formatted_num = sutra_num.replace('.', '/')
    return f"https://ashtadhyayi.com/sutraani/{formatted_num}"


# --- १. पद संज्ञा (१.४.१४) ---

def check_pada_sanjna_1_4_14(varna_list, source_type):
    """
    संज्ञा सूत्र: सुप्तिङन्तं पदम् (१.४.१४)
    नियम: सुबन्त और तिङन्त की पद संज्ञा होती है।
    """
    if not varna_list:
        return False, "रिक्त वर्ण सूची।"

    valid_types = [UpadeshaType.VIBHAKTI, UpadeshaType.PRATYAYA]
    if source_type in valid_types:
        link = get_sutra_link("1.4.14")
        return True, f"[१.४.१४ सुप्तिङन्तं पदम्]({link}): पद संज्ञा स्वीकृत।"

    return False, "अपद: केवल प्रातिपदिक या धातु।"


# --- २. इत्-संज्ञा प्रकरण (१.३.२ - १.३.८) ---

def apply_upadeshe_ajanunasika_1_3_2(varna_list):
    """सूत्र: उपदेशेऽजनुनासिक इत् (१.३.२)"""
    it_indices, it_tags = [], []
    link = get_sutra_link("1.3.2")
    tag = f"[१.३.२ उपदेशेऽजनुनासिक इत्]({link})"

    for i, v in enumerate(varna_list):
        if v.is_anunasika:
            it_indices.append(i)
            it_tags.append(f"{v.char} {tag}")
            if i > 0 and varna_list[i - 1].is_vowel:
                it_indices.append(i - 1)
    return list(set(it_indices)), list(set(it_tags))


'''def apply_halantyam_1_3_3(varna_list, blocked_indices):
    """सूत्र: हलन्त्यम् (१.३.३)"""
    if not varna_list: return [], []
    last_idx = len(varna_list) - 1
    if last_idx in blocked_indices: return [], []

    v = varna_list[last_idx]
    is_hal = not v.is_vowel and v.char[0] not in 'ंःँ' and '्' in v.char
    if is_hal:
        link = get_sutra_link("1.3.3")
        return [last_idx], [f"[१.३.३ हलन्त्यम्]({link})"]
    return [], []'''


# Refactored 1.3.3 Hal check
def apply_halantyam_1_3_3(varna_list, blocked_indices):
    from core.sanjna_engine import SanjnaEngine  # Use our dynamic engine

    if not varna_list: return [], []
    last_idx = len(varna_list) - 1
    if last_idx in blocked_indices: return [], []

    v = varna_list[last_idx]
    # Use our Pratyahara-based Hal check
    if SanjnaEngine.is_hal(v.char):
        link = get_sutra_link("1.3.3")
        return [last_idx], [f"[१.३.३ हलन्त्यम्]({link})"]
    return [], []

def apply_na_vibhaktau_1_3_4(varna_list, source_type):
    """
    सूत्र: १.३.४ न विभक्तौ तुस्माः
    Clinical Fix: अब सीधे source_type का उपयोग करता है।
    """
    if not varna_list or source_type != UpadeshaType.VIBHAKTI:
        return []

    tu_s_m = ['त्', 'थ्', 'द्', 'ध्', 'न्', 'स्', 'म्']
    last_idx = len(varna_list) - 1
    if varna_list[last_idx].char in tu_s_m:
        return [last_idx]
    return []







def apply_adir_nitudavah_1_3_5(varna_list):
    """
    सूत्र: १.३.५ आदिर्ञिटुडवः
    नियम: धातु के आदि (शुरुआत) में स्थित 'ञि', 'टु', 'डु' की इत्-संज्ञा होती है।
    """
    # कम से कम २ वर्ण होने चाहिए (व्यंजन + स्वर)
    if len(varna_list) < 2:
        return [], []

    link = get_sutra_link("1.3.5")

    # पहले दो वर्णों के .char को मिलाकर पैटर्न बनाएं
    # उदा: 'ञ्' + 'इ' = 'ञ्इ'
    first_char = varna_list[0].char
    second_char = varna_list[1].char
    starting_pattern = first_char + second_char

    # मिलान के लिए मैप (धातु पाठ के उपदेशानुसार)
    mapping = {
        'ञ्इ': 'ञि',
        'ट्उ': 'टु',
        'ड्उ': 'डु'
    }

    if starting_pattern in mapping:
        tag = f"[१.३.५ आदिर्ञिटुडवः ({mapping[starting_pattern]})]({link})"
        # प्रथम दोनों वर्णों (व्यंजन और स्वर) की इत्-संज्ञा होगी
        return [0, 1], [tag]

    return [], []


def apply_shah_pratyayasya_1_3_6(varna_list, source_type):
    """
    सूत्र: १.३.६ षः प्रत्ययस्य
    नियम: प्रत्यय के आदि (शुरुआत) में स्थित 'ष्' की इत्-संज्ञा होती है।
    उदाहरण: 'ष्वुन्' प्रत्यय का 'ष्'।
    """
    from core.upadesha_registry import UpadeshaType

    # यह नियम केवल प्रत्यय (PRATYAYA) पर लागू होता है
    if not varna_list or source_type != UpadeshaType.PRATYAYA:
        return [], []

    # varna_list[0].char का उपयोग TypeError से बचाता है
    if varna_list[0].char == 'ष्':
        link = get_sutra_link("1.3.6")
        return [0], [f"[१.३.६ षः प्रत्ययस्य]({link})"]

    return [], []


def apply_chuttu_1_3_7(varna_list, source_type):
    """
    सूत्र: १.३.७ चुटू
    नियम: प्रत्यय के आदि में स्थित च-वर्ग (च, छ, ज, झ, ञ) और
          ट-वर्ग (ट, ठ, ड, ढ, ण) की इत्-संज्ञा होती है।
    """
    from core.upadesha_registry import UpadeshaType

    if not varna_list or source_type != UpadeshaType.PRATYAYA:
        return [], []

    # च-वर्ग और ट-वर्ग की शुद्ध व्यंजन सूची
    chuvarga = ['च्', 'छ्', 'ज्', 'झ्', 'ञ्']
    tuvarga = ['ट्', 'ठ्', 'ड्', 'ढ्', 'ण्']
    target_varnas = chuvarga + tuvarga

    # varna_list[0].char का उपयोग करें (TypeError Fix)
    if varna_list[0].char in target_varnas:
        link = get_sutra_link("1.3.7")
        return [0], [f"[१.३.७ चुटू]({link})"]

    return [], []


def apply_lashakvataddhite_1_3_8(varna_list, source_type, is_taddhita=False):
    """
    सूत्र: १.३.८ लशक्वतद्धिते
    नियम: प्रत्यय के आदि में स्थित 'ल्', 'श्' और 'कु' (क-वर्ग) की इत्-संज्ञा होती है,
          परन्तु 'तद्धित' प्रत्ययों को छोड़कर।
    """
    from core.upadesha_registry import UpadeshaType

    # १.३.८ केवल प्रत्ययों (PRATYAYA) पर लागू होता है (तद्धित वर्जित)
    if not varna_list or source_type != UpadeshaType.PRATYAYA or is_taddhita:
        return [], []

    # 'कु' (क-वर्ग), 'ल्' और 'श्' की शुद्ध व्यंजन सूची
    target = ['ल्', 'श्', 'क्', 'ख्', 'ग्', 'घ्', 'ङ्']

    # Clinical Fix: varna_list[0].char का उपयोग करें (TypeError से बचाव)
    first_varna_obj = varna_list[0]

    if first_varna_obj.char in target:
        # सूत्र लिंक और टैग
        link = get_sutra_link("1.3.8")
        tag = f"[१.३.८ लशक्वतद्धिते (आदि {first_varna_obj.char} की इत्-संज्ञा)]({link})"

        return [0], [tag]

    return [], []