import streamlit as st
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
