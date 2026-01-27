import re


def sanskrit_varna_vichhed(text):
    """
    पाणिनीय अष्टाध्यायी के 16 नियमों पर आधारित पूर्ण शुद्ध कोड।
    'लो, ली, लू, लाँ' और 'एधँ' जैसी समस्याओं का स्थायी समाधान।
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

    # नियम 16 (Standard): अंत में आने वाला अनुस्वार 'म्' में बदलना
    if text.endswith('ं'):
        text = text[:-1] + 'म्'

    vowels_map = {
        'ा': 'आ', 'ि': 'इ', 'ी': 'ई', 'ु': 'उ', 'ू': 'ऊ',
        'ृ': 'ऋ', 'ॄ': 'ॠ', 'ॢ': 'ऌ', 'ॣ': 'ॡ',
        'े': 'ए', 'ै': 'ऐ', 'ो': 'ओ', 'ौ': 'औ'
    }
    independent_vowels = set('अआइईउऊऋॠऌॡएऐओऔ')

    res = []
    i = 0
    while i < len(text):
        char = text[i]

        # 1. स्वतंत्र स्वर प्रबंधन (Independent Vowels)
        if char in independent_vowels:
            res.append(char)
            i += 1
            if i < len(text) and text[i] == '३':  # प्लुत स्वर
                res[-1] += '३'
                i += 1
            # स्वर के आश्रित अनुस्वार/विसर्ग/अनुनासिक
            while i < len(text) and text[i] in 'ंःँ':
                res.append(text[i])
                i += 1
            continue

        # 2. व्यंजन प्रबंधन (Fix for एधँ, लाँ, टी, मे)
        elif '\u0915' <= char <= '\u0939' or char == 'ळ':
            res.append(char + '्')
            i += 1

            found_vowel = False
            if i < len(text):
                if text[i] == '्':  # शुद्ध हलन्त
                    i += 1
                    found_vowel = True
                elif text[i] in vowels_map:  # मात्रा
                    res.append(vowels_map[text[i]])
                    i += 1
                    found_vowel = True
                elif text[i] in 'ंःँ':  # सीधे अयोगवाह (जैसे एधँ का धँ)
                    res.append('अ')  # अनुनासिक चिन्ह से पहले 'अ' जोड़ना अनिवार्य है
                    found_vowel = True

            # यदि कोई मात्रा/हलन्त नहीं मिला, तो 'अ' अनिवार्य है (नियम 1)
            if not found_vowel:
                res.append('अ')

            # व्यंजन/स्वर के बाद अनुस्वार/विसर्ग/अनुनासिक (नियम 14, 15)
            while i < len(text) and text[i] in 'ंःँ':
                res.append(text[i])
                i += i if i >= len(text) else 1
                # नोट: यहाँ i += 1 का प्रयोग सुरक्षित है

            # ऊपर वाले loop में i update करने का सही तरीका:
            # while i < len(text) and text[i] in 'ंःँ':
            #     res.append(text[i])
            #     i += 1
            continue

        # 3. अयोगवाह चिह्न
        elif char in 'ᳲᳳ':
            res.append(char)
            i += 1
        else:
            i += 1

    return res


def sanskrit_varna_samyoga(varna_list):
    """
    वर्णों को जोड़कर शुद्ध रूप बनाना (Surgical Reconstruction)
    """
    combined = ""
    vowels_map = {
        'आ': 'ा', 'इ': 'ि', 'ई': 'ी', 'उ': 'ु', 'ऊ': 'ू',
        'ऋ': 'ृ', 'ॠ': 'ॄ', 'ऌ': 'ॢ', 'ॡ': 'ॣ',
        'ए': 'े', 'ऐ': 'ै', 'ओ': 'ो', 'औ': 'ौ'
    }

    for varna in varna_list:
        if varna in vowels_map and combined.endswith('्'):
            combined = combined[:-1] + vowels_map[varna]
        elif varna == 'अ' and combined.endswith('्'):
            combined = combined[:-1]
        else:
            combined += varna
    return combined