import re

# आंतरिक नियमों से इम्पोर्ट (सुनिश्चित करें कि ये फाइलें मौजूद हैं)
try:
    from logic.svara_rules import apply_svara_sanjna
    from logic.sthana_rules import apply_sthana_to_varna
except ImportError:
    # टेस्टिंग के लिए डमी फंक्शन्स (यदि फाइलें न मिलें)
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

MATRA_DATA = {
    'अ': 1, 'इ': 1, 'उ': 1, 'ऋ': 1, 'ऌ': 1,
    'आ': 2, 'ई': 2, 'ऊ': 2, 'ॠ': 2, 'ए': 2, 'ओ': 2, 'ऐ': 2, 'औ': 2
}


# --- २. वर्ण क्लास (The Varna Entity) ---
class Varna:
    def __init__(self, raw_unit):
        """
        raw_unit: वर्ण के साथ स्वर-चिह्न (उदा. 'अ॒', 'ई॑', 'ओ३', या पृथक 'ँ')
        """
        self.char = raw_unit[0]
        # प्लुत '३' को वर्ण का हिस्सा माना (उदा. 'ओ३')
        if len(raw_unit) > 1 and raw_unit[1] == '३':
            self.char = raw_unit[:2]

        # अच् (Vowel) की पहचान
        self.is_vowel = self.char in INDEPENDENT_VOWELS or '३' in self.char

        # मात्रा निर्धारण (१.२.२७ ऊकालोऽज्झ्रस्वदीर्घप्लुतः)
        self.matra = self._calculate_matra(self.char)

        # संज्ञा स्लॉट्स
        self.kala_sanjna = None
        self.svara = "उदात्त"  # डिफ़ॉल्ट
        self.svara_mark = None

        # अनुनासिक पहचान (१.१.८ मुखनासिकावचनोऽनुनासिकः)
        self.is_anunasika = 'ँ' in raw_unit

        # १.१.९: स्थान एवं प्रयत्न
        self.sthana = None
        self.prayatna = None

        # संज्ञाएँ अपडेट करना (Diagnostics)
        apply_svara_sanjna(self, raw_unit)
        apply_sthana_to_varna(self)

    def _calculate_matra(self, char):
        """पाणिनीय मात्रा गणना"""
        if char in 'ंःँ': return 0
        if '३' in char: return 3
        if char == 'ऌ' or char == 'ॡ': return 1
        if char in ['ए', 'ओ', 'ऐ', 'औ']: return 2
        if char in MATRA_DATA: return MATRA_DATA[char]
        if '्' in char: return 0.5  # व्यञ्जनमर्धमात्रिकम्
        return 0

    def __repr__(self):
        # अ(१)[ह्रस्व][उदात्त][निरनुनासिक][कण्ठ]
        kala = f"[{self.kala_sanjna}]" if self.kala_sanjna else ""
        svara = f"[{self.svara}]" if self.is_vowel else ""
        anu = "[अनुनासिक]" if self.is_anunasika else "[निरनुनासिक]"
        sth = f"[{self.sthana}]" if self.sthana else ""
        return f"{self.char}({self.matra}){kala}{svara}{anu}{sth}"


# --- ३. विच्छेद इंजन (Surgical Patch for Anunasika Separation) ---
def sanskrit_varna_vichhed(text, return_objects=True):
    """
    गाधृँ -> ग् + आ + ध् + ऋ + ँ (अनुनासिक पृथक इकाई)
    व्यंजन हमेशा हलन्त रहेंगे।
    """
    if not text:
        return []

    # नियम १६, ३, १२: विशिष्ट संयुक्ताक्षर
    if text == "ॐ":
        res_strings = ["अ", "उ", "म्"]
    else:
        text = text.replace('क्ष', 'क्‌ष').replace('त्र', 'त्‌र').replace('ज्ञ', 'ज्‌ञ').replace('श्र', 'श्‌र').replace(
            'ऽ', 'अ')

        # नियम ६: पञ्चम वर्ण
        text = re.sub(r'ं(?=[कखगघ])', 'ङ्', text)
        text = re.sub(r'ं(?=[चछजझ])', 'ञ्', text)
        text = re.sub(r'ं(?=[टठडढ])', 'ण्', text)
        text = re.sub(r'ं(?=[तथदध])', 'न्', text)
        text = re.sub(r'ं(?=[पफबभ])', 'म्', text)

        res_strings = []
        i = 0
        while i < len(text):
            char = text[i]

            # १. स्वतंत्र स्वर
            if char in INDEPENDENT_VOWELS:
                current_unit = char
                if i + 1 < len(text) and text[i + 1] == '३':
                    current_unit += '३'
                    i += 1

                # स्वर-चिह्नों को साथ रखें (॒ ॑) पर 'ँ' को अलग करें
                while i + 1 < len(text) and text[i + 1] in '\u0331\u030d_॒॑|':
                    current_unit += text[i + 1]
                    i += 1
                res_strings.append(current_unit)

                # अयोगवाह/अनुनासिक (पृथक वर्ण के रूप में)
                while i + 1 < len(text) and text[i + 1] in 'ंःँ':
                    if text[i + 1] == 'ं' and (i + 2 == len(text) or text[i + 2] == ' '):
                        res_strings.append('म्')
                    else:
                        res_strings.append(text[i + 1])
                    i += 1

            # २. व्यंजन प्रबंधन (Consonants)
            elif '\u0915' <= char <= '\u0939' or char == 'ळ':
                res_strings.append(char + '्')  # हमेशा हलन्त
                found_vowel = False

                if i + 1 < len(text):
                    next_char = text[i + 1]
                    if next_char == '्':
                        i += 1
                        found_vowel = True
                    elif next_char in VOWELS_MAP:
                        vowel_unit = VOWELS_MAP[next_char]
                        i += 1
                        # चिह्नों को साथ रखें, 'ँ' को अलग करें
                        while i + 1 < len(text) and text[i + 1] in '\u0331\u030d_॒॑|':
                            vowel_unit += text[i + 1]
                            i += 1
                        res_strings.append(vowel_unit)
                        found_vowel = True

                        while i + 1 < len(text) and text[i + 1] in 'ंःँ':
                            if text[i + 1] == 'ं' and (i + 2 == len(text) or text[i + 2] == ' '):
                                res_strings.append('म्')
                            else:
                                res_strings.append(text[i + 1])
                            i += 1
                    elif next_char in 'ंःँ':
                        res_strings.append('अ')
                        found_vowel = True
                        if next_char == 'ं' and (i + 2 == len(text) or text[i + 2] == ' '):
                            res_strings.append('म्')
                        else:
                            res_strings.append(next_char)
                        i += 1
                    elif next_char == ' ':
                        res_strings.append('अ')
                        found_vowel = True

                if not found_vowel:
                    res_strings.append('अ')

            elif char in 'ᳲᳳ':
                res_strings.append(char)
            i += 1

    if return_objects:
        return [Varna(s) for s in res_strings]
    return res_strings


# --- ४. संयोग इंजन (Samyoga) ---
def sanskrit_varna_samyoga(varna_list):
    """
    विच्छेदित वर्णों को पुनः जोड़ना। 'ग्' + 'आ' + 'ध्' -> 'गाध्'
    """
    if not varna_list:
        return ""

    text_list = [v.char if hasattr(v, 'char') else v for v in varna_list]

    res = ""
    for char in text_list:
        if not res:
            res = char
            continue

        # १. व्यंजन + स्वर (हलन्त लोप और मात्रा योग)
        if res.endswith('्') and char in INDEPENDENT_VOWELS:
            res = res[:-1] + REVERSE_VOWELS_MAP.get(char, "")

        # २. अयोगवाह / अनुनासिक
        elif char in 'ँंः':
            res += char

        # ३. अन्य (व्यंजन + व्यंजन आदि)
        else:
            res += char

    return res