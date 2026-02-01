"""
FILE: core/sanjna_controller.py
"""
from core.core_foundation import Varna, UpadeshaType

class SanjnaController:
    
    @staticmethod
    def run_it_prakaran(varnas, context=UpadeshaType.VIBHAKTI):
        if not varnas: return varnas, []
        
        res = list(varnas)
        applied = []
        
        # Track if Halantyam removed something
        halantyam_applied = False

        # --- 1. HALANTYAM (1.3.3) FIRST ---
        # We check end FIRST to distinguish Sup (ends in p) from Su (ends in u)
        if res:
            last = res[-1]
            if not last.is_vowel:
                # Tusmah check
                is_tusma = last.char in ['त', 'थ', 'द', 'ध', 'न', 'स', 'स्', 'म', 'म्']
                if not is_tusma:
                    # Sup (p), Out (t), etc.
                    if last.char in ['प्', 'ट', 'ङ', 'ट्', 'ण्', 'ञ्']:
                        res.pop()
                        applied.append("1.3.3")
                        halantyam_applied = True

        # --- 2. LASHAKVA / CHUTU (Initial) ---
        if res:
            c0 = res[0].char
            # Chutu (Jas, Ta)
            if c0 in ['च', 'छ', 'ज', 'झ', 'ञ', 'ट', 'ठ', 'ड', 'ढ', 'ण']:
                res.pop(0)
                applied.append("1.3.7")
            # Lashakva (Shas, Ne...)
            elif c0 in ['ल', 'श्', 'श', 'क', 'ख', 'ग', 'घ', 'ङ']:
                res.pop(0)
                applied.append("1.3.8")

        # --- 3. UPADESHE AJ (1.3.2) ---
        # Only if Halantyam did NOT apply (distinguish Su from Sup)
        # Su (1.1) -> No halantyam (u is final). Remove u.
        # Sup (7.3) -> Halantyam removed p. Remaining is Su. Keep u.
        
        if not halantyam_applied:
            if len(res) >= 1 and res[0].char == 'स':
                # Check for u
                if len(res) > 1 and res[1].char in ['उ', 'ु', 'ँ']:
                     # Remove everything after s
                     while len(res) > 1: res.pop()
                     applied.append("1.3.2")

        return res, applied
