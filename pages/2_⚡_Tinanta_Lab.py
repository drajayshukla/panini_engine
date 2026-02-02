import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
"""
PAGE: Tiṅanta Laboratory
"""
import streamlit as st
from logic.tinanta_processor import TinantaDiagnostic

st.set_page_config(page_title="Tiṅanta Lab", page_icon="⚡", layout="wide")

st.title("⚡ Tiṅanta Prakriyā (Verb Conjugation)")
st.caption("Phase 1: Laṭ Lakāra Generator")

col1, col2 = st.columns([1, 2])

with col1:
    with st.form("tin_form"):
        root_input = st.text_input("Root (Upadesha)", value="भू")
        lakara = st.selectbox("Lakāra", ["Lat (Present)", "Lit (Perfect)", "Lrt (Future)"])
        purusha = st.selectbox("Purusha", ["Prathama (3rd)", "Madhyama (2nd)", "Uttama (1st)"])
        vacana = st.selectbox("Vacana", ["Eka (Singular)", "Dvi (Dual)", "Bahu (Plural)"])

        submitted = st.form_submit_button("Generate Form")

if submitted:
    # Map inputs to indices
    p_map = {"Prathama (3rd)": 1, "Madhyama (2nd)": 2, "Uttama (1st)": 3}
    v_map = {"Eka (Singular)": 1, "Dvi (Dual)": 2, "Bahu (Plural)": 3}

    tin = TinantaDiagnostic(root_input, lakara.split()[0], p_map[purusha], v_map[vacana])

    with col2:
        st.markdown(f"""
        <div style="background:#e8f5e9;padding:20px;border-radius:10px;border-left:5px solid #2e7d32;">
            <h3>🏁 Final Form: <span style="color:#d32f2f;font-size:2em;">{tin.final_form}</span></h3>
            <p><strong>Root:</strong> {tin.root} | <strong>Voice:</strong> {tin.pada_type}</p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        st.subheader("📜 Prakriyā Trace")
        for step in tin.history:
            st.code(step, language="text")
