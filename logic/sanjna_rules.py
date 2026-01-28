import os


def get_sutra_link(sutra_num):
    """Ashtadhyayi.com के लिए सटीक लिंक जेनरेट करता है।"""
    formatted_num = sutra_num.replace('.', '/')
    return f"https://ashtadhyayi.com/sutraani/{formatted_num}"


# --- १.१.१ वृद्धि और १.१.२ गुण संज्ञा (Analysis Only) ---

def check_vriddhi_1_1_1(varna_obj):
    """१.१.१ वृद्धिरादैच्: आ, ऐ, औ की वृद्धि संज्ञा।"""
    vriddhi_letters = ['आ', 'ऐ', 'औ']

    # varna_obj.char का उपयोग करें
    if varna_obj.char in vriddhi_letters:
        link = get_sutra_link("1.1.1")
        return f"[वृद्धि (१.१.१)]({link})"
    return None


def check_guna_1_1_2(varna_obj):
    """१.१.२ अदेङ् गुणः: अ (ह्रस्व), ए, ओ की गुण संज्ञा।"""
    guna_letters = ['अ', 'ए', 'ओ']

    # पाणिनीय सूक्ष्मता: केवल ह्रस्व 'अ' ही गुण है।
    # varna_obj.matra == 1 सुनिश्चित करता है कि 'आ' गुण न कहलाए।
    if varna_obj.char in guna_letters:
        if varna_obj.char == 'अ' and varna_obj.matra != 1:
            return None

        link = get_sutra_link("1.1.2")
        return f"[गुण (१.१.२)]({link})"
    return None
# --- १.३.२ से १.३.८ इत्-संज्ञा प्रकरण (Tagging Model) ---

def apply_upadeshe_ajanunasika_1_3_2(varna_list):
    """
    सूत्र: उपदेशेऽजनुनासिक इत् (१.३.२)
    एकीकृत लॉजिक: Varna ऑब्जेक्ट्स का उपयोग करते हुए अनुनासिक अच् की इत्-संज्ञा।
    """
    it_indices = []
    it_tags = []

    # सूत्र लिंक और टैग (पुराने फंक्शन से सुरक्षित)
    # यदि get_sutra_link उपलब्ध नहीं है, तो सामान्य स्ट्रिंग का प्रयोग करें
    try:
        from utils.links import get_sutra_link
        link = get_sutra_link("1.3.2")
        tag = f"[१.३.२ उपदेशेऽजनुनासिक इत्]({link})"
    except ImportError:
        tag = "१.३.२ उपदेशेऽजनुनासिक इत्"

    for i, v in enumerate(varna_list):
        # चूंकि 'v' एक Varna ऑब्जेक्ट है, हम सीधे .is_anunasika चेक करेंगे
        if v.is_anunasika:
            # १. वर्तमान अनुनासिक चिह्न की इत्-संज्ञा
            it_indices.append(i)
            it_tags.append(f"{v.char} {tag}")

            # २. पाणिनीय बॉन्डिंग (Legacy Logic Preservation):
            # यदि पिछला वर्ण अच् (vowel) है, तो वह भी इत् संज्ञक होगा
            if i > 0 and varna_list[i - 1].is_vowel:
                it_indices.append(i - 1)

    # list(set()) का उपयोग करके duplicate indices हटाना (पुराने कोड की तरह)
    return list(set(it_indices)), list(set(it_tags))


def apply_halantyam_1_3_3(varna_list, blocked_indices):
    """
    सूत्र: हलन्त्यम् (१.३.३)
    संशोधित लॉजिक: केवल तभी लागू होगा जब अन्तिम वर्ण शुद्ध व्यंजन (हल्) हो।
    """
    if not varna_list:
        return [], []

    last_idx = len(varna_list) - 1

    # १. सुरक्षा कवच (१.३.४ न विभक्तौ तुस्माः) की जाँच
    if last_idx in blocked_indices:
        return [], []

    v = varna_list[last_idx]

    # २. पाणिनीय फिल्टर: क्या यह 'हल्' (व्यंजन) है?
    # स्वर (v.is_vowel) और अनुनासिक/अयोगवाह (ँ, ं, ः) पर १.३.३ लागू नहीं होता।
    is_hal = not v.is_vowel and v.char[0] not in 'ंःँ' and '्' in v.char

    if is_hal:
        return [last_idx], ["१.३.३ हलन्त्यम्"]

    return [], []
def apply_na_vibhaktau_1_3_4(varna_list, is_vibhakti=True):
    """
    सूत्र: १.३.४ न विभक्तौ तुस्माः
    नियम: यदि उपदेश एक 'विभक्ति' है, तो उसके अंत में स्थित 'तु' (त-वर्ग),
          'स्' और 'म्' की इत्-संज्ञा (१.३.३ द्वारा) नहीं होती।
    """
    if not varna_list or not is_vibhakti:
        return []

    # १. अंतिम वर्ण की पहचान (Varna Object)
    last_idx = len(varna_list) - 1
    last_varna_obj = varna_list[last_idx]

    # २. 'तु' (त-वर्ग), 'स्', 'म्' की पहचान सूची
    # ध्यान दें: हम यहाँ शुद्ध व्यंजन (क्लीन कैरेक्टर) देख रहे हैं
    tu_s_m = ['त्', 'थ्', 'द्', 'ध्', 'न्', 'स्', 'म्']

    # ३. जाँच: क्या अंतिम वर्ण का मूल रूप इस लिस्ट में है?
    # last_varna_obj.char का उपयोग TypeError से बचाता है
    if last_varna_obj.char in tu_s_m:
        # यह इंडेक्स १.३.३ (हलन्त्यम्) के लिए 'Blocked' माना जाएगा
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