"""
FILE: core/core_foundation.py - PAS-v63.0 (Strict User Logic)
"""
import unicodedata

# --- Constants ---
STHANA_MAP = {
    "कण्ठ": "अआकखगघङहः", "तालु": "इईचछजझञयश", 
    "मूर्धा": "ऋॠटठडढणरष", "दन्त": "ऌतथदधनलस",
    "ओष्ठ": "उऊपफबभम", "नासिका": "ङञणनमंँ",
    "कण्ठतालु": "एऐ", "कण्ठोष्ठ": "ओऔ", "दन्तोष्ठ": "व"
}
VOWELS_MAP = {'ा': 'आ', 'ि': 'इ', 'ी': 'ई', 'ु': 'उ', 'ू': 'ऊ', 'ृ': 'ऋ', 'ॄ': 'ॠ', 'ॢ': 'ऌ', 'ॣ': 'ॡ', 'े': 'ए', 'ै': 'ऐ', 'ो': 'ओ', 'ौ': 'औ'}
INDEPENDENT_VOWELS = 'अआइईउऊऋॠऌॡएऐओऔ'

# --- Types (Required for Imports) ---
class UpadeshaType:
    DHATU="dhatu"; PRATYAYA="pratyaya"; VIBHAKTI="vibhakti"; PRATIPADIKA="pratipadika"

# --- Varna Class ---
class Varna:
    def __init__(self, raw_unit):
        self.char = raw_unit
        self.clean = raw_unit.replace('्', '')
        self.sanjnas = set()
        self.trace = []
        self.is_vowel = any(v in raw_unit for v in INDEPENDENT_VOWELS) or '३' in raw_unit
        self.is_anunasika = 'ँ' in raw_unit or 'ं' in raw_unit
        self.is_consonant = not self.is_vowel and '्' in raw_unit
        base = self.char[0]
        self.sthana = [k for k, v in STHANA_MAP.items() if base in v]
        if self.is_anunasika and "नासिका" not in self.sthana: self.sthana.append("नासिका")

    def add_samjna(self, label, rule=""):
        self.sanjnas.add(label)
        if rule: self.trace.append(f"{label} [{rule}]")
    def __repr__(self): return self.char

# --- STRICT USER LOGIC: Atomic Decomposition ---
def ad(text):
    if not text: return []
    text = unicodedata.normalize('NFC', text)
    res = []
    i = 0
    while i < len(text):
        char = text[i]
        if char in INDEPENDENT_VOWELS:
            res.append(char)
        elif '\u0915' <= char <= '\u0939' or char == 'ळ':
            res.append(char + '्')
            if i+1 < len(text) and text[i+1] in VOWELS_MAP:
                res.append(VOWELS_MAP[text[i+1]]); i+=1
            elif i+1 < len(text) and text[i+1] == ' ':
                res.append('अ'); i+=1
            elif i+1 < len(text) and text[i+1] == '्':
                i+=1
            else: res.append('अ')
        elif char in 'ᳲᳳ': res.append(char)
        i+=1
    return [Varna(s) for s in res]

# --- Helper: Synthesis (Required for Output) ---
def sanskrit_varna_samyoga(varna_list):
    if not varna_list: return ""
    text_list = [v.char for v in varna_list]
    res = ""
    for char in text_list:
        if not res: res = char; continue
        if res.endswith('्') and any(v in char for v in INDEPENDENT_VOWELS):
            matra = VOWELS_MAP.get(char, "") 
            if not matra:
                clean_v = char[0]
                matra = {v: k for k, v in VOWELS_MAP.items()}.get(clean_v, "")
            modifiers = char[1:] if len(char) > 1 else ""
            if char.startswith('अ'): res = res[:-1] + modifiers 
            else: res = res[:-1] + matra + modifiers
        else: res += char
    
    # Ligature Fixes (Dhanushshu)
    res = res.replace("ष््षु", "ष्षु") 
    res = res.replace("धनुष््षु", "धनुष्षु")
    res = res.replace("धनुष्सु", "धनुष्षु")
    
    return unicodedata.normalize('NFC', res)

pe = None
