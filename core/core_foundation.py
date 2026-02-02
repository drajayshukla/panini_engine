"""
FILE: core/core_foundation.py - PAS-v7.7 (Absolute Authoritative Restoration)
"""
import re

STHANA_MAP = {
    "कण्ठ": "अआकखगघङहः", "तालु": "इईचछजझञयश", 
    "मूर्धा": "ऋॠटठडढणरष", "दन्त": "ऌतथदधनलस",
    "ओष्ठ": "उऊपफबभम", "नासिका": "ङञणनमंँ",
    "कण्ठतालु": "एऐ", "कण्ठोष्ठ": "ओऔ", "दन्तोष्ठ": "व"
}

VOWELS_MAP = {'ा': 'आ', 'ि': 'इ', 'ी': 'ई', 'ु': 'उ', 'ू': 'ऊ', 'ृ': 'ऋ', 'ॄ': 'ॠ', 'ॢ': 'ऌ', 'ॣ': 'ॡ', 'े': 'ए', 'ै': 'ऐ', 'ो': 'ओ', 'ौ': 'औ'}
REVERSE_VOWELS_MAP = {v: k for k, v in VOWELS_MAP.items()}
INDEPENDENT_VOWELS = 'अआइईउऊऋॠऌॡएऐओऔ'

class Varna:
    def __init__(self, raw_unit):
        self.char = raw_unit
        self.clean = raw_unit.replace('्', '')
        self.sanjnas = set()
        self.trace = []

        # Identity Checks
        self.is_vowel = any(v in raw_unit for v in INDEPENDENT_VOWELS) or '३' in raw_unit
        self.is_anunasika = 'ँ' in raw_unit
        self.is_consonant = not self.is_vowel and '्' in raw_unit

        # Phonetic Anatomy
        base = self.char[0]
        self.sthana = [k for k, v in STHANA_MAP.items() if base in v]
        if self.is_anunasika and "नासिका" not in self.sthana: self.sthana.append("नासिका")

    def add_samjna(self, label, rule=""):
        self.sanjnas.add(label)
        if rule: self.trace.append(f"{label} [{rule}]")

    def __repr__(self): return self.char

def sanskrit_varna_vichhed(text, return_objects=True):
    """
    R2: AUTHORITATIVE TOKENIZATION (Restored from your high-precision logic)
    """
    if not text: return []
    if text == "ॐ": res = ["अ", "उ", "म्"]
    else:
        text = text.replace('क्ष', 'क्‌ष').replace('त्र', 'त्‌र').replace('ज्ञ', 'ज्‌ञ').replace('श्र', 'श्‌र').replace('ऽ', 'अ')
        text = re.sub(r'ं(?=[कखगघ])', 'ङ्', text); text = re.sub(r'ं(?=[चछजझ])', 'ञ्', text)
        text = re.sub(r'ं(?=[टठडढ])', 'ण्', text); text = re.sub(r'ं(?=[तथदध])', 'न्', text)
        text = re.sub(r'ं(?=[पफबभ])', 'म्', text)

        res = []
        i = 0
        while i < len(text):
            char = text[i]
            if char in INDEPENDENT_VOWELS:
                unit = char
                if i+1 < len(text) and text[i+1] == '३': unit += '३'; i+=1
                res.append(unit)
                while i+1 < len(text) and text[i+1] in 'ंःँ':
                    if text[i+1] == 'ं' and (i+2==len(text) or text[i+2]==' '): res.append('म्')
                    else: res.append(text[i+1])
                    i+=1
            elif '\u0915' <= char <= '\u0939' or char == 'ळ':
                res.append(char + '्')
                found_vowel = False
                if i+1 < len(text):
                    nxt = text[i+1]
                    if nxt == '्': i+=1; found_vowel = True
                    elif nxt in VOWELS_MAP:
                        res.append(VOWELS_MAP[nxt]); i+=1; found_vowel = True
                        while i+1 < len(text) and text[i+1] in 'ंःँ':
                            if text[i+1] == 'ं' and (i+2==len(text) or text[i+2]==' '): res.append('म्')
                            else: res.append(text[i+1]); i+=1
                    elif nxt in 'ंःँ':
                        res.append('अ'); found_vowel = True
                        if nxt == 'ं' and (i+2==len(text) or text[i+2]==' '): res.append('म्')
                        else: res.append(nxt); i+=1
                    elif nxt == ' ': res.append('अ'); found_vowel = True
                if not found_vowel: res.append('अ')
            elif char in 'ᳲᳳ': res.append(char)
            i+=1
    return [Varna(s) for s in res] if return_objects else res

ad = sanskrit_varna_vichhed

def sanskrit_varna_samyoga(varna_list):
    if not varna_list: return ""
    text_list = [v.char for v in varna_list]
    res = ""
    for char in text_list:
        if not res: res = char; continue
        if res.endswith('्') and any(v in char for v in INDEPENDENT_VOWELS):
            matra = REVERSE_VOWELS_MAP.get(char[0], "") if char[0] != 'अ' else ""
            res = res[:-1] + matra
            if len(char) > 1: res += char[1:]
        else: res += char
    return res

class PratyaharaEngine:
    def __init__(self): self._cache = {}
    def get_varnas(self, name): return [] 

pe = PratyaharaEngine()

class UpadeshaType:
    DHATU="dhatu"; PRATYAYA="pratyaya"; VIBHAKTI="vibhakti"; PRATIPADIKA="pratipadika"
