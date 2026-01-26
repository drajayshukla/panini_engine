# logic/sanjna_rules.py
import os

def check_vriddhi_1_1_1(varna):
    """
    सूत्र: वृद्धिरादैच् (1.1.1)
    तर्क: आ, ऐ, और औ वर्णों की 'वृद्धि' संज्ञा होती है।
    """
    vriddhi_letters = ['आ', 'ऐ', 'औ']
    return "वृद्धि" if varna in vriddhi_letters else None


def check_guna_1_1_2(varna):
    """
    सूत्र: अदेङ्गुणः (1.1.2)
    तर्क: अ, ए, और ओ वर्णों की 'गुण' संज्ञा होती है।
    """
    guna_letters = ['अ', 'ए', 'ओ']
    return "गुण" if varna in guna_letters else None


def apply_upadeshe_ajanunasika_1_3_2(varna_list):
    """
    सूत्र: उपदेशेऽजनुनासिक इत् (1.3.2)
    तर्क: उपदेश की अवस्था में अनुनासिक स्वर की इत् संज्ञा और लोप।
    """
    anunasik_map = {
        'अँ': 'अ', 'आँ': 'आ', 'इँ': 'इ', 'ईँ': 'ई', 'उँ': 'उ',
        'ऊँ': 'ऊ', 'ऋँ': 'ऋ', 'ॠँ': 'ॠ', 'ऌँ': 'ऌ', 'ॡँ': 'ॡ',
        'एँ': 'ए', 'ओँ': 'ओ', 'ऐँ': 'ऐ', 'औँ': 'औ'
    }

    it_tags = []
    final_list = []

    for varna in varna_list:
        if varna in anunasik_map:
            base_vowel = anunasik_map[varna]
            # पाणिनीय टैगिंग: 'उँ' -> {उदित्}
            it_tags.append(f"{{{base_vowel}दित्}}")
        else:
            final_list.append(varna)

    return final_list, it_tags


def apply_halantyam_1_3_3(varna_list, original_word):
    """
    सूत्र: हलन्त्यम् (1.3.3) + न विभक्तौ तुस्माः (1.3.4)
    तर्क: अंतिम व्यंजन की इत् संज्ञा, अपवाद: विभक्ति के 'त-वर्ग, स, म'।
    """
    if not varna_list:
        return varna_list, []

    # अपवाद जाँच: १.३.४ न विभक्तौ तुस्माः
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "vibhakti_tusma.txt")

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            exception_words = {line.strip() for line in f}
            if original_word in exception_words:
                return varna_list, []

    it_tags = []
    if varna_list[-1].endswith('्'):
        # १.३.९ तस्य लोपः
        base_varna = varna_list.pop().replace('्', '')
        it_tags.append(f"{{{base_varna}ित्}}")

    return varna_list, it_tags


def apply_adir_nitudavah_1_3_5(varna_list):
    """
    सूत्र: आदिर्ञिटुडवः (1.3.5)
    तर्क: धातु के आदि में 'ञि', 'टु', 'डु' की इत् संज्ञा।
    """
    if len(varna_list) < 2:
        return varna_list, []

    # आदि के दो वर्णों को जोड़कर पैटर्न चेक करें (जैसे: 'ञ्' + 'इ' = 'ञि')
    starting_pattern = varna_list[0] + varna_list[1]
    mapping = {
        'ञ्इ': '{ञीत्}',
        'ट्उ': '{ट्वित्}',
        'ड्उ': '{ड्वित्}'
    }

    if starting_pattern in mapping:
        tag = mapping[starting_pattern]
        # शुरुआत के दो वर्ण हटाएँ (तस्य लोपः)
        return varna_list[2:], [tag]

    return varna_list, []