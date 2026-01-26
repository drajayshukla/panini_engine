import os


def get_sutra_link(sutra_num):
    """Ashtadhyayi.com के लिए सटीक लिंक जेनरेट करता है।"""
    formatted_num = sutra_num.replace('.', '/')
    return f"https://ashtadhyayi.com/sutraani/{formatted_num}"


# --- १.१.१ वृद्धि और १.१.२ गुण संज्ञा (General Sanjna) ---

def check_vriddhi_1_1_1(varna):
    """सूत्र: वृद्धिरादैच् (1.1.1) - आ, ऐ, औ की पहचान"""
    vriddhi_letters = ['आ', 'ऐ', 'औ']
    if varna in vriddhi_letters:
        link = get_sutra_link("1.1.1")
        return f"[वृद्धि (१.१.१)]({link})"
    return None


def check_guna_1_1_2(varna):
    """सूत्र: अदेङ्गुणः (1.1.2) - अ, ए, ओ की पहचान"""
    guna_letters = ['अ', 'ए', 'ओ']
    if varna in guna_letters:
        link = get_sutra_link("1.1.2")
        return f"[गुण (१.१.२)]({link})"
    return None


# --- १.३.२ से १.३.८ इत्-संज्ञा प्रकरण (It-Sanjna Rules) ---

def apply_upadeshe_ajanunasika_1_3_2(varna_list):
    """१.३.२ उपदेशेऽजनुनासिक इत्"""
    anunasik_varnas = ['अँ', 'आँ', 'इँ', 'ईँ', 'उँ', 'ऊँ', 'ऋँ', 'ॠँ', 'ऌँ', 'ॡँ', 'एँ', 'ओँ', 'ऐँ', 'औँ']
    it_tags = []
    final_list = []
    link = get_sutra_link("1.3.2")

    for v in varna_list:
        if v in anunasik_varnas or v == 'ँ':
            it_tags.append(f"[१.३.२ उपदेशेऽजनुनासिक इत्]({link})")
        else:
            final_list.append(v)
    return final_list, list(set(it_tags))


def apply_halantyam_1_3_3(varna_list, original_word, is_vibhakti=False):
    """१.३.३ हलन्त्यम् + १.३.४ न विभक्तौ तुस्माः"""
    if not varna_list: return varna_list, []

    last_varna = varna_list[-1]
    if last_varna.endswith('्'):
        tusma = ['त्', 'थ्', 'द्', 'ध्', 'न्', 'स्', 'म्']
        if is_vibhakti and last_varna in tusma:
            link = get_sutra_link("1.3.4")
            return varna_list, [f"[१.३.४ न विभक्तौ तुस्माः (प्रतिषेध)]({link})"]

        varna_list.pop()
        link = get_sutra_link("1.3.3")
        return varna_list, [f"[१.३.३ हलन्त्यम्]({link})"]
    return varna_list, []


def apply_adir_nitudavah_1_3_5(varna_list):
    """१.३.५ आदिर्ञिटुडवः (केवल धातु)"""
    if len(varna_list) < 2: return varna_list, []

    starting_pattern = varna_list[0] + varna_list[1]
    mapping = {'ञ्इ': 'ञि', 'ट्उ': 'टु', 'ड्उ': 'डु'}

    if starting_pattern in mapping:
        link = get_sutra_link("1.3.5")
        return varna_list[2:], [f"[१.३.५ आदिर्ञिटुडवः ({mapping[starting_pattern]})]({link})"]
    return varna_list, []


def apply_shah_pratyayasya_1_3_6(varna_list):
    """१.३.६ षः प्रत्ययस्य (केवल प्रत्यय)"""
    if varna_list and varna_list[0] == 'ष्':
        varna_list.pop(0)
        link = get_sutra_link("1.3.6")
        return varna_list, [f"[१.३.६ षः प्रत्ययस्य]({link})"]
    return varna_list, []


def apply_chuttu_1_3_7(varna_list):
    """१.३.७ चुट्टू (केवल प्रत्यय)"""
    if not varna_list: return varna_list, []
    chutuvarga = ['च्', 'छ्', 'ज्', 'झ्', 'ञ्', 'ट्', 'ठ्', 'ड्', 'ढ्', 'ण्']
    if varna_list[0] in chutuvarga:
        varna_list.pop(0)
        link = get_sutra_link("1.3.7")
        return varna_list, [f"[१.३.७ चुट्टू]({link})"]
    return varna_list, []


def apply_lashakvataddhite_1_3_8(varna_list, is_taddhita=False):
    """१.३.८ लशक्वतद्धिते (केवल प्रत्यय, तद्धित वर्जित)"""
    if not varna_list or is_taddhita: return varna_list, []
    kavarga = ['क्', 'ख्', 'ग्', 'घ्', 'ङ्']
    target = ['ल्', 'श्'] + kavarga
    if varna_list[0] in target:
        varna_list.pop(0)
        link = get_sutra_link("1.3.8")
        return varna_list, [f"[१.३.८ लशक्वतद्धिते]({link})"]
    return varna_list, []