# panini_engine/core/phonology.py
import re

# आंतरिक नियमों से इम्पोर्ट (सुनिश्चित करें कि logic/ फोल्डर में ये मौजूद हैं)
try:
    from logic.svara_rules import apply_svara_sanjna
    from logic.sthana_rules import apply_sthana_to_varna
except ImportError:
    def apply_svara_sanjna(obj, unit):
        pass


    def apply_sthana_to_varna(obj):
        pass

# --- १. व्याकरणिक स्थिरांक (Grammar Constants) ---
VOWELS_MAP = {
    'ा': 'आ', 'ि': 'इ', 'ी': 'ई', 'ु': 'उ', 'ू': 'ऊ',
    'ृ': 'ऋ', 'ॄ': 'ॠ', 'ॢ': 'ऌ', 'ॣ': 'ॡ',
    'े': 'ए', 'ै': 'ऐ', 'ो': 'ओ', 'ौ': 'औ'
}

REVERSE_VOWELS_MAP = {v: k for k, v in VOWELS_MAP.items()}
INDEPENDENT_VOWELS = 'अआइईउऊऋॠऌॡएऐओऔ'


# --- २. वर्ण क्लास (The Varna Entity) ---
class Varna:
    def __init__(self, raw_unit):
        """
        raw_unit: यह 'ग्', 'आ', 'ध्', 'ऋ' या 'ँ' जैसी शुद्ध इकाइयाँ होंगी।
        """
        self.char = raw_unit

        # अच् (Vowel) की पहचान: यदि इसमें स्वतंत्र स्वर या प्लुत '३' है
        self.is_vowel = any(v in raw_unit for v in INDEPENDENT_VOWELS) or '३' in raw_unit

        # १.१.८: अनुनासिक पहचान
        self.is_anunasika = 'ँ' in raw_unit

        # संज्ञा स्लॉट्स
        self.sthana = None
        self.svara = "उदात्त"
        self.kala_sanjna = None

        # डायग्नोस्टिक अपडेट्स
        apply_svara_sanjna(self, raw_unit)
        apply_sthana_to_varna(self)

    def __repr__(self):
        # UI पर दिखाने के लिए शुद्ध वर्ण रूप
        return self.char


# --- ३. विच्छेद इंजन (Exact Logic as per User Input) ---
def sanskrit_varna_vichhed(text, return_objects=True):
    """
    गाधृँ -> ['ग्', 'आ', 'ध्', 'ऋ', 'ँ']
    व्यंजन हमेशा हलन्त रहेंगे और अनुनासिक (ँ) पृथक इकाई रहेगा।
    """
    if not text:
        return []

    # नियम 16: ॐ
    if text == "ॐ":
        res = ["अ", "उ", "म्"]
    else:
        # नियम 3, 12: विशिष्ट संयुक्ताक्षर और अवग्रह
        text = text.replace('क्ष', 'क्‌ष').replace('त्र', 'त्‌र').replace('ज्ञ', 'ज्‌ञ').replace('श्र', 'श्‌र').replace(
            'ऽ', 'अ')

        # नियम 6: पञ्चम वर्ण नियम
        text = re.sub(r'ं(?=[कखगघ])', 'ङ्', text)
        text = re.sub(r'ं(?=[चछजझ])', 'ञ्', text)
        text = re.sub(r'ं(?=[टठडढ])', 'ण्', text)
        text = re.sub(r'ं(?=[तथदध])', 'न्', text)
        text = re.sub(r'ं(?=[पफबभ])', 'म्', text)

        res = []
        i = 0
        while i < len(text):
            char = text[i]

            # 1. स्वतंत्र स्वर प्रबंधन
            if char in INDEPENDENT_VOWELS:
                current_unit = char
                if i + 1 < len(text) and text[i + 1] == '३':
                    current_unit += '३'
                    i += 1
                res.append(current_unit)

                # अयोगवाह/अनुनासिक पृथक रखना
                while i + 1 < len(text) and text[i + 1] in 'ंःँ':
                    if text[i + 1] == 'ं' and (i + 2 == len(text) or text[i + 2] == ' '):
                        res.append('म्')
                    else:
                        res.append(text[i + 1])
                    i += 1

            # 2. व्यंजन प्रबंधन (Pure Consonants Logic)
            elif '\u0915' <= char <= '\u0939' or char == 'ळ':
                res.append(char + '्')  # व्यंजन हमेशा हलन्त

                found_vowel = False
                if i + 1 < len(text):
                    next_char = text[i + 1]

                    if next_char == '्':
                        i += 1
                        found_vowel = True
                    elif next_char in VOWELS_MAP:
                        res.append(VOWELS_MAP[next_char])
                        i += 1
                        found_vowel = True
                        while i + 1 < len(text) and text[i + 1] in 'ंःँ':
                            if text[i + 1] == 'ं' and (i + 2 == len(text) or text[i + 2] == ' '):
                                res.append('म्')
                            else:
                                res.append(text[i + 1])
                            i += 1
                    elif next_char in 'ंःँ':
                        res.append('अ')
                        found_vowel = True
                        if next_char == 'ं' and (i + 2 == len(text) or text[i + 2] == ' '):
                            res.append('म्')
                        else:
                            res.append(next_char)
                        i += 1
                    elif next_char == ' ':
                        res.append('अ')
                        found_vowel = True

                if not found_vowel:
                    res.append('अ')

            elif char in 'ᳲᳳ':
                res.append(char)
            i += 1

    if return_objects:
        return [Varna(s) for s in res]
    return " + ".join(res)


# --- ४. संयोग इंजन (Joining Logic) ---
def sanskrit_varna_samyoga(varna_list):
    """
    'ग्' + 'आ' + 'ध्' -> 'गाध्'
    'ग्' + 'आ' + 'ध्' + 'ऋ' + 'ँ' -> 'गाधृँ'
    """
    if not varna_list:
        return ""

    text_list = [v.char if hasattr(v, 'char') else v for v in varna_list]

    res = ""
    for char in text_list:
        if not res:
            res = char
            continue

        # हलन्त व्यंजन + स्वर का मिलन
        if res.endswith('्') and any(v in char for v in INDEPENDENT_VOWELS):
            # 'अ' होने पर सिर्फ हलन्त हटेगा, बाकी स्वरों के लिए मात्रा लगेगी
            matra = REVERSE_VOWELS_MAP.get(char[0], "") if char[0] != 'अ' else ""
            res = res[:-1] + matra
            # यदि स्वर के साथ चिह्न हैं (जैसे प्लुत ३), उन्हें जोड़ें
            if len(char) > 1: res += char[1:]

        else:
            res += char

    return res