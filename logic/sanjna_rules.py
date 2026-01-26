import os


def get_sutra_link(sutra_num):
    """Ashtadhyayi.com के लिए सटीक लिंक जेनरेट करता है।"""
    formatted_num = sutra_num.replace('.', '/')
    return f"https://ashtadhyayi.com/sutraani/{formatted_num}"


# --- १.१.१ वृद्धि और १.१.२ गुण संज्ञा (No deletion needed) ---

def check_vriddhi_1_1_1(varna):
    vriddhi_letters = ['आ', 'ऐ', 'औ']
    if varna in vriddhi_letters:
        link = get_sutra_link("1.1.1")
        return f"[वृद्धि (१.१.१)]({link})"
    return None


def check_guna_1_1_2(varna):
    guna_letters = ['अ', 'ए', 'ओ']
    if varna in guna_letters:
        link = get_sutra_link("1.1.2")
        return f"[गुण (१.१.२)]({link})"
    return None


# --- १.३.२ से १.३.८ इत्-संज्ञा प्रकरण (अब केवल Tagging करेंगे) ---

def apply_upadeshe_ajanunasika_1_3_2(varna_list):
    """
    १.३.२: अनुनासिक स्वर की इत्-संज्ञा।
    अब यह वर्ण हटाता नहीं है, केवल प्रभावित indices और tags लौटता है।
    """
    ach_list = set('अआइईउऊऋॠऌॡएऐओऔ')
    it_indices = []
    it_tags = []
    link = get_sutra_link("1.3.2")
    tag = f"[१.३.२ उपदेशेऽजनुनासिक इत्]({link})"

    for i, v in enumerate(varna_list):
        # यदि अनुनासिक चिन्ह मिले
        if 'ँ' in v or v == 'ँ':
            it_indices.append(i)
            it_tags.append(tag)
            # पाणिनीय बॉन्डिंग: यदि पिछला वर्ण स्वर (Ach) है, तो वह भी इत् है
            if i > 0 and varna_list[i - 1] in ach_list:
                it_indices.append(i - 1)

    return list(set(it_indices)), list(set(it_tags))


def apply_halantyam_1_3_3(varna_list, original_word, is_vibhakti=False):
    """१.३.३: अन्त्य हल् की इत्-संज्ञा।"""
    if not varna_list: return [], []

    last_idx = len(varna_list) - 1
    last_varna = varna_list[last_idx]

    if last_varna.endswith('्'):
        # १.३.४ न विभक्तौ तुस्माः (प्रतिषेध)
        tusma = ['त्', 'थ्', 'द्', 'ध्', 'न्', 'स्', 'म्']
        if is_vibhakti and last_varna in tusma:
            link = get_sutra_link("1.3.4")
            return [], [f"[१.३.४ न विभक्तौ तुस्माः (प्रतिषेध)]({link})"]

        link = get_sutra_link("1.3.3")
        return [last_idx], [f"[१.३.३ हलन्त्यम्]({link})"]
    return [], []


def apply_adir_nitudavah_1_3_5(varna_list):
    """१.३.५: आदि ञि, टु, डु की इत्-संज्ञा।"""
    if len(varna_list) < 2: return [], []

    link = get_sutra_link("1.3.5")
    # 'ञ्' + 'इ' = 'ञि'
    starting_pattern = varna_list[0] + varna_list[1]
    mapping = {'ञ्इ': 'ञि', 'ट्उ': 'टु', 'ड्उ': 'डु'}

    if starting_pattern in mapping:
        return [0, 1], [f"[१.३.५ आदिर्ञिटुडवः ({mapping[starting_pattern]})]({link})"]
    return [], []


def apply_shah_pratyayasya_1_3_6(varna_list):
    """१.३.६: प्रत्यय के आदि 'ष्' की इत्-संज्ञा।"""
    if varna_list and varna_list[0] == 'ष्':
        link = get_sutra_link("1.3.6")
        return [0], [f"[१.३.६ षः प्रत्ययस्य]({link})"]
    return [], []


def apply_chuttu_1_3_7(varna_list, source_type):
    """
    सूत्र: १.३.७ चुट्टू
    नियम: प्रत्यय के आदि (initial) में स्थित च-वर्ग या ट-वर्ग की इत्-संज्ञा होती है।
    """
    # १. सुरक्षा जाँच: यदि लिस्ट खाली है या उपदेश 'प्रत्यय' नहीं है, तो नियम लागू न करें
    # धातु के आदि में 'चु' या 'टु' होने पर इत्-संज्ञा नहीं होती (जैसे 'च्यु' धातु)
    from core.upadesha_registry import UpadeshaType
    if not varna_list or source_type != UpadeshaType.PRATYAYA:
        return [], []

    # २. च-वर्ग (चु) और ट-वर्ग (टू) की सूची
    chuvarga = ['च्', 'छ्', 'ज्', 'झ्', 'ञ्']
    tuvarga = ['ट्', 'ठ्', 'ड्', 'ढ्', 'ण्']
    target_varnas = chuvarga + tuvarga

    # ३. 'आदि' (Index 0) वर्ण की जाँच
    first_varna = varna_list[0]

    if first_varna in target_varnas:
        link = get_sutra_link("1.3.7")
        # index 0 को इत् मार्क करें और टैग लौटाएं
        return [0], [f"[१.३.७ चुट्टू]({link})"]

    return [], []

def apply_lashakvataddhite_1_3_8(varna_list, is_taddhita=False):
    """१.३.८: प्रत्यय के आदि ल, श, कु की इत्-संज्ञा।"""
    if not varna_list or is_taddhita: return [], []
    kavarga = ['क्', 'ख्', 'ग्', 'घ्', 'ङ्']
    target = ['ल्', 'श्'] + kavarga
    if varna_list[0] in target:
        link = get_sutra_link("1.3.8")
        return [0], [f"[१.३.८ लशक्वतद्धिते]({link})"]
    return [], []