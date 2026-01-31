"""
FILE: core/core_foundation.py
PAS-v6.0 (Siddha) | PILLAR: The Physics (R1, R2, R17)
"""
import re

VOWELS_MAP = {'ा': 'आ', 'ि': 'इ', 'ी': 'ई', 'ु': 'उ', 'ू': 'ऊ', 'ृ': 'ऋ', 'ॄ': 'ॠ', 'ॢ': 'ऌ', 'ॣ': 'ॡ', 'े': 'ए', 'ै': 'ऐ', 'ो': 'ओ', 'ौ': 'औ'}
REVERSE_VOWELS_MAP = {v: k for k, v in VOWELS_MAP.items()}
INDEPENDENT_VOWELS = 'अआइईउऊऋॠऌॡएऐओऔ'
STHANA_MAP = {"कण्ठ": "अआकखगघङहः", "तालु": "इईचछजझञयश", "मूर्धा": "ऋॠटठडढणरष", "दन्त": "ऌतथदधनलस", "ओष्ठ": "उऊपफबभम", "नासिका": "ङञणनमंँ", "कण्ठतालु": "एऐ", "कण्ठोष्ठ": "ओऔ", "दन्तोष्ठ": "व"}

class Varna:
    def __init__(self, raw_unit):
        self.char = raw_unit

        # Identity Checks
        self.is_vowel = any(v in raw_unit for v in INDEPENDENT_VOWELS) or '३' in raw_unit
        self.is_anunasika = 'ँ' in raw_unit
        self.is_consonant = not self.is_vowel and '्' in raw_unit

        # [CRITICAL FIX]: These attributes are required by SanjnaController
        self.sanjnas = set()  # Tag storage
        self.trace = []       # History storage
        self.sthana = []      # Physics storage

        self._set_shiksha_profile()

    def _set_shiksha_profile(self):
        base = self.char[0]
        for place, chars in STHANA_MAP.items():
            if base in chars: self.sthana.append(place)
        if self.is_anunasika and "नासिका" not in self.sthana: self.sthana.append("नासिका")
    def __repr__(self): return self.char

def sanskrit_varna_vichhed(text, return_objects=True):
    """
    R2: Varnaviccheda - Robust Tokenization
    Handles complex cases like 'Su~' (सुँ) -> [s, u, ~]
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

            # CASE A: Independent Vowels (e.g., 'A')
            if char in INDEPENDENT_VOWELS:
                unit = char
                if i+1 < len(text) and text[i+1] == '३': unit += '३'; i+=1
                res.append(unit)
                # Consume modifiers (Anusvara/Visarga/Chandra)
                while i+1 < len(text) and text[i+1] in 'ंःँ':
                    if text[i+1] == 'ं' and (i+2==len(text) or text[i+2]==' '): res.append('म्')
                    else: res.append(text[i+1])
                    i+=1

            # CASE B: Consonants (e.g., 'K')
            elif '\u0915' <= char <= '\u0939' or char == 'ळ':
                res.append(char + '्')
                found_vowel = False

                if i+1 < len(text):
                    nxt = text[i+1]

                    # 1. Virama (Half-letter)
                    if nxt == '्':
                        i+=1; found_vowel = True

                    # 2. Matra (Vowel Sign) e.g., 'u' in 'Su'
                    elif nxt in VOWELS_MAP:
                        res.append(VOWELS_MAP[nxt])
                        i+=1; found_vowel = True

                        # [CRITICAL]: Look for modifiers AFTER the Matra (e.g., 'Su~')
                        while i+1 < len(text) and text[i+1] in 'ंःँ':
                            if text[i+1] == 'ं' and (i+2==len(text) or text[i+2]==' '): res.append('म्')
                            else: res.append(text[i+1])
                            i+=1

                    # 3. Implicit 'A' triggers
                    elif nxt in 'ंःँ':
                        res.append('अ'); found_vowel = True
                        if nxt == 'ं' and (i+2==len(text) or text[i+2]==' '): res.append('म्')
                        else: res.append(nxt)
                        i+=1

                    # 4. Space
                    elif nxt == ' ':
                        res.append('अ'); found_vowel = True

                if not found_vowel: res.append('अ')

            # CASE C: Vedic Accents
            elif char in 'ᳲᳳ': res.append(char)
            i+=1

    return [Varna(s) for s in res] if return_objects else res

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

ad = sanskrit_varna_vichhed

class PratyaharaEngine:
    def __init__(self):
        self.sutras = [
            {"varnas": ["अ", "इ", "उ"], "it": "ण्"}, {"varnas": ["ऋ", "ऌ"], "it": "क्"},
            {"varnas": ["ए", "ओ"], "it": "ङ्"}, {"varnas": ["ऐ", "औ"], "it": "च्"},
            {"varnas": ["ह", "य", "व", "र"], "it": "ट्"}, {"varnas": ["ल"], "it": "ण्"},
            {"varnas": ["ञ", "म", "ङ", "ण", "न"], "it": "म्"}, {"varnas": ["झ", "भ"], "it": "ञ्"},
            {"varnas": ["घ", "ढ", "ध"], "it": "ष्"}, {"varnas": ["ज", "ब", "ग", "ड", "द"], "it": "श्"},
            {"varnas": ["ख", "फ", "छ", "ठ", "थ", "च", "ट", "त"], "it": "व्"},
            {"varnas": ["क", "प"], "it": "य्"}, {"varnas": ["श", "ष", "स"], "it": "र्"},
            {"varnas": ["ह"], "it": "ल्"}
        ]
        self._cache = {}

    def get_varnas(self, name):
        if name in self._cache: return self._cache[name]

        # Robust IT extraction
        if not name: return []
        adi = name[0]
        it_marker = name[1:]
        if it_marker and not it_marker.endswith('्'): it_marker += '्'

        res = []
        collecting = False
        for sutra in self.sutras:
            s_varnas = sutra['varnas']
            s_it = sutra['it']
            if not s_it.endswith('्'): s_it += '्'
            if not collecting and adi in s_varnas:
                idx = s_varnas.index(adi)
                res.extend(s_varnas[idx:])
                collecting = True
                if s_it == it_marker: self._cache[name] = res; return res
                continue
            if collecting:
                res.extend(s_varnas)
                if s_it == it_marker: self._cache[name] = res; return res
        return []

    def is_in(self, char, p_name):
        simple_char = char[0]
        savarna_map = {'आ':'अ', 'ई':'इ', 'ऊ':'उ', 'ॠ':'ऋ'}
        lookup = savarna_map.get(simple_char, simple_char)
        pset = self.get_varnas(p_name)
        return lookup in pset

class UpadeshaType:
    DHATU="dhatu"; PRATYAYA="pratyaya"; VIBHAKTI="vibhakti"; AGAMA="agama"; ADESHA="adesha"; PRATIPADIKA="pratipadika"
    @staticmethod
    def auto_detect(text): return UpadeshaType.PRATIPADIKA, None, "Default"

pe = PratyaharaEngine()