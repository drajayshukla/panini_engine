import streamlit as st
import sys, os
sys.path.append(os.path.abspath('.'))
st.title("🔍 Metadata Tagger")
st.text_input("Sentence", "रामः गच्छति")
st.button("Analyze")
