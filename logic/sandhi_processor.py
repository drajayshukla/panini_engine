"""
FILE: logic/sandhi_processor.py
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga

class SandhiProcessor:
    
    AC = {'अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ॠ', 'ऌ', 'ए', 'ऐ', 'ओ', 'औ'}
    
    @staticmethod
    def is_vowel(char):
        return char in SandhiProcessor.AC

    @staticmethod
    def apply_ac_sandhi(stem_varnas, suffix_varnas):
        if not stem_varnas or not suffix_varnas:
            return stem_varnas + suffix_varnas, None

        res = stem_varnas[:] + suffix_varnas[:]
        idx = len(stem_varnas) - 1
        
        if idx < 0 or (idx + 1) >= len(res):
            return res, None

        v1 = res[idx].char
        v2 = res[idx+1].char
        
        if not (SandhiProcessor.is_vowel(v1) and SandhiProcessor.is_vowel(v2)):
            return res, None

        # 1. SAVARNA DIRGHA (6.1.101)
        savarna_pairs = {
            ('अ', 'अ'): 'आ', ('अ', 'आ'): 'आ', ('आ', 'अ'): 'आ', ('आ', 'आ'): 'आ',
            ('इ', 'इ'): 'ई', ('इ', 'ई'): 'ई', ('ई', 'इ'): 'ई', ('ई', 'ई'): 'ई',
            ('उ', 'उ'): 'ऊ', ('उ', 'ऊ'): 'ऊ', ('ऊ', 'उ'): 'ऊ', ('ऊ', 'ऊ'): 'ऊ',
            ('ऋ', 'ऋ'): 'ॠ', ('ऋ', 'ॠ'): 'ॠ'
        }
        if (v1, v2) in savarna_pairs:
            res[idx].char = savarna_pairs[(v1, v2)]
            del res[idx+1]
            return res, "6.1.101 Akah Savarne Dirghah"

        # 2. GUNA (6.1.87)
        guna_map = {'इ': 'ए', 'ई': 'ए', 'उ': 'ओ', 'ऊ': 'ओ', 'ऋ': 'अर्', 'ॠ': 'अर्'}
        if v1 in ['अ', 'आ'] and v2 in guna_map:
            res_char = guna_map[v2]
            if 'र्' in res_char:
                res[idx].char = 'अ'
                res[idx+1].char = 'र्' 
                return res, "6.1.87 Adgunah"
            else:
                res[idx].char = res_char
                del res[idx+1]
                return res, "6.1.87 Adgunah"

        # 3. VRIDDHI (6.1.88)
        vriddhi_map = {'ए': 'ऐ', 'ऐ': 'ऐ', 'ओ': 'औ', 'औ': 'औ'}
        if v1 in ['अ', 'आ'] and v2 in vriddhi_map:
            res[idx].char = vriddhi_map[v2]
            del res[idx+1]
            return res, "6.1.88 Vriddhir-eci"

        # 4. YAN SANDHI (6.1.77)
        yan_map = {'इ': 'य्', 'ई': 'य्', 'उ': 'व्', 'ऊ': 'व्', 'ऋ': 'र्', 'ॠ': 'र्'}
        if v1 in yan_map:
            res[idx].char = yan_map[v1]
            return res, "6.1.77 Iko Yanachi"

        # 5. AYADI (6.1.78)
        ayadi_map = {'ए': ['अ', 'य्'], 'ओ': ['अ', 'व्'], 'ऐ': ['आ', 'य्'], 'औ': ['आ', 'व्']}
        if v1 in ayadi_map:
            expansion = ayadi_map[v1]
            res[idx].char = expansion[0]
            semivowel_list = ad(expansion[1]) 
            res.insert(idx+1, semivowel_list[0])
            return res, "6.1.78 Eco'yavayavah"

        return res, None

    @staticmethod
    def apply_natva(varnas):
        """
        8.4.1 Rashabhyam No Nah Samanapade
        """
        r_sh_found = False
        ALLOWED_BASE = [
            'अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ॠ', 'ए', 'ऐ', 'ओ', 'औ',
            'ा', 'ि', 'ी', 'ु', 'ू', 'ृ', 'ॄ', 'े', 'ै', 'ो', 'ौ',
            'ं', 'ह', 'य', 'व', 'र', 'क', 'ख', 'ग', 'घ', 'ङ', 'प', 'फ', 'ब', 'भ', 'म'
        ]
        ALLOWED_SET = set(ALLOWED_BASE)
        for char in ALLOWED_BASE: ALLOWED_SET.add(char + '्')
        ALLOWED_SET.update(['क्', 'ख्', 'ग्', 'घ्', 'ङ्', 'प्', 'फ्', 'ब्', 'भ्', 'म्', 'य्', 'व्', 'र्', 'ह्'])

        res = varnas[:] 
        for i in range(len(res)):
            char = res[i].char
            if char in ['र्', 'ष्', 'ऋ', 'ॠ', 'ृ', 'ॄ', 'र', 'ष']:
                r_sh_found = True
                continue
            if char in ['न', 'न्'] and r_sh_found:
                if i == len(res) - 1: continue
                if '्' in char: res[i].char = 'ण्'
                else: res[i].char = 'ण'
            if r_sh_found:
                # FIX: Only 'n' (dental) allows pass-through as target.
                # 'N' (Retroflex) IS A BLOCKER (Tavarga).
                if char in ['न', 'न्']: pass
                elif char not in ALLOWED_SET: r_sh_found = False
        return res, "8.4.1 Rashabhyam No Nah"

    @staticmethod
    def apply_shatva(varnas):
        IN_BASE = {
            'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ॠ', 'ए', 'ऐ', 'ओ', 'औ', 
            'ि', 'ी', 'ु', 'ू', 'ृ', 'ॄ', 'े', 'ै', 'ो', 'ौ',
            'ह', 'य', 'व', 'र', 'ल'
        }
        KU_BASE = {'क', 'ख', 'ग', 'घ', 'ङ'}
        TRIGGER_SET = set()
        for c in IN_BASE | KU_BASE:
            TRIGGER_SET.add(c)
            TRIGGER_SET.add(c + '्')
        TRIGGER_SET.update(['क्', 'ख्', 'ग्', 'घ्', 'ङ्', 'य्', 'व्', 'र्', 'ल्', 'ह्'])

        res = varnas[:]
        for i in range(1, len(res)):
            curr = res[i].char
            prev = res[i-1].char
            
            if curr in ['स', 'स्']:
                if i == len(res) - 1: continue
                if prev in TRIGGER_SET:
                    if '्' in curr: res[i].char = 'ष्'
                    else: res[i].char = 'ष'
                    
        return res, "8.3.59 Adesha-pratyayayoh"

    @staticmethod
    def run_tripadi(varnas, logger=None):
        if not varnas: return []
        
        # 1. Rutva
        res = varnas[:]
        if res[-1].char == 'स्':
            res[-1].char = 'र्'
            if logger: logger.log("8.2.66", "Sasajusho Ruh", sanskrit_varna_samyoga(res), res, "Maharshi Pāṇini")
        
        # 2. Visarga
        if res[-1].char == 'र्':
             res[-1].char = 'ः'
             if logger: logger.log("8.3.15", "Kharavasanayo Visarjaniyah", sanskrit_varna_samyoga(res), res, "Maharshi Pāṇini")

        # 3. Natva
        res, _ = SandhiProcessor.apply_natva(res)
        
        # 4. Shatva
        res, _ = SandhiProcessor.apply_shatva(res)

        return res
