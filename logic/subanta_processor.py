"""
FILE: logic/subanta_processor.py
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga, UpadeshaType
from core.sanjna_controller import SanjnaController
from core.knowledge_base import KnowledgeBase
from logic.sandhi_processor import SandhiProcessor
from core.adhikara_controller import AdhikaraController

class SubantaProcessor:
    # --- KNOWLEDGE BASE OF FORBIDDEN INPUTS (Mock Data) ---
    # In a real engine, this would be a query to the Dhatupatha & Pratyaya DB.
    KNOWN_DHATUS = {
        'भू', 'एध', 'पच्', 'गम्', 'स्था', 'दृश्', 'अस्', 'कृ', 'हृ', 'नी', 'या', 'वा', 
        'जि', 'क्षि', 'श्रु', 'दा', 'धा'
    }
    
    KNOWN_PRATYAYAS = {
        'सु', 'औ', 'जस्', 'अम्', 'औट्', 'शस्', 'टा', 'भ्याम्', 'भिस्', 
        'ङे', 'भ्यस्', 'ङसि', 'ङस्', 'ओस्', 'आम्', 'ङि', 'सुप्',
        'तिप्', 'तस्', 'झि', 'सिप्', 'थस्', 'थ', 'मिप्', 'वस्', 'मस्',
        'शप्', 'श्नु', 'स्य', 'तासि', 'क्विप्', 'घञ्'
    }

    @staticmethod
    def derive_pada(stem_str, vibhakti, vacana, logger=None):
        stem = ad(stem_str)
        
        # ========================================================
        # 🛡️ STEP 0: PRATIPADIKA VALIDATION (1.2.45)
        # ========================================================
        # "Arthavad-adhatu-rapratyayah Pratipadikam"
        
        # 1. Adhatu Check (Not a Root)
        if stem_str in SubantaProcessor.KNOWN_DHATUS:
            msg = f"⛔ PROHIBITED: '{stem_str}' is a Dhatu (Root)."
            if logger: 
                logger.log("1.2.45", "Adhatuh (Validation Fail)", msg, stem, "Maharshi Pāṇini")
            return "Error: Dhatu"

        # 2. Apratyaya Check (Not a Suffix)
        if stem_str in SubantaProcessor.KNOWN_PRATYAYAS:
            msg = f"⛔ PROHIBITED: '{stem_str}' is a Pratyaya (Suffix)."
            if logger: 
                logger.log("1.2.45", "Apratyayah (Validation Fail)", msg, stem, "Maharshi Pāṇini")
            return "Error: Pratyaya"

        # 3. Success Log
        if logger:
            logger.log("1.2.45", "Arthavad-adhatu-rapratyayah Pratipadikam", f"✅ '{stem_str}' is a valid Stem.", stem, "Maharshi Pāṇini")

        # ========================================================
        # 🚀 DERIVATION START
        # ========================================================
        last_char = stem[-1].char
        
        is_at = (last_char == 'अ')   
        is_aa = (last_char == 'आ')   
        is_it = (last_char == 'इ')                 
        is_ut = (last_char == 'उ')                 
        is_ghi = (is_it or is_ut)                  
        
        # Gender Heuristics (Simple for now)
        # Assuming explicit feminine list or Aa-ending
        FEMININE_STEMS = {'मति', 'बुद्धि', 'धेनु', 'रमा', 'गौरी', 'लता'}
        is_fem_ghi = (stem_str in FEMININE_STEMS) or is_aa
        
        sup_data = KnowledgeBase.get_sup(vibhakti, vacana)
        if not sup_data: return "?"
        raw_sup, tags = sup_data; suffix = ad(raw_sup)
        
        if logger: logger.log("4.1.2", f"Suffix Attachment ({raw_sup})", f"{stem_str} + {raw_sup}", stem + suffix, "Maharshi Pāṇini")
        
        clean_suffix, trace = SanjnaController.run_it_prakaran(suffix, UpadeshaType.VIBHAKTI)
        if clean_suffix: clean_suffix[0].sanjnas.update(tags)
        
        if logger and trace:
             logger.log(trace[-1], "It-Lopa", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")

        # --- RAMA (Feminine) ---
        if is_aa:
            # 1.1 Su Lopa
            if vibhakti == 1 and vacana == 1:
                clean_suffix = [] 
                if logger: logger.log("6.1.68", "Hal-Ngya-Bbhyo (Su Lopa)", sanskrit_varna_samyoga(stem), stem, "Maharshi Pāṇini")
                return sanskrit_varna_samyoga(stem)
            
            # 8.1 Sambodhana
            if vibhakti == 8 and vacana == 1:
                stem[-1].char = 'ए'
                if logger: logger.log("7.3.106", "Sambuddhau Ca (Aa->E)", "रमे + स्", stem + clean_suffix, "Maharshi Pāṇini")
                if clean_suffix and clean_suffix[0].char == 'स्': clean_suffix = []
                return "हे " + sanskrit_varna_samyoga(stem)

            # 1.2/2.2 Au -> Shee
            if vacana == 2 and (vibhakti == 1 or vibhakti == 2):
                stem[-1].char = 'ए'; clean_suffix = []
                if logger: logger.log("7.1.18", "Aungaapah", "रमे", stem, "Maharshi Pāṇini")
                return sanskrit_varna_samyoga(stem)

            # 3.1 Ta -> Ramaya
            if vibhakti == 3 and vacana == 1:
                stem[-1].char = 'ए'
                if logger: logger.log("7.3.105", "Angi Capah", "रमे + आ", stem + clean_suffix, "Maharshi Pāṇini")

            # Yat Agama (4.1, 5.1, 6.1, 7.1)
            if vibhakti in [4, 5, 6, 7] and vacana == 1:
                if vibhakti == 7:
                    clean_suffix = ad("आम्")
                    if logger: logger.log("7.3.116", "Neraam", "रमा + आम्", stem + clean_suffix, "Maharshi Pāṇini")
                
                clean_suffix = ad("या") + clean_suffix
                if logger: logger.log("7.3.113", "Yadaapah", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")

                # Vriddhi / Dirgha handling inside suffixes
                if vibhakti == 4:
                    clean_suffix = ad("यै")
                    if logger: logger.log("6.1.88", "Vriddhi", "रमायै", stem + clean_suffix, "Maharshi Pāṇini")
                    return "रमायै"
                if vibhakti in [5, 6]:
                    clean_suffix = ad("यास्")
                    if logger: logger.log("6.1.101", "Dirgha", "रमायास्", stem + clean_suffix, "Maharshi Pāṇini")
                if vibhakti == 7:
                    clean_suffix = ad("याम्")
                    if logger: logger.log("6.1.101", "Dirgha", "रमायाम्", stem + clean_suffix, "Maharshi Pāṇini")
                    return "रमायाम्"

            if vibhakti == 6 and vacana == 3:
                clean_suffix = ad("नाम्")
                if logger: logger.log("7.1.54", "Nut", "रमानाम्", stem + clean_suffix, "Maharshi Pāṇini")

        # --- PRE-CHECKS ---
        if (is_at or is_ghi or is_aa) and vibhakti == 2 and vacana == 1:
            res_str = stem_str + "म्"
            if logger: logger.log("6.1.107", "Ami Purvah", res_str, ad(res_str), "Maharshi Pāṇini")
            return res_str

        # --- GHI (HARI/GURU/MATI) ---
        if is_ghi:
            guna_char = 'ए' if is_it else 'ओ'
            dirgha_char = 'ई' if is_it else 'ऊ'
            
            if (vibhakti == 1 and vacana == 2) or                (vibhakti == 2 and vacana == 2) or                (vibhakti == 2 and vacana == 3):
                stem[-1].char = dirgha_char
                if vacana == 2: clean_suffix = []
                if vacana == 3: clean_suffix = ad("स्")
                if logger: logger.log("6.1.102", "Prathamayoh Purvasavarnah", sanskrit_varna_samyoga(stem+clean_suffix), stem, "Maharshi Pāṇini")

            elif vibhakti == 3 and vacana == 1:
                if not is_fem_ghi:
                    clean_suffix = ad("ना")
                    if logger: logger.log("7.3.120", "Ango Na Astriyam", sanskrit_varna_samyoga(stem+clean_suffix), stem, "Maharshi Pāṇini")
                else:
                    if logger: logger.log("7.3.120", "Astriyam (No Na)", sanskrit_varna_samyoga(stem+clean_suffix), stem, "Maharshi Pāṇini")

            elif vibhakti in [4, 5, 6, 7] and vacana == 1:
                # Ghi Form
                stem_a = stem[:]; stem_a[-1].char = guna_char
                suffix_a = clean_suffix[:]
                if vibhakti in [5, 6]: suffix_a = ad("स्")
                if vibhakti == 7: stem_a = ad(stem_str[:-1]+"औ"); suffix_a = []
                res_a = sanskrit_varna_samyoga(stem_a + suffix_a)
                if vibhakti == 4:
                    fp, _ = SandhiProcessor.apply_ac_sandhi(stem_a, suffix_a)
                    res_a = sanskrit_varna_samyoga(fp)

                if not is_fem_ghi:
                    if logger: logger.log("7.3.111", "Gher-Niti", res_a, ad(res_a), "Maharshi Pāṇini")
                    return res_a
                
                # Nadi Form (Mati)
                stem_b = stem[:]
                res_b = ""
                if vibhakti == 4: res_b = stem_str[:-1] + "्यै"
                elif vibhakti in [5, 6]: res_b = stem_str[:-1] + "्याः"
                elif vibhakti == 7: res_b = stem_str[:-1] + "्याम्"
                
                if logger: logger.log("7.3.117", "Idudbhyam (Option)", f"{res_a} / {res_b}", stem, "Maharshi Pāṇini")
                return f"{res_a} / {res_b}"

            elif vibhakti == 1 and vacana == 3:
                stem[-1].char = guna_char
                if logger: logger.log("7.3.109", "Jasi Ca", sanskrit_varna_samyoga(stem+clean_suffix), stem, "Maharshi Pāṇini")

            elif vibhakti == 6 and vacana == 3:
                clean_suffix = ad("नाम्"); stem[-1].char = dirgha_char
                if logger: logger.log("6.4.3", "Nami", sanskrit_varna_samyoga(stem+clean_suffix), stem, "Maharshi Pāṇini")

            elif vibhakti == 8 and vacana == 1:
                stem[-1].char = guna_char
                if logger: logger.log("7.3.108", "Hrasvasya Gunah", sanskrit_varna_samyoga(stem+clean_suffix), stem, "Maharshi Pāṇini")
                if clean_suffix and clean_suffix[0].char == 'स्': clean_suffix = []
                return "हे " + sanskrit_varna_samyoga(stem)

        # --- RAMA (Masculine) ---
        if vibhakti == 8 and vacana == 1 and is_at:
            if clean_suffix and clean_suffix[0].char == 'स्': clean_suffix = []
            if logger: logger.log("6.1.69", "Sambuddhi Lopa", sanskrit_varna_samyoga(stem), stem, "Maharshi Pāṇini")

        if is_at:
            if vibhakti == 3 and vacana == 1: clean_suffix = ad("इन")
            elif vibhakti == 3 and vacana == 3: clean_suffix = ad("ऐस्")
            elif vibhakti == 4 and vacana == 1: clean_suffix = ad("य")
            elif vibhakti == 5 and vacana == 1: clean_suffix = ad("आत्")
            elif vibhakti == 6 and vacana == 1: clean_suffix = ad("स्य")
            elif vibhakti == 6 and vacana == 3: 
                clean_suffix = ad("न्") + clean_suffix; stem[-1].char = 'आ'
        
        if is_at and clean_suffix:
            f = clean_suffix[0].char
            if vacana == 3 and f in ['भ्', 'स्']: 
                if not (vibhakti == 2 and vacana == 3): stem[-1].char = 'ए'
            elif vibhakti in [6, 7] and vacana == 2: stem[-1].char = 'ए'
            elif f in ['भ्', 'य', 'व्', 'य्', 'व']: 
                if AdhikaraController.is_rule_in_scope("7.3.102", "ANGASYA"): stem[-1].char = 'आ'

        # --- SANDHI ---
        fp, rule = SandhiProcessor.apply_ac_sandhi(stem, clean_suffix)
        if logger and rule: logger.log(rule, "Sandhi", sanskrit_varna_samyoga(fp), fp, "Maharshi Pāṇini")
        
        if vibhakti == 2 and vacana == 3:
            if fp[-1].char == 'स्' or fp[-1].char == 'ः': fp[-1].char = 'न्'

        final = SandhiProcessor.run_tripadi(fp, logger) 
        res = sanskrit_varna_samyoga(final)
        if vibhakti == 8: return "हे " + res
        return res
