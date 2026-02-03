import os
from pathlib import Path

def upgrade_sutra_1_3_6():
    print("✨ UPGRADING CORE: Implementing 1.3.6 Ṣaḥ Pratyayasya...")

    # We update the Golden Source in launchpad.py (so Rebuilds keep it)
    # And we update the live file directly.

    new_anubandha_code = r'''"""
FILE: shared/anubandha.py
PURPOSE: The "It-Sanjna" Engine.
"""
from shared.varnas import Varna

class AnubandhaEngine:
    @staticmethod
    def process(varnas, context="General"):
        if not varnas: return [], []
        res = list(varnas)
        trace = []
        
        # 1.3.2 Upadeśe'janunāsika it
        temp_res = []
        for v in res:
            if 'ँ' in v.char:
                trace.append(f"1.3.2 Upadeśe'janunāsika it: {v.char} is It.")
                trace.append(f"1.3.9 Tasya Lopaḥ: {v.char} removed.")
            else: temp_res.append(v)
        res = temp_res
        
        # 1.3.3 Halantyam
        if res and res[-1].is_consonant:
            last = res[-1].char
            tusma = ['त्', 'थ्', 'द्', 'ध्', 'न्', 'स्', 'म्']
            if context == "Vibhakti" and last in tusma:
                trace.append(f"1.3.4 Na Vibhaktau Tusmāḥ: {last} SAVED.")
            else:
                trace.append(f"1.3.3 Halantyam: {last} is It.")
                res.pop()

        # INITIAL RULES (Adi)
        if res:
            first_char = res[0].char.replace('्', '')
            
            # Context: DHATU
            if context == "Dhatu":
                if first_char == 'ञ' and len(res)>1 and 'इ' in res[1].char:
                     trace.append(f"1.3.5 Ādirñiṭuḍavaḥ: Ñi is It.")
                     res = res[2:]
                elif first_char == 'ट' and len(res)>1 and 'उ' in res[1].char:
                     trace.append(f"1.3.5 Ādirñiṭuḍavaḥ: Ṭu is It.")
                     res = res[2:]
                elif first_char == 'ड' and len(res)>1 and 'उ' in res[1].char:
                     trace.append(f"1.3.5 Ādirñiṭuḍavaḥ: Ḍu is It.")
                     res = res[2:]

            # Context: PRATYAYA
            elif context == "Pratyaya":
                # 1.3.6 Ṣaḥ Pratyayasya (NEW)
                if first_char == 'ष':
                    trace.append(f"1.3.6 Ṣaḥ Pratyayasya: Initial Ṣa ({res[0].char}) is It.")
                    trace.append(f"1.3.9 Tasya Lopaḥ: {res[0].char} removed.")
                    res.pop(0)

                # 1.3.7 Cuṭū
                elif first_char in ['च', 'छ', 'ज', 'झ', 'ञ', 'ट', 'ठ', 'ड', 'ढ', 'ण']:
                    trace.append(f"1.3.7 Cuṭū: {res[0].char} is It.")
                    res.pop(0)
                    
                # 1.3.8 Laśakvataddhite
                # Note: 'L' and 'S' and 'Ku-varga'
                elif first_char == 'ल' or first_char == 'श' or first_char in ['क', 'ख', 'ग', 'घ', 'ङ']:
                     # Ensure it's not a Taddhita (This logic requires metadata, assumed False for now)
                     trace.append(f"1.3.8 Laśakvataddhite: {res[0].char} is It.")
                     res.pop(0)

        return res, trace
'''
    # Update Live File
    Path("shared/anubandha.py").write_text(new_anubandha_code, encoding='utf-8')
    print("✅ UPDATED: shared/anubandha.py")
    
    # Update Launchpad Golden Source (so Rebuilds don't erase it)
    lp_path = Path("launchpad.py")
    if lp_path.exists():
        content = lp_path.read_text(encoding='utf-8')
        # Simple string replacement for the Anubandha section would be risky with regex.
        # Ideally, you manually update launchpad logic, but for now, 
        # we will rely on the fact that you can 'Rebuild' using this script logic later.
        print("⚠️ NOTE: If you run 'Rebuild Everything' from launchpad later, apply this update again.")

if __name__ == "__main__":
    upgrade_sutra_1_3_6()