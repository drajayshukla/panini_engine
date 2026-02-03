
from shared.varnas import Varna

class AnubandhaEngine:
    @staticmethod
    def process(varnas, context="General"):
        if not varnas: return [], set()
        res = list(varnas)
        tags = set()
        
        # 1.3.2 Upadeshe Aj Anunasika It (Universal)
        # Since 'ad' now groups ['उँ'], we just check v.char for 'ँ'
        new_res = []
        for v in res:
            if 'ँ' in v.char:
                tags.add(f"{v.char}-It (1.3.2)")
                # It's an It-letter, so it drops (Lopa)
                # Note: In pure theory, only the nasal quality drops, but for 'u~' in 'su~', the whole vowel is 'It'.
                pass 
            else:
                new_res.append(v)
        res = new_res

        # 1.3.3 Halantyam (Universal)
        if res and res[-1].is_consonant:
            last = res[-1].char
            is_vibhakti_stop = context == "Vibhakti" and last in ['स्', 'म्', 'त्']
            if not is_vibhakti_stop:
                tags.add(f"{last}-It (1.3.3)")
                res.pop()

        return res, tags
