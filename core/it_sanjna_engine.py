import os


def apply_upadeshe_ajanunasika_1_3_2(varna_list):
    """
    सूत्र: उपदेशेऽजनुनासिक इत् (1.3.2)
    तर्क: उपदेश अवस्था में अनुनासिक स्वरों की इत् संज्ञा और लोप।
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
            # पाणिनीय टैगिंग: 'उँ' -> उदित्
            base_vowel = anunasik_map[varna]
            it_tags.append(f"{{{base_vowel}दित्}}")
            # १.३.९ तस्य लोपः (सूची में शामिल नहीं किया गया)
        else:
            final_list.append(varna)

    return final_list, it_tags


def apply_halantyam_with_tags(varna_list, original_word):
    """
    सूत्र: हलन्त्यम् (1.3.3) + न विभक्तौ तुस्माः (1.3.4)
    तर्क: अंतिम व्यंजन की इत् संज्ञा, अपवाद: विभक्ति के 'त-वर्ग, स, म'।
    """
    if not varna_list:
        return varna_list, []

    # 1. अपवाद जाँच: १.३.४ न विभक्तौ तुस्माः
    exception_words = set()
    # Path logic for Streamlit/Local consistency
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "vibhakti_tusma.txt")

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            exception_words = {line.strip() for line in file}

    # यदि शब्द विभक्ति अपवाद सूची में है, तो लोप नहीं होगा
    if original_word in exception_words:
        return varna_list, []

    # 2. हलन्त्यम् कार्यान्वयन
    it_tags = []
    last_char = varna_list[-1]

    # यदि अंतिम वर्ण हलन्त व्यंजन है (जैसे 'ञ्', 'ट्')
    if last_char.endswith('्'):
        base_varna = last_char.replace('्', '')
        it_tag = f"{{{base_varna}ित्}}"

        varna_list.pop()  # १.३.९ तस्य लोपः
        it_tags.append(it_tag)

    return varna_list, it_tags


def apply_adir_nitudavah_1_3_5(varna_list):
    """
    सूत्र: आदिर्ञिटुडवः (1.3.5)
    तर्क: धातु के आदि में 'ञि', 'टु', 'डु' की इत् संज्ञा।
    """
    if len(varna_list) < 2:
        return varna_list, []

    it_tags = []
    # आदि के दो वर्णों को जोड़कर पैटर्न चेक करें
    # उदाहरण: ['ञ्', 'इ', 'वि', 'द्', 'ि'] -> 'ञि'
    starting_pattern = varna_list[0] + varna_list[1]

    mapping = {
        'ञ्इ': '{ञीत्}',
        'ट्उ': '{ट्वित्}',
        'ड्उ': '{ड्वित्}'
    }

    if starting_pattern in mapping:
        it_tags.append(mapping[starting_pattern])
        # १.३.९ तस्य लोपः (शुरुआत के दो वर्ण हटाएँ)
        varna_list = varna_list[2:]

    return varna_list, it_tags
def run_it_sanjna_prakaran(varna_list, original_word):
    """
    इत्-संज्ञा प्रकरण के सूत्रों का सामूहिक और क्रमवार संचालन।
    """
    all_its = []

    # १. आदिर्ञिटुडवः (1.3.5) - धातु के आदि के वर्ण
    varna_list, adi_its = apply_adir_nitudavah_1_3_5(varna_list)
    all_its.extend(adi_its)

    # २. उपदेशेऽजनुनासिक इत् (1.3.2) - अनुनासिक स्वर
    varna_list, anunasika_its = apply_upadeshe_ajanunasika_1_3_2(varna_list)
    all_its.extend(anunasika_its)

    # ३. हलन्त्यम् (1.3.3) - अंतिम व्यंजन (विभक्ति अपवाद के साथ)
    varna_list, hal_its = apply_halantyam_with_tags(varna_list, original_word)
    all_its.extend(hal_its)

    return varna_list, all_its