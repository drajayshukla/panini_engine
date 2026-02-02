"""
FILE: app.py (Home Dashboard)
"""
import streamlit as st

st.set_page_config(
    page_title="Panini Engine",
    layout="wide",
    page_icon="🕉️",
    initial_sidebar_state="expanded"
)

st.title("🕉️ Pāṇinian Engine: The Digital Ashtadhyayi")
st.markdown("### *Yena dhautaṁ giraḥ puṁsāṁ vimalaiḥ śabdavāribhiḥ...*")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.info("### 🧪 Dhātu Lab")
    st.markdown("""
    **Status:** ✅ 100% Siddha
    * **Roots Analyzed:** 2000+
    * **Phonology:** Shatva, Natva, Upadha-Dirgha
    * **Features:** Database Validator, Upadesha Decoder
    """)

with col2:
    st.info("### ⚡ Tiṅanta Lab")
    st.markdown("""
    **Status:** 🚧 Prototype (Phase 1)
    * **Lakāras:** Laṭ (Present)
    * **Operations:** Vikarana (Śap), Guna, Ayadi
    * **Output:** Simple Conjugation (e.g. Bhavati)
    """)

st.success("👈 Select a Laboratory from the Sidebar to begin.")
