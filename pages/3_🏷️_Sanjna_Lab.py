import streamlit as st
import sys
import os

# --- PATH HACK ---
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared.varnas import ad, join
from shared.anubandha import AnubandhaEngine

st.set_page_config(page_title="Sanjna Lab", page_icon="🏷️", layout="wide")

st.markdown("""
<style>
    .it-box { background:#ffebee; padding:10px; border-radius:5px; border-left:4px solid #c62828; margin-bottom:5px; }
    .save-box { background:#e8f5e9; padding:10px; border-radius:5px; border-left:4px solid #2e7d32; margin-bottom:5px; }
    .final-res { font-size:1.5em; font-weight:bold; color:#2c3e50; }
</style>
""", unsafe_allow_html=True)

st.title("🏷️ Sanjñā Prakaraṇa (It-Kārya)")
st.caption("The Machine that Cleans the Code: It-Tagging & Lopa")

# 1. INPUT
c1, c2 = st.columns([2, 1])
with c1:
    raw_input = st.text_input("Upadeśa (Raw Input)", value="डुकृञ्")
    st.caption("Examples: डुकृञ् (Dhatu), जस् (Pratyaya), सुँ (Pratyaya), शप् (Vikarna)")

with c2:
    context = st.selectbox("Context (Sanjna Scope)", 
                           ["Dhatu", "Pratyaya", "Vibhakti", "General"],
                           index=0)
    st.caption("Different rules apply to Dhatus vs Pratyayas.")

if st.button("Run It-Prakriyā", type="primary"):
    # A. Varna Viccheda
    varnas = ad(raw_input)
    
    st.subheader("1. Atomic Analysis")
    st.code(f"{[v.char for v in varnas]}", language="json")

    # B. Run Engine
    clean_varnas, trace = AnubandhaEngine.process(varnas, context)
    
    # C. Display Trace
    st.subheader("2. Rule Application")
    if not trace:
        st.info("No It-Sanjna rules applied.")
    else:
        for t in trace:
            style = "save-box" if "SAVED" in t else "it-box"
            st.markdown(f'<div class="{style}">{t}</div>', unsafe_allow_html=True)

    # D. Final Result
    st.subheader("3. Final Result (Nirubandha)")
    final_str = join(clean_varnas)
    st.markdown(f'<div class="final-res">{final_str}</div>', unsafe_allow_html=True)
    
    if final_str == "कृ":
        st.success("Correct derivation for Ḍukṛñ!")
    if final_str == "अ" and raw_input == "जस्":
        st.success("Correct derivation for Jas (as -> a)!")

