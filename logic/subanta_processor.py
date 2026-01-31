"""
FILE: logic/subanta_processor.py
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga, UpadeshaType
from core.sanjna_controller import SanjnaController
from core.knowledge_base import KnowledgeBase
from logic.sandhi_processor import SandhiProcessor
from core.adhikara_controller import AdhikaraController

class SubantaProcessor:
    @staticmethod
    def derive_pada(stem_str, vibhakti, vacana, logger=None):
        stem = ad(stem_str); is_at = (stem[-1].char == 'अ')
        sup_data = KnowledgeBase.get_sup(vibhakti, vacana)
        if not sup_data: return "?"
        raw_sup, tags = sup_data; suffix = ad(raw_sup)
        
        # A1: Citation - Pāṇini 4.1.2
        if logger: logger.log("4.1.2", f"Suffix Attachment ({raw_sup})", f"{stem_str} + {raw_sup}", stem + suffix, "Maharshi Pāṇini")
        
        clean_suffix, trace = SanjnaController.run_it_prakaran(suffix, UpadeshaType.VIBHAKTI)
        if clean_suffix: clean_suffix[0].sanjnas.update(tags)
        
        if logger and trace:
             logger.log(trace[-1], "It-Lopa", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")

        # Context Analysis for R31 (Nivṛtti)
        # Check Bha Sanjna (1.4.18 Yachi Bham)
        is_yachi = False
        if clean_suffix:
            f = clean_suffix[0].char
            if clean_suffix[0].is_vowel or f == 'य्': is_yachi = True
        
        # Simple Logic: 1.1 to 2.2 are Sarvanamasthana (Strong) -> Pada (mostly). 
        # 4.1 (Ne -> Ya) is Bha? No, Ne starts with Ng (It), remaining is E. Yachi Bham applies.
        # For Rama, we simplify:
        context = {"is_bham": is_yachi and vibhakti >= 4} # Rough heuristic for demonstration

        # [8.1] Sambodhana
        if vibhakti == 8 and vacana == 1 and is_at:
            if clean_suffix and clean_suffix[0].char == 'स्':
                clean_suffix = [] 
                if logger: logger.log("6.1.69", "Sambuddhi Lopa", sanskrit_varna_samyoga(stem), stem, "Maharshi Pāṇini")

        # R11: Niyama
        if is_at:
            if vibhakti == 3 and vacana == 1: 
                clean_suffix = ad("इन")
                if logger: logger.log("7.1.12", "Ta -> Ina", "रामेन", stem + clean_suffix, "Maharshi Pāṇini")
            elif vibhakti == 3 and vacana == 3: 
                clean_suffix = ad("ऐस्")
                if logger: logger.log("7.1.9", "Bhis -> Ais", "रामऐस्", stem + clean_suffix, "Maharshi Pāṇini")
            elif vibhakti == 4 and vacana == 1: 
                clean_suffix = ad("य")
                if logger: logger.log("7.1.13", "Ne -> Ya", "रामय", stem + clean_suffix, "Maharshi Pāṇini")
            elif vibhakti == 5 and vacana == 1: 
                clean_suffix = ad("आत्")
                if logger: logger.log("7.1.12", "Ngasi -> At", "रामआत्", stem + clean_suffix, "Maharshi Pāṇini")
            elif vibhakti == 6 and vacana == 1: 
                clean_suffix = ad("स्य")
                if logger: logger.log("7.1.12", "Ngas -> Sya", "रामस्य", stem + clean_suffix, "Maharshi Pāṇini")
            elif vibhakti == 6 and vacana == 3: 
                clean_suffix = ad("न्") + clean_suffix
                if logger: logger.log("7.1.54", "Nut Agama", "रामनाम्", stem + clean_suffix, "Maharshi Pāṇini")
                stem[-1].char = 'आ' # Nami
                if logger: logger.log("6.4.3", "Nami (Dirgha)", "रामानाम्", stem + clean_suffix, "Maharshi Pāṇini")

        # R12: Adhikara - Mutators (Requires R31 check!)
        if is_at and clean_suffix:
            f = clean_suffix[0].char
            
            # Jhalyet (7.3.103) - Under Angasya
            # R31 Check: Is Angasya Active? Yes (Global for Subanta).
            if vacana == 3 and f in ['भ्', 'स्']: 
                if not (vibhakti == 2 and vacana == 3): 
                    stem[-1].char = 'ए'
                    if logger: logger.log("7.3.103", "Bahuvacane Jhalyet", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")
            
            # Osi Ca (7.3.104)
            elif vibhakti in [6, 7] and vacana == 2: 
                stem[-1].char = 'ए'
                if logger: logger.log("7.3.104", "Osi Ca", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")
            
            # Supi Ca (7.3.102) - Under Angasya
            elif f in ['भ्', 'य', 'व्', 'य्', 'व']: 
                # Verify Adhikara Scope
                if AdhikaraController.is_rule_in_scope("7.3.102", "ANGASYA"):
                     stem[-1].char = 'आ'
                     if logger: logger.log("7.3.102", "Supi Ca", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")

        # 2.1 Ami Purvah Bypass
        if is_at and vibhakti == 2 and vacana == 1:
            res_str = stem_str + "म्"
            if logger: logger.log("6.1.107", "Ami Purvah", res_str, ad(res_str), "Maharshi Pāṇini")
            return res_str

        # Sandhi
        fp, rule = SandhiProcessor.apply_ac_sandhi(stem, clean_suffix)
        if logger and rule:
             logger.log(rule, "Sandhi", sanskrit_varna_samyoga(fp), fp, "Maharshi Pāṇini")
        
        # 2.3 Shaso Nah Pumsi
        if is_at and vibhakti == 2 and vacana == 3:
            if fp[-1].char == 'स्' or fp[-1].char == 'ः':
                fp[-1].char = 'न्'
                if logger: logger.log("6.1.103", "Shaso Nah", sanskrit_varna_samyoga(fp), fp, "Maharshi Pāṇini")
                return sanskrit_varna_samyoga(fp)

        # Tripadi (Visarga etc.)
        final = SandhiProcessor.run_tripadi(fp, logger) 
        res = sanskrit_varna_samyoga(final)
        
        if vibhakti == 8: return "हे " + res

        return res
