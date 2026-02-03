import streamlit as st
import sys, os
sys.path.append(os.path.abspath('.'))
from logic.tinanta_processor import TinantaDiagnostic

st.set_page_config(page_title="Tiṅanta Lab", page_icon="⚡", layout="wide")
st.title("⚡ Tiṅanta Prakriyā (Verb Conjugation)")

with st.form("tin"):
    root = st.text_input("Root", "भू")
    submitted = st.form_submit_button("Generate")

if submitted:
    tin = TinantaDiagnostic(root)
    st.success(f"Form: {tin.final_form}")
    st.write(tin.history)
