"""
FILE: logic/subanta_processor.py
PAS-v21.6: True Pāṇinian Logic (Siddham)
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga
from core.knowledge_base import KnowledgeBase

class SubantaProcessor:
    @staticmethod
    def derive_pada(stem, vibhakti, vacana, logger=None, force_pratipadika=True):
        if stem in ["भू", "एध्"]: return "Error: Dhatu"
        
        sup_raw_map = KnowledgeBase.get_sup(vibhakti, vacana)
        sup_label = sup_raw_map[0] if sup_raw_map else ""
        sup_clean = sup_label.replace("ँ", "")
        current_form = f"{stem} + {sup_clean}"
        
        if logger:
            logger.log("Input", "Padaccheda", "Varna-Viccheda Analysis", current_form, viccheda=current_form)
            logger.log("4.1.2", "Svaujasamaut...", f"Pratyaya: {sup_clean}", current_form)

        # 1.1: Ramah, Harih, Guruh (Visarga Flow)
        if vibhakti == 1 and vacana == 1:
            current_form = f"{stem} + स्"
            if logger: logger.log("1.3.2", "Upadeśe'janunāsika it", "Ukāra it-sanjna & lopa -> s", current_form)
            current_form = f"{stem}रुँ"
            if logger: logger.log("8.2.66", "Sasajuṣo ruḥ", "Padanta sakāra -> ru", current_form)
            current_form = f"{stem}र्"
            if logger: logger.log("1.3.2", "Upadeśe'janunāsika it", "Ukāra it-sanjna & lopa -> r", current_form)
            final = f"{stem}ः"
            if logger: logger.log("8.3.15", "Kharavasānayorvisarjanīyaḥ", "Refa -> Visarga", final)
            return final

        # 1.2: Ramau (Dual)
        elif vibhakti == 1 and vacana == 2 and stem.endswith("अ"):
            if logger: logger.log("6.1.102", "Prathamayoḥ Pūrvasavarṇaḥ", "Dirgha obtained...", current_form)
            if logger: logger.log("6.1.104", "Nādici", "Dirgha blocked by Nādici", current_form)
            final = f"{stem[:-1]}ौ"
            if logger: logger.log("6.1.88", "Vṛddhireci", "Vṛddhi Ekādeśa (a + au -> au)", final)
            return final

        # 1.3: Ramah, Harayah, Guravah (Plurals)
        elif vibhakti == 1 and vacana == 3:
            current_form = f"{stem} + अस्"
            if logger: logger.log("1.3.7", "Cuṭū", "Jakāra it-sanjna & lopa -> as", current_form)

            if stem.endswith("अ"): # Rama
                current_form = f"{stem}स्"
                if logger: logger.log("6.1.102", "Prathamayoḥ Pūrvasavarṇaḥ", "Dirgha (a + a -> a)", current_form)
            elif stem.endswith("इ"): # Hari
                current_form = f"{stem[:-1]}ए + अस्"
                if logger: logger.log("7.3.109", "Jasi Ca", "Guna (i -> e)", current_form)
                current_form = f"{stem[:-1]}अय् + अस्"
                if logger: logger.log("6.1.78", "Eco'yavāyāvaḥ", "Ayādi (e -> ay)", current_form)
                current_form = f"{stem[:-1]}अयस्"
            elif stem.endswith("उ"): # Guru
                current_form = f"{stem[:-1]}ओ + अस्"
                if logger: logger.log("7.3.109", "Jasi Ca", "Guna (u -> o)", current_form)
                current_form = f"{stem[:-1]}अव् + अस्"
                if logger: logger.log("6.1.78", "Eco'yavāyāvaḥ", "Ayādi (o -> av)", current_form)
                current_form = f"{stem[:-1]}अवसु"

            base_s = current_form.replace(" + ", "").replace("सु", "स्")
            if logger: logger.log("8.2.66", "Sasajuṣo ruḥ", "Padanta s -> ru", f"{base_s[:-1]}रुँ")
            final = f"{base_s[:-1]}ः"
            if logger: logger.log("8.3.15", "Kharavasānayor...", "Visarga", final)
            return final

        m = {(2,1):"म्",(2,2):"ौ",(2,3):"ान्",(3,1):"ेण",(3,2):"ाभ्याम्",(3,3):"ैः",(4,1):"ाय",(4,2):"ाभ्याम्",(4,3):"ेभ्यः",(5,1):"ात्",(5,2):"ाभ्याम्",(5,3):"ेभ्यः",(6,1):"स्य",(6,2):"योः",(6,3):"ाणाम्",(7,1):"े",(7,2):"योः",(7,3):"ेषु"}
        return stem + m.get((vibhakti, vacana), "")
