# utils/sanskrit_utils.py
import re


def sanskrit_varna_vichhed(text):
    """पाणिनीय १६-नियम विच्छेद (Centralized Utility)"""
    if not text: return []
    text = re.sub(r'[0-9०-९.]', '', text).strip()
    text = text.replace('क्ष', 'क्‌ष').replace('त्र', 'त्‌र').replace('ज्ञ', 'ज्‌ञ').replace('श्र', 'श्‌र')

    vowels_map = {'ा': 'आ', 'ि': 'इ', 'ी': 'ई', 'ु': 'उ', 'ू': 'ऊ', 'ृ': 'ऋ', 'ॄ': 'ॠ', 'ॢ': 'ऌ', 'ॣ': 'ॡ', 'े': 'ए',
                  'ै': 'ऐ', 'ो': 'ओ', 'ौ': 'औ'}
    independent_vowels = set('अआइईउऊऋॠऌॡएऐओऔ')

    res = []
    i = 0
    while i < len(text):
        char = text[i]
        if char in independent_vowels:
            res.append(char);
            i += 1
        elif '\u0915' <= char <= '\u0939' or char == 'ळ':
            res.append(char + '्');
            i += 1
            if i < len(text):
                if text[i] == '्':
                    i += 1
                elif text[i] in vowels_map:
                    res.append(vowels_map[text[i]]); i += 1
                elif text[i] not in 'ंःँ':
                    res.append('अ')
            else:
                res.append('अ')
        elif char in 'ंःँ':
            res.append(char); i += 1
        else:
            i += 1
    return res


def sanskrit_varna_samyoga(varna_list):
    """वर्णों को जोड़कर वापस शब्द बनाना"""
    combined = ""
    vowels_map = {'आ': 'ा', 'इ': 'ि', 'ई': 'ी', 'उ': 'ु', 'ऊ': 'ू', 'ऋ': 'ृ', 'ॠ': 'ॄ', 'ऌ': 'ॢ', 'ॡ': 'ॣ', 'ए': 'े',
                  'ऐ': 'ै', 'ओ': 'ो', 'औ': 'ौ'}
    for varna in varna_list:
        if varna in vowels_map and combined.endswith('्'):
            combined = combined[:-1] + vowels_map[varna]
        elif varna == 'अ' and combined.endswith('्'):
            combined = combined[:-1]
        else:
            combined += varna
    return combined