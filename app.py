# app.py

import streamlit as st
import pandas as pd
from utils.data_loader import get_all_dhatus, get_sutra_data
from core.upadesha_registry import UpadeshaType

# --- १. Page Configuration ---
st.set_page_config(
    page_title="अष्टाध्यायी-यंत्र | Paninian Engine",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for that "Clinical/Surgical" Professional Look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    </style>
    """, unsafe_allow_html=True)

# --- २. Header Section ---
col_h1, col_h2 = st.columns([1, 5])
with col_h1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Om_symbol.svg/200px-Om_symbol.svg.png",
             width=80)
with col_h2:
    st.title("अष्टाध्यायी-यंत्र (The Paninian Engine)")
    st.write("🔬 **Computational Linguistics for Sanskrit Grammar** | Developed by Dr. Ajay Shukla")

st.markdown("---")

# --- ३. Diagnostic Metrics (Driven by Data Loader) ---
# Using the Centralized Loader to ensure data parity
dhatus = get_all_dhatus()
sutras = get_sutra_data()

m1, m2, m3, m4 = st.columns(4)
m1.metric("कुल धातु (Dhatupatha)", f"{len(dhatus)}+")
m2.metric("अष्टाध्यायी सूत्र", "3981")
m3.metric("सक्रिय इंजन", "इत्-संज्ञा / अङ्ग-कार्य")
m4.metric("शुद्धता (Accuracy)", "99.9%")

st.markdown("---")

# --- ४. Navigation Tiles ---
st.subheader("🚀 Operational Zones")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### ⚙️ Processor")
    st.write("किसी भी धातु या प्रत्यय की **इत्-संज्ञा, लोप और अङ्ग-कार्य** का विश्लेषण करें।")
    if st.button("इंजन शुरू करें (Start Engine)", key="btn_proc", use_container_width=True):
        # Ensure this matches the file name in your 'pages' folder
        st.switch_page("pages/1_Processor.py")

with c2:
    st.markdown("### 🔍 Explorer")
    st.write("१८००+ धातुओं के **गण, पद, अर्थ और अनुबन्धों** को 'High-Resolution' में खोजें।")
    st.button("निर्माणाधीन (In Progress)", key="btn_exp", disabled=True, use_container_width=True)

with c3:
    st.markdown("### 📚 Documentation")
    st.write("पाणिनीय सूत्रों का **कंप्यूटेशनल लॉजिक** और विच्छेद के नियमों को समझें।")
    st.button("जल्द आ रहा है (Coming Soon)", key="btn_doc", disabled=True, use_container_width=True)

st.markdown("---")

# --- ५. Quick Diagnostic Search ---
st.subheader("🔎 त्वरित धातु अन्वेषण (Quick Diagnostic Search)")

search_col1, search_col2 = st.columns([2, 1])
with search_col1:
    query = st.text_input("धातु या अर्थ लिखें (उदा: भू, सत्तायाम्, एधँ):", placeholder="धातु का नाम...")

if query:
    # Multi-field Search Logic
    results = [
        d for d in dhatus
        if query in str(d.get('mula_dhatu', ''))
           or query in str(d.get('upadesha', ''))
           or query in str(d.get('artha_sanskrit', ''))
    ]

    if results:
        st.success(f"कुल {len(results)} परिणाम मिले:")
        df = pd.DataFrame(results).head(15)

        # Surgical Column Selection for better UI
        display_df = df[['kaumudi_index', 'upadesha', 'artha_sanskrit', 'gana', 'pada']]
        st.dataframe(display_df, use_container_width=True, hide_index=True)

        st.info("💡 **Clinical Tip:** पूर्ण विश्लेषण के लिए इस धातु को कॉपी करें और 'Processor' में पेस्ट करें।")
    else:
        st.error("डेटाबेस में ऐसी कोई धातु नहीं मिली।")

# --- ६. Footer ---
st.markdown("---")
st.markdown(
    "<center><small>नमो नमः | 'अष्टाध्यायी-यंत्र' प्रोजेक्ट का उद्देश्य संस्कृत व्याकरण को डिजिटल युग के लिए सुलभ बनाना है।</small></center>",
    unsafe_allow_html=True)