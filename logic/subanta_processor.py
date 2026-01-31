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
        if not sup_data: return "?"
        raw_sup, tags = sup_data; suffix = ad(raw_sup)
        
        # 1. Suffix Attachment (प्रत्यय उत्पत्ति)
        if logger: logger.log("4.1.2", f"Suffix Attachment ({raw_sup})", f"{stem_str} + {raw_sup}", stem + suffix)
        
        # 2. It-Prakaran (इत् संज्ञा और लोप)
        clean_suffix, trace = SanjnaController.run_it_prakaran(suffix, UpadeshaType.VIBHAKTI)
        if clean_suffix: clean_suffix[0].sanjnas.update(tags)
        
        # Log It-Lopa steps
        if logger and trace:
             logger.log(f"{trace[-1]}", "It-Lopa (इत् संज्ञा लोप)", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix)

        # [8.1] Sambodhana - Su Lopa (6.1.69)
        if vibhakti == 8 and vacana == 1 and is_at:
            if clean_suffix and clean_suffix[0].char == 'स्':
                clean_suffix = [] 
                if logger: logger.log("6.1.69 (एङ्ह्रस्वात् सम्बुद्धेः)", "Sambuddhi Lopa (सम्बुद्धिलोपा)", sanskrit_varna_samyoga(stem), stem)

        # R11: Niyama - Special Substitutions
        if is_at:
            if vibhakti == 3 and vacana == 1: 
                clean_suffix = ad("इन")
                if logger: logger.log("7.1.12", "Ta -> Ina (टाङसिङ...)", "रामेन", stem + clean_suffix)
            elif vibhakti == 3 and vacana == 3: 
                clean_suffix = ad("ऐस्")
                if logger: logger.log("7.1.9", "Bhis -> Ais (अतो भिस ऐस्)", "रामऐस्", stem + clean_suffix)
            elif vibhakti == 4 and vacana == 1: 
                clean_suffix = ad("य")
                if logger: logger.log("7.1.13", "Ne -> Ya (ङेर्यः)", "रामय", stem + clean_suffix)
            elif vibhakti == 5 and vacana == 1: 
                clean_suffix = ad("आत्")
                if logger: logger.log("7.1.12", "Ngasi -> At (टाङसिङ...)", "रामआत्", stem + clean_suffix)
            elif vibhakti == 6 and vacana == 1: 
                clean_suffix = ad("स्य")
                if logger: logger.log("7.1.12", "Ngas -> Sya (टाङसिङ...)", "रामस्य", stem + clean_suffix)
            elif vibhakti == 6 and vacana == 3: 
                clean_suffix = ad("न्") + clean_suffix
                if logger: logger.log("7.1.54", "Nut Agama (ह्रस्वनद्यापो नुट्)", "रामनाम्", stem + clean_suffix)
                stem[-1].char = 'आ' # Nami
                if logger: logger.log("6.4.3", "Nami (Dirgha) (नामि)", "रामानाम्", stem + clean_suffix)

        # R12: Adhikara - Mutators
        if is_at and clean_suffix:
            f = clean_suffix[0].char
            # Jhalyet
            if vacana == 3 and f in ['भ्', 'स्']: 
                if not (vibhakti == 2 and vacana == 3): 
                    stem[-1].char = 'ए'
                    if logger: logger.log("7.3.103", "Bahuvacane Jhalyet (बहुवचने झल्येत्)", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix)
            # Osi Ca
            elif vibhakti in [6, 7] and vacana == 2: 
                stem[-1].char = 'ए'
                if logger: logger.log("7.3.104", "Osi Ca (ओसि च)", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix)
            # Supi Ca
            elif f in ['भ्', 'य', 'व्', 'य्', 'व']: 
                stem[-1].char = 'आ'
                if logger: logger.log("7.3.102", "Supi Ca (सुपि च)", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix)

        # 2.1 Ami Purvah Bypass
        if is_at and vibhakti == 2 and vacana == 1:
            res_str = stem_str + "म्"
            if logger: logger.log("6.1.107", "Ami Purvah (अमि पूर्वः)", res_str, ad(res_str))
            return res_str

        # Sandhi
        fp, rule = SandhiProcessor.apply_ac_sandhi(stem, clean_suffix)
        if logger and rule:
             logger.log(rule, "Sandhi", sanskrit_varna_samyoga(fp), fp)
        
        # 2.3 Shaso Nah Pumsi
        if is_at and vibhakti == 2 and vacana == 3:
            if fp[-1].char == 'स्' or fp[-1].char == 'ः':
                fp[-1].char = 'न्'
                if logger: logger.log("6.1.103", "Shaso Nah (तस्माच्छसो नः पुंसि)", sanskrit_varna_samyoga(fp), fp)
                return sanskrit_varna_samyoga(fp)

        # Tripadi (Visarga etc.)
        final = SandhiProcessor.run_tripadi(fp, logger) # Sending Logger to Tripadi
        res = sanskrit_varna_samyoga(final)
        
        # [USER REQUEST]: Add 'He' prefix for Case 8 output
        if vibhakti == 8:
            return "हे " + res

        return res
