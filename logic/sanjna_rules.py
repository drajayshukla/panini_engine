import os


def get_sutra_link(sutra_num):
    """Ashtadhyayi.com के लिए डायरेक्ट लिंक जेनरेट करता है।"""
    # फॉर्मेट: 1.3.2 -> https://ashtadhyayi.com/sutra/prakaran/1/3/2
    formatted_num = sutra_num.replace('.', '/')
    return f"https://ashtadhyayi.com/sutra/prakaran/{formatted_num}"


def check_vriddhi_1_1_1(varna):
    """
    सूत्र: वृद्धिरादैच् (1.1.1)
    """
    vriddhi_letters = ['आ', 'ऐ', 'औ']
    if varna in vriddhi_letters:
        link = get_sutra_link("1.1.1")
        return f"[वृद्धि (१.१.१)]({link})"
    return None


def check_guna_1_1_2(varna):
    """
    सूत्र: अदेङ्गुणः (1.1.2)
    """
    guna_letters = ['अ', 'ए', 'ओ']
    if varna in guna_letters:
        link = get_sutra_link("1.1.2")
        return f"[गुण (१.१.२)]({link})"
    return None


def apply_upadeshe_ajanunasika_1_3_2(varna_list):
    """
    सूत्र: उपदेशेऽजनुनासिक इत् (1.3.2)
    """
    anunasik_map = {
        'अँ': 'अ', 'आँ': 'आ', 'इँ': 'इ', 'ईँ': 'ई', 'उँ': 'उ',
        'ऊँ': 'ऊ', 'ऋँ': 'ऋ', 'ॠँ': 'ॠ', 'ऌँ': 'ऌ', 'ॡँ': 'ॡ',
        'एँ': 'ए', 'ओँ': 'ओ', 'ऐँ': 'ऐ', 'औँ': 'औ'
    }

    it_tags = []
    final_list = []
    link = get_sutra_link("1.3.2")

    i = 0
    while i < len(varna_list):
        current_varna = varna_list[i]
        if current_varna == 'ँ' and i > 0:
            if final_list:
                last_vowel = final_list.pop()
                it_tags.append(f"[{{{last_vowel}दित्}} (१.३.२)]({link})")
        elif current_varna in anunasik_map:
            base_vowel = anunasik_map[current_varna]
            it_tags.append(f"[{{{base_vowel}दित्}} (१.३.२)]({link})")
        else:
            final_list.append(current_varna)
        i += 1

    return final_list, it_tags


def apply_halantyam_1_3_3(varna_list, original_word, is_vibhakti=False):
    """
    सूत्र: हलन्त्यम् (1.3.3) + न विभक्तौ तुस्माः (1.3.4)
    """
    if not varna_list:
        return varna_list, []

    last_varna = varna_list[-1]
    it_tags = []
    link_1_3_3 = get_sutra_link("1.3.3")
    link_1_3_4 = get_sutra_link("1.3.4")

    if last_varna.endswith('्'):
        # १.३.४ न विभक्तौ तुस्माः चेक
        tusma = ['त्', 'थ्', 'द्', 'ध्', 'न्', 'स्', 'म्']
        if is_vibhakti and last_varna in tusma:
            it_tags.append(f"[न विभक्तौ तुस्माः (१.३.४) - {last_varna} सुरक्षित]({link_1_3_4})")
            return varna_list, it_tags

        # सामान्य लोप १.३.३
        base_varna = varna_list.pop().replace('्', '')
        it_tags.append(f"[{{{base_varna}ित्}} (१.३.३)]({link_1_3_3})")

    return varna_list, it_tags


def apply_adir_nitudavah_1_3_5(varna_list):
    """
    सूत्र: आदिर्ञिटुडवः (1.3.5)
    """
    if len(varna_list) < 2:
        return varna_list, []

    link = get_sutra_link("1.3.5")
    starting_pattern = varna_list[0] + varna_list[1]
    mapping = {
        'ञ्इ': '{ञीत्}',
        'ट्उ': '{ट्वित्}',
        'ड्उ': '{ड्वित्}'
    }

    if starting_pattern in mapping:
        tag = mapping[starting_pattern]
        return varna_list[2:], [f"[{tag} (१.३.५)]({link})"]

    return varna_list, []