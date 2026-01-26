import re

def sanskrit_varna_vichhed(text):
    """
    पाणिनीय अष्टाध्यायी नियमों के आधार पर संस्कृत वर्ण-विच्छेद।
    रिटर्न: वर्णों की सूची (List of characters)
    """
    if not text:
        return []

    # नियम 16: ॐ का विशिष्ट विच्छेद (अपवाद)
    if text == "ॐ":
        return ["अ", "उ", "म्"]

    # नियम 3 और 12: विशिष्ट संयुक्ताक्षर और अवग्रह
    text = text.replace('क्ष', 'क्‌ष').replace('त्र', 'त्‌र').replace('ज्ञ', 'ज्‌ञ').replace('श्र', 'श्‌र').replace('ऽ', 'अ')

    # नियम 6: पञ्चम वर्ण नियम
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

        # 1. स्वतंत्र स्वर और प्लुत प्रबंधन (नियम 9, 10, 14, 15)
        if char in independent_vowels:
            current_unit = char
            if i + 1 < len(text) and text[i + 1] == '३':
                current_unit += '३'
                i += 1
            res.append(current_unit)

            while i + 1 < len(text) and text[i + 1] in 'ंःँ':
                if text[i + 1] == 'ं' and (i + 2 == len(text) or text[i + 2] == ' '):
                    res.append('म्')
                else:
                    res.append(text[i + 1])
                i += 1

        # 2. व्यंजन प्रबंधन (नियम 1, 2, 4, 5, 11, 13)
        elif '\u0915' <= char <= '\u0939' or char == 'ळ':
            res.append(char + '्')
            if i + 1 < len(text):
                next_char = text[i + 1]
                if next_char == '्':
                    i += 1
                elif next_char in vowels_map:
                    res.append(vowels_map[next_char])
                    i += 1
                    while i + 1 < len(text) and text[i + 1] in 'ंःँ':
                        if text[i + 1] == 'ं' and (i + 2 == len(text) or text[i + 2] == ' '):
                            res.append('म्')
                        else:
                            res.append(text[i + 1])
                        i += 1
                elif next_char in 'ंःँ':
                    res.append('अ')
                    if next_char == 'ं' and (i + 2 == len(text) or text[i + 2] == ' '):
                        res.append('म्')
                    else:
                        res.append(next_char)
                    i += 1
                elif next_char == ' ':
                    res.append('अ')
                else:
                    res.append('अ')
            else:
                res.append('अ')

        elif char in 'ᳲᳳ':
            res.append(char)
        i += 1

    return res