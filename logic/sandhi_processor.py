"""
FILE: logic/sandhi_processor.py
"""
from core.core_foundation import Varna, sanskrit_varna_samyoga

class SandhiProcessor:
    @staticmethod
    def apply_ac_sandhi(anga, suffix):
        if not anga or not suffix: return anga + suffix, None
        last = anga[-1]; first = suffix[0]

        # R6: Ayadi (6.1.78)
        if first.is_vowel:
            if last.char == 'ए':
                last.char = 'अ'; y_v = Varna('य्'); y_v.trace.append("6.1.78")
                anga.append(y_v); return anga + suffix, "6.1.78 (एचोऽयवायावः)"
            elif last.char == 'ओ':
                last.char = 'अ'; v_v = Varna('व्'); v_v.trace.append("6.1.78")
                anga.append(v_v); return anga + suffix, "6.1.78 (एचोऽयवायावः)"

        # Guna (6.1.87)
        if last.char in ['अ', 'आ'] and first.char in ['इ', 'ई']:
            last.char = 'ए'; suffix.pop(0); return anga + suffix, "6.1.87 (आद्गुणः)"

        # Savarna Dirgha (6.1.101)
        if last.char in ['अ', 'आ'] and first.char in ['अ', 'आ']:
            last.char = 'आ'; suffix.pop(0); return anga + suffix, "6.1.101 (अकः सवर्णे दीर्घः)"

        # Vriddhi (6.1.88)
        if last.char in ['अ', 'आ'] and first.char in ['ए', 'ऐ', 'ओ', 'औ']:
            last.char = 'ऐ' if first.char in ['ए', 'ऐ'] else 'औ'
            suffix.pop(0); return anga + suffix, "6.1.88 (वृद्धिरेचि)"

        return anga + suffix, None

    @staticmethod
    def run_tripadi(v_list, logger=None):
        if not v_list: return []
        
        # R7: Shattva (8.3.59)
        for i in range(1, len(v_list)):
            if v_list[i].char == 'स्':
                prev = v_list[i-1].char
                if any(v in prev for v in "इईउऊऋॠएऐओऔ") or prev in ['य्','व्','र्','ल्','ह्', 'क्','ख्','ग्','घ्','ङ्']:
                    v_list[i].char = 'ष्'; v_list[i].trace.append("8.3.59")
                    if logger: logger.log("8.3.59 (आदेशप्रत्यययोः)", "Shattva (षत्व)", sanskrit_varna_samyoga(v_list), v_list)

        # R17: Natva (8.4.2)
        triggers = [i for i, v in enumerate(v_list) if v.char in ['र्', 'ष्', 'ऋ', 'ॠ']]
        targets = [i for i, v in enumerate(v_list) if v.char == 'न्']
        for t_idx in targets:
            valid_trigs = [tr for tr in triggers if tr < t_idx]
            if valid_trigs:
                blocked = False
                for j in range(valid_trigs[-1] + 1, t_idx):
                    c = v_list[j].char
                    if not (any(v in c for v in "अआइईउऊऋॠएऐओऔं") or c in "ह् य् व् र् क् ख् ग् घ् ङ् प् फ् ब् भ् म्".split()):
                        blocked = True; break
                if not blocked: 
                    v_list[t_idx].char = 'ण्'; v_list[t_idx].trace.append("8.4.2")
                    if logger: logger.log("8.4.2 (अट्कुप्वाङ्...)", "Natva (णत्व)", sanskrit_varna_samyoga(v_list), v_list)

        # R9: Visarga Logic (Rutva -> Visarga)
        if v_list[-1].char in ['स्', 'ष्']:
            # 1. Sasajusho Ruh (8.2.66)
            v_list[-1].char = 'र्' 
            if logger: logger.log("8.2.66 (ससजुषोः रुः)", "Rutva (रुँत्वम्)", sanskrit_varna_samyoga(v_list), v_list)
            
            # 2. Kharavasanayor Visarjaniyah (8.3.15)
            v_list[-1].char = 'ः'
            if logger: logger.log("8.3.15 (खरवसानयोर्विसर्जनीयः)", "Visarga (विसर्गः)", sanskrit_varna_samyoga(v_list), v_list)
        
        # Check if already R (e.g. Punar)
        elif v_list[-1].char == 'र्':
             v_list[-1].char = 'ः'
             if logger: logger.log("8.3.15 (खरवसानयोर्विसर्जनीयः)", "Visarga (विसर्गः)", sanskrit_varna_samyoga(v_list), v_list)
             
        return v_list
