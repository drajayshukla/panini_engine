import re


def sanskrit_varna_vichhed(text):
    if not text:
        return []

    # 1. ॐ और संयुक्ताक्षर (नियम 3, 12, 16)
    if text == "ॐ": return ["अ", "उ", "म्"]
    text = text.replace('क्ष', 'क्‌ष').replace('त्र', 'त्‌र').replace('ज्ञ', 'ज्‌ञ').replace('श्र', 'श्‌र').replace('ऽ',
                                                                                                                    'अ')

    # 2. पञ्चम वर्ण नियम (नियम 6, 7)
    text = re.sub(r'ं(?=[कखगघ])', 'ङ्', text)
    text = re.sub(r'ं(?=[चछजझ])', 'ञ्', text)
    text = re.sub(r'ं(?=[टठडढ])', 'ण्', text)
    text = re.sub(r'ं(?=[तथदध])', 'न्', text)
    text = re.sub(r'ं(?=[पफबभ])', 'म्', text)

    vowels_map = {
        'ा': 'आ', 'ि': 'इ', 'ी': 'ई', 'ु': 'उ', 'ू': 'ऊ',
        'ृ': 'ऋ', 'ॄ': 'ॠ', 'ॢ': 'लृ', 'ॣ': 'लॢ',
        'े': 'ए', 'ै': 'ऐ', 'ो': 'ओ', 'ौ': 'औ'
    }
    independent_vowels = 'अआइईउऊऋॠलृलॢएऐओऔ'

    res = []
    i = 0
    while i < len(text):
        char = text[i]

        # --- स्वर प्रबंधन ---
        if char in independent_vowels:
            res.append(char)
            idx = i + 1
            if idx < len(text) and text[idx] == '३':
                res[-1] += '३'
                idx += 1
            while idx < len(text) and text[idx] in 'ंःँ':
                res.append(text[idx])
                idx += 1
            i = idx
            continue

        # --- व्यंजन प्रबंधन (Fix for लं, ल, लो, ली, लू, लाँ) ---
        elif '\u0915' <= char <= '\u0939' or char == 'ळ':
            res.append(char + '्')
            idx = i + 1
            found_vowel = False

            if idx < len(text):
                if text[idx] == '्':  # हलन्त
                    idx += 1
                    found_vowel = True
                elif text[idx] in vowels_map:  # मात्रा
                    res.append(vowels_map[text[idx]])
                    idx += 1
                    found_vowel = True
                elif text[idx] in 'ंःँ':  # सीधे अनुस्वार/अनुनासिक
                    res.append('अ')
                    # यहाँ idx नहीं बढ़ाएंगे क्योंकि नीचे वाला while इसे लेगा
                    found_vowel = True

            if not found_vowel:
                res.append('अ')

            # व्यंजन/स्वर के बाद के चिह्न (ंःँ)
            while idx < len(text) and text[idx] in 'ंःँ':
                res.append(text[idx])
                idx += 1

            i = idx  # कर्सर को सीधे अगले अक्षर पर पहुँचाएं
            continue

        elif char in 'ᳲᳳ':
            res.append(char)

        i += 1
    return res