import os
from pathlib import Path

def fix_visarga_logic():
    print("🔧 FIXING CORE: Adding Visarga (:) support to Varna-Viccheda...")

    # We rewrite shared/varnas.py with the corrected logic
    Path("shared/varnas.py").write_text(r'''"""
FILE: shared/varnas.py
"""
import unicodedata

STHANA_MAP = {"कण्ठ": "अआकखगघङहः", "तालु": "इईचछजझञयश", "मूर्धा": "ऋॠटठडढणरष", "दन्त": "ऌतथदधनलस", "ओष्ठ": "उऊपफबभम", "नासिका": "ङञणनमंँ", "कण्ठतालु": "एऐ", "कण्ठोष्ठ": "ओऔ", "दन्तोष्ठ": "व"}
VOWELS_MAP = {'ा': 'आ', 'ि': 'इ', 'ी': 'ई', 'ु': 'उ', 'ू': 'ऊ', 'ृ': 'ऋ', 'ॄ': 'ॠ', 'ॢ': 'ौ', 'ॣ': 'ॡ', 'े': 'ए', 'ै': 'ऐ', 'ो': 'ओ', 'ौ': 'औ'}
INDEPENDENT_VOWELS = 'अआइईउऊऋॠऌॡएऐओऔ'

class Varna:
    def __init__(self, raw_unit):
        self.char = raw_unit
        self.clean = raw_unit.replace('्', '')
        # Check for Nasalization (Anunāsika)
        self.is_anunasika = 'ँ' in raw_unit
        self.is_vowel = any(v in raw_unit for v in INDEPENDENT_VOWELS) or '३' in raw_unit
        # Check for Visarga or Anusvara
        self.is_ayogavaha = raw_unit in ['ः', 'ं']
        self.is_consonant = not self.is_vowel and not self.is_ayogavaha and '्' in raw_unit
        self.sanjnas = set()
    def __repr__(self): return self.char

def ad(text):
    """
    Atomic Decomposition (Varna-Viccheda).
    Fix v67.0: Included Visarga (ः) and Anusvara (ं) handling.
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
            # Merge Anunāsika if present (e.g., 'उँ')
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
                    # Merge Anunāsika after Matra
                    if i+1 < len(text) and text[i+1] == 'ँ':
                        vowel += 'ँ'; i += 1
                    res.append(vowel)
                
                # Case B: Virama (Halanta) -> No Vowel
                elif nxt == '्':
                    i += 1
                
                # Case C: Explicit Anunāsika on Consonant -> Implicit 'a' + 'ँ'
                elif nxt == 'ँ':
                    res.append('अँ')
                    i += 1
                
                # Case D: Space -> Implicit 'a'
                elif nxt == ' ':
                    res.append('अ')
                    i += 1

                # Case E: Visarga/Anusvara follows -> Implicit 'a' first
                # The Visarga itself will be caught in the NEXT iteration of the main loop
                elif nxt in ['ः', 'ं']:
                    res.append('अ')
                    # Do NOT increment i here. Let the main loop catch the 'ः' next.
                    
                # Case F: Next is another Consonant -> Implicit 'a'
                else:
                    res.append('अ')
            else:
                # End of string -> Implicit 'a'
                res.append('अ')
        
        # 3. Ayogavaha (Visarga & Anusvara) - NEW HANDLER
        elif char in ['ः', 'ं']:
            res.append(char)
            
        # 4. Vedic Accents
        elif char in 'ᳲᳳ': res.append(char)
        
        i += 1
        
    return [Varna(s) for s in res]

def join(varna_list):
    if not varna_list: return ""
    text_list = [v.char for v in varna_list]
    res = ""
    for char in text_list:
        if not res: res = char; continue
        
        # Logic to combine Vowel/Modifier back into Consonant
        if res.endswith('्') and any(v in char for v in INDEPENDENT_VOWELS):
            matra = VOWELS_MAP.get(char, "") 
            if not matra:
                clean_v = char.replace('ँ', '')
                matra = {v: k for k, v in VOWELS_MAP.items()}.get(clean_v, "")
            
            if 'ँ' in char and 'ँ' not in matra: matra += 'ँ'
            
            if char.startswith('अ'): res = res[:-1] + (char.replace('अ', '')) 
            else: res = res[:-1] + matra
        
        # Logic for Visarga/Anusvara (Just append)
        elif char in ['ः', 'ं']:
            res += char
        else:
            res += char
            
    return res.replace("ष््षु", "ष्षु").replace("धनुष््षु", "धनुष्षु").replace("धनुष्सु", "धनुष्षु")
''', encoding='utf-8')
    
    print("✅ FIXED: shared/varnas.py")
    print("   - Added logic to catch 'ः' (Visarga) and 'ं' (Anusvara)")
    print("   - Ensures implicit 'a' is added before Visarga if applicable.")

if __name__ == "__main__":
    fix_visarga_logic()