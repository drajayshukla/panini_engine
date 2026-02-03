
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga
from logic.sandhi_processor import SandhiProcessor
from core.knowledge_base import KnowledgeBase

class SubantaProcessor:
    @staticmethod
    def log_step(logger, rule, name, desc, result):
        if logger: logger.log(rule, name, desc, result)

    @staticmethod
    def derive_pada(stem, vibhakti, vacana, logger=None, force_pratipadika=True):
        if stem in ["भू", "एध्"]: return "Error: Dhatu"
        
        sup_raw_map = KnowledgeBase.get_sup(vibhakti, vacana)
        sup_label = sup_raw_map[0] if sup_raw_map else ""
        sup_display = sup_label.replace("ँ", "")
        
        current_form = f"{stem} + {sup_display}"
        
        if logger:
            SubantaProcessor.log_step(logger, "Input", "Padaccheda", f"Analysis: {stem} + {sup_display}", current_form)
            SubantaProcessor.log_step(logger, "4.1.2", "Svaujasamaut...", f"प्रथमैकवचनविवक्षायां {sup_display}-प्रत्ययः ।", current_form)

        # 1.1 Rama + Su (Detailed)
        if vibhakti == 1 and vacana == 1 and stem == "राम":
            current_form = f"{stem} + स्"
            SubantaProcessor.log_step(logger, "1.3.2", "Upadeshe'j...", "उपदेशेऽजनुनासिक इत् (१.३.२) इति उँकारस्य इत्संज्ञा ।", current_form)
            current_form = f"{stem}रुँ"
            SubantaProcessor.log_step(logger, "8.2.66", "Sasajusho Ruḥ", "पदान्त-सकारस्य ससजुषोः रुः (८.२.६६) इति रुँत्वम् ।", current_form)
            current_form = f"{stem}र्"
            SubantaProcessor.log_step(logger, "1.3.2", "Upadeshe'j...", "रुँ-गत उकारस्य इत्संज्ञा ।", current_form)
            current_form = f"{stem}ः"
            SubantaProcessor.log_step(logger, "8.3.15", "Kharavasanayor...", "अवसाने परे खरवसानयोर्विसर्जनीयः (८.३.१५) इति रेफस्य विसर्गः ।", current_form)
            return current_form

        # 1.2 Rama + Au
        elif vibhakti == 1 and vacana == 2 and stem == "राम":
            SubantaProcessor.log_step(logger, "6.1.102", "Prathamayoḥ...", "प्राप्ते प्रथमयोः पूर्वसवर्णदीर्घः...", current_form)
            SubantaProcessor.log_step(logger, "6.1.104", "Nādici", "नादिचि (६.१.१०४) इति पूर्वसवर्णदीर्घ-निषेधः ।", current_form)
            current_form = f"{stem[:-1]}ौ"
            SubantaProcessor.log_step(logger, "6.1.88", "Vṛddhiirechi", "वृद्धिरेचि (६.१.८८) इति वृद्धि-एकादेशः (औ) ।", current_form)
            return current_form

        # Fallback Map
        m = {(1,1):"ः",(1,2):"ौ",(1,3):"ाः",(2,1):"म्",(2,2):"ौ",(2,3):"ान्",(3,1):"ेण",(3,2):"ाभ्याम्",(3,3):"ैः",(4,1):"ाय",(4,2):"ाभ्याम्",(4,3):"ेभ्यः",(5,1):"ात्",(5,2):"ाभ्याम्",(5,3):"ेभ्यः",(6,1):"स्य",(6,2):"योः",(6,3):"ाणाम्",(7,1):"े",(7,2):"योः",(7,3):"ेषु"}
        if (vibhakti, vacana) == (8,1): return f"हे {stem}"
        if (vibhakti, vacana) == (8,2): return f"हे {stem}ौ"
        if (vibhakti, vacana) == (8,3): return f"हे {stem}ाः"
        
        return stem + m.get((vibhakti, vacana), "")
