import re


def sanskrit_varna_vichhed(text):
    """
    पाणिनीय अष्टाध्यायी नियमों के आधार पर वैज्ञानिक संस्कृत वर्ण-विच्छेद।
    'कुलँ' -> ['क्', 'उ', 'ल्', 'अ', 'ँ']
    """
    if not text:
        return []

    # १. ॐ का विशिष्ट विच्छेद (नियम १६)
    if text == "ॐ":
        return ["अ", "उ", "म्"]

    # २. विशिष्ट संयुक्ताक्षर और अवग्रह प्रबंधन
    # '‌' (Zero Width Non-Joiner) का प्रयोग विच्छेद दिखाने के लिए
    text = text.replace('क्ष', 'क्‌ष').replace('त्र', 'त्‌र').replace('ज्ञ', 'ज्‌ञ').replace('श्र', 'श्‌र').replace('ऽ',
                                                                                                                    'अ')

    # ३. अनुस्वार का पञ्चम वर्ण में परिवर्तन (संधि नियम)
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

        # ४. स्वतंत्र स्वर और प्लुत प्रबंधन
        if char in independent_vowels:
            res.append(char)
            # प्लुत (३) की जाँच
            if i + 1 < len(text) and text[i + 1] == '३':
                res[-1] += '३'
                i += 1
            # स्वर के बाद अनुनासिक/विसर्ग की जाँच (जैसे 'अँ')
            while i + 1 < len(text) and text[i + 1] in 'ंःँ':
                res.append(text[i + 1])
                i += 1

        # ५. व्यंजन प्रबंधन (मुख्य सुधार यहाँ है)
        elif '\u0915' <= char <= '\u0939' or char == 'ळ':
            res.append(char + '्')  # पहले व्यंजन को हलन्त करें

            if i + 1 < len(text):
                next_char = text[i + 1]

                # केस १: व्यंजन के बाद हलन्त लगा हो (जैसे 'क्')
                if next_char == '्':
                    i += 1

                    # केस २: व्यंजन के बाद कोई स्वर मात्रा हो (जैसे 'कु')
                elif next_char in vowels_map:
                    res.append(vowels_map[next_char])
                    i += 1
                    # मात्रा के बाद अनुनासिक चिन्ह (जैसे 'कुँ')
                    while i + 1 < len(text) and text[i + 1] in 'ंःँ':
                        res.append(text[i + 1])
                        i += 1

                # केस ३: व्यंजन के बाद सीधे अनुनासिक/विसर्ग हो (जैसे 'लँ')
                # यह 'कुलँ' के 'ल' के लिए है
                elif next_char in 'ंःँ':
                    res.append('अ')  # अंतर्निहित 'अ' जोड़ें
                    res.append(next_char)
                    i += 1

                # केस ४: व्यंजन पूर्ण है और आगे कोई चिन्ह नहीं (जैसे 'कुल' का 'ल')
                else:
                    res.append('अ')
            else:
                # शब्द के अंत में पूर्ण व्यंजन (जैसे 'राम')
                res.append('अ')

        elif char in 'ᳲᳳ':  # जिह्वामूलीय और उपध्मानीय
            res.append(char)

        i += 1

    return res