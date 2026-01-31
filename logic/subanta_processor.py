"""
FILE: logic/subanta_processor.py
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga, UpadeshaType
from core.sanjna_controller import SanjnaController
from core.knowledge_base import KnowledgeBase
from logic.sandhi_processor import SandhiProcessor

class SubantaProcessor:
    @staticmethod
    def derive_pada(stem_str, vibhakti, vacana, logger=None):
        stem = ad(stem_str); is_at = (stem[-1].char == 'अ')
        sup_data = KnowledgeBase.get_sup(vibhakti, vacana)
        raw_sup, tags = sup_data; suffix = ad(raw_sup)
        
        clean_suffix, trace = SanjnaController.run_it_prakaran(suffix, UpadeshaType.VIBHAKTI)
        if clean_suffix: clean_suffix[0].sanjnas.update(tags)

        # [8.1] Sambodhana - Su Lopa (6.1.69)
        if vibhakti == 8 and vacana == 1 and is_at:
            if clean_suffix and clean_suffix[0].char == 'स्':
                clean_suffix = [] # लोप (Delete 's')
                if logger: logger.log("6.1.69 (एङ्ह्रस्वात् सम्बुद्धेः)", "Sambuddhi Lopa", sanskrit_varna_samyoga(stem), stem)

        # R11: Niyama - Special Substitutions
        if is_at:
            if vibhakti == 3 and vacana == 1: clean_suffix = ad("इन")
            elif vibhakti == 3 and vacana == 3: clean_suffix = ad("ऐस्")
            elif vibhakti == 4 and vacana == 1: clean_suffix = ad("य")
            elif vibhakti == 5 and vacana == 1: clean_suffix = ad("आत्")
            elif vibhakti == 6 and vacana == 1: clean_suffix = ad("स्य")
            elif vibhakti == 6 and vacana == 3: 
                clean_suffix = ad("न्") + clean_suffix
                stem[-1].char = 'आ' # Nami

        # R12: Adhikara - Mutators
        if is_at and clean_suffix:
            f = clean_suffix[0].char
            # Jhalyet
            if vacana == 3 and f in ['भ्', 'स्']: 
                if not (vibhakti == 2 and vacana == 3): stem[-1].char = 'ए'
            # Osi Ca
            elif vibhakti in [6, 7] and vacana == 2: stem[-1].char = 'ए'
            # Supi Ca
            elif f in ['भ्', 'य', 'व्', 'य्', 'व']: stem[-1].char = 'आ'

        # 2.1 Ami Purvah Bypass
        if is_at and vibhakti == 2 and vacana == 1:
            res_str = stem_str + "म्"
            if logger: logger.log("6.1.107", "Ami Purvah", res_str, ad(res_str))
            return res_str

        fp, rule = SandhiProcessor.apply_ac_sandhi(stem, clean_suffix)
        
        # 2.3 Shaso Nah Pumsi
        if is_at and vibhakti == 2 and vacana == 3:
            if fp[-1].char == 'स्' or fp[-1].char == 'ः':
                fp[-1].char = 'न्'
                if logger: logger.log("6.1.103", "Shaso Nah", sanskrit_varna_samyoga(fp), fp)
                return sanskrit_varna_samyoga(fp)

        final = SandhiProcessor.run_tripadi(fp)
        res = sanskrit_varna_samyoga(final)
        
        if logger: logger.log("Final", "Prakriya Complete", res, final)

        # [USER REQUEST]: Add 'He' prefix for Case 8 output
        if vibhakti == 8:
            return "हे " + res

        return res
