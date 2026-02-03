"""
FILE: shared/anubandha.py
PURPOSE: The "It-Sanjna" Engine. Identifies and removes meta-markers.
"""
from shared.varnas import Varna

class AnubandhaEngine:
    @staticmethod
    def process(varnas, context="General"):
        """
        Input: List of Varna objects
        Output: (Cleaned Varnas, Trace Log)
        """
        if not varnas: return [], []
        
        # Working copy
        res = list(varnas)
        trace = []
        
        # --- RULE 1.3.2: Upadeśe'janunāsika it ---
        # (Nasal Vowels are It)
        # Note: In our 'ad' function, we merged 'u~' into single units.
        # We just check for the nasal marker.
        temp_res = []
        for v in res:
            if 'ँ' in v.char:
                trace.append(f"1.3.2 Upadeśe'janunāsika it: {v.char} is It-Sanjna.")
                trace.append(f"1.3.9 Tasya Lopaḥ: {v.char} removed.")
                # Lopa (Do not add to temp_res)
            else:
                temp_res.append(v)
        res = temp_res
        
        # --- RULE 1.3.3: Halantyam ---
        # (Final Consonant is It)
        if res and res[-1].is_consonant:
            last = res[-1].char
            
            # EXCEPTION 1.3.4: Na Vibhaktau Tusmāḥ
            # (t, th, d, dh, n, s, m are NOT It in Vibhakti)
            tusma = ['त्', 'थ्', 'द्', 'ध्', 'न्', 'स्', 'म्']
            if context == "Vibhakti" and last in tusma:
                trace.append(f"1.3.4 Na Vibhaktau Tusmāḥ: {last} is SAVED from It-Sanjna.")
            else:
                trace.append(f"1.3.3 Halantyam: {last} is It-Sanjna.")
                trace.append(f"1.3.9 Tasya Lopaḥ: {last} removed.")
                res.pop() # Remove last

        # --- INITIAL RULES (Adi) ---
        if res:
            first = res[0].char.replace('्', '') # Remove virama for checking
            
            # RULE 1.3.5: Ādirñiṭuḍavaḥ (ñi, ṭu, ḍu at start of Dhatu)
            if context == "Dhatu":
                if first == 'ञ' and len(res)>1 and 'इ' in res[1].char:
                     # e.g., Ñi-Dhrish
                     trace.append(f"1.3.5 Ādirñiṭuḍavaḥ: Ñi is It-Sanjna.")
                     res = res[2:] # Remove Ñi
                elif first == 'ट' and len(res)>1 and 'उ' in res[1].char:
                     trace.append(f"1.3.5 Ādirñiṭuḍavaḥ: Ṭu is It-Sanjna.")
                     res = res[2:]
                elif first == 'ड' and len(res)>1 and 'उ' in res[1].char:
                     trace.append(f"1.3.5 Ādirñiṭuḍavaḥ: Ḍu is It-Sanjna (e.g. Ḍukṛñ).")
                     res = res[2:] # Remove Du

            # RULE 1.3.7: Cuṭū (Cu, Tu at start of Pratyaya)
            elif context == "Pratyaya":
                # Cu = c, ch, j, jh, ñ
                # Tu = ṭ, ṭh, ḍ, ḍh, ṇ
                cu_group = ['च', 'छ', 'ज', 'झ', 'ञ']
                tu_group = ['ट', 'ठ', 'ड', 'ढ', 'ण']
                
                if first in cu_group or first in tu_group:
                    trace.append(f"1.3.7 Cuṭū: {res[0].char} is It-Sanjna.")
                    trace.append(f"1.3.9 Tasya Lopaḥ: {res[0].char} removed.")
                    res.pop(0)

            # RULE 1.3.8: Laśakvataddhite (L, S, K-varga at start of Pratyaya)
            # Exception: Taddhita pratyayas are excluded (not handled here yet)
            if context == "Pratyaya" and res:
                # Re-check first after potential 1.3.7 removal
                first = res[0].char.replace('्', '')
                ku_group = ['क', 'ख', 'ग', 'घ', 'ङ']
                if first == 'ल' or first == 'श' or first in ku_group:
                    trace.append(f"1.3.8 Laśakvataddhite: {res[0].char} is It-Sanjna.")
                    trace.append(f"1.3.9 Tasya Lopaḥ: {res[0].char} removed.")
                    res.pop(0)

        return res, trace
