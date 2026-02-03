import os
from pathlib import Path

def setup_ui_structure():
    print("🎨 SETTING UP UI: App.py + Pages 1 & 2...")

    Path("pages").mkdir(exist_ok=True)

    # ====================================================
    # 1. APP.PY (The Landing Page)
    # ====================================================
    # This is just the "Basic Name" page as you requested.
    app_code = r'''import streamlit as st

st.set_page_config(
    page_title="Panini Engine",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🕉️ Modular Panini Engine")
st.markdown("### *Siddhānta-Based Sanskrit Grammar Architecture*")
st.markdown("---")
st.info("👈 **Select a module from the Sidebar to begin.**")

st.markdown("""
#### Available Engines:
* **1. Varna Lab:** Phonetic Analysis (Varna-Viccheda & Samyoga)
* **2. Subanta Engine:** Noun Declension (e.g. Rāma + Su → Rāmaḥ)
""")
'''
    Path("app.py").write_text(app_code, encoding='utf-8')
    print("✅ Created: app.py (Landing Page)")

    # ====================================================
    # 2. PAGE 1: VARNA LAB (Phonetics)
    # ====================================================
    p1_code = r'''import streamlit as st
import sys
import os

# --- PATH HACK (Critical for Modular Imports) ---
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared.varnas import ad, join

st.set_page_config(page_title="Varna Lab", page_icon="🔤", layout="wide")
st.title("🔤 Varna Lab")
st.caption("The Atomic Foundation: Viccheda & Samyoga")

text_input = st.text_input("Enter Sanskrit Text:", value="रामः सुँ")

if text_input:
    # 1. Split
    varnas = ad(text_input)
    st.markdown("### 1. Analysis (Viccheda)")
    
    # Visual Tiles
    html = ""
    for v in varnas:
        c = "#2980b9" if v.is_vowel else "#c0392b"
        if v.is_anunasika: c = "#d35400"
        html += f"<span style='border:1px solid {c};color:{c};padding:4px 8px;margin:2px;border-radius:4px;font-weight:bold;background:#fff;display:inline-block;'>{v.char}</span>"
    st.markdown(html, unsafe_allow_html=True)

    # 2. Join
    st.markdown("### 2. Synthesis (Samyoga)")
    joined = join(varnas)
    if joined == text_input:
        st.success(f"Perfect Reconstruction: {joined}")
    else:
        st.error(f"Mismatch: {joined}")
'''
    (Path("pages") / "1_🔤_Varna_Lab.py").write_text(p1_code, encoding='utf-8')
    print("✅ Created: pages/1_🔤_Varna_Lab.py")

    # ====================================================
    # 3. PAGE 2: SUBANTA ENGINE (Nouns)
    # ====================================================
    p2_code = r'''import streamlit as st
import sys
import os
import pandas as pd

# --- PATH HACK ---
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from subanta.declension import SubantaGenerator

st.set_page_config(page_title="Subanta Engine", page_icon="🔍", layout="wide")

st.markdown("""
<style>
    .step-box { background:#fff; padding:10px; border-radius:5px; border-left:4px solid #8e44ad; margin-bottom:10px; box-shadow:0 1px 3px rgba(0,0,0,0.1); }
    .sutra { font-weight:bold; color:#2c3e50; }
    .result { float:right; font-weight:bold; color:#8e44ad; font-size:1.1em; }
</style>
""", unsafe_allow_html=True)

st.title("🔍 Subanta Engine (Nouns)")
st.caption("Step-by-Step Declension Generator")

with st.sidebar:
    stem = st.text_input("Stem (Pratipadika)", value="राम")
    st.info("Try: राम, देव (More coming soon)")

c1, c2 = st.columns(2)
vib = c1.selectbox("Vibhakti", range(1,9))
vac = c2.selectbox("Vacana", range(1,4))

if st.button("Derive (Siddha)", type="primary"):
    gen = SubantaGenerator()
    final, history = gen.derive(stem, vib, vac)
    
    st.success(f"Final Form: **{final}**")
    
    st.subheader("Prakriyā (Derivation Process)")
    for step in history:
        st.markdown(f"""
        <div class="step-box">
            <span class="sutra">📖 {step['step']}</span>
            <span class="result">{step['result']}</span>
        </div>
        """, unsafe_allow_html=True)
'''
    (Path("pages") / "2_🔍_Subanta_Engine.py").write_text(p2_code, encoding='utf-8')
    print("✅ Created: pages/2_🔍_Subanta_Engine.py")

if __name__ == "__main__":
    setup_ui_structure()