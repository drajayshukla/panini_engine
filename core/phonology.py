import re


def sanskrit_varna_vichhed(text):
    if not text:
        return []

    # नियम 16: ॐ का विशिष्ट विच्छेद
    if text == "ॐ":
        return ["अ", "उ", "म्"]

    # नियम 3 और 12: संयुक्ताक्षर (क्ष, त्र, ज्ञ, श्र) और अवग्रह (ऽ)
    # यहाँ ZWNJ हटाकर शुद्ध विच्छेद सुनिश्चित किया गया है
    text = text.replace('क्ष', 'क्‌ष').replace('त्र', 'त्‌र').replace('ज्ञ', 'ज्‌ञ').replace('श्र', 'श्‌र').replace('ऽ',
                                                                                                                    'अ')

    # नियम 6 और 7: पञ्चम वर्ण और अनुस्वार अपवाद (स्पर्श व्यंजन vs य-र-ल-व)
    # 'नश्चापदान्तस्य झलि' के अनुसार स्पर्श व्यंजनों से पहले परिवर्तन
    text = re.sub(r'ं(?=[कखगघ])', 'ङ्', text)
    text = re.sub(r'ं(?=[चछजझ])', 'ञ्', text)
    text = re.sub(r'ं(?=[टठडढ])', 'ण्', text)
    text = re.sub(r'ं(?=[तथदध])', 'न्', text)
    text = re.sub(r'ं(?=[पफबभ])', 'म्', text)
    # नियम 16 (Standard): अंत में आने वाला अनुस्वार 'म्' बनता है
    if text.endswith('ं'):
        text = text[:-1] + 'म्'

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

        # --- स्वर और प्लुत (नियम 9, 10, 14, 15) ---
        if char in independent_vowels:
            res.append(char)
            # प्लुत (ओ३)
            if i + 1 < len(text) and text[i + 1] == '३':
                res[-1] += '३'
                i += 1
            # अनुनासिक/विसर्ग स्वर के आश्रित (अँ, अः)
            while i + 1 < len(text) and text[i + 1] in 'ंःँ':
                res.append(text[i + 1])
                i += 1

        # --- व्यंजन (नियम 1, 2, 4, 5, 11, 13) ---
        elif '\u0915' <= char <= '\u0939' or char == 'ळ':
            res.append(char + '्')  # हलन्त व्यंजन

            has_vowel = False
            if i + 1 < len(text):
                next_char = text[i + 1]

                if next_char == '्':  # हलन्त (जैसे 'जगत्')
                    i += 1
                    has_vowel = True
                elif next_char in vowels_map:  # मात्रा (जैसे 'का', 'को')
                    res.append(vowels_map[next_char])
                    i += 1
                    has_vowel = True
                elif next_char in 'ंःँ':  # व्यंजन के बाद सीधे अयोगवाह (जैसे 'कँ')
                    res.append('अ')  # स्वर देना अनिवार्य है
                    has_vowel = True

                    # नियम 1 & 11: यदि स्वर/हलन्त नहीं है, तो 'अ' जोड़ें (सिवाय शब्द के अंत के हलन्त के)
            if not has_vowel:
                res.append('अ')

            # व्यंजन/स्वर के बाद अनुस्वार/विसर्ग/अनुनासिक (नियम 14, 15)
            while i + 1 < len(text) and text[i + 1] in 'ंःँ':
                res.append(text[i + 1])
                i += 1

        # नियम 8: अयोगवाह (जिह्वामूलीय/उपध्मानीय)
        elif char in 'ᳲᳳ':
            res.append(char)

        i += 1
    return res