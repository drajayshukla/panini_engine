"""
FILE: shared/anubandha.py
PURPOSE: The "It-Sanjna" Engine.
RETURNS: (Cleaned Varnas, Trace Log, Active Tags)
"""
from shared.varnas import Varna

class AnubandhaEngine:
    @staticmethod
    def process(varnas, context="General"):
        if not varnas: return [], [], set()
        
        res = list(varnas)
        trace = []
        tags = set() # The "Soul" of the letters
        
        # Helper to map char to Tag Name (k -> Kit)
        def add_tag(char, rule):
            clean_char = char.replace('्', '').replace('ँ', '')
            tag_name = f"{clean_char}it" # e.g., Kit, Nit, Śit
            tags.add(tag_name)
            return tag_name

        # ---------------------------------------------------------
        # 1.3.2 Upadeśe'janunāsika it (Nasal Vowels)
        # ---------------------------------------------------------
        temp_res = []
        for v in res:
            if 'ँ' in v.char:
                # Special handling for Vowels: Udit, Idit, etc.
                clean_v = v.char.replace('ँ', '')
                tag_name = f"{clean_v}dit" # u~ -> Udit
                if 'इ' in clean_v: tag_name = "Idit" # Special spelling
                
                tags.add(tag_name)
                trace.append(f"1.3.2 Upadeśe'janunāsika it: {v.char} is {tag_name}.")
                trace.append(f"1.3.9 Tasya Lopaḥ: {v.char} disappears.")
            else: temp_res.append(v)
        res = temp_res
        
        # ---------------------------------------------------------
        # 1.3.3 Halantyam (Final Consonant)
        # ---------------------------------------------------------
        if res and res[-1].is_consonant:
            last_varna = res[-1]
            last_char_clean = last_varna.char.replace('्', '')
            
            # EXCEPTION 1.3.4: Na Vibhaktau Tusmāḥ
            tusma_set = {'त', 'थ', 'द', 'ध', 'न', 'स', 'म'}
            
            if context == "Vibhakti" and last_char_clean in tusma_set:
                trace.append(f"1.3.4 Na Vibhaktau Tusmāḥ: {last_varna.char} is SAVED.")
            else:
                t_name = add_tag(last_char_clean, "1.3.3")
                trace.append(f"1.3.3 Halantyam: {last_varna.char} is {t_name}.")
                trace.append(f"1.3.9 Tasya Lopaḥ: {last_varna.char} disappears.")
                res.pop()

        # ---------------------------------------------------------
        # INITIAL RULES (Adi)
        # ---------------------------------------------------------
        if res:
            first_char = res[0].char.replace('्', '')
            
            # Context: DHATU
            if context == "Dhatu":
                if first_char == 'ञ' and len(res)>1 and 'इ' in res[1].char:
                     tags.add("Ñit")
                     trace.append(f"1.3.5 Ādirñiṭuḍavaḥ: Ñi is Ñit.")
                     res = res[2:]
                elif first_char == 'ट' and len(res)>1 and 'उ' in res[1].char:
                     tags.add("Ṭit")
                     trace.append(f"1.3.5 Ādirñiṭuḍavaḥ: Ṭu is Ṭit.")
                     res = res[2:]
                elif first_char == 'ड' and len(res)>1 and 'उ' in res[1].char:
                     tags.add("Ḍit")
                     trace.append(f"1.3.5 Ādirñiṭuḍavaḥ: Ḍu is Ḍit.")
                     res = res[2:]

            # Context: PRATYAYA
            elif context in ["Pratyaya", "Vibhakti"]:
                # 1.3.6 Ṣaḥ Pratyayasya
                if first_char == 'ष':
                    add_tag("ष", "1.3.6")
                    trace.append(f"1.3.6 Ṣaḥ Pratyayasya: Ṣa is Ṣit.")
                    trace.append(f"1.3.9 Tasya Lopaḥ: Ṣa disappears.")
                    res.pop(0)

                # 1.3.7 Cuṭū
                elif first_char in ['च', 'छ', 'ज', 'झ', 'ञ', 'ट', 'ठ', 'ड', 'ढ', 'ण']:
                    add_tag(first_char, "1.3.7")
                    trace.append(f"1.3.7 Cuṭū: {first_char} is It.")
                    res.pop(0)
                    
                # 1.3.8 Laśakvataddhite
                elif first_char == 'ल' or first_char == 'श' or first_char in ['क', 'ख', 'ग', 'घ', 'ङ']:
                     add_tag(first_char, "1.3.8")
                     trace.append(f"1.3.8 Laśakvataddhite: {first_char} is It.")
                     res.pop(0)

        return res, trace, tags
