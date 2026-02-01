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
        stem = ad(stem_str)
        last_char = stem[-1].char
        
        is_at = (last_char == 'अ')   
        is_aa = (last_char == 'आ')   # Ramā (Strīliṅga)
        is_it = (last_char == 'इ')                 
        is_ut = (last_char == 'उ')                 
        is_ghi = (is_it or is_ut)                  
        
        sup_data = KnowledgeBase.get_sup(vibhakti, vacana)
        if not sup_data: return "?"
        raw_sup, tags = sup_data; suffix = ad(raw_sup)
        
        if logger: logger.log("4.1.2", f"Suffix Attachment ({raw_sup})", f"{stem_str} + {raw_sup}", stem + suffix, "Maharshi Pāṇini")
        
        clean_suffix, trace = SanjnaController.run_it_prakaran(suffix, UpadeshaType.VIBHAKTI)
        if clean_suffix: clean_suffix[0].sanjnas.update(tags)
        
        if logger and trace:
             logger.log(trace[-1], "It-Lopa", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")

        # ========================================================
        # 🟣 RAMĀ STRATEGY (Ākārānta Strīliṅga)
        # ========================================================
        if is_aa:
            # 1.1 Su-Lopa
            if vibhakti == 1 and vacana == 1:
                clean_suffix = [] 
                if logger: logger.log("6.1.68", "Hal-Ngya-Bbhyo (Su Lopa)", sanskrit_varna_samyoga(stem), stem, "Maharshi Pāṇini")
                return sanskrit_varna_samyoga(stem)

            # 8.1 Sambodhana (He Rame)
            if vibhakti == 8 and vacana == 1:
                stem[-1].char = 'ए'
                if logger: logger.log("7.3.106", "Sambuddhau Ca (Aa->E)", "रमे + स्", stem + clean_suffix, "Maharshi Pāṇini")
                if clean_suffix and clean_suffix[0].char == 'स्':
                    clean_suffix = []
                    if logger: logger.log("6.1.69", "Sambuddhi Lopa", "रमे", stem, "Maharshi Pāṇini")
                return "हे " + sanskrit_varna_samyoga(stem)

            # 1.2 / 2.2 Au -> Shee (Rame)
            if vacana == 2 and (vibhakti == 1 or vibhakti == 2):
                stem[-1].char = 'ए' 
                clean_suffix = []
                if logger: logger.log("7.1.18", "Aungaapah (Au->Shee)", "रमे", stem, "Maharshi Pāṇini")
                return sanskrit_varna_samyoga(stem)

            # 3.1 Ta -> Ramaya
            if vibhakti == 3 and vacana == 1:
                stem[-1].char = 'ए'
                if logger: logger.log("7.3.105", "Angi Capah (Aa->E)", "रमे + आ", stem + clean_suffix, "Maharshi Pāṇini")
                # Sandhi will handle Rame + a -> Ramaya

            # 4.1 Ramayai (Vriddhi)
            if vibhakti == 4 and vacana == 1:
                clean_suffix = ad("यै") # Yāṭ + E (Vriddhi)
                if logger: logger.log("7.3.113", "Yadaapah + Vriddhi", "रमायै", stem + clean_suffix, "Maharshi Pāṇini")
                return "रमायै"

            # 5.1 / 6.1 Ramayah (Yat + Visarga)
            if vibhakti in [5, 6] and vacana == 1:
                # Ngasi/Ngas -> As. Yāṭ -> Ya. Ya + As -> Yāḥ (Dirgha + Rutva/Visarga)
                clean_suffix = ad("याः")
                if logger: logger.log("7.3.113", "Yadaapah (Yat + As -> Yaah)", "रमायाः", stem + clean_suffix, "Maharshi Pāṇini")
                return "रमायाः"

            # 7.1 Ramayam (Ngi -> Aam + Yat)
            if vibhakti == 7 and vacana == 1:
                clean_suffix = ad("याम्") # Ngi -> Aam (7.3.116) + Yat -> Yaam
                if logger: logger.log("7.3.116", "Neraam + Yadaapah", "रमायाम्", stem + clean_suffix, "Maharshi Pāṇini")
                return "रमायाम्"

            # 6.3 Ramanam (Nut)
            if vibhakti == 6 and vacana == 3:
                clean_suffix = ad("नाम्")
                if logger: logger.log("7.1.54", "Hrasvanadyapo Nut", "रमानाम्", stem + clean_suffix, "Maharshi Pāṇini")

        # ========================================================
        # 🔵 PRE-CHECKS
        # ========================================================
        if (is_at or is_ghi or is_aa) and vibhakti == 2 and vacana == 1:
            res_str = stem_str + "म्"
            if logger: logger.log("6.1.107", "Ami Purvah", res_str, ad(res_str), "Maharshi Pāṇini")
            return res_str

        # ========================================================
        # 🟢 GHI STRATEGY (HARI & GURU)
        # ========================================================
        if is_ghi:
            guna_char = 'ए' if is_it else 'ओ'
            dirgha_char = 'ई' if is_it else 'ऊ'
            
            if (vibhakti == 1 and vacana == 2) or                (vibhakti == 2 and vacana == 2) or                (vibhakti == 2 and vacana == 3):
                stem[-1].char = dirgha_char
                if vacana == 2: 
                    clean_suffix = []
                    if logger: logger.log("6.1.102", "Prathamayoh Purvasavarnah", sanskrit_varna_samyoga(stem), stem, "Maharshi Pāṇini")
                    return sanskrit_varna_samyoga(stem)
                if vacana == 3:
                     clean_suffix = ad("स्")
                     if logger: logger.log("6.1.102", "Prathamayoh Purvasavarnah", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")

            elif vibhakti == 3 and vacana == 1:
                clean_suffix = ad("ना")
                if logger: logger.log("7.3.120", "Ango Na Astriyam", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")
            
            elif (vibhakti == 4 and vacana == 1) or                  (vibhakti == 1 and vacana == 3) or                  (vibhakti in [5, 6] and vacana == 1):
                stem[-1].char = guna_char
                rule_ref = "7.3.109" if (vibhakti==1) else "7.3.111"
                rule_name = "Jasi Ca (Guna)" if (vibhakti==1) else "Gher-Niti (Guna)"
                if logger: logger.log(rule_ref, rule_name, sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")
                
                if vibhakti in [5, 6] and vacana == 1:
                    clean_suffix = ad("स्") 
                    if logger: logger.log("6.1.110", "Ngasi-Ngasosh-Ca (Purvarupa)", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")

            elif vibhakti == 6 and vacana == 3:
                clean_suffix = ad("नाम्")
                if logger: logger.log("7.1.54", "Hrasvanadyapo Nut", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")
                stem[-1].char = dirgha_char
                if logger: logger.log("6.4.3", "Nami (Dirgha)", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")

            elif vibhakti == 7 and vacana == 1:
                stem[-1].char = 'अ'
                if logger: logger.log("7.3.119", "Accha Gheh (Stem->a)", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")
                clean_suffix = ad("औ")
                if logger: logger.log("7.3.118", "Aut (Ni->Au)", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")

            elif vibhakti == 8 and vacana == 1:
                stem[-1].char = guna_char
                if logger: logger.log("7.3.108", "Hrasvasya Gunah", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")
                if clean_suffix and clean_suffix[0].char == 'स्':
                    clean_suffix = []
                    if logger: logger.log("6.1.69", "Sambuddhi Lopa", sanskrit_varna_samyoga(stem), stem, "Maharshi Pāṇini")
                    return "हे " + sanskrit_varna_samyoga(stem)

        # ========================================================
        # 🟠 RAMA STRATEGY
        # ========================================================
        if vibhakti == 8 and vacana == 1 and is_at:
            if clean_suffix and clean_suffix[0].char == 'स्':
                clean_suffix = [] 
                if logger: logger.log("6.1.69", "Sambuddhi Lopa", sanskrit_varna_samyoga(stem), stem, "Maharshi Pāṇini")

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
                stem[-1].char = 'आ'
                if logger: logger.log("6.4.3", "Nami (Dirgha)", "रामानाम्", stem + clean_suffix, "Maharshi Pāṇini")
        
        if is_at and clean_suffix:
            f = clean_suffix[0].char
            if vacana == 3 and f in ['भ्', 'स्']: 
                if not (vibhakti == 2 and vacana == 3): 
                    stem[-1].char = 'ए'
                    if logger: logger.log("7.3.103", "Bahuvacane Jhalyet", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")
            elif vibhakti in [6, 7] and vacana == 2: 
                stem[-1].char = 'ए'
                if logger: logger.log("7.3.104", "Osi Ca", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")
            elif f in ['भ्', 'य', 'व्', 'य्', 'व']: 
                if AdhikaraController.is_rule_in_scope("7.3.102", "ANGASYA"):
                     stem[-1].char = 'आ'
                     if logger: logger.log("7.3.102", "Supi Ca", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")

        # ========================================================
        # 🟡 COMMON SANDHI
        # ========================================================
        
        fp, rule = SandhiProcessor.apply_ac_sandhi(stem, clean_suffix)
        if logger and rule:
             logger.log(rule, "Sandhi", sanskrit_varna_samyoga(fp), fp, "Maharshi Pāṇini")
        
        if vibhakti == 2 and vacana == 3:
            if fp[-1].char == 'स्' or fp[-1].char == 'ः':
                 fp[-1].char = 'न्'
                 if logger: logger.log("6.1.103", "Tasmacchaso Nah Pumsi", sanskrit_varna_samyoga(fp), fp, "Maharshi Pāṇini")
                 return sanskrit_varna_samyoga(fp)

        # Tripadi
        final = SandhiProcessor.run_tripadi(fp, logger) 
        res = sanskrit_varna_samyoga(final)
        
        if vibhakti == 8: return "हे " + res

        return res
