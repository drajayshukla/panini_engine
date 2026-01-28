import re
# यहाँ से इम्पोर्ट करना सुरक्षित है
from logic.svara_rules import apply_svara_sanjna
from logic.sthana_rules import apply_sthana_to_varna
# --- व्याकरणिक स्थिरांक (Grammar Constants) ---
VOWELS_MAP = {
    'ा': 'आ', 'ि': 'इ', 'ी': 'ई', 'ु': 'उ', 'ू': 'ऊ',
    'ृ': 'ऋ', 'ॄ': 'ॠ', 'ॢ': 'ऌ', 'ॣ': 'ॡ',
    'े': 'ए', 'ै': 'ऐ', 'ो': 'ओ', 'ौ': 'औ'
}

REVERSE_VOWELS_MAP = {v: k for k, v in VOWELS_MAP.items()}
INDEPENDENT_VOWELS = 'अआइईउऊऋॠऌॡएऐओऔ'

# --- १.२.२७ ऊकालोऽज्झ्रस्वदीर्घप्लुतः के लिए डेटा ---
MATRA_DATA = {
    'अ': 1, 'इ': 1, 'उ': 1, 'ऋ': 1, 'ऌ': 1,
    'आ': 2, 'ई': 2, 'ऊ': 2, 'ॠ': 2, 'ए': 2, 'ओ': 2, 'ऐ': 2, 'औ': 2
}


# --- १. वर्ण क्लास (The Varna Entity) ---
class Varna:
    def __init__(self, raw_unit):
        """
        raw_unit में वर्ण के साथ उसके चिह्न भी हो सकते हैं (उदा. 'अ॒', 'ई॑', 'ओ३', या 'आँ॑')
        """
        # स्वर-चिह्नों को अलग कर शुद्ध वर्ण निकालें
        self.char = raw_unit[0]
        # प्लुत '३' को वर्ण का हिस्सा माना
        if len(raw_unit) > 1 and raw_unit[1] == '३':
            self.char = raw_unit[:2]

        # अच् (Vowel) की पहचान
        self.is_vowel = self.char in INDEPENDENT_VOWELS or '३' in self.char

        # १.२.२७ और नियमों के आधार पर मात्रा निर्धारण
        self.matra = self._calculate_matra(self.char)

        # संज्ञा स्लॉट्स
        self.kala_sanjna = None  # logic/kala_rules.py द्वारा भरा जाएगा
        self.svara = "उदात्त"  # डिफ़ॉल्ट (१.२.२९)
        self.svara_mark = None

        # १.१.८: मुखनासिकावचनोऽनुनासिकः (चंद्रबिंदु की पहचान)
        self.is_anunasika = 'ँ' in raw_unit

        # १.१.९: स्थान एवं प्रयत्न
        self.sthana = None  # logic/sthana_rules.py द्वारा भरा जाएगा
        self.prayatna = None

        # --- डायग्नोस्टिक प्रोसेस: संज्ञाएँ अपडेट करना ---

        # १. पिच (Pitch) अपडेट करें
        apply_svara_sanjna(self, raw_unit)

        # २. उच्चारण स्थान (Sthana) अपडेट करें - (अकुहविसर्जनीयानां कण्ठः आदि)
        apply_sthana_to_varna(self)

    def _calculate_matra(self, char):
        """
        पाणिनीय नियमों (१, २, ३) का कड़ाई से पालन।
        """
        if char in 'ंःँ': return 0
        if '३' in char: return 3
        if char == 'ऌ' or char == 'ॡ': return 1  # नियम २: दीर्घाभाव
        if char in ['ए', 'ओ', 'ऐ', 'औ']: return 2  # नियम ३: ह्रस्वाभाव
        if char in MATRA_DATA: return MATRA_DATA[char]
        if '्' in char: return 0.5  # व्यञ्जनमर्धमात्रिकम्
        return 0

    def __repr__(self):
        # क्लीन रिप्रजेंटेशन: अ(१)[ह्रस्व][उदात्त][निरनुनासिक][कण्ठ]
        kala = f"[{self.kala_sanjna}]" if self.kala_sanjna else ""
        svara = f"[{self.svara}]" if self.is_vowel else ""
        anu = "[अनुनासिक]" if self.is_anunasika else "[निरनुनासिक]"
        sth = f"[{self.sthana}]" if self.sthana else ""
        return f"{self.char}({self.matra}){kala}{svara}{anu}{sth}"

# --- २. विच्छेद इंजन (16 Rules + Svara & Anunasika Patch) ---
def sanskrit_varna_vichhed(text, return_objects=True):
    """
    पाणिनीय १६-नियमों पर आधारित वर्ण-विच्छेद।
    Surgical Patch: अब यह स्वर-चिह्न (॒ ॑) और अनुनासिक (ँ) को स्वर के साथ ही पकड़ेगा।
    """
    if not text:
        return []

    # नियम १६, ३, १२: मूल रिप्लेसमेंट
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

            # १. स्वतंत्र स्वर (Independent Vowels)
            if char in INDEPENDENT_VOWELS:
                current_unit = char
                if i + 1 < len(text) and text[i + 1] == '३':
                    current_unit += '३'
                    i += 1

                # --- SURGICAL PATCH UPDATE: स्वर-चिह्न और अनुनासिक की जाँच ---
                while i + 1 < len(text) and text[i + 1] in '\u0331\u030d_॒॑|ँ':
                    current_unit += text[i + 1]
                    i += 1

                res_strings.append(current_unit)

                # स्वर के बाद अयोगवाह
                while i + 1 < len(text) and text[i + 1] in 'ंःँ':
                    if text[i + 1] == 'ं' and (i + 2 == len(text) or text[i + 2] == ' '):
                        res_strings.append('म्')
                    else:
                        res_strings.append(text[i + 1])
                    i += 1

            # २. व्यंजन प्रबंधन (Inherent Vowel & Matra Injection)
            elif '\u0915' <= char <= '\u0939' or char == 'ळ':
                res_strings.append(char + '्')
                found_vowel = False

                if i + 1 < len(text):
                    next_char = text[i + 1]
                    if next_char == '्':
                        i += 1
                        found_vowel = True
                    elif next_char in VOWELS_MAP:
                        vowel_unit = VOWELS_MAP[next_char]
                        i += 1

                        # --- SURGICAL PATCH UPDATE: मात्रा के बाद चिह्न/अनुनासिक ---
                        while i + 1 < len(text) and text[i + 1] in '\u0331\u030d_॒॑|ँ':
                            vowel_unit += text[i + 1]
                            i += 1

                        res_strings.append(vowel_unit)
                        found_vowel = True

                        # मात्रा के बाद अयोगवाह
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


# --- ३. संयोग इंजन ---
def sanskrit_varna_samyoga(varna_list):
    """
    विच्छेदित वर्णों को पुनः जोड़ना।
    """
    combined = ""
    for v in varna_list:
        char = v.char if isinstance(v, Varna) else v
        if char in 'ंःँ':
            combined += char
        elif char in REVERSE_VOWELS_MAP and combined.endswith('्'):
            combined = combined[:-1] + REVERSE_VOWELS_MAP[char]
        elif char == 'अ' and combined.endswith('्'):
            combined = combined[:-1]
        else:
            combined += char
    return combined