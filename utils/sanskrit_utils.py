# panini_engine/utils/sanskrit_utils.py

import re

def normalize_sanskrit_text(text):
    """
    Sutra: परः संनिकर्षः संहिता (१.४.१०९)
    Logic: Establishes phonetic proximity (Saṃhitā) by removing
    artificial whitespace or non-phonemic markers.
    """
    if not text:
        return ""
    # Removing 'Vivrtti' (gaps) to allow Sandhi and It-rules to see neighbors
    text = text.strip()
    return text

def is_vowel(char):
    """
    Sutra: अचश्च (१.२.२८) / 'अच्' प्रत्याहार
    Clinical Check: Identifies if a character belongs to the 'Ac' range.
    """
    # The 'Ac' pratyahara represents the universal set of vowels
    vowels = 'अआइईउऊऋॠऌॡएऐओऔ'
    return char in vowels

def strip_halant(char):
    """
    Concept: उच्चारणार्थः अकारः (Standard Paribhāṣā)
    Logic: Removes the indicator of a pure consonant (Hal) to
    reveal the base phonetic unit for lookup or display.
    """
    return char.replace('्', '')

def add_halant(char):
    """
    Sutra: हलन्त्यम् (१.३.३) / हल्-लक्षणम्
    Logic: Marks a varna as a pure 'Hal' (consonant) by ensuring
    it is not associated with an inherent 'a' (अकार).
    """
    # Exclude markers and vowels
    vowels = 'अआइईउऊऋॠऌॡएऐओऔँ'
    if char not in vowels and not char.endswith('्'):
        return char + '्'
    return char

def get_varna_count(text):
    """
    Sutra: अलोऽन्त्यात् पूर्व उपधा (१.१.६५) context.
    Logic: Performs a full 'Vichheda' to count individual 'Al' units
    (phonemes), which is essential for identifying Upadhā or Ti boundaries.
    """
    from core.phonology import ad
    # Uses the 'ad' physiological basis to count real phonemes, not characters
    return len(ad(text))