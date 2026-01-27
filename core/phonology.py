import re

# --- व्याकरणिक स्थिरांक (Grammar Constants) ---
VOWELS_MAP = {
    'ा': 'आ', 'ि': 'इ', 'ी': 'ई', 'ु': 'उ', 'ू': 'ऊ',
    'ृ': 'ऋ', 'ॄ': 'ॠ', 'ॢ': 'ऌ', 'ॣ': 'ॡ',
    'े': 'ए', 'ै': 'ऐ', 'ो': 'ओ', 'ौ': 'औ'
}

REVERSE_VOWELS_MAP = {v: k for k, v in VOWELS_MAP.items()}
INDEPENDENT_VOWELS = 'अआइईउऊऋॠऌॡएऐओऔ'

def sanskrit_varna_vichhed(text):
    """
    पाणिनीय १६-नियमों पर आधारित वर्ण-विच्छेद।
    'Separation' मॉडल: यह अच् और अयोगवाह को पृथक रखता है।
    """
    if not text:
        return []

    # नियम 16: ॐ का विशिष्ट विच्छेद
    if text == "ॐ":
        return ["अ", "उ", "म्"]

    # नियम 3, 12: विशिष्ट संयुक्ताक्षर और अवग्रह प्रबंधन
    text = text.replace('क्ष', 'क्‌ष').replace('त्र', 'त्‌र').replace('ज्ञ', 'ज्‌ञ').replace('श्र', 'श्‌र').replace('ऽ', 'अ')

    # नियम 6: पञ्चम वर्ण (Anusvara to Nasal Consonant)
    text = re.sub(r'ं(?=[कखगघ])', 'ङ्', text)
    text = re.sub(r'ं(?=[चछजझ])', 'ञ्', text)
    text = re.sub(r'ं(?=[टठडढ])', 'ण्', text)
    text = re.sub(r'ं(?=[तथदध])', 'न्', text)
    text = re.sub(r'ं(?=[पफबभ])', 'म्', text)

    res = []
    i = 0
    while i < len(text):
        char = text[i]

        # 1. स्वतंत्र स्वर (Independent Vowels)
        if char in INDEPENDENT_VOWELS:
            current_unit = char
            if i + 1 < len(text) and text[i + 1] == '३':
                current_unit += '३'
                i += 1
            res.append(current_unit)

            # स्वर के बाद अयोगवाह (ंःँ)
            while i + 1 < len(text) and text[i + 1] in 'ंःँ':
                if text[i + 1] == 'ं' and (i + 2 == len(text) or text[i + 2] == ' '):
                    res.append('म्')
                else:
                    res.append(text[i + 1])
                i += 1

        # 2. व्यंजन प्रबंधन (Consonant Handling & Inherent Vowel Injection)
        elif '\u0915' <= char <= '\u0939' or char == 'ळ':
            res.append(char + '्')
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
                    # मात्रा के बाद अयोगवाह की जाँच
                    while i + 1 < len(text) and text[i + 1] in 'ंःँ':
                        if text[i + 1] == 'ं' and (i + 2 == len(text) or text[i + 2] == ' '):
                            res.append('म्')
                        else:
                            res.append(text[i + 1])
                        i += 1
                elif next_char in 'ंःँ':
                    res.append('अ') # 'अ' का इंजेक्शन
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

        # 3. विशेष चिह्न (ᳲ, ᳳ)
        elif char in 'ᳲᳳ':
            res.append(char)

        i += 1
    return res

def sanskrit_varna_samyoga(varna_list):
    """
    विच्छेदित वर्णों को पुनः जोड़कर शुद्ध रूप बनाना।
    Surgical Reconstruction Logic.
    """
    combined = ""
    for varna in varna_list:
        if varna in 'ंःँ':
            combined += varna
        elif varna in REVERSE_VOWELS_MAP and combined.endswith('्'):
            combined = combined[:-1] + REVERSE_VOWELS_MAP[varna]
        elif varna == 'अ' and combined.endswith('्'):
            combined = combined[:-1]
        else:
            combined += varna
    return combined