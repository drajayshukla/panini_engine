import re


def sanskrit_varna_vichhed(text):
    if not text:
        return []

    # नियम 16: ॐ और विशिष्ट संयुक्ताक्षर
    if text == "ॐ": return ["अ", "उ", "म्"]
    text = text.replace('क्ष', 'क्‌ष').replace('त्र', 'त्‌र').replace('ज्ञ', 'ज्‌ञ').replace('श्र', 'श्‌र').replace('ऽ',
                                                                                                                    'अ')

    # पञ्चम वर्ण नियम
    text = re.sub(r'ं(?=[कखगघ])', 'ङ्', text)
    text = re.sub(r'ं(?=[चछजझ])', 'ञ्', text)
    text = re.sub(r'ं(?=[टठडढ])', 'ण्', text)
    text = re.sub(r'ं(?=[तथदध])', 'न्', text)
    text = re.sub(r'ं(?=[पफबभ])', 'म्', text)

    # सुधारी गई मैपिंग: 'ॢ' स्वयं में स्वर है, इसे 'लृ' न लिखें
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

        # 1. स्वतंत्र स्वर (जैसे अ, इ, लृ)
        if char in independent_vowels:
            res.append(char)
            i += 1
            while i < len(text) and text[i] in 'ंःँ':
                res.append(text[i])
                i += 1
            continue

        # 2. व्यंजन प्रबंधन (लो, ली, लू, मे, कि फिक्स)
        elif '\u0915' <= char <= '\u0939' or char == 'ळ':
            res.append(char + '्')
            i += 1

            found_vowel = False
            if i < len(text):
                if text[i] == '्':  # हलन्त
                    i += 1
                    found_vowel = True
                elif text[i] in vowels_map:  # मात्रा
                    res.append(vowels_map[text[i]])
                    i += 1
                    found_vowel = True
                elif text[i] in 'ंःँ':  # सीधे अयोगवाह
                    res.append('अ')
                    found_vowel = True

            if not found_vowel:
                res.append('अ')

            while i < len(text) and text[i] in 'ंःँ':
                res.append(text[i])
                i += 1
            continue

        elif char in 'ᳲᳳ':
            res.append(char)
            i += 1
        else:
            i += 1

    return res