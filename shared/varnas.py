"""
FILE: shared/varnas.py
"""
import unicodedata

STHANA_MAP = {"कण्ठ": "अआकखगघङहः", "तालु": "इईचछजझञयश", "मूर्धा": "ऋॠटठडढणरष", "दन्त": "ऌतथदधनलस", "ओष्ठ": "उऊपफबभम", "नासिका": "ङञणनमंँ", "कण्ठतालु": "एऐ", "कण्ठोष्ठ": "ओऔ", "दन्तोष्ठ": "व"}
VOWELS_MAP = {'ा': 'आ', 'ि': 'इ', 'ी': 'ई', 'ु': 'उ', 'ू': 'ऊ', 'ृ': 'ऋ', 'ॄ': 'ॠ', 'ॢ': 'ऌ', 'ॣ': 'ॡ', 'े': 'ए', 'ै': 'ऐ', 'ो': 'ओ', 'ौ': 'औ'}
INDEPENDENT_VOWELS = 'अआइईउऊऋॠऌॡएऐओऔ'

class Varna:
    def __init__(self, raw_unit):
        self.char = raw_unit
        self.clean = raw_unit.replace('्', '')
        # Check for Nasalization (Anunāsika)
        self.is_anunasika = 'ँ' in raw_unit
        self.is_vowel = any(v in raw_unit for v in INDEPENDENT_VOWELS) or '३' in raw_unit
        self.is_consonant = not self.is_vowel and '्' in raw_unit
        self.sanjnas = set()
    def __repr__(self): return self.char

def ad(text):
    """
    Atomic Decomposition with Anunāsika Merging.
    Example: 'सुँ' -> ['स्', 'उँ'] (Not ['स्', 'उ', 'ँ'])
    """
    if not text: return []
    text = unicodedata.normalize('NFC', text)
    res = []
    i = 0
    while i < len(text):
        char = text[i]
        
        # 1. Independent Vowel (e.g., 'उ')
        if char in INDEPENDENT_VOWELS:
            unit = char
            # Merge Anunāsika if present
            if i+1 < len(text) and text[i+1] == 'ँ':
                unit += 'ँ'
                i += 1
            res.append(unit)
            
        # 2. Consonants (e.g., 'क', 'स')
        elif '\u0915' <= char <= '\u0939' or char == 'ळ':
            res.append(char + '्') # Pure Consonant
            
            # Look ahead for Vowel/Modifier
            if i+1 < len(text):
                nxt = text[i+1]
                
                # Case A: Matra (e.g., 'ु' -> 'उ')
                if nxt in VOWELS_MAP:
                    vowel = VOWELS_MAP[nxt]
                    i += 1
                    # Merge Anunāsika after Matra (e.g., 'ु' + 'ँ' -> 'उँ')
                    if i+1 < len(text) and text[i+1] == 'ँ':
                        vowel += 'ँ'; i += 1
                    res.append(vowel)
                
                # Case B: Virama (Halanta) -> No Vowel
                elif nxt == '्':
                    i += 1
                
                # Case C: Explicit Anunāsika on Consonant -> Implicit 'a' + 'ँ' (e.g. 'कँ')
                elif nxt == 'ँ':
                    res.append('अँ')
                    i += 1
                    
                # Case D: Space -> Implicit 'a'
                elif nxt == ' ':
                    res.append('अ')
                    i += 1
                    
                # Case E: Next is another Consonant -> Implicit 'a'
                else:
                    res.append('अ')
            else:
                # End of string -> Implicit 'a'
                res.append('अ')
        
        elif char in 'ᳲᳳ': res.append(char)
        i += 1
        
    return [Varna(s) for s in res]

def join(varna_list):
    # (Same synthesis logic)
    if not varna_list: return ""
    text_list = [v.char for v in varna_list]
    res = ""
    for char in text_list:
        if not res: res = char; continue
        if res.endswith('्') and any(v in char for v in INDEPENDENT_VOWELS):
            matra = VOWELS_MAP.get(char, "") 
            if not matra:
                clean_v = char.replace('ँ', '')
                matra = {v: k for k, v in VOWELS_MAP.items()}.get(clean_v, "")
            
            # Re-attach 'ँ' if it was part of the vowel
            if 'ँ' in char and 'ँ' not in matra: matra += 'ँ'
            
            if char.startswith('अ'): res = res[:-1] + (char.replace('अ', '')) 
            else: res = res[:-1] + matra
        else: res += char
    return res.replace("ष््षु", "ष्षु").replace("धनुष््षु", "धनुष्षु")
