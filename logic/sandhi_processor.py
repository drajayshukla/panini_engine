"""
FILE: logic/sandhi_processor.py
FINAL Siddha Patch for Guru/Bhanu (Ayadi Logic)
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

        last = s[-1]
        first = p[0]

        # --- CRITICAL: AC Definition for Ayadi ---
        # Includes independent vowels, matras, and explicit list
        all_vowels = SandhiProcessor.AC.union(SandhiProcessor.MATRAS).union(
            set(['अ','आ','इ','ई','उ','ऊ','ऋ','ॠ','ऌ','ए','ऐ','ओ','औ'])
        )
        is_ac = first in all_vowels

        # 1. AYADI (6.1.78) - Priority check to prevent 'Guru + Jas' failure
        if last == 'ए' and is_ac:
            s.pop(); return ad("".join(s) + "अय्" + "".join(p)), "6.1.78 H.O.A.V"
        elif last == 'ओ' and is_ac:
            s.pop(); return ad("".join(s) + "अव्" + "".join(p)), "6.1.78 H.O.A.V"
        elif last == 'ऐ' and is_ac:
            s.pop(); return ad("".join(s) + "आय्" + "".join(p)), "6.1.78 H.O.A.V"
        elif last == 'औ' and is_ac:
            s.pop(); return ad("".join(s) + "आाव्" + "".join(p)), "6.1.78 H.O.A.V"

        # 2. VRIDDHI (6.1.88)
        if last in ['अ', 'आ']:
            if first in ['ए', 'ऐ']: s.pop(); p[0]='ऐ'; return ad("".join(s)+"".join(p)), "6.1.88 Vriddhirechi"
            elif first in ['ओ', 'औ']: s.pop(); p[0]='औ'; return ad("".join(s)+"".join(p)), "6.1.88 Vriddhirechi"

        # 3. GUNA (6.1.87)
        if last in ['अ', 'आ']:
            if first in ['इ', 'ई']: s.pop(); p[0]='ए'; return ad("".join(s)+"".join(p)), "6.1.87 Ad Gunah"
            elif first in ['उ', 'ऊ']: s.pop(); p[0]='ओ'; return ad("".join(s)+"".join(p)), "6.1.87 Ad Gunah"
            elif first in ['ऋ', 'ॠ']: s.pop(); p.pop(0); return ad("".join(s)+"अर्"+"".join(p)), "6.1.87 Ad Gunah"

        # 4. YAN (6.1.77)
        if last in ['इ', 'ई'] and is_ac and first != last:
            s[-1]='य्'; return ad("".join(s)+"".join(p)), "6.1.77 Iko Yanachi"
        elif last in ['उ', 'ऊ'] and is_ac and first != last:
            s[-1]='व्'; return ad("".join(s)+"".join(p)), "6.1.77 Iko Yanachi"

        # 5. SAVARNA DIRGHA (6.1.101)
        savarna_pairs = [(['अ','आ'],['अ','आ'],'आ'), (['इ','ई'],['इ','ई'],'ई'), (['उ','ऊ'],['उ','ऊ'],'ऊ'), (['ऋ','ॠ'],['ऋ','ॠ'],'ॠ')]
        for l_set, f_set, res_c in savarna_pairs:
            if last in l_set and first in f_set:
                s.pop(); p[0]=res_c; return ad("".join(s)+"".join(p)), "6.1.101 Aka Savarne Dirghah"

        return stem_varnas + suffix_varnas, None

    @staticmethod
    def run_tripadi(varnas, logger=None):
        res = list(varnas)
        # RUTVA (8.2.66)
        if res and res[-1].char in ['स्', 's']:
            res[-1].char = 'र्';
            if logger: logger.log("8.2.66", "Sasajusho Ruh", sanskrit_varna_samyoga(res), res, "Maharshi Pāṇini")
        # SHATVA (8.3.59)
        for i, v in enumerate(res):
            clean_char = v.char.replace('्', '')
            if clean_char in ['स', 'स्', 's']:
                if i > 0:
                    prev = res[i-1].char
                    check_char = prev
                    if prev == '्' and i > 1: check_char = res[i-2].char
                    check_clean = check_char.replace('्', '')
                    in_set = SandhiProcessor.IN_PRATYAHARA.union(SandhiProcessor.MATRAS)
                    if (check_clean in in_set) or (check_clean in SandhiProcessor.KU_VARGA):
                        res[i].char = 'ष्'
                        if logger: logger.log("8.3.59", "Adeshapratyayoh", sanskrit_varna_samyoga(res), res, "Maharshi Pāṇini")
        # VISARGA (8.3.15)
        if res and res[-1].char == 'र्':
            res[-1].char = 'ः';
            if logger: logger.log("8.3.15", "Kharavasanayo Visarjaniyah", sanskrit_varna_samyoga(res), res, "Maharshi Pāṇini")
        # NATVA (8.4.2)
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
                if is_valid and not (i == len(res)-1):
                    res[i].char = 'ण्' if v.char == 'न्' else 'ण'
                    if logger: logger.log("8.4.2", "Atkupvangnumvyavaye'pi", sanskrit_varna_samyoga(res), res, "Maharshi Pāṇini")
        return res

