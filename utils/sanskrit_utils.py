import re


def sanskrit_varna_vichhed(text):
    """
    पाणिनि इंजन के लिए पूर्ण शुद्ध विच्छेद।
    नियम: अयोगवाह (ंःँ) को हमेशा पिछले स्वर के साथ जोड़ा जाता है।
    """
    if not text: return []
    if text == "ॐ": return ["अँ", "उ", "म्"]

    # संयुक्ताक्षर प्रतिस्थापन
    text = text.replace('क्ष', 'क्‌ष').replace('त्र', 'त्‌र').replace('ज्ञ', 'ज्‌ञ').replace('श्र', 'श्‌र').replace('ऽ',
                                                                                                                    'अ')

    # पञ्चम वर्ण प्रतिस्थापन
    text = re.sub(r'ं(?=[कखगघ])', 'ङ्', text)
    text = re.sub(r'ं(?=[चछजझ])', 'ञ्', text)
    text = re.sub(r'ं(?=[टठडढ])', 'ण्', text)
    text = re.sub(r'ं(?=[तथदध])', 'न्', text)
    text = re.sub(r'ं(?=[पफबभ])', 'म्', text)

    if text.endswith('ं'): text = text[:-1] + 'म्'

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

        # १. स्वतंत्र स्वर प्रबंधन
        if char in independent_vowels:
            vowel = char
            i += 1
            if i < len(text) and text[i] == '३':
                vowel += '३';
                i += 1
            # अयोगवाह को स्वर के साथ ही जोड़ें (e.g. अँ)
            while i < len(text) and text[i] in 'ंःँ':
                vowel += text[i];
                i += 1
            res.append(vowel)
            continue

        # २. व्यंजन प्रबंधन
        elif '\u0915' <= char <= '\u0939' or char == 'ळ':
            res.append(char + '्')
            i += 1

            found_vowel_marker = False
            vowel_to_add = ""

            if i < len(text):
                if text[i] == '्':
                    i += 1
                    found_vowel_marker = True  # हलन्त है तो 'अ' नहीं जोड़ेंगे
                elif text[i] in vowels_map:
                    vowel_to_add = vowels_map[text[i]]
                    i += 1
                    found_vowel_marker = True
                elif text[i] in 'ंःँ':
                    vowel_to_add = 'अ'  # अनुनासिक के लिए 'अ' का इंजेक्शन
                    found_vowel_marker = True

            if not found_vowel_marker:
                vowel_to_add = 'अ'

            # अयोगवाह को इस 'vowel_to_add' के साथ जोड़ें
            if vowel_to_add:
                while i < len(text) and text[i] in 'ंःँ':
                    vowel_to_add += text[i]
                    i += 1
                res.append(vowel_to_add)
            continue
        else:
            i += 1
    return res


def sanskrit_varna_samyoga(varna_list):
    """Reconstruction logic with merged vowel support."""
    combined = ""
    vowels_map = {
        'आ': 'ा', 'इ': 'ि', 'ई': 'ी', 'उ': 'ु', 'ऊ': 'ू',
        'ऋ': 'ृ', 'ॠ': 'ॄ', 'ऌ': 'ॢ', 'ॡ': 'ॣ',
        'ए': 'े', 'ऐ': 'ै', 'ओ': 'ो', 'औ': 'ौ'
    }
    for varna in varna_list:
        base_vowel = varna[0]  # 'अँ' में से 'अ' लें
        marker = varna[1:]  # 'अँ' में से 'ँ' लें

        if base_vowel in vowels_map and combined.endswith('्'):
            combined = combined[:-1] + vowels_map[base_vowel] + marker
        elif base_vowel == 'अ' and combined.endswith('्'):
            combined = combined[:-1] + marker
        else:
            combined += varna
    return combined