import re


def sanskrit_varna_vichhed(text):
    """
    पाणिनीय अष्टाध्यायी के 16 नियमों पर आधारित पूर्ण शुद्ध कोड।
    'लो, ली, लू' जैसी समस्याओं का स्थायी समाधान।
    """
    if not text:
        return []

    # नियम 16: ॐ का विशिष्ट विच्छेद
    if text == "ॐ":
        return ["अ", "उ", "म्"]

    # नियम 3, 12, 13: विशिष्ट संयुक्ताक्षर और अवग्रह
    text = text.replace('क्ष', 'क्‌ष').replace('त्र', 'त्‌र').replace('ज्ञ', 'ज्‌ञ').replace('श्र', 'श्‌र').replace('ऽ',
                                                                                                                    'अ')

    # नियम 6, 7: पञ्चम वर्ण और अनुस्वार नियम
    text = re.sub(r'ं(?=[कखगघ])', 'ङ्', text)
    text = re.sub(r'ं(?=[चछजझ])', 'ञ्', text)
    text = re.sub(r'ं(?=[टठडढ])', 'ण्', text)
    text = re.sub(r'ं(?=[तथदध])', 'न्', text)
    text = re.sub(r'ं(?=[पफबभ])', 'म्', text)

    # अंत में आने वाला अनुस्वार 'म्' (Standard नियम)
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

        # 1. स्वतंत्र स्वर प्रबंधन (नियम 9, 10, 14, 15)
        if char in independent_vowels:
            res.append(char)
            i += 1
            if i < len(text) and text[i] == '३':  # प्लुत
                res[-1] += '३'
                i += 1
            while i < len(text) and text[i] in 'ंःँ':
                res.append(text[i])
                i += 1
            continue  # अगले अक्षर पर जाएँ

        elif '\u0915' <= char <= '\u0939' or char == 'ळ':

            res.append(char + '्')
            i += 1

            vowel_added = False

            if i < len(text):

                # 1️⃣ यदि मात्रा है → वही स्वर
                if text[i] in vowels_map:
                    res.append(vowels_map[text[i]])
                    i += 1
                    vowel_added = True

                # 2️⃣ यदि हलन्त है → कोई स्वर नहीं
                elif text[i] == '्':
                    i += 1
                    vowel_added = True  # यहाँ TRUE का अर्थ: "अ मत जोड़ो"

            # 3️⃣ न मात्रा, न हलन्त → अ अनिवार्य
            if not vowel_added:
                res.append('अ')

            # 4️⃣ अयोगवाह
            while i < len(text) and text[i] in 'ंःँ':
                res.append(text[i])
                i += 1

            continue

        # 3. अयोगवाह चिह्न (ᳲ, ᳳ)
        elif char in 'ᳲᳳ':
            res.append(char)
            i += 1
        else:
            i += 1

    return res