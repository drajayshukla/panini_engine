import streamlit as st
import sys, os
sys.path.append(os.path.abspath('.'))
from logic.subanta_processor import SubantaProcessor

st.set_page_config(page_title="Tagger", page_icon="🔍")
st.title("🔍 Metadata Tagger")
sent = st.text_input("Sentence", "रामः गच्छति")
if st.button("Tag"):
    st.write("Tagging Engine Active.")
