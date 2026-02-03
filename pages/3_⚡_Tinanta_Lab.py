import streamlit as st
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
