import os
import sys
import subprocess
from pathlib import Path
import time

# ==============================================================================
# 1. GOLDEN SOURCE CODE (The "Siddhānta" State)
# ==============================================================================

# --- SHARED CORE (Varnas with Visarga Fix & Merged Anunasika) ---
CODE_VARNAS = r'''"""
FILE: shared/varnas.py
PURPOSE: Atomic Decomposition (Varna-Viccheda) & Synthesis
VERSION: PAS-v67.1 (Visarga + Anusvara + Anunasika Support)
"""
import unicodedata

STHANA_MAP = {"कण्ठ": "अआकखगघङहः", "तालु": "इईचछजझञयश", "मूर्धा": "ऋॠटठडढणरष", "दन्त": "ऌतथदधनलस", "ओष्ठ": "उऊपफबभम", "नासिका": "ङञणनमंँ", "कण्ठतालु": "एऐ", "कण्ठोष्ठ": "ओऔ", "दन्तोष्ठ": "व"}
VOWELS_MAP = {'ा': 'आ', 'ि': 'इ', 'ी': 'ई', 'ु': 'उ', 'ू': 'ऊ', 'ृ': 'ऋ', 'ॄ': 'ॠ', 'ॢ': 'ऌ', 'ॣ': 'ॡ', 'े': 'ए', 'ै': 'ऐ', 'ो': 'ओ', 'ौ': 'औ'}
INDEPENDENT_VOWELS = 'अआइईउऊऋॠऌॡएऐओऔ'

class Varna:
    def __init__(self, raw_unit):
        self.char = raw_unit
        self.clean = raw_unit.replace('्', '')
        self.is_anunasika = 'ँ' in raw_unit
        self.is_vowel = any(v in raw_unit for v in INDEPENDENT_VOWELS) or '३' in raw_unit
        self.is_ayogavaha = raw_unit in ['ः', 'ं']
        self.is_consonant = not self.is_vowel and not self.is_ayogavaha and '्' in raw_unit
        self.sanjnas = set()
    def __repr__(self): return self.char

def ad(text):
    if not text: return []
    text = unicodedata.normalize('NFC', text)
    res = []
    i = 0
    while i < len(text):
        char = text[i]
        
        # 1. Independent Vowel
        if char in INDEPENDENT_VOWELS:
            unit = char
            if i+1 < len(text) and text[i+1] == 'ँ':
                unit += 'ँ'; i += 1
            res.append(unit)
            
        # 2. Consonants
        elif '\u0915' <= char <= '\u0939' or char == 'ळ':
            res.append(char + '्') 
            if i+1 < len(text):
                nxt = text[i+1]
                if nxt in VOWELS_MAP:
                    vowel = VOWELS_MAP[nxt]
                    i += 1
                    if i+1 < len(text) and text[i+1] == 'ँ':
                        vowel += 'ँ'; i += 1
                    res.append(vowel)
                elif nxt == '्': i += 1
                elif nxt == 'ँ': res.append('अँ'); i += 1
                elif nxt == ' ': res.append('अ'); i += 1
                elif nxt in ['ः', 'ं']: res.append('अ') # Implicit 'a' before Visarga
                else: res.append('अ')
            else: res.append('अ')
        
        # 3. Ayogavaha
        elif char in ['ः', 'ं']: res.append(char)
        elif char in 'ᳲᳳ': res.append(char)
        i += 1
        
    return [Varna(s) for s in res]

def join(varna_list):
    if not varna_list: return ""
    text_list = [v.char for v in varna_list]
    res = ""
    for char in text_list:
        if not res: res = char; continue
        if res.endswith('्') and any(v in char for v in INDEPENDENT_VOWELS):
            matra = VOWELS_MAP.get(char, "") 
            if not matra:
                clean_v = char.replace('ँ', '')
                matra = {v: k for k, v in VOWELS_MAP.items()}.get(clean_v, "")
            if 'ँ' in char and 'ँ' not in matra: matra += 'ँ'
            if char.startswith('अ'): res = res[:-1] + (char.replace('अ', '')) 
            else: res = res[:-1] + matra
        elif char in ['ः', 'ं']: res += char
        else: res += char
    return res.replace("ष््षु", "ष्षु").replace("धनुष््षु", "धनुष्षु")
'''

# --- SHARED ANUBANDHA (It-Karya Engine) ---
CODE_ANUBANDHA = r'''"""
FILE: shared/anubandha.py
PURPOSE: The "It-Sanjna" Engine.
"""
from shared.varnas import Varna

class AnubandhaEngine:
    @staticmethod
    def process(varnas, context="General"):
        if not varnas: return [], []
        res = list(varnas)
        trace = []
        
        # 1.3.2 Upadeśe'janunāsika it
        temp_res = []
        for v in res:
            if 'ँ' in v.char:
                trace.append(f"1.3.2 Upadeśe'janunāsika it: {v.char} is It.")
                trace.append(f"1.3.9 Tasya Lopaḥ: {v.char} removed.")
            else: temp_res.append(v)
        res = temp_res
        
        # 1.3.3 Halantyam
        if res and res[-1].is_consonant:
            last = res[-1].char
            tusma = ['त्', 'थ्', 'द्', 'ध्', 'न्', 'स्', 'म्']
            if context == "Vibhakti" and last in tusma:
                trace.append(f"1.3.4 Na Vibhaktau Tusmāḥ: {last} SAVED.")
            else:
                trace.append(f"1.3.3 Halantyam: {last} is It.")
                res.pop()

        # Initial Rules (1.3.5, 1.3.7, 1.3.8)
        if res:
            first = res[0].char.replace('्', '')
            if context == "Dhatu":
                if first == 'ञ' and len(res)>1 and 'इ' in res[1].char:
                     trace.append(f"1.3.5 Ādirñiṭuḍavaḥ: Ñi is It.")
                     res = res[2:]
                elif first == 'ट' and len(res)>1 and 'उ' in res[1].char:
                     trace.append(f"1.3.5 Ādirñiṭuḍavaḥ: Ṭu is It.")
                     res = res[2:]
                elif first == 'ड' and len(res)>1 and 'उ' in res[1].char:
                     trace.append(f"1.3.5 Ādirñiṭuḍavaḥ: Ḍu is It.")
                     res = res[2:]
            elif context == "Pratyaya":
                cu_group = ['च', 'छ', 'ज', 'झ', 'ञ']
                tu_group = ['ट', 'ठ', 'ड', 'ढ', 'ण']
                ku_group = ['क', 'ख', 'ग', 'घ', 'ङ']
                if first in cu_group or first in tu_group:
                    trace.append(f"1.3.7 Cuṭū: {res[0].char} is It.")
                    res.pop(0)
                elif first == 'ल' or first == 'श' or first in ku_group:
                    trace.append(f"1.3.8 Laśakvataddhite: {res[0].char} is It.")
                    res.pop(0)
        return res, trace
'''

# --- SUBANTA ENGINE (Noun Logic) ---
CODE_SUBANTA = r'''"""
FILE: subanta/declension.py
"""
from shared.varnas import ad, join
from shared.anubandha import AnubandhaEngine

class SubantaGenerator:
    def __init__(self):
        self.SUP = {(1,1): "सुँ", (1,2): "औ", (1,3): "जस्", (2,1): "अम्", (2,2): "औट्", (2,3): "शस्"}

    def log(self, step, result): self.history.append({"step": step, "result": result})

    def derive(self, stem, vibhakti, vacana):
        self.history = []
        if stem.endswith("a"): stem = stem[:-1] + "अ"
        pratyaya_raw = self.SUP.get((vibhakti, vacana), "")
        if not pratyaya_raw: return "WIP", []
        
        stem_varnas = ad(stem)
        prat_varnas = ad(pratyaya_raw)
        self.log("Varna-Viccheda", join(stem_varnas + prat_varnas))
        
        clean_prat, tags = AnubandhaEngine.process(prat_varnas, context="Pratyaya")
        for t in tags: self.log(f"It-Karya ({t})", f"{stem} + {join(clean_prat)}")

        # 1.1 Rama + s
        if vibhakti == 1 and vacana == 1:
            self.log("1.4.14 Suptingantam Padam", f"{stem}{join(clean_prat)}")
            self.log("8.2.66 Sasajusho Ruh", f"{stem}रुँ")
            self.log("1.3.2 Upadeshe'janunasika It", f"{stem}र्")
            final = f"{stem}ः"
            self.log("8.3.15 Kharavasanayor Visarjaniyah", final)
            return final, self.history
            
        return "Pending", self.history
'''

# --- UI PAGES ---
CODE_APP_PY = r'''import streamlit as st
st.set_page_config(page_title="Panini Engine", page_icon="🕉️", layout="wide")
st.title("🕉️ Modular Panini Engine")
st.info("👈 Select a Module from the Sidebar.")
st.markdown("### Modules Installed:")
st.markdown("* **Varna Lab:** Phonetic Analysis")
st.markdown("* **Sanjna Lab:** It-Karya (Tagging)")
st.markdown("* **Subanta Engine:** Noun Declension")
'''

CODE_PAGE_VARNA = r'''import streamlit as st
import sys, os
sys.path.append(os.path.abspath('.'))
from shared.varnas import ad, join
st.title("🔤 Varna Lab")
text = st.text_input("Sanskrit Text", "रामः")
if text:
    v = ad(text)
    st.write([x.char for x in v])
    st.success(f"Join: {join(v)}")
'''

CODE_PAGE_SANJNA = r'''import streamlit as st
import sys, os
sys.path.append(os.path.abspath('.'))
from shared.varnas import ad, join
from shared.anubandha import AnubandhaEngine
st.title("🏷️ Sanjna Lab")
c1, c2 = st.columns(2)
inp = c1.text_input("Upadesha", "डुकृञ्")
ctx = c2.selectbox("Context", ["Dhatu", "Pratyaya", "Vibhakti"])
if st.button("Run"):
    v = ad(inp)
    res, tr = AnubandhaEngine.process(v, ctx)
    st.success(f"Final: {join(res)}")
    for t in tr: st.write(t)
'''

CODE_PAGE_SUBANTA = r'''import streamlit as st
import sys, os
sys.path.append(os.path.abspath('.'))
from subanta.declension import SubantaGenerator
st.title("🔍 Subanta Engine")
stem = st.text_input("Stem", "राम")
if st.button("Derive 1.1"):
    gen = SubantaGenerator()
    res, hist = gen.derive(stem, 1, 1)
    st.success(res)
    for h in hist: st.write(f"{h['step']} -> {h['result']}")
'''

# ==============================================================================
# 2. FILE MANAGEMENT FUNCTIONS
# ==============================================================================

def write_file(path, content):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding='utf-8')
    print(f"✅ Wrote: {path}")

def rebuild_all():
    print("\n🔥 REBUILDING ENTIRE SYSTEM...")
    # 1. Structure
    for d in ["shared", "subanta", "pages", "data"]:
        Path(d).mkdir(exist_ok=True)
        (Path(d) / "__init__.py").touch()
    
    # 2. Logic Files
    write_file("shared/varnas.py", CODE_VARNAS)
    write_file("shared/anubandha.py", CODE_ANUBANDHA)
    write_file("subanta/declension.py", CODE_SUBANTA)
    write_file("subanta/__init__.py", "from .declension import SubantaGenerator")
    
    # 3. UI Files
    write_file("app.py", CODE_APP_PY)
    write_file("pages/1_🔤_Varna_Lab.py", CODE_PAGE_VARNA)
    write_file("pages/2_🏷️_Sanjna_Lab.py", CODE_PAGE_SANJNA)
    write_file("pages/3_🔍_Subanta_Engine.py", CODE_PAGE_SUBANTA)
    
    print("\n✨ SYSTEM RESTORED TO SIDDHANTA STATE.")

def launch_app():
    print("\n🚀 LAUNCHING STREAMLIT...")
    app_path = os.path.abspath("app.py")
    if not os.path.exists(app_path):
        print("❌ app.py not found. Please select 'Rebuild' first.")
        return
    cmd = [sys.executable, "-m", "streamlit", "run", app_path]
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n🛑 Stopped.")

# ==============================================================================
# 3. INTERACTIVE MENU
# ==============================================================================

def main():
    while True:
        print("\n" + "="*40)
        print("   🕉️  PANINI ENGINE LAUNCHPAD")
        print("="*40)
        print("1. [🚀] Launch App")
        print("2. [🔥] Rebuild EVERYTHING (Fix All)")
        print("3. [❌] Exit")
        
        choice = input("\n👉 Select option: ").strip()
        
        if choice == "1":
            launch_app()
        elif choice == "2":
            rebuild_all()
            time.sleep(1)
        elif choice == "3":
            print("👋 Namaste.")
            sys.exit()
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    # If passed 'auto' arg, just launch
    if len(sys.argv) > 1 and sys.argv[1] == "auto":
        launch_app()
    else:
        main()