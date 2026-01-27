import re

def sanskrit_varna_vichhed(text):
    """
    पाणिनीय अष्टाध्यायी के 16 नियमों पर आधारित पूर्ण शुद्ध कोड।
    'एधँ', 'लाँ' जैसी समस्याओं का स्थायी समाधान।
    """
    if not text:
        return []

    # नियम 16: ॐ का विशिष्ट विच्छेद
    if text == "ॐ":
        return ["अ", "उ", "म्"]

    # संयुक्ताक्षर और अवग्रह प्रबंधन
    text = text.replace('क्ष', 'क्‌ष').replace('त्र', 'त्‌र').replace('ज्ञ', 'ज्‌ञ').replace('श्र', 'श्‌र').replace('ऽ', 'अ')

    # अनुस्वार नियम (पञ्चम वर्ण)
    text = re.sub(r'ं(?=[कखगघ])', 'ङ्', text)
    text = re.sub(r'ं(?=[चछजझ])', 'ञ्', text)
    text = re.sub(r'ं(?=[टठडढ])', 'ण्', text)
    text = re.sub(r'ं(?=[तथदध])', 'न्', text)
    text = re.sub(r'ं(?=[पफबभ])', 'म्', text)

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

        # 1. स्वतंत्र स्वर (ए, ओ, आदि)
        if char in independent_vowels:
            res.append(char)
            i += 1
            if i < len(text) and text[i] == '३':
                res[-1] += '३'; i += 1
            while i < len(text) and text[i] in 'ंःँ':
                res.append(text[i]); i += 1
            continue

        # 2. व्यंजन प्रबंधन (Fix for एधँ - 'ध' के बाद 'अ' का इन्जेक्शन)
        elif '\u0915' <= char <= '\u0939' or char == 'ळ':
            res.append(char + '्')
            i += 1

            # व्यंजन के बाद क्या है? (Surgical Check)
            if i < len(text):
                if text[i] == '्': # शुद्ध हलन्त
                    i += 1
                elif text[i] in vowels_map: # मात्रा (ा, ि, ी...)
                    res.append(vowels_map[text[i]])
                    i += 1
                else:
                    # यदि आगे कुछ नहीं है या सीधे अयोगवाह (ंःँ) है, तो 'अ' अनिवार्य है
                    res.append('अ')
            else:
                # शब्द का अंत व्यंजन पर हुआ तो 'अ' अनिवार्य (नियम 1)
                res.append('अ')

            # अयोगवाह (अनुनासिक 'ँ' यहाँ जुड़ेगा)
            while i < len(text) and text[i] in 'ंःँ':
                res.append(text[i])
                i += 1
            continue

        else:
            i += 1

    return res

def sanskrit_varna_samyoga(varna_list):
    """वर्णों का शुद्ध पुनर्निर्माण"""
    combined = ""
    vowels_map = {'आ': 'ा', 'इ': 'ि', 'ई': 'ी', 'उ': 'ु', 'ऊ': 'ू', 'ऋ': 'ृ', 'ॠ': 'ॄ', 'ऌ': 'ॢ', 'ॡ': 'ॣ', 'ए': 'े', 'ऐ': 'ै', 'ओ': 'ो', 'औ': 'ौ'}
    for varna in varna_list:
        if varna in vowels_map and combined.endswith('्'):
            combined = combined[:-1] + vowels_map[varna]
        elif varna == 'अ' and combined.endswith('्'):
            combined = combined[:-1]
        else:
            combined += varna
    return combined