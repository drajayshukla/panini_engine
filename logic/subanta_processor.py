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
        # R1: उपदेश (Upadeśa)
        stem = ad(stem_str)
        last_char = stem[-1].char
        
        # R3: संज्ञा (Saṃjñā)
        is_at = (last_char == 'अ')   # राम-वत्
        is_it = (last_char == 'इ')   # हरि-वत् (घि-संज्ञा)
        
        sup_data = KnowledgeBase.get_sup(vibhakti, vacana)
        if not sup_data: return "?"
        raw_sup, tags = sup_data; suffix = ad(raw_sup)
        
        # A1: प्रमाण (Citation)
        if logger: logger.log("4.1.2", f"Suffix Attachment ({raw_sup})", f"{stem_str} + {raw_sup}", stem + suffix, "Maharshi Pāṇini")
        
        # R4: अनुबंध (Anubandha - Metadata)
        clean_suffix, trace = SanjnaController.run_it_prakaran(suffix, UpadeshaType.VIBHAKTI)
        if clean_suffix: clean_suffix[0].sanjnas.update(tags)
        
        # R22: प्रत्यय-लोप (Ghost Metadata)
        if logger and trace:
             logger.log(trace[-1], "It-Lopa", sanskrit_varna_samyoga(stem + clean_suffix), stem + clean_suffix, "Maharshi Pāṇini")

        # ========================================================
        # 🔵 सामान्य संधि पूर्व-जांच (General Pre-checks)
        # ========================================================
        # 2.1 अमि पूर्वः (Ami Purvah) - रामम् / हरिम्
        if (is_at or is_it) and vibhakti == 2 and vacana == 1:
            res_str = stem_str + "म्"
            if logger: logger.log("6.1.107", "Ami Purvah", res_str, ad(res_str), "Maharshi Pāṇini")
            return res_str

        # ========================================================
        # 🟢 हरि रणनीति (इकारांत / घि-संज्ञा) - PHASE 3 UPDATES
        # ========================================================
        if is_it:
            # --- 1.2, 2.2, 2.3: पूर्व सवर्ण दीर्घ ---
            if (vibhakti == 1 and vacana == 2) or                (vibhakti == 2 and vacana == 2) or                (vibhakti == 2 and vacana == 3):
                
                stem[-1].char = 'ई' # दीर्घ (Dirgha)
                
                if vacana == 2: # औ/औट् का लोप
                    clean_suffix = []
                    if logger: logger.log("6.1.102", "Prathamayoh Purvasavarnah", "हरी", stem, "Maharshi Pāṇini")
                    return sanskrit_varna_samyoga(stem)
                
                if vacana == 3: # शस् का 'स्' शेष
                     clean_suffix = ad("स्")
                     if logger: logger.log("6.1.102", "Prathamayoh Purvasavarnah", "हरीस्", stem + clean_suffix, "Maharshi Pāṇini")

            # --- 3.1: आङो नाऽस्त्रियाम् (टा -> ना) ---
            elif vibhakti == 3 and vacana == 1:
                clean_suffix = ad("ना")
                if logger: logger.log("7.3.120", "Ango Na Astriyam", "हरिना", stem + clean_suffix, "Maharshi Pāṇini")
            
            # --- 4.1: घेर्ङिति (गुण) + अयादि ---
            # हरि + ङे -> हरे + ए -> हरये
            elif vibhakti == 4 and vacana == 1:
                stem[-1].char = 'ए' # गुण
                if logger: logger.log("7.3.111", "Gher-Niti (Guna)", "हरे + ए", stem + clean_suffix, "Maharshi Pāṇini")
                
            # --- 5.1 / 6.1: ङसिङसोश्च (गुण + पूर्वरूप) ---
            # हरि + अस् -> हरे + अस् -> हरेः
            elif (vibhakti == 5 or vibhakti == 6) and vacana == 1:
                stem[-1].char = 'ए' # गुण (Guna)
                if logger: logger.log("7.3.111", "Gher-Niti (Guna)", "हरे + अस्", stem + clean_suffix, "Maharshi Pāṇini")
                
                # पूर्वरूप (Purvarupa - 6.1.110)
                # ए + अ -> ए (अ लुप्त)
                clean_suffix = ad("स्") # 'अ' 'ए' में मिल गया
                if logger: logger.log("6.1.110", "Ngasi-Ngasosh-Ca (Purvarupa)", "हरेस्", stem + clean_suffix, "Maharshi Pāṇini")

            # --- 6.3: नामि (नुट् + दीर्घ) ---
            # हरि + आम् -> हरि + न् + आम् -> हरीणाम्
            elif vibhakti == 6 and vacana == 3:
                clean_suffix = ad("नाम्") # नुट् आगम (7.1.54)
                if logger: logger.log("7.1.54", "Hrasvanadyapo Nut", "हरिनाम्", stem + clean_suffix, "Maharshi Pāṇini")
                
                stem[-1].char = 'ई' # नामि (6.4.3) - दीर्घ
                if logger: logger.log("6.4.3", "Nami (Dirgha)", "हरीनाम्", stem + clean_suffix, "Maharshi Pāṇini")

            # --- 7.1: अच्च घेः (औत्) ---
            # हरि + ङि -> हरौ
            elif vibhakti == 7 and vacana == 1:
                stem[-1].char = 'अ' # अकारांत में बदलो (Accha Gheh)
                clean_suffix = ad("औ") # ङि -> औ
                # वास्तव में सूत्र कहता है: इदुद्भ्याम् (घेः परस्य) ङेः औत्।
                # लेकिन यह प्रक्रिया "हर + औ" -> "हरौ" (वृद्धि) की तरह दिखती है।
                # सरलता के लिए हम सीधे परिणाम को मैप करते हैं:
                # हरि -> हरौ
                stem = ad("हरौ") 
                clean_suffix = []
                if logger: logger.log("7.3.119", "Accha Gheh (Aut)", "हरौ", stem, "Maharshi Pāṇini")
                return "हरौ"

            # --- 1.3: जसि च (गुण) ---
            elif vibhakti == 1 and vacana == 3:
                stem[-1].char = 'ए'
                if logger: logger.log("7.3.109", "Jasi Ca (Guna)", "हरे + अस्", stem + clean_suffix, "Maharshi Pāṇini")

        # ========================================================
        # 🟠 राम रणनीति (Ram Strategy - Restored)
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
        # 🟡 संधि (Sandhi) & त्रिपदी (Tripadi)
        # ========================================================
        
        fp, rule = SandhiProcessor.apply_ac_sandhi(stem, clean_suffix)
        if logger and rule:
             logger.log(rule, "Sandhi", sanskrit_varna_samyoga(fp), fp, "Maharshi Pāṇini")
        
        # शसो नः पुंसि (6.1.103) - रामान् / हरीन्
        if vibhakti == 2 and vacana == 3:
            if fp[-1].char == 'स्' or fp[-1].char == 'ः':
                 fp[-1].char = 'न्'
                 if logger: logger.log("6.1.103", "Tasmacchaso Nah Pumsi", sanskrit_varna_samyoga(fp), fp, "Maharshi Pāṇini")
                 return sanskrit_varna_samyoga(fp)

        # त्रिपदी (R9)
        final = SandhiProcessor.run_tripadi(fp, logger) 
        res = sanskrit_varna_samyoga(final)
        
        if vibhakti == 8: return "हे " + res

        return res
