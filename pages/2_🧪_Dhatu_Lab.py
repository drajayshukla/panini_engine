import streamlit as st
import sys, os
sys.path.append(os.path.abspath('.'))
from logic.dhatu_processor import DhatuDiagnostic
st.title("🧪 Dhatu Lab")
root = st.text_input("Upadesha", "डुकृञ्")
if st.button("Analyze"):
    d = DhatuDiagnostic(root)
    st.success(f"Final Root: {d.get_final_root()}")
    st.write(d.history)
