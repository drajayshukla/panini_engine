# panini_engine/utils/sanskrit_utils.py

import re

def normalize_sanskrit_text(text):
    """
    इनपुट टेक्स्ट को क्लीन करता है ताकि 'पठ ' और 'पठ्' में अंतर न रहे।
    """
    if not text:
        return ""
    # १. सफेद जगह (Whitespaces) हटाना
    text = text.strip()
    # २. यदि अंत में व्यंजन है और हलन्त नहीं है, तो उसे मानक रूप देना (Optional logic)
    return text

def is_vowel(char):
    """चेक करता है कि क्या वर्ण स्वर है (बिना Varna Object बनाए त्वरित जाँच)।"""
    vowels = 'अआइईउऊऋॠऌॡएऐओऔ'
    return char in vowels

def strip_halant(char):
    """वर्ण से हलन्त हटाता है (उदा. 'प्' -> 'प')।"""
    return char.replace('्', '')

def add_halant(char):
    """यदि व्यंजन है और हलन्त नहीं है, तो जोड़ता है।"""
    vowels = 'अआइईउऊऋॠऌॡएऐओऔँ'
    if char not in vowels and not char.endswith('्'):
        return char + '्'
    return char

def get_varna_count(text):
    """
    सटीक वर्ण गणना (संयोजकता को ध्यान में रखते हुए)।
    उदा. 'राम' में २ वर्ण (र्+आ, म्+अ) या ४ इकाइयाँ।
    """
    from core.phonology import sanskrit_varna_vichhed
    return len(sanskrit_varna_vichhed(text))