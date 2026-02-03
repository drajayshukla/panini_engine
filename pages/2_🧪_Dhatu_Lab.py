import streamlit as st
import sys, os
sys.path.append(os.path.abspath('.'))
import pandas as pd
from logic.dhatu_processor import DhatuDiagnostic

st.set_page_config(page_title="Dhātu Lab", page_icon="🧪", layout="wide")
st.title("🧪 Dhātu Prakriyā Laboratory")

mode = st.radio("Mode", ["Single Analysis", "Master Database Validator"], horizontal=True)

if mode == "Single Analysis":
    raw_root = st.text_input("Enter Upadesha (e.g. डुकृञ्)", value="डुकृञ्")
    if st.button("Run Diagnostics", type="primary"):
        diag = DhatuDiagnostic(raw_root)
        st.success(f"Final Root: **{diag.get_final_root()}**")
        st.table(pd.DataFrame(diag.history, columns=["Transformation Step"]))

elif mode == "Master Database Validator":
    st.info("Batch Processing Module Loaded")
    # Simulation for demo
    data = [
        {"upadesha": "डुकृञ्", "expected": "कृ"},
        {"upadesha": "टुनादिँ", "expected": "नन्द्"},
        {"upadesha": "षहँ", "expected": "सह्"}
    ]
    st.table(pd.DataFrame(data))
