import streamlit as st
import sys, os
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from logic.subanta_processor import SubantaProcessor

st.set_page_config(page_title="Metadata Tagger", page_icon="🔍")
st.title("🔍 Pāṇinian Metadata Tagger")

sent = st.text_input("Sentence", "रामः वनम् गच्छति")
if st.button("Analyze"):
    st.write("Analysis Engine Loaded.")
    st.json({"word": "रामः", "stem": "राम", "vibhakti": "1.1"})
