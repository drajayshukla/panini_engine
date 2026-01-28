# logic/svara_rules.py
from core.phonology import Varna


def apply_svara_sanjna(varna_obj, raw_string):
    """
    सूत्र: उच्चैरुदात्तः (१.२.२९), नीचैरनुदात्तः (१.२.३०), समाहारः स्वरितः (१.२.३१)
    उद्देश्य: यूनिकोड चिह्नों के आधार पर अच् (Vowel) की पिच संज्ञा निर्धारित करना।
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
    # यदि कोई चिह्न नहीं है, तो पाणिनीय तंत्र में उसे उदात्त माना जाता है
    else:
        varna_obj.svara = "उदात्त"
        varna_obj.svara_mark = None

    return varna_obj