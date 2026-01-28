# logic/svara_rules.py


# logic/svara_rules.py

def apply_svara_sanjna(varna_obj, raw_string):
    """
    सूत्र: उच्चैरुदात्तः (१.२.२९), नीचैरनुदात्तः (१.२.३०), समाहारः स्वरितः (१.२.३१)
    वृत्तीय आयात (Circular Import) से बचने के लिए यहाँ Varna इम्पोर्ट नहीं किया गया है।
    """

    # १. अचश्च (१.२.२८) नियम का पालन: केवल अच् पर ही स्वर संज्ञा संभव है
    if not varna_obj.is_vowel:
        varna_obj.svara = None
        varna_obj.svara_mark = None
        return varna_obj

    # २. अनुदात्त (॒) - नीचैरनुदात्तः (१.२.३०)
    # Unicode: \u0331 (Combining Low Line) या भौतिक चिह्न '_'
    if "\u0331" in raw_string or "_" in raw_string or "॒" in raw_string:
        varna_obj.svara = "अनुदात्त"
        varna_obj.svara_mark = "॒"

    # ३. स्वरित (॑) - समाहारः स्वरितः (१.२.३१)
    # Unicode: \u030d (Vertical Line Above) या वैदिक स्वरित चिह्न
    elif "\u030d" in raw_string or "'" in raw_string or "॑" in raw_string or "|" in raw_string:
        varna_obj.svara = "स्वरित"
        varna_obj.svara_mark = "॑"

    # ४. उदात्त (Default) - उच्चैरुदात्तः (१.२.२९)
    else:
        varna_obj.svara = "उदात्त"
        varna_obj.svara_mark = None

    return varna_obj