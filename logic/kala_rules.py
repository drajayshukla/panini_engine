# logic/kala_rules.py
from core.phonology import Varna


def apply_1_2_28_filter(varna_obj, action_type):
    """
    परिभाषा सूत्र: अचश्च (१.२.२८)
    उद्देश्य: यह सुनिश्चित करना कि ह्रस्व/दीर्घ/प्लुत केवल अच् (Vowels) पर लागू हों।
    """
    if not varna_obj.is_vowel:
        return False, f"अचश्च (१.२.२८): '{varna_obj.char}' व्यञ्जन है, अतः {action_type} कार्य वर्जित है।"
    return True, "Valid"


def apply_ukalo_aj_1_2_27(varna_obj):
    """
    संज्ञा सूत्र: ऊकालोऽज्झ्रस्वदीर्घप्लुतः (१.२.२७)
    यह फ़ंक्शन वर्ण की मात्रा के आधार पर उसे अंतिम संज्ञा प्रदान करता है।
    """
    # १.२.२८ का फ़िल्टर सबसे पहले (Safety First)
    is_valid, _ = apply_1_2_28_filter(varna_obj, "काल-संज्ञा")

    if not is_valid:
        varna_obj.kala_sanjna = "व्यञ्जन"
        return varna_obj

    # १.२.२७ के अनुसार संज्ञा आवंटन
    if varna_obj.matra == 1:
        varna_obj.kala_sanjna = "ह्रस्व"
    elif varna_obj.matra == 2:
        varna_obj.kala_sanjna = "दीर्घ"
    elif varna_obj.matra >= 3:
        varna_obj.kala_sanjna = "प्लुत"
    else:
        varna_obj.kala_sanjna = "अज्ञात"

    return varna_obj


def apply_specific_kala_action(varna_obj, target_matra):
    """
    यह फंक्शन किसी सूत्र द्वारा दिए गए 'आदेश' (Action) को प्रोसेस करता है।
    जैसे: 'ह्रस्वः' (१.२.२७) आदेश आने पर।
    """
    action_name = "ह्रस्व" if target_matra == 1 else "दीर्घ" if target_matra == 2 else "प्लुत"

    # १.२.२८ का कड़ा पहरा
    is_valid, error_msg = apply_1_2_28_filter(varna_obj, action_name)

    if is_valid:
        varna_obj.matra = target_matra
        varna_obj.kala_sanjna = action_name
    else:
        # यदि व्यञ्जन पर कार्य करने की कोशिश की जाए तो लॉग करें (Clinical Log)
        print(f"DEBUG: {error_msg}")

    return varna_obj


def generate_18_bheda_matrix(varna_obj):
    """
    पाणिनीय अष्टाध्यायी के आधार पर स्वर के १८ भेदों का निर्माण।
    ह्रस्व/दीर्घ/प्लुत (३) * उदात्त/अनुदात्त/स्वरित (३) * अनुनासिक/निरनुनासिक (२)
    """
    if not varna_obj.is_vowel:
        return []

    # आधार वर्ण (चिह्न हटाकर)
    base_char = varna_obj.char[0]

    # नियमों के आधार पर काल-सीमा (नियम २ और ३)
    kalas = ["ह्रस्व", "दीर्घ", "प्लुत"]

    # २. ऌकारस्य दीर्घाभावात् (ऌ का दीर्घ नहीं होता)
    if base_char == 'ऌ':
        kalas = ["ह्रस्व", "प्लुत"]
        # ३. एचां ह्रस्वाभावात् (ए, ओ, ऐ, औ का ह्रस्व नहीं होता)
    elif base_char in ['ए', 'ओ', 'ऐ', 'औ']:
        kalas = ["दीर्घ", "प्लुत"]

    svaras = ["उदात्त", "अनुदात्त", "स्वरित"]
    nasals = ["अनुनासिक", "निरनुनासिक"]

    matrix = []
    for k in kalas:
        for s in svaras:
            for n in nasals:
                matrix.append({
                    "काल": k,
                    "सवर": s,
                    "नासिका": n
                })
    return matrix