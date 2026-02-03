import streamlit as st
import sys, os
sys.path.append(os.path.abspath('.'))
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

st.set_page_config(page_title="Declension", page_icon="🔍")
st.title("🕉️ Declension Engine (Siddhanta Mode)")

with st.sidebar:
    stem = st.text_input("Stem", "राम")

c1, c2 = st.columns(2)
v = c1.selectbox("Vibhakti", range(1,9))
n = c2.selectbox("Vacana", range(1,4))

if st.button("Derive"):
    logger = PrakriyaLogger()
    res = SubantaProcessor.derive_pada(stem, v, n, logger)
    st.success(f"Result: {res}")
    for step in logger.get_history():
        st.markdown(f"**{step['rule']}**: {step['desc']} -> `{step['result']}`")
