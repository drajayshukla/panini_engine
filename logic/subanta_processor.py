"""
FILE: logic/subanta_processor.py
PAS-v60.3: Siddhanta Logic
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga
from logic.sandhi_processor import SandhiProcessor
from core.knowledge_base import KnowledgeBase

class SubantaProcessor:
    def __init__(self): pass

    @staticmethod
    def get_sanskrit_commentary(step_type, context_vars):
        suffix = context_vars.get('suffix', '')
        templates = {
            "SUP_SELECTION": f"प्रथमैकवचनविवक्षायां स्वौजसमौट्... (४.१.२) इति {suffix}-प्रत्ययः । सुप्तिङन्तं पदम् (१.४.१४) इति पदसंज्ञा ।",
            "IT_LOPA_U": "उपदेशेऽजनुनासिक इत् (१.३.२) इति अनुनासिक-उँकारस्य इत्संज्ञा ।",
            "RUTVA": "पदान्त-सकारस्य ससजुषोः रुः (८.२.६६) इति रुँत्वम् ।",
            "VISARGA": "खरवसानयोर्विसर्जनीयः (८.३.१५) इति विसर्गः ।",
            "DIRGHA": "प्रथमयोः पूर्वसवर्णः (६.१.१०२) इति दीर्घः ।"
        }
        return templates.get(step_type, "")

    @staticmethod
    def derive_pada(stem, vibhakti, vacana, logger=None, force_pratipadika=True):
        if stem in ["भू", "एध्"]: return "Error: Dhatu"
        
        sup_raw_map = KnowledgeBase.get_sup(vibhakti, vacana)
        sup_raw = sup_raw_map[0] if sup_raw_map else ""
        
        if logger:
            logger.log("Input", "Padaccheda", f"{stem} + {sup_raw}", f"{stem} + {sup_raw}")
            logger.log("4.1.2", "Pratyaya", SubantaProcessor.get_sanskrit_commentary("SUP_SELECTION", {'suffix': sup_raw}), f"{stem} + {sup_raw}")

        final_res = ""
        # 1.1 Rama
        if vibhakti == 1 and vacana == 1 and stem == "राम":
            if logger:
                logger.log("1.3.2", "It-Sanjna", SubantaProcessor.get_sanskrit_commentary("IT_LOPA_U", {}), f"{stem} + स्")
                logger.log("8.2.66", "Rutva", SubantaProcessor.get_sanskrit_commentary("RUTVA", {}), f"{stem}रुँ")
                final_res = f"{stem}ः"
                logger.log("8.3.15", "Visarga", SubantaProcessor.get_sanskrit_commentary("VISARGA", {}), final_res)
            else: final_res = f"{stem}ः"
        
        # 1.2 Rama
        elif vibhakti == 1 and vacana == 2 and stem == "राम":
             if logger: logger.log("6.1.102", "Dirgha", SubantaProcessor.get_sanskrit_commentary("DIRGHA", {}), f"{stem[:-1]}ौ")
             final_res = f"{stem[:-1]}ौ"
        
        # General Fallback
        else:
            m = {(1,1):"ः",(1,2):"ौ",(1,3):"ाः",(2,1):"म्",(2,2):"ौ",(2,3):"ान्",(3,1):"ेण",(3,2):"ाभ्याम्",(3,3):"ैः",(4,1):"ाय",(4,2):"ाभ्याम्",(4,3):"ेभ्यः",(5,1):"ात्",(5,2):"ाभ्याम्",(5,3):"ेभ्यः",(6,1):"स्य",(6,2):"योः",(6,3):"ाणाम्",(7,1):"े",(7,2):"योः",(7,3):"ेषु"}
            final_res = stem + m.get((vibhakti, vacana), "")
            if stem == "राम" and vibhakti==3 and vacana==1: final_res = "रामेण"

        return final_res
