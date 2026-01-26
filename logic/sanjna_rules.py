import os


def get_sutra_link(sutra_num):
    """Ashtadhyayi.com के लिए सटीक लिंक जेनरेट करता है।"""
    # सही फॉर्मेट: https://ashtadhyayi.com/sutra/1/3/2
    formatted_num = sutra_num.replace('.', '/')
    return f"https://ashtadhyayi.com/sutra/{formatted_num}"


def check_vriddhi_1_1_1(varna):
    """सूत्र: वृद्धिरादैच् (1.1.1)"""
    vriddhi_letters = ['आ', 'ऐ', 'औ']
    if varna in vriddhi_letters:
        link = get_sutra_link("1.1.1")
        return f"[वृद्धि (१.१.१)]({link})"
    return None


def check_guna_1_1_2(varna):
    """सूत्र: अदेङ्गुणः (1.1.2)"""
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
    tag_name = f"[१.३.२ उपदेशेऽजनुनासिक इत्]({link})"

    i = 0
    while i < len(varna_list):
        current_varna = varna_list[i]

        # स्थिति A: अनुनासिक चिन्ह 'ँ' अलग मिले
        if current_varna == 'ँ' and i > 0:
            if final_list:
                final_list.pop()  # स्वर हटाएँ
                it_tags.append(tag_name)

        # स्थिति B: संयुक्त अनुनासिक वर्ण
        elif current_varna in anunasik_map:
            it_tags.append(tag_name)
            # लोप के कारण final_list में नहीं जोड़ेंगे

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
    link_1_3_3 = get_sutra_link("1.3.3")
    link_1_3_4 = get_sutra_link("1.3.4")

    if last_varna.endswith('्'):
        # १.३.४ न विभक्तौ तुस्माः चेक
        tusma = ['त्', 'थ्', 'द्', 'ध्', 'न्', 'स्', 'म्']
        if is_vibhakti and last_varna in tusma:
            tag = f"[१.३.४ न विभक्तौ तुस्माः (प्रतिषेध)]({link_1_3_4})"
            return varna_list, [tag]

        # सामान्य लोप १.३.३
        varna_list.pop()
        tag = f"[१.३.३ हलन्त्यम्]({link_1_3_3})"
        return varna_list, [tag]

    return varna_list, []


def apply_adir_nitudavah_1_3_5(varna_list):
    """
    सूत्र: आदिर्ञिटुडवः (1.3.5)
    """
    if len(varna_list) < 2:
        return varna_list, []

    link = get_sutra_link("1.3.5")
    # 'ञ्' + 'इ' = 'ञि' आदि पैटर्न्स
    starting_pattern = varna_list[0] + varna_list[1]

    mapping = {
        'ञ्इ': 'ञि',
        'ट्उ': 'टु',
        'ड्उ': 'डु'
    }

    if starting_pattern in mapping:
        base = mapping[starting_pattern]
        tag = f"[१.३.५ आदिर्ञिटुडवः ({base})]({link})"
        return varna_list[2:], [tag]

    return varna_list, []