"""
FILE: shared/anubandha.py
PURPOSE: The "It-Sanjna" Engine.
RETURNS: (Cleaned Varnas, Trace Log, Active Tags)
VERSION: Stable 1.0 (Full Logic + Tag Persistence)
"""
from shared.varnas import Varna

class AnubandhaEngine:
    @staticmethod
    def process(varnas, context="General"):
        """
        Input: List of Varna objects
        Context: "Dhatu", "Pratyaya", "Vibhakti", "General"
        Output: (Cleaned Varnas, Trace Log, Active Tags)
        """
        if not varnas: return [], [], set()
        
        res = list(varnas)
        trace = []
        tags = set()
        
        # --- Helper: Map char to Tag Name ---
        def add_tag(char, rule_ref):
            # Clean the char (remove virama/chandrabindu)
            clean_char = char.replace('्', '').replace('ँ', '')
            
            # Standard naming: k -> Kit, n -> Nit
            tag_name = f"{clean_char}it" 
            
            # Special Vowel Names
            if 'इ' in clean_char: tag_name = "Idit"
            elif 'उ' in clean_char: tag_name = "Udit"
            elif 'ऋ' in clean_char: tag_name = "Ṛdit"
            elif 'ऌ' in clean_char: tag_name = "Lṛdit"
            
            tags.add(tag_name)
            return tag_name

        # =========================================================
        # RULE 1.3.2: Upadeśe'janunāsika it (Nasal Vowels)
        # =========================================================
        # We scan for any vowel marked with Chandrabindu (e.g., u~)
        temp_res = []
        for v in res:
            if 'ँ' in v.char:
                t_name = add_tag(v.char, "1.3.2")
                trace.append(f"1.3.2 Upadeśe'janunāsika it: {v.char} is {t_name}.")
                trace.append(f"1.3.9 Tasya Lopaḥ: {v.char} disappears (Lopa).")
                # Do not append to temp_res (Deletion)
            else:
                temp_res.append(v)
        res = temp_res
        
        # =========================================================
        # RULE 1.3.3: Halantyam (Final Consonant)
        # =========================================================
        if res and res[-1].is_consonant:
            last_varna = res[-1]
            last_char_clean = last_varna.char.replace('्', '')
            
            # EXCEPTION 1.3.4: Na Vibhaktau Tusmāḥ
            # T-varga (t, th, d, dh, n), s, m are SAVED in Vibhakti
            tusma_set = {'त', 'थ', 'द', 'ध', 'न', 'स', 'म'}
            
            if context == "Vibhakti" and last_char_clean in tusma_set:
                trace.append(f"1.3.4 Na Vibhaktau Tusmāḥ: {last_varna.char} is SAVED from deletion.")
            else:
                t_name = add_tag(last_char_clean, "1.3.3")
                trace.append(f"1.3.3 Halantyam: {last_varna.char} is {t_name}.")
                trace.append(f"1.3.9 Tasya Lopaḥ: {last_varna.char} disappears (Lopa).")
                res.pop() # Remove final element

        # =========================================================
        # INITIAL RULES (Adi - Beginning of Term)
        # =========================================================
        if res:
            # Get the first character without virama for checking
            first_char = res[0].char.replace('्', '')
            
            # --- CONTEXT: DHATU ---
            if context == "Dhatu":
                # 1.3.5 Ādirñiṭuḍavaḥ
                if first_char == 'ञ' and len(res)>1 and 'इ' in res[1].char:
                     add_tag("Ñ", "1.3.5")
                     trace.append(f"1.3.5 Ādirñiṭuḍavaḥ: Ñi is Ñit.")
                     res = res[2:] # Remove 2 chars (Ñ + i)
                elif first_char == 'ट' and len(res)>1 and 'उ' in res[1].char:
                     add_tag("Ṭ", "1.3.5")
                     trace.append(f"1.3.5 Ādirñiṭuḍavaḥ: Ṭu is Ṭit.")
                     res = res[2:]
                elif first_char == 'ड' and len(res)>1 and 'उ' in res[1].char:
                     add_tag("Ḍ", "1.3.5")
                     trace.append(f"1.3.5 Ādirñiṭuḍavaḥ: Ḍu is Ḍit.")
                     res = res[2:]

            # --- CONTEXT: PRATYAYA or VIBHAKTI ---
            elif context in ["Pratyaya", "Vibhakti"]:
                
                # 1.3.6 Ṣaḥ Pratyayasya (Initial Ṣ)
                if first_char == 'ष':
                    add_tag("ष", "1.3.6")
                    trace.append(f"1.3.6 Ṣaḥ Pratyayasya: Ṣa is Ṣit.")
                    trace.append(f"1.3.9 Tasya Lopaḥ: Ṣa disappears.")
                    res.pop(0)

                # 1.3.7 Cuṭū (Ch-varga, T-varga)
                elif first_char in ['च', 'छ', 'ज', 'झ', 'ञ', 'ट', 'ठ', 'ड', 'ढ', 'ण']:
                    add_tag(first_char, "1.3.7")
                    trace.append(f"1.3.7 Cuṭū: {first_char} is It.")
                    trace.append(f"1.3.9 Tasya Lopaḥ: {first_char} disappears.")
                    res.pop(0)
                    
                # 1.3.8 Laśakvataddhite (L, S, K-varga)
                # Note: Technically applies to non-Taddhita, but general logic applies here.
                elif first_char in ['ल', 'श', 'क', 'ख', 'ग', 'घ', 'ङ']:
                        if not getattr(varnas, 'is_taddhita', False):
                            t_name = add_tag(first_char, "1.3.8")
                            trace.append(f"1.3.8 Laśakvataddhite: {first_char} is {t_name}.")
            res.pop(0)

        return res, trace, tags