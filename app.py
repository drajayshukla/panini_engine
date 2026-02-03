import streamlit as st

st.set_page_config(
    page_title="Panini Engine",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🕉️ Modular Panini Engine")
st.markdown("### *Siddhānta-Based Sanskrit Grammar Architecture*")
st.markdown("---")
st.info("👈 **Select a module from the Sidebar to begin.**")

st.markdown("""
#### Available Engines:
* **1. Varna Lab:** Phonetic Analysis (Varna-Viccheda & Samyoga)
* **2. Subanta Engine:** Noun Declension (e.g. Rāma + Su → Rāmaḥ)
""")
