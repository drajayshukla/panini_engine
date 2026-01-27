import re

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
    def __init__(self, char):
        self.char = char
        self.is_vowel = char in INDEPENDENT_VOWELS or '३' in char
        # १.२.२७ और आपके द्वारा बताए गए ३ नियमों के आधार पर मात्रा
        self.matra = self._calculate_matra(char)
        self.sthana = None
        self.prayatna = None
        self.svara = "उदात्त"
        self.kala_sanjna = None

    def _calculate_matra(self, char):
        # नियम १, २, ३ का क्रियान्वयन

        # अयोगवाह (ं, ः) के लिए
        if char in 'ंःँ': return 0

        # १. प्लुत प्रबंधन (३ मात्रा) - सभी स्वरों के लिए संभव (नियम १, २, ३)
        if '३' in char:
            return 3

        # २. ऌ-कार का विशेष नियम (नियम २)
        # 'ऌ' का दीर्घ नहीं होता, यदि कोई 'ॡ' (दीर्घ ऌ) दे, तो उसे अमान्य या ह्रस्व मानें
        if char == 'ऌ': return 1
        if char == 'ॡ': return 1  # पाणिनीय व्याकरण में दीर्घ ऌ का अभाव है

        # ३. सन्ध्यक्षर (ए, ऐ, ओ, औ) का विशेष नियम (नियम ३)
        # इनका ह्रस्व नहीं होता, ये हमेशा न्यूनतम २ मात्रा के होते हैं
        if char in ['ए', 'ओ', 'ऐ', 'औ']:
            return 2

        # ४. सामान्य स्वर (अ, इ, उ, ऋ) (नियम १)
        if char in MATRA_DATA:
            return MATRA_DATA[char]

        # ५. व्यञ्जनमर्धमात्रिकम्
        if '्' in char:
            return 0.5

        return 0

    def __repr__(self):
        return f"{self.char}({self.matra})"
# --- २. विच्छेद इंजन (Your Original Logic Preserved) ---
def sanskrit_varna_vichhed(text, return_objects=True):
    """
    पाणिनीय १६-नियमों पर आधारित वर्ण-विच्छेद।
    return_objects=True रखने पर यह Varna Objects की लिस्ट देगा।
    """
    if not text:
        return []

    # --- आपका मूल विच्छेद लॉजिक (START) ---
    if text == "ॐ":
        res_strings = ["अ", "उ", "म्"]
    else:
        text = text.replace('क्ष', 'क्‌ष').replace('त्र', 'त्‌र').replace('ज्ञ', 'ज्‌ञ').replace('श्र', 'श्‌र').replace(
            'ऽ', 'अ')
        text = re.sub(r'ं(?=[कखगघ])', 'ङ्', text)
        text = re.sub(r'ं(?=[चछजझ])', 'ञ्', text)
        text = re.sub(r'ं(?=[टठडढ])', 'ण्', text)
        text = re.sub(r'ं(?=[तथदध])', 'न्', text)
        text = re.sub(r'ं(?=[पफबभ])', 'म्', text)

        res_strings = []
        i = 0
        while i < len(text):
            char = text[i]
            if char in INDEPENDENT_VOWELS:
                current_unit = char
                if i + 1 < len(text) and text[i + 1] == '३':
                    current_unit += '३'
                    i += 1
                res_strings.append(current_unit)
                while i + 1 < len(text) and text[i + 1] in 'ंःँ':
                    if text[i + 1] == 'ं' and (i + 2 == len(text) or text[i + 2] == ' '):
                        res_strings.append('म्')
                    else:
                        res_strings.append(text[i + 1])
                    i += 1
            elif '\u0915' <= char <= '\u0939' or char == 'ळ':
                res_strings.append(char + '्')
                found_vowel = False
                if i + 1 < len(text):
                    next_char = text[i + 1]
                    if next_char == '्':
                        i += 1
                        found_vowel = True
                    elif next_char in VOWELS_MAP:
                        res_strings.append(VOWELS_MAP[next_char])
                        i += 1
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
    # --- आपका मूल विच्छेद लॉजिक (END) ---

    # अब इसे Objects में बदलें या Strings ही रहने दें
    if return_objects:
        return [Varna(s) for s in res_strings]
    return res_strings


# --- ३. संयोग इंजन ---
def sanskrit_varna_samyoga(varna_list):
    combined = ""
    for v in varna_list:
        # अगर Varna Object है तो .char लें, वरना सीधा स्ट्रिंग लें
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
