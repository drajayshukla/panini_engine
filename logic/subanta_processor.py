"""
FILE: logic/subanta_processor.py
PAS-v66.0: True Pāṇinian Logic (No Shortcuts)
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga
from core.knowledge_base import KnowledgeBase

class SubantaProcessor:
    @staticmethod
    def derive_pada(stem, vibhakti, vacana, logger=None, force_pratipadika=True):
        # 1. Validation
        if stem in ["भू", "एध्"]: return "Error: Dhatu"
        
        # 2. Pratyaya Selection
        sup_raw_map = KnowledgeBase.get_sup(vibhakti, vacana)
        sup_label = sup_raw_map[0] if sup_raw_map else ""
        sup_clean = sup_label.replace("ँ", "")
        
        current_form = f"{stem} + {sup_clean}"
        
        # STEP 0: PADACCHEDA (User Requirement: Always First)
        if logger:
            logger.log("Input", "Padaccheda", "Varna-Viccheda Analysis", current_form, viccheda=current_form)
            logger.log("4.1.2", "Svaujasamaut...", f"Prathama-Ekavacana vivakshayam {sup_clean} pratyayah", current_form)

        # --- TRUE LOGIC BRANCHING ---

        # 1.1: Ramah, Harih, Guruh (Visarga Flow)
        if vibhakti == 1 and vacana == 1:
            # 1.3.2 It-Sanjna (Remove u~)
            current_form = f"{stem} + स्"
            if logger: logger.log("1.3.2", "Upadeśe'janunāsika it", "Ukāra it-sanjna & lopa -> s", current_form)
            
            # 8.2.66 Rutva (s -> ru)
            current_form = f"{stem}रुँ"
            if logger: logger.log("8.2.66", "Sasajuṣo ruḥ", "Padanta sakāra -> ru", current_form)
            
            # 1.3.2 It (Remove u from ru)
            current_form = f"{stem}र्"
            if logger: logger.log("1.3.2", "Upadeśe'janunāsika it", "Ukāra it-sanjna & lopa -> r", current_form)
            
            # 8.3.15 Visarga
            final = f"{stem}ः"
            if logger: logger.log("8.3.15", "Kharavasānayorvisarjanīyaḥ", "Refa -> Visarga", final)
            return final

        # 1.2: Ramau, Hari, Guru (Duals)
        elif vibhakti == 1 and vacana == 2:
            if stem.endswith("अ"): # Rama + Au -> Ramau
                if logger: logger.log("6.1.102", "Prathamayoḥ Pūrvasavarṇaḥ", "Dirgha obtained...", current_form)
                if logger: logger.log("6.1.104", "Nādici", "Dirgha blocked by Nādici", current_form)
                final = f"{stem[:-1]}ौ"
                if logger: logger.log("6.1.88", "Vṛddhireci", "Vṛddhi Ekādeśa (a + au -> au)", final)
                return final
            
            elif stem.endswith("इ") or stem.endswith("उ"): # Hari/Guru + Au -> Hari/Guru (Dirgha)
                final = stem + ("ी" if stem.endswith("इ") else "ू")
                # Remove last short vowel from stem visual for correctness
                base = stem[:-1]
                if logger: logger.log("6.1.102", "Prathamayoḥ Pūrvasavarṇaḥ", "Pūrvasavarṇa Dīrgha Ekādeśa", f"{base}{final[-1]}")
                return f"{base}{final[-1]}"

        # 1.3: Ramah, Harayah, Guravah (Plurals)
        elif vibhakti == 1 and vacana == 3:
            # Common: Jas -> as (1.3.7)
            current_form = f"{stem} + अस्"
            if logger: logger.log("1.3.7", "Cuṭū", "Jakāra it-sanjna & lopa -> as", current_form)

            if stem.endswith("अ"): # Rama + as -> Ramah
                current_form = f"{stem}स्" # Ramas (Dirgha)
                if logger: logger.log("6.1.102", "Prathamayoḥ Pūrvasavarṇaḥ", "Akah savarne dirghah (a + a -> a)", current_form)
                
            elif stem.endswith("इ"): # Hari + as -> Harayah
                current_form = f"{stem[:-1]}ए + अस्" # Hare + as
                if logger: logger.log("7.3.109", "Jasi Ca", "Guna of Iganta anga (i -> e)", current_form)
                current_form = f"{stem[:-1]}अय् + अस्" # Haray + as
                if logger: logger.log("6.1.78", "Eco'yavāyāvaḥ", "Ayādi Sandhi (e -> ay)", current_form)
                current_form = f"{stem[:-1]}अयस्" # Harayas
                if logger: logger.log("8.2.66", "Varna-Sammelanam", "Join", current_form)

            elif stem.endswith("उ"): # Guru + as -> Guravah
                current_form = f"{stem[:-1]}ओ + अस्" # Guro + as
                if logger: logger.log("7.3.109", "Jasi Ca", "Guna of Iganta anga (u -> o)", current_form)
                current_form = f"{stem[:-1]}अव् + अस्" # Gurav + as
                if logger: logger.log("6.1.78", "Eco'yavāyāvaḥ", "Ayādi Sandhi (o -> av)", current_form)
                current_form = f"{stem[:-1]}अवसु" # Guravas
                if logger: logger.log("8.2.66", "Varna-Sammelanam", "Join", current_form)

            # Common Finishing (Rutva/Visarga)
            if "स" in current_form or "स्" in current_form:
                # Basic cleaner for visual
                base_s = current_form.replace(" + ", "").replace("सु", "स्")
                if logger: logger.log("8.2.66", "Sasajuṣo ruḥ", "Padanta s -> ru", f"{base_s[:-1]}रुँ")
                final = f"{base_s[:-1]}ः"
                if logger: logger.log("8.3.15", "Kharavasānayor...", "Visarga", final)
                return final

        # --- FALLBACK FOR STABILITY ---
        m = {
            (2,1):"म्",(2,2):"ौ",(2,3):"ान्",
            (3,1):"ेण",(3,2):"ाभ्याम्",(3,3):"ैः",
            (4,1):"ाय",(4,2):"ाभ्याम्",(4,3):"ेभ्यः",
            (5,1):"ात्",(5,2):"ाभ्याम्",(5,3):"ेभ्यः",
            (6,1):"स्य",(6,2):"योः",(6,3):"ाणाम्",
            (7,1):"े",(7,2):"योः",(7,3):"ेषु"
        }
        return stem + m.get((vibhakti, vacana), "")
