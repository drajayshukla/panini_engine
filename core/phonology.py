import re


def sanskrit_varna_vichhed(text):
    """
    पाणिनीय अष्टाध्यायी के 16 नियमों पर आधारित पूर्ण शुद्ध वर्ण-विच्छेद।
    विशेषता: यह 'अच्' (Vowels) और 'अयोगवाह' (Nasal/Visarga) को अलग-अलग रखता है,
    ताकि सूत्र 1.3.2 (उपदेशेऽजनुनासिक इत्) सटीक काम कर सके।
    """
    if not text:
        return []

    # नियम 16: ॐ का विशिष्ट विच्छेद
    if text == "ॐ":
        return ["अ", "उ", "म्"]

    # नियम 3, 12, 13: संयुक्ताक्षर और अवग्रह प्रबंधन
    text = text.replace('क्ष', 'क्‌ष').replace('त्र', 'त्‌र').replace('ज्ञ', 'ज्‌ञ').replace('श्र', 'श्‌र').replace('ऽ',
                                                                                                                    'अ')

    # नियम 6, 7: पञ्चम वर्ण और अनुस्वार नियम
    text = re.sub(r'ं(?=[कखगघ])', 'ङ्', text)
    text = re.sub(r'ं(?=[चछजझ])', 'ञ्', text)
    text = re.sub(r'ं(?=[टठडढ])', 'ण्', text)
    text = re.sub(r'ं(?=[तथदध])', 'न्', text)
    text = re.sub(r'ं(?=[पफबभ])', 'म्', text)

    # नियम 16: अंत में आने वाला अनुस्वार 'म्' में बदलना
    if text.endswith('ं'):
        text = text[:-1] + 'म्'

    # 'ॢ' (\u0962) की मैपिंग शुद्ध स्वर 'ऌ' (\u090c) में
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

        # 1. स्वतंत्र स्वर प्रबंधन (نियम 9, 10, 14, 15)
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

        # 2. व्यंजन प्रबंधन (Fix for लो, ली, लू, लाँ, टी, मे, कि)
        elif '\u0915' <= char <= '\u0939' or char == 'ळ':
            res.append(char + '्')  # शुद्ध हलन्त व्यंजन
            i += 1

            found_vowel = False
            if i < len(text):
                if text[i] == '्':  # हलन्त स्थिति
                    i += 1
                    found_vowel = True
                elif text[i] in vowels_map:  # मात्रा स्थिति
                    res.append(vowels_map[text[i]])
                    i += 1
                    found_vowel = True
                elif text[i] in 'ंःँ':  # सीधे अयोगवाह (जैसे लँ)
                    res.append('अ')  # अनुनासिक का आधार 'अ'
                    found_vowel = True

            # नियम 1: यदि कोई मात्रा नहीं मिली, तो 'अ' अनिवार्य है
            if not found_vowel:
                res.append('अ')

            # व्यंजन/स्वर के बाद अनुस्वार/विसर्ग/अनुनासिक
            while i < len(text) and text[i] in 'ंःँ':
                res.append(text[i])
                i += 1
            continue

        # 3. अयोगवाह चिह्न (जिह्वामूलीय ᳲ, उपध्मानीय ᳳ)
        elif char in 'ᳲᳳ':
            res.append(char)
            i += 1
        else:
            i += 1

    return res


def sanskrit_varna_samyoga(varna_list):
    """
    विच्छेदित वर्णों को पुनः जोड़कर शुद्ध शब्द बनाना।
    यह 'Separated' तत्वों (जैसे ['अ', 'ँ']) को भी सही ढंग से रिकन्स्ट्रक्ट करता है।
    """
    combined = ""
    vowels_map = {
        'आ': 'ा', 'इ': 'ि', 'ई': 'ी', 'उ': 'ु', 'ऊ': 'ू',
        'ऋ': 'ृ', 'ॠ': 'ॄ', 'ऌ': 'ॢ', 'ॡ': 'ॣ',
        'ए': 'े', 'ऐ': 'ै', 'ओ': 'ो', 'औ': 'ौ'
    }

    for varna in varna_list:
        # अगर वर्ण अयोगवाह (ं, ः, ँ) है, तो उसे सीधे जोड़ें
        if varna in 'ंःँ':
            combined += varna
        # अगर वर्ण मात्रा बनने योग्य स्वर है और पिछला वर्ण हलन्त है
        elif varna in vowels_map and combined.endswith('्'):
            combined = combined[:-1] + vowels_map[varna]
        # अगर वर्ण 'अ' है और पिछला वर्ण हलन्त है, तो बस हलन्त हटा दें
        elif varna == 'अ' and combined.endswith('्'):
            combined = combined[:-1]
        else:
            combined += varna
    return combined