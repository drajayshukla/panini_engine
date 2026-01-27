import os


def get_sutra_link(sutra_num):
    """Ashtadhyayi.com के लिए सटीक लिंक जेनरेट करता है।"""
    formatted_num = sutra_num.replace('.', '/')
    return f"https://ashtadhyayi.com/sutraani/{formatted_num}"


# --- १.१.१ वृद्धि और १.१.२ गुण संज्ञा (Analysis Only) ---

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


# --- १.३.२ से १.३.८ इत्-संज्ञा प्रकरण (Tagging Model) ---

def apply_upadeshe_ajanunasika_1_3_2(varna_list):
    """१.३.२: अनुनासिक स्वर की इत्-संज्ञा।"""
    ach_list = set('अआइईउऊऋॠऌॡएऐओऔ')
    it_indices = []
    it_tags = []
    link = get_sutra_link("1.3.2")
    tag = f"[१.३.२ उपदेशेऽजनुनासिक इत्]({link})"

    for i, v in enumerate(varna_list):
        if 'ँ' in v or v == 'ँ':
            it_indices.append(i)
            it_tags.append(tag)
            # पाणिनीय बॉन्डिंग: यदि पिछला वर्ण अच् है
            if i > 0 and varna_list[i - 1] in ach_list:
                it_indices.append(i - 1)

    return list(set(it_indices)), list(set(it_tags))


def apply_halantyam_1_3_3(varna_list, original_word, source_type):
    """
    सूत्र: १.३.३ हलन्त्यम् + १.३.४ न विभक्तौ तुस्माः
    नियम: यदि उपदेश 'विभक्ति' है और अंत में 'त-वर्ग, स्, म' है, तो लोप नहीं होगा।
    """
    from core.upadesha_registry import UpadeshaType
    if not varna_list: return [], []

    last_idx = len(varna_list) - 1
    last_varna = varna_list[last_idx]

    # Check if it is a Vibhakti
    is_vibhakti = (source_type == UpadeshaType.VIBHAKTI)

    if last_varna.endswith('्'):
        # १.३.४ न विभक्तौ तुस्माः (तु = त-वर्ग, स्, म्)
        tusma = ['त्', 'थ्', 'द्', 'ध्', 'न्', 'स्', 'म्']

        if is_vibhakti and last_varna in tusma:
            link = get_sutra_link("1.3.4")
            # यहाँ कोई इत्-इंडेक्स नहीं लौटेगी (Protection Active)
            return [], [f"[१.३.४ न विभक्तौ तुस्माः (प्रतिषेध)]({link})"]

        # यदि विभक्ति नहीं है, तो सामान्य हलन्त्यम् लगेगा
        link = get_sutra_link("1.3.3")
        return [last_idx], [f"[१.३.३ हलन्त्यम्]({link})"]

    return [], []


def apply_adir_nitudavah_1_3_5(varna_list):
    """१.३.५: आदि ञि, टु, डु की इत्-संज्ञा (केवल धातु)।"""
    if len(varna_list) < 2: return [], []

    link = get_sutra_link("1.3.5")
    starting_pattern = varna_list[0] + varna_list[1]
    mapping = {'ञ्इ': 'ञि', 'ट्उ': 'टु', 'ड्उ': 'डु'}

    if starting_pattern in mapping:
        return [0, 1], [f"[१.३.५ आदिर्ञिटुडवः ({mapping[starting_pattern]})]({link})"]
    return [], []


def apply_shah_pratyayasya_1_3_6(varna_list):
    """१.३.६: प्रत्यय के आदि 'ष्' की इत्-संज्ञा।"""
    # नोट: इंजन में source_type फिल्टर पहले ही लगा है
    if varna_list and varna_list[0] == 'ष्':
        link = get_sutra_link("1.3.6")
        return [0], [f"[१.३.६ षः प्रत्ययस्य]({link})"]
    return [], []


def apply_chuttu_1_3_7(varna_list, source_type):
    """१.३.७: प्रत्यय के आदि च-वर्ग/ट-वर्ग की इत्-संज्ञा।"""
    from core.upadesha_registry import UpadeshaType
    if not varna_list or source_type != UpadeshaType.PRATYAYA:
        return [], []

    chuvarga = ['च्', 'छ्', 'ज्', 'झ्', 'ञ्']
    tuvarga = ['ट्', 'ठ्', 'ड्', 'ढ्', 'ण्']
    target_varnas = chuvarga + tuvarga

    if varna_list[0] in target_varnas:
        link = get_sutra_link("1.3.7")
        return [0], [f"[१.३.७ चुट्टू]({link})"]
    return [], []


def apply_lashakvataddhite_1_3_8(varna_list, source_type, is_taddhita=False):
    """
    १.३.८: प्रत्यय के आदि ल, श, कु की इत्-संज्ञा (तद्धित वर्जित)।
    """
    from core.upadesha_registry import UpadeshaType

    # Clinical Fix 1: यह नियम प्रत्यय (PRATYAYA) और विभक्ति (VIBHAKTI) दोनों पर लागू होता है
    allowed_types = [UpadeshaType.PRATYAYA, UpadeshaType.VIBHAKTI]

    if not varna_list or source_type not in allowed_types or is_taddhita:
        return [], []

    # क-वर्ग की पूर्ण सूची (क्, ख्, ग्, घ्, ङ्)
    kavarga = ['क्', 'ख्', 'ग्', 'घ्', 'ङ्']
    target = ['ल्', 'श्'] + kavarga

    # Clinical Fix 2: प्रत्यय के 'आदि' (शुरुआत) में वर्ण की जाँच
    first_varna = varna_list[0]

    if first_varna in target:
        # १.३.८ सूत्र का लिंक और इंडेक्स 0 को टैग करना
        link = "https://ashtadhyayi.com/sutraani/1/3/8"
        return [0], [f"१.३.८ लशक्वतद्धिते (आदि {first_varna} की इत्-संज्ञा)"]

    return [], []