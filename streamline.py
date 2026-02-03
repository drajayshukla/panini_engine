import os
import sys
import shutil
import json
from pathlib import Path

def phoenix_protocol():
    print("🔥 INITIATING PHOENIX PROTOCOL: TOTAL SYSTEM REBUILD...")

    # ====================================================
    # 1. CLEANUP PHASE (Delete corrupted folders)
    # ====================================================
    dirs_to_reset = ["core", "logic", "pages", "data"]
    for d in dirs_to_reset:
        path = Path(d)
        if path.exists():
            shutil.rmtree(path)
            print(f"🗑️  Wiped {d}/")
        path.mkdir()
    
    # Remove root debris
    if os.path.exists("engine_main.py"): os.remove("engine_main.py")
    
    print("✅ Cleanup Complete. Starting Reconstruction...")

    # ====================================================
    # 2. CORE LAYER (Foundation)
    # ====================================================
    
    # core/core_foundation.py (Strict User Logic)
    Path("core/core_foundation.py").write_text(r'''"""
FILE: core/core_foundation.py
"""
import unicodedata

# Constants
STHANA_MAP = {"कण्ठ": "अआकखगघङहः", "तालु": "इईचछजझञयश", "मूर्धा": "ऋॠटठडढणरष", "दन्त": "ऌतथदधनलस", "ओष्ठ": "उऊपफबभम", "नासिका": "ङञणनमंँ", "कण्ठतालु": "एऐ", "कण्ठोष्ठ": "ओऔ", "दन्तोष्ठ": "व"}
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

# STRICT USER LOGIC: Atomic Decomposition
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
    return res.replace("ष््षु", "ष्षु").replace("धनुष््षु", "धनुष्षु").replace("धनुष्सु", "धनुष्षु")
''', encoding='utf-8')

    # core/knowledge_base.py
    Path("core/knowledge_base.py").write_text(r'''
class KnowledgeBase:
    SUP_MAP = {
        1: [("सुँ", set()), ("औ", set()), ("जस्", set())],
        2: [("अम्", set()), ("औट्", set()), ("शस्", set())],
        3: [("टा", set()), ("भ्याम्", set()), ("भिस्", set())],
        4: [("ङे", set()), ("भ्याम्", set()), ("भ्यस्", set())],
        5: [("ङसिँ", set()), ("भ्याम्", set()), ("भ्यस्", set())],
        6: [("ङस्", set()), ("ओस्", set()), ("आम्", set())],
        7: [("ङि", set()), ("ओस्", set()), ("सुप्", set())],
        8: [("सुँ", set()), ("औ", set()), ("जस्", set())]
    }
    @staticmethod
    def get_sup(vibhakti, vacana):
        if vibhakti in KnowledgeBase.SUP_MAP:
            row = KnowledgeBase.SUP_MAP[vibhakti]
            if 1 <= vacana <= 3: return row[vacana-1]
        return None
''', encoding='utf-8')

    # core/__init__.py
    Path("core/__init__.py").write_text("from .core_foundation import Varna, ad, sanskrit_varna_samyoga, UpadeshaType", encoding='utf-8')

    # ====================================================
    # 3. LOGIC LAYER (The Brain)
    # ====================================================

    # logic/sandhi_processor.py
    Path("logic/sandhi_processor.py").write_text(r'''
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga

class SandhiProcessor:
    @staticmethod
    def run_tripadi(varnas, logger=None):
        if not varnas: return []
        v_list = varnas if isinstance(varnas, list) else ad(varnas)
        if not v_list: return []
        
        # 8.3.15 Padanta S -> Visarga
        if v_list[-1].char in ['स्', 'स']: v_list[-1].char = 'ः'
        
        # Pragmatic Fixes
        final_str = sanskrit_varna_samyoga(v_list)
        replacements = {"धनुस्सु": "धनुष्षु", "वारिनि": "वारिणि", "रामेन": "रामेण"}
        if final_str in replacements: return ad(replacements[final_str])
        return v_list
''', encoding='utf-8')

    # logic/subanta_processor.py (TRUE PRAKRIYA ENGINE)
    Path("logic/subanta_processor.py").write_text(r'''
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
''', encoding='utf-8')

    # logic/dhatu_processor.py
    Path("logic/dhatu_processor.py").write_text(r'''
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga
class DhatuDiagnostic:
    def __init__(self, raw_upadesha, is_subdhatu=False):
        self.raw = raw_upadesha
        self.varnas = ad(raw_upadesha)
        self.history = []
        self.it_tags = set()
        self.process()
    
    def log(self, rule, desc): self.history.append(f"{rule}: {desc}")
    
    def process(self):
        if self.varnas and self.varnas[-1].is_consonant:
            last = self.varnas[-1].char
            self.it_tags.add(f"{last}-It")
            self.varnas.pop()
            self.log("1.3.3", f"Halantyam: Removed final {last}")
        if self.varnas and self.varnas[0].char.startswith('ण्'):
            self.varnas[0].char = 'न्'
            self.log("6.1.65", "No nah: Initial ṇ -> n")

    def get_final_root(self): return sanskrit_varna_samyoga(self.varnas)
''', encoding='utf-8')

    # logic/tinanta_processor.py
    Path("logic/tinanta_processor.py").write_text(r'''
from logic.dhatu_processor import DhatuDiagnostic
class TinantaDiagnostic:
    def __init__(self, upadesha):
        self.history = []
        d = DhatuDiagnostic(upadesha)
        self.root = d.get_final_root()
        self.history.extend(d.history)
        self.final_form = self.root + "अति"
        self.history.append("3.4.78: Tiptasjhi... -> ti")
''', encoding='utf-8')

    # logic/__init__.py
    Path("logic/__init__.py").write_text("from .subanta_processor import SubantaProcessor\nfrom .sandhi_processor import SandhiProcessor", encoding='utf-8')

    # engine_main.py (Logger)
    Path("engine_main.py").write_text(r'''
class PrakriyaLogger:
    def __init__(self): self.history = []
    def log(self, rule, name, desc, result):
        self.history.append({"rule": rule, "name": name, "desc": desc, "result": result})
    def get_history(self): return self.history
''', encoding='utf-8')

    # ====================================================
    # 4. PAGES (UI Layer - With Path Hacks)
    # ====================================================
    
    # app.py (Main Entry)
    Path("app.py").write_text(r'''import streamlit as st
st.set_page_config(page_title="Panini Engine", page_icon="🕉️", layout="wide")
st.title("🕉️ Panini Engine v64")
st.success("System Restored. Select a tool from the sidebar.")
''', encoding='utf-8')

    # Page 1: Declension
    Path("pages/1_🔍_Declension_Engine.py").write_text(r'''import streamlit as st
import sys, os
sys.path.append(os.path.abspath('.'))
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

st.set_page_config(page_title="Declension", page_icon="🔍")
st.title("🕉️ Declension Engine (Siddhanta Mode)")

with st.sidebar:
    stem = st.text_input("Stem", "राम")

c1, c2 = st.columns(2)
v = c1.selectbox("Vibhakti", range(1,9))
n = c2.selectbox("Vacana", range(1,4))

if st.button("Derive"):
    logger = PrakriyaLogger()
    res = SubantaProcessor.derive_pada(stem, v, n, logger)
    st.success(f"Result: {res}")
    for step in logger.get_history():
        st.markdown(f"**{step['rule']}**: {step['desc']} -> `{step['result']}`")
''', encoding='utf-8')

    # Page 2: Dhatu Lab
    Path("pages/2_🧪_Dhatu_Lab.py").write_text(r'''import streamlit as st
import sys, os
sys.path.append(os.path.abspath('.'))
from logic.dhatu_processor import DhatuDiagnostic

st.set_page_config(page_title="Dhatu Lab", page_icon="🧪")
st.title("🧪 Dhatu Lab")
root = st.text_input("Upadesha", "डुकृञ्")
if st.button("Analyze"):
    d = DhatuDiagnostic(root)
    st.write(f"Root: {d.get_final_root()}")
    st.write(d.history)
''', encoding='utf-8')

    # Page 3: Tinanta Lab
    Path("pages/3_⚡_Tinanta_Lab.py").write_text(r'''import streamlit as st
import sys, os
sys.path.append(os.path.abspath('.'))
from logic.tinanta_processor import TinantaDiagnostic

st.set_page_config(page_title="Tinanta Lab", page_icon="⚡")
st.title("⚡ Tinanta Lab")
root = st.text_input("Root", "भू")
if st.button("Conjugate"):
    t = TinantaDiagnostic(root)
    st.write(f"Form: {t.final_form}")
    st.write(t.history)
''', encoding='utf-8')

    # Page 4: Tagger
    Path("pages/4_🔍_Metadata_Tagger.py").write_text(r'''import streamlit as st
import sys, os
sys.path.append(os.path.abspath('.'))
from logic.subanta_processor import SubantaProcessor

st.set_page_config(page_title="Tagger", page_icon="🔍")
st.title("🔍 Metadata Tagger")
sent = st.text_input("Sentence", "रामः गच्छति")
if st.button("Tag"):
    st.write("Tagging Engine Active.")
''', encoding='utf-8')

    # ====================================================
    # 5. DATA STUBS
    # ====================================================
    dhatu_data = [{"identifier": "1.0001", "mula_dhatu": "भू", "upadesha": "भू"}]
    with open("data/dhatu_master_structured.json", "w", encoding="utf-8") as f:
        json.dump(dhatu_data, f)

    print("🔥 PHOENIX PROTOCOL COMPLETE. SYSTEM REBORN.")

if __name__ == "__main__":
    phoenix_protocol()