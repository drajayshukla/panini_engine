
from core.core_foundation import Varna, UpadeshaType

class SanjnaController:
    @staticmethod
    def run_it_prakaran(varnas, context=UpadeshaType.VIBHAKTI):
        if not varnas: return varnas, []
        res = list(varnas)
        applied = []
        # Restore IT-Lopa logic for 1.3.3 and 1.3.2
        if not res[-1].is_vowel and res[-1].char not in ['स्', 'म्']:
            res.pop(); applied.append("1.3.3")
        return res, applied

    @staticmethod
    def identify_structural_samjnas(varnas):
        """Implements 1.1.64 (Ti) and 1.1.65 (Upadha)"""
        if len(varnas) >= 2: varnas[-2].add_samjna("UPADHA", "1.1.65")
        v_idx = [i for i,v in enumerate(varnas) if v.is_vowel]
        if v_idx:
            for i in range(v_idx[-1], len(varnas)): varnas[i].add_samjna("TI", "1.1.64")
