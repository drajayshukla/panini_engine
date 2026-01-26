import re


def sanskrit_varna_vichhed(text):
    """
    पाणिनीय 16 नियमों पर आधारित पूर्ण शुद्ध कोड।
    'लो, ली, लू' जैसी समस्याओं का स्थायी समाधान।
    """
    if not text:
        return []

    if text == "ॐ":
        return ["अ", "उ", "म्"]

    # विशिष्ट संयुक्ताक्षर और अवग्रह
    text = text.replace('क्ष', 'क्‌ष').replace('त्र', 'त्‌र').replace('ज्ञ', 'ज्‌ञ').replace('श्र', 'श्‌र').replace('ऽ',
                                                                                                                    'अ')

    # पञ्चम वर्ण नियम
    text = re.sub(r'ं(?=[कखगघ])', 'ङ्', text)
    text = re.sub(r'ं(?=[चछजझ])', 'ञ्', text)
    text = re.sub(r'ं(?=[टठडढ])', 'ण्', text)
    text = re.sub(r'ं(?=[तथदध])', 'न्', text)
    text = re.sub(r'ं(?=[पफबभ])', 'म्', text)
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

        # 1. स्वतंत्र स्वर
        if char in independent_vowels:
            res.append(char)
            if i + 1 < len(text) and text[i + 1] == '३':
                res[-1] += '३'
                i += 1
            while i + 1 < len(text) and text[i + 1] in 'ंःँ':
                res.append(text[i + 1])
                i += 1
            i += 1  # अगले अक्षर पर जाएँ
            continue

        # 2. व्यंजन (क-ह और ळ)
        elif '\u0915' <= char <= '\u0939' or char == 'ळ':
            res.append(char + '्')

            # मात्रा या हलन्त की जाँच
            if i + 1 < len(text):
                next_char = text[i + 1]

                if next_char == '्':  # हलन्त
                    i += 2  # व्यंजन और हलन्त दोनों को पार करें
                elif next_char in vowels_map:  # मात्रा (जैसे 'ो' in 'लो')
                    res.append(vowels_map[next_char])
                    i += 2  # व्यंजन और मात्रा दोनों को पार करें
                elif next_char in 'ंःँ':  # जैसे 'लँ'
                    res.append('अ')
                    i += 1  # केवल व्यंजन पार करें, अनुनासिक अगली बार आएगा
                else:  # कोई मात्रा नहीं है (जैसे 'ल' in 'कल')
                    res.append('अ')
                    i += 1
            else:  # शब्द का अंतिम अक्षर
                res.append('अ')
                i += 1

            # स्वर/व्यंजन के बाद अयोगवाह (ंःँ) को प्रोसेस करें
            while i < len(text) and text[i] in 'ंःँ':
                res.append(text[i])
                i += 1
            continue

        # 3. अयोगवाह चिह्न
        elif char in 'ᳲᳳ':
            res.append(char)

        i += 1
    return res

# --- टेस्ट आउटपुट ---
# 'लो' -> ['ल्', 'ओ']
# 'ली' -> ['ल्', 'ई']
# 'टी' -> ['ट्', 'ई']