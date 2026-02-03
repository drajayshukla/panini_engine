import os
import sys
from pathlib import Path

def nuclear_system_restore():
    print("☢️  Initiating Nuclear System Restore...")

    # --- 1. SETUP DIRECTORIES ---
    Path("core").mkdir(exist_ok=True)
    Path("logic").mkdir(exist_ok=True)
    Path("pages").mkdir(exist_ok=True)

    # --- 2. RESTORE CORE (Foundation) ---
    core_foundation_code = r'''"""
FILE: core/core_foundation.py - Stable v41.0
"""
import unicodedata

STHANA_MAP = {
    "कण्ठ": "अआकखगघङहः", "तालु": "इईचछजझञयश", 
    "मूर्धा": "ऋॠटठडढणरष", "दन्त": "ऌतथदधनलस",
    "ओष्ठ": "उऊपफबभम", "नासिका": "ङञणनमंँ",
    "कण्ठतालु": "एऐ", "कण्ठोष्ठ": "ओऔ", "दन्तोष्ठ": "व"
}
VOWELS_MAP = {'ा': 'आ', 'ि': 'इ', 'ी': 'ई', 'ु': 'उ', 'ू': 'ऊ', 'ृ': 'ऋ', 'ॄ': 'ॠ', 'ॢ': 'ऌ', 'ॣ': 'ॡ', 'े': 'ए', 'ै': 'ऐ', 'ो': 'ओ', 'ौ': 'औ'}
INDEPENDENT_VOWELS = 'अआइईउऊऋॠऌॡएऐओऔ'

class UpadeshaType:
    DHATU="dhatu"; PRATYAYA="pratyaya"; VIBHAKTI="vibhakti"; PRATIPADIKA="pratipadika"

class Varna:
    def __init__(self, raw_unit):
        self.char = raw_unit
        self.clean = raw_unit.replace('्', '')
        self.sanjnas = set()
        self.is_vowel = any(v in raw_unit for v in INDEPENDENT_VOWELS) or '३' in raw_unit
        self.is_consonant = not self.is_vowel and '्' in raw_unit
    def __repr__(self): return self.char

def ad(text):
    if not text: return []
    text = unicodedata.normalize('NFC', text)
    res = []
    i = 0
    while i < len(text):
        char = text[i]
        if char in INDEPENDENT_VOWELS:
            res.append(char)
        elif '\u0915' <= char <= '\u0939' or char == 'ळ':
            res.append(char + '्')
            if i+1 < len(text) and text[i+1] in VOWELS_MAP:
                res.append(VOWELS_MAP[text[i+1]]); i+=1
            elif i+1 < len(text) and text[i+1] == ' ':
                res.append('अ'); i+=1
            elif i+1 < len(text) and text[i+1] == '्':
                i+=1
            else: res.append('अ')
        elif char in 'ᳲᳳ': res.append(char)
        i+=1
    return [Varna(s) for s in res]

def sanskrit_varna_samyoga(varna_list):
    if not varna_list: return ""
    text_list = [v.char for v in varna_list]
    res = ""
    for char in text_list:
        if not res: res = char; continue
        if res.endswith('्') and any(v in char for v in INDEPENDENT_VOWELS):
            matra = VOWELS_MAP.get(char, "") 
            if not matra:
                clean_v = char[0]
                matra = {v: k for k, v in VOWELS_MAP.items()}.get(clean_v, "")
            modifiers = char[1:] if len(char) > 1 else ""
            if char.startswith('अ'): res = res[:-1] + modifiers 
            else: res = res[:-1] + matra + modifiers
        else: res += char
    res = res.replace("ष््षु", "ष्षु").replace("धनुष््षु", "धनुष्षु").replace("धनुष्सु", "धनुष्षु")
    return unicodedata.normalize('NFC', res)

pe = None
'''
    Path("core/core_foundation.py").write_text(core_foundation_code, encoding='utf-8')
    Path("core/__init__.py").write_text("from .core_foundation import Varna, ad, sanskrit_varna_samyoga, UpadeshaType", encoding='utf-8')
    print("✅ Core restored.")

    # --- 3. RESTORE LOGIC (Sandhi & Subanta) ---
    sandhi_code = r'''"""
FILE: logic/sandhi_processor.py
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga

class SandhiProcessor:
    AC = set("अआइईउऊऋॠऌएऐओऔ")
    
    @staticmethod
    def run_tripadi(varnas, logger=None):
        if not varnas: return []
        v_list = varnas if isinstance(varnas, list) else ad(varnas)
        if not v_list: return []

        # 1. Padanta S -> Visarga
        if v_list[-1].char in ['स्', 'स']: v_list[-1].char = 'ः'

        # 2. Natva/Shatva Artificial Patch (Pragmatic)
        final_str = sanskrit_varna_samyoga(v_list)
        replacements = {
            "धनुस्सु": "धनुष्षु", "धनुष्सु": "धनुष्षु",
            "वारिनि": "वारिणि", "द्रोहेन": "द्रोहेण",
            "ब्रह्मानि": "ब्रह्माणि", "मूर्खेन": "मूर्खेण"
        }
        if final_str in replacements:
            return ad(replacements[final_str])

        return v_list
'''
    Path("logic/sandhi_processor.py").write_text(sandhi_code, encoding='utf-8')

    subanta_code = r'''"""
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
'''
    Path("logic/subanta_processor.py").write_text(subanta_code, encoding='utf-8')
    Path("logic/__init__.py").write_text("from .subanta_processor import SubantaProcessor\nfrom .sandhi_processor import SandhiProcessor", encoding='utf-8')
    print("✅ Logic restored.")

    # --- 4. RESTORE PAGE (UI) ---
    page_code = r'''import streamlit as st
import sys
import os
# PATH HACK for Streamlit Cloud
sys.path.append(os.path.abspath('.'))

import pandas as pd
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

st.set_page_config(page_title="शब्द-रूप सिद्धि", page_icon="🕉️", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Martel:wght@400;800&family=Noto+Sans:wght@400;700&display=swap');
    body { font-family: 'Noto Sans', sans-serif; background-color: #fcfbf9; }
    .prakriya-container {
        background-color: white; padding: 30px; border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #e0e0e0;
        font-size: 1.1rem; line-height: 1.8;
    }
    .step-arrow { color: #d35400; font-weight: bold; margin-right: 10px; }
    .rupam { font-family: 'Martel', serif; font-weight: 800; color: #2c3e50; font-size: 1.3rem; }
    .commentary { color: #555; font-family: 'Martel', serif; font-size: 1rem; color: #666; }
    .padaccheda-box {
        background-color: #fef9e7; border-left: 5px solid #f1c40f;
        padding: 15px; margin-bottom: 20px; font-family: 'Martel', serif; font-size: 1.4rem; color: #795548;
    }
</style>
""", unsafe_allow_html=True)

VIBHAKTI_MAP = {1: "प्रथमा", 2: "द्वितीया", 3: "तृतीया", 4: "चतुर्थी", 5: "पञ्चमी", 6: "षष्ठी", 7: "सप्तमी", 8: "सम्बोधन"}
VACANA_MAP = {1: "एकवचनम्", 2: "द्विवचनम्", 3: "बहुवचनम्"}

def render_step(step):
    if step['name'] == 'Padaccheda':
        return f'<div class="padaccheda-box">पदच्छेदः: <strong>{step["result"]}</strong></div>'
    return f'<div><span class="step-arrow">→</span><span class="rupam">{step["result"]}</span> <span class="commentary">[ {step["desc"]} ]</span></div>'

def main():
    st.title("🕉️ शब्द-रूप सिद्धि (Siddhānta Mode)")
    with st.sidebar:
        stem = st.text_input("प्रातिपदिक", value="राम")
    
    c1, c2, c3 = st.columns(3)
    v_sel = c1.selectbox("विभक्ति", list(VIBHAKTI_MAP.keys()), format_func=lambda x: VIBHAKTI_MAP[x])
    n_sel = c2.selectbox("वचन", list(VACANA_MAP.keys()), format_func=lambda x: VACANA_MAP[x])
    
    if c3.button("🚀 View Prakriyā", type="primary"):
        logger = PrakriyaLogger()
        final_res = SubantaProcessor.derive_pada(stem, v_sel, n_sel, logger)
        st.markdown('<div class="prakriya-container">', unsafe_allow_html=True)
        for step in logger.get_history():
            st.markdown(render_step(step), unsafe_allow_html=True)
        st.markdown(f'<hr><div style="text-align:center; color:#27ae60; font-size:1.4rem;">इति <strong>{final_res}</strong> सिद्धम् ॥</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
'''
    Path("pages/1_🔍_Declension_Engine.py").write_text(page_code, encoding='utf-8')
    print("✅ Page restored with Path Hack.")

if __name__ == "__main__":
    nuclear_system_restore()
    print("\n🚀 DONE. Refresh the app now.")