"""
FILE: fix_typo_sandhi.py
PURPOSE: Fix 'NameError: check_clean' by ensuring variable names are consistent (clean_check).
"""
import os
import sys
import subprocess

# ==============================================================================
# LOGIC: SANDHI PROCESSOR (Typo Fixed)
# ==============================================================================
SANDHI_CODE = '''"""
FILE: logic/sandhi_processor.py
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga
from core.maheshwara_sutras import MaheshwaraSutras

class SandhiProcessor:
    AC = MaheshwaraSutras.get_pratyahara("अच्")
    IN_PRATYAHARA = MaheshwaraSutras.get_pratyahara("इण्", force_n2=True)
    AT_PRATYAHARA = MaheshwaraSutras.get_pratyahara("अट्")
    
    KU_VARGA = set(['क', 'ख', 'ग', 'घ', 'ङ', 'क्', 'ख्', 'ग्', 'घ्', 'ङ्'])
    PU_VARGA = set(['प', 'फ', 'ब', 'भ', 'म', 'प्', 'फ्', 'ब्', 'भ्', 'म्'])
    MATRAS = set(['ा', 'ि', 'ी', 'ु', 'ू', 'ृ', 'ॄ', 'ॢ', 'े', 'ै', 'ो', 'ौ', 'ं', 'ः'])
    
    ALLOWED_NATVA_INTERVENERS = AT_PRATYAHARA.union(KU_VARGA).union(PU_VARGA).union(MATRAS).union({'ं', 'ँ'})

    @staticmethod
    def apply_ac_sandhi(stem_varnas, suffix_varnas):
        if not suffix_varnas: return stem_varnas, None
        s = [v.char for v in stem_varnas]; p = [v.char for v in suffix_varnas]
        if not s or not p: return stem_varnas + suffix_varnas, None
        last = s[-1]; first = p[0]
        
        # VRIDDHI
        if last in ['अ', 'आ']:
            if first in ['ए', 'ऐ']: s.pop(); p[0]='ऐ'; return ad("".join(s)+"".join(p)), "6.1.88 Vriddhirechi"
            elif first in ['ओ', 'औ']: s.pop(); p[0]='औ'; return ad("".join(s)+"".join(p)), "6.1.88 Vriddhirechi"
        # GUNA
        if last in ['अ', 'आ']:
            if first in ['इ', 'ई']: s.pop(); p[0]='ए'; return ad("".join(s)+"".join(p)), "6.1.87 Ad Gunah"
            elif first in ['उ', 'ऊ']: s.pop(); p[0]='ओ'; return ad("".join(s)+"".join(p)), "6.1.87 Ad Gunah"
            elif first in ['ऋ', 'ॠ']: s.pop(); p.pop(0); return ad("".join(s)+"अर्"+"".join(p)), "6.1.87 Ad Gunah"
        # YAN
        if last in ['इ', 'ई'] and first in SandhiProcessor.AC and first!=last:
            s[-1]='य्'; return ad("".join(s)+"".join(p)), "6.1.77 Iko Yanachi"
        elif last in ['उ', 'ऊ'] and first in SandhiProcessor.AC and first!=last:
            s[-1]='व्'; return ad("".join(s)+"".join(p)), "6.1.77 Iko Yanachi"
        # AYADI
        is_ac = first in SandhiProcessor.AC or first in SandhiProcessor.MATRAS or first in ['ए','ओ','ऐ','औ']
        if last == 'ए' and is_ac: s.pop(); return ad("".join(s)+"अय्"+"".join(p)), "6.1.78 H.O.A.V"
        elif last == 'ओ' and is_ac: s.pop(); return ad("".join(s)+"अव्"+"".join(p)), "6.1.78 H.O.A.V"
        elif last == 'ऐ' and is_ac: s.pop(); return ad("".join(s)+"आय्"+"".join(p)), "6.1.78 H.O.A.V"
        elif last == 'औ' and is_ac: s.pop(); return ad("".join(s)+"राव्"+"".join(p)), "6.1.78 H.O.A.V"
        # SAVARNA
        is_savarna=False; res_char=''
        if last in ['अ','आ'] and first in ['अ','आ']: is_savarna=True; res_char='आ'
        elif last in ['इ','ई'] and first in ['इ','ई']: is_savarna=True; res_char='ई'
        elif last in ['उ','ऊ'] and first in ['उ','ऊ']: is_savarna=True; res_char='ऊ'
        elif last in ['ऋ','ॠ'] and first in ['ऋ','ॠ']: is_savarna=True; res_char='ॠ'
        if is_savarna: s.pop(); p[0]=res_char; return ad("".join(s)+"".join(p)), "6.1.101 Aka Savarne Dirghah"

        return stem_varnas + suffix_varnas, None

    @staticmethod
    def run_tripadi(varnas, logger=None):
        res = list(varnas)
        # RUTVA
        if res and res[-1].char in ['स्', 's']:
            res[-1].char = 'र्'; 
            if logger: logger.log("8.2.66", "Sasajusho Ruh", sanskrit_varna_samyoga(res), res, "Maharshi Pāṇini")
        # SHATVA
        for i, v in enumerate(res):
            clean_char = v.char.replace('्', '')
            if clean_char in ['स', 'स्', 's']:
                if i > 0:
                    prev = res[i-1].char; 
                    # If prev is halant, look back one more (e.g. Vaks + su -> k + s + s)
                    # But for Ramesu (e + s), prev is 'e'.
                    check_char = prev
                    if prev == '्' and i > 1: check_char = res[i-2].char
                    
                    # Normalize check_char
                    check_clean = check_char.replace('्', '') # FIXED VARIABLE NAME
                    
                    in_set = SandhiProcessor.IN_PRATYAHARA.union(SandhiProcessor.MATRAS)
                    # Check against Swara/Matra OR Ku-Varga
                    if check_clean in in_set or check_char in in_set or check_clean in SandhiProcessor.KU_VARGA:
                        res[i].char = 'ष्'
                        if logger: logger.log("8.3.59", "Adeshapratyayoh", sanskrit_varna_samyoga(res), res, "Maharshi Pāṇini")
        # VISARGA
        if res and res[-1].char == 'र्':
            res[-1].char = 'ः'; 
            if logger: logger.log("8.3.15", "Kharavasanayo Visarjaniyah", sanskrit_varna_samyoga(res), res, "Maharshi Pāṇini")
        # NATVA
        cause_found = False; cause_index = -1
        for i, v in enumerate(res):
            c = v.char.replace('्', '')
            if c in ['र्', 'ष्', 'r', 'ṣ', 'र', 'ष']: cause_found=True; cause_index=i; continue
            if cause_found and v.char in ['न', 'न्']:
                is_valid = True
                for k in range(cause_index + 1, i):
                    mid = res[k].char.replace('्', '')
                    if res[k].char == '्': continue
                    if mid not in SandhiProcessor.ALLOWED_NATVA_INTERVENERS: is_valid=False; break
                is_padanta = (i == len(res)-1) or (i == len(res)-2 and res[-1].char == '्')
                if is_valid and not is_padanta:
                    res[i].char = 'ण्' if v.char == 'न्' else 'ण'
                    if logger: logger.log("8.4.2", "Atkupvangnumvyavaye'pi", sanskrit_varna_samyoga(res), res, "Maharshi Pāṇini")
        return res
'''

with open("logic/sandhi_processor.py", "w", encoding="utf-8") as f:
    f.write(SANDHI_CODE)

print("🚀 Fixed 'check_clean' typo. Running Master Tests...")
subprocess.run([sys.executable, "master_runner.py"])