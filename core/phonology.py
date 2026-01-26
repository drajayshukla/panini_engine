import re


def sanskrit_varna_vichhed(text):
    """
    पाणिनीय अष्टाध्यायी के 16 मास्टर नियमों पर आधारित
    सटीक संस्कृत वर्ण-विच्छेद (डॉ. अजय शुक्ला हेतु संशोधित)।
    """
    if not text:
        return []

    # नियम 16: ॐ का विशिष्ट विच्छेद
    if text == "ॐ":
        return ["अ", "उ", "म्"]

    # नियम 3, 12 & 13: विशिष्ट संयुक्ताक्षर, अवग्रह और द्वित्व
    text = text.replace('क्ष', 'क्‌ष').replace('त्र', 'त्‌र').replace('ज्ञ', 'ज्‌ञ').replace('श्र', 'श्‌र').replace('ऽ',
                                                                                                                    'अ')

    # नियम 6, 7 & 16: पञ्चम वर्ण और अनुस्वार नियम
    text = re.sub(r'ं(?=[कखगघ])', 'ङ्', text)
    text = re.sub(r'ं(?=[चछजझ])', 'ञ्', text)
    text = re.sub(r'ं(?=[टठडढ])', 'ण्', text)
    text = re.sub(r'ं(?=[तथदध])', 'न्', text)
    text = re.sub(r'ं(?=[पफबभ])', 'म्', text)

    # शब्द के अंत में अनुस्वार को 'म्' में बदलना
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

        # --- स्वर और प्लुत प्रबंधन (नियम 9, 10, 14, 15) ---
        if char in independent_vowels:
            res.append(char)
            # प्लुत (जैसे ओ३)
            if i + 1 < len(text) and text[i + 1] == '३':
                res[-1] += '३'
                i += 1
            # स्वर-आश्रित अनुनासिक/विसर्ग (जैसे अँ, अः)
            while i + 1 < len(text) and text[i + 1] in 'ंःँ':
                res.append(text[i + 1])
                i += 1

        # --- व्यंजन प्रबंधन (नियम 1, 2, 4, 5, 11 - लो, ली, लू फिक्स) ---
        elif '\u0915' <= char <= '\u0939' or char == 'ळ':
            res.append(char + '्')

            found_vowel = False
            if i + 1 < len(text):
                next_char = text[i + 1]

                if next_char == '्':  # शुद्ध हलन्त
                    i += 1
                    found_vowel = True
                elif next_char in vowels_map:  # मात्रा (जैसे लो -> ल् + ओ)
                    res.append(vowels_map[next_char])
                    i += 1
                    found_vowel = True
                elif next_char in 'ंःँ':  # सीधे अनुनासिक/अनुस्वार (जैसे लँ)
                    res.append('अ')
                    # यहाँ i नहीं बढ़ाएंगे ताकि अगले while में 'ंःँ' प्रोसेस हो सके
                    found_vowel = True

                    # यदि मात्रा या हलन्त नहीं मिला, तो 'अ' अनिवार्य है (नियम 1)
            if not found_vowel:
                res.append('अ')

            # व्यंजन के स्वर के बाद वाले अयोगवाह (नियम 14, 15)
            while i + 1 < len(text) and text[i + 1] in 'ंःँ':
                res.append(text[i + 1])
                i += 1

        # नियम 8: अयोगवाह (जिह्वामूलीय/उपध्मानीय)
        elif char in 'ᳲᳳ':
            res.append(char)

        i += 1
    return res


# --- टेस्ट रन ---
test_words = ["लो", "ली", "लू", "कुलँ", "प्र", "कर्म", "संवाद", "सिंहः"]
for word in test_words:
    print(f"{word} -> {' + '.join(sanskrit_varna_vichhed(word))}")