import streamlit as st
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
