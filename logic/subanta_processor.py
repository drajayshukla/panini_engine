"""
FILE: logic/subanta_processor.py
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga, UpadeshaType
from core.sanjna_controller import SanjnaController
from core.knowledge_base import KnowledgeBase
from logic.sandhi_processor import SandhiProcessor
from core.adhikara_controller import AdhikaraController
from core.dhatu_repo import DhatuRepository 

class SubantaProcessor:
    KNOWN_PRATYAYAS = {'सु', 'औ', 'जस्', 'अम्', 'औट्', 'शस्', 'टा', 'भ्याम्', 'भिस्', 'ङे', 'भ्यस्', 'ङसि', 'ङस्', 'ओस्', 'आम्', 'ङि', 'सुप्', 'तिप्', 'तस्', 'झि', 'सिप्', 'थस्', 'थ', 'मिप्', 'वस्', 'मस्', 'शप्', 'श्नु', 'स्य', 'तासि', 'क्विप्', 'घञ्'}
    FEMININE_I_U_STEMS = {'मति', 'बुद्धि', 'धेनु', 'कीर्ति', 'जाति', 'भक्ति'}
    VALID_SINGLE_LETTERS = {'अ', 'इ', 'उ', 'ऋ'}

    @staticmethod
    def _finalize(varnas, vibhakti, vacana, logger=None):
        """Helper to apply Tripadi and format output."""
        if not varnas: return ""
        
        # 2.3 Shaso Nah Logic (Only for Pum-linga, but currently generalized)
        # Assuming only applied if relevant logic triggered it? 
        # Actually, Shaso Nah (6.1.103) is Tripathi-purva (Sapad-saptadhyayi).
        # We handle it here or before Tripadi.
        # Logic: If suffix was Shas (As) and became 'n' via Purva Savarna (Ramaan).
        # We assume that handled in main logic.
        
        final = SandhiProcessor.run_tripadi(varnas, logger) 
        res = sanskrit_varna_samyoga(final)
        
        if vibhakti == 8: return "हे " + res
        return res

    @staticmethod
    def derive_pada(stem_str, vibhakti, vacana, logger=None, force_pratipadika=False):
        stem = ad(stem_str)
        
        # --- VALIDATION ---
        if force_pratipadika:
            if logger: logger.log("1.2.45", "Manual Override", f"⚠️ Forced: '{stem_str}'", stem, "User")
        else:
            if stem_str in SubantaProcessor.KNOWN_PRATYAYAS: return "Error: Pratyaya"
            if stem_str not in SubantaProcessor.VALID_SINGLE_LETTERS:
                try:
                    dhatu = DhatuRepository.get_dhatu_info(stem_str)
                    if dhatu: return "Error: Dhatu"
                except: pass
            if logger: logger.log("1.2.45", "Arthavad... Pratipadikam", f"✅ '{stem_str}'", stem, "Maharshi Pāṇini")

        # --- DERIVATION START ---
        last_char = stem[-1].char
        is_at = (last_char == 'अ')   
        is_aa = (last_char == 'आ')   
        is_it = (last_char == 'इ')                 
        is_ut = (last_char == 'उ')                 
        is_fem_ghi = (stem_str in SubantaProcessor.FEMININE_I_U_STEMS) or is_aa
        is_ghi_any = (is_it or is_ut)
        
        sup_data = KnowledgeBase.get_sup(vibhakti, vacana)
        if not sup_data: return "?"
        raw_sup, tags = sup_data; suffix = ad(raw_sup)
        
        if logger: logger.log("4.1.2", f"Suffix Attachment ({raw_sup})", f"{stem_str} + {raw_sup}", stem + suffix, "Maharshi Pāṇini")
        
        clean_suffix, trace = SanjnaController.run_it_prakaran(suffix, UpadeshaType.VIBHAKTI)
        if clean_suffix: clean_suffix[0].sanjnas.update(tags)
        if logger and trace: logger.log(trace[-1], "It-Lopa", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")

        # --- RAMA (AA) ---
        if is_aa:
            if vibhakti == 1 and vacana == 1: return SubantaProcessor._finalize(stem, vibhakti, vacana, logger) 
            if vibhakti == 8 and vacana == 1: 
                stem[-1].char = 'ए'; clean_suffix=[]
                if logger: logger.log("7.3.106", "Sambuddhau Ca", "रमे", stem, "Maharshi Pāṇini")
                return SubantaProcessor._finalize(stem, vibhakti, vacana, logger)
            if vacana == 2 and (vibhakti in [1,2]): 
                stem[-1].char = 'ए'; clean_suffix=[]
                if logger: logger.log("7.1.18", "Aungaapah", "रमे", stem, "Maharshi Pāṇini")
                return SubantaProcessor._finalize(stem, vibhakti, vacana, logger)
            if vibhakti == 3 and vacana == 1: stem[-1].char = 'ए'
            if vibhakti in [4,5,6,7] and vacana == 1:
                if vibhakti==7: clean_suffix=ad("आम्")
                clean_suffix = ad("या") + clean_suffix
                if vibhakti==4: clean_suffix=ad("यै")
                if vibhakti in [5,6]: clean_suffix=ad("यास्")
                if vibhakti==7: clean_suffix=ad("याम्")
            if vibhakti==6 and vacana==3: clean_suffix=ad("नाम्")

        # --- PRE-CHECKS ---
        if (is_at or is_ghi_any or is_aa) and vibhakti == 2 and vacana == 1:
            res_str = stem_str + "म्"
            return res_str # Ami Purvah is final

        # --- GHI ---
        if is_ghi_any:
            guna_char = 'ए' if is_it else 'ओ'
            dirgha_char = 'ई' if is_it else 'ऊ'
            
            if (vibhakti in [1,2,8] and vacana == 2) or (vibhakti == 2 and vacana == 3):
                stem[-1].char = dirgha_char
                if vacana == 2: clean_suffix = []
                if vacana == 3: clean_suffix = ad("स्")

            elif vibhakti == 3 and vacana == 1:
                if not is_fem_ghi:
                    clean_suffix = ad("ना")
                    if logger: logger.log("7.3.120", "Ango Na Astriyam", sanskrit_varna_samyoga(stem+clean_suffix), stem, "Maharshi Pāṇini")
            
            elif vibhakti in [4, 5, 6, 7] and vacana == 1:
                stem_a = stem[:]; stem_a[-1].char = guna_char
                suffix_a = clean_suffix[:]
                if vibhakti in [5, 6]: suffix_a = ad("स्")
                if vibhakti == 7: stem_a[-1].char = 'अ'; suffix_a = ad("औ")
                
                fp_a, _ = SandhiProcessor.apply_ac_sandhi(stem_a, suffix_a)
                res_a_final = SubantaProcessor._finalize(fp_a, vibhakti, vacana, logger)

                if not is_fem_ghi: return res_a_final
                
                stem_b = stem[:]
                # Nadi forms need to be manually constructed or processed
                # Simple logic for now as placeholders, ideally pass through Tripadi too
                suffix_b_str = ""
                if vibhakti == 4: suffix_b_str = "्यै"
                elif vibhakti in [5, 6]: suffix_b_str = "्याः"
                elif vibhakti == 7: suffix_b_str = "्याम्"
                
                res_b = stem_str[:-1] + suffix_b_str # Simplified
                return f"{res_a_final} / {res_b}"

            elif (vibhakti == 1 or vibhakti == 8) and vacana == 3:
                stem[-1].char = guna_char

            elif vibhakti == 6 and vacana == 3:
                clean_suffix = ad("नाम्"); stem[-1].char = dirgha_char

            elif vibhakti == 8 and vacana == 1:
                stem[-1].char = guna_char; clean_suffix = []
                if logger: logger.log("7.3.108", "Hrasvasya Gunah", sanskrit_varna_samyoga(stem), stem, "Maharshi Pāṇini")
                return SubantaProcessor._finalize(stem, vibhakti, vacana, logger)

        # --- RAMA (Masculine) ---
        if vibhakti == 8 and vacana == 1 and is_at: clean_suffix = []
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
            if vacana == 3 and f in ['भ्', 'स्'] and vibhakti != 2: stem[-1].char = 'ए'
            elif vibhakti in [6, 7] and vacana == 2: stem[-1].char = 'ए'
            elif f in ['भ्', 'य', 'व्', 'य्', 'व'] and AdhikaraController.is_rule_in_scope("7.3.102", "ANGASYA"): stem[-1].char = 'आ'

        # --- SANDHI & FINALIZE ---
        fp, rule = SandhiProcessor.apply_ac_sandhi(stem, clean_suffix)
        if logger and rule: logger.log(rule, "Sandhi", sanskrit_varna_samyoga(fp), fp, "Maharshi Pāṇini")
        
        # 2.3 Shaso Nah
        if vibhakti == 2 and vacana == 3:
            if fp[-1].char == 'स्' or fp[-1].char == 'ः': fp[-1].char = 'न्'

        return SubantaProcessor._finalize(fp, vibhakti, vacana, logger)
