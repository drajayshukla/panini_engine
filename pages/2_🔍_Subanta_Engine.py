import streamlit as st
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
