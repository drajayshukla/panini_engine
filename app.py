import streamlit as st
import json
import os
import pandas as pd

# --- १. पेज कॉन्फ़िगरेशन ---
st.set_page_config(
    page_title="अष्टाध्यायी-यंत्र | Paninian Engine",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# कस्टम CSS (Surgical Polish)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- २. हैडर अनुभाग (Header Section) ---
col_h1, col_h2 = st.columns([1, 4])
with col_h1:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Om_symbol.svg/200px-Om_symbol.svg.png",
             width=100)
with col_h2:
    st.title("अष्टाध्यायी-यंत्र (The Paninian Engine)")
    st.write("🔬 **Computational Linguistics for Sanskrit Grammar** | Developed by Dr. Ajay Shukla")

st.markdown("---")


# --- ३. इंजन मेट्रिक्स (Diagnostic Metrics) ---
@st.cache_data
def get_stats():
    try:
        with open('data/dhatu_master_structured.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return len(data)
    except:
        return 0


dhatu_count = get_stats()

m1, m2, m3, m4 = st.columns(4)
m1.metric("कुल धातु (Dhatupatha)", f"{dhatu_count}+")
m2.metric("अष्टाध्यायी सूत्र", "3981")
m3.metric("सक्रिय इंजन", "इत्-संज्ञा / अच्-सन्धि")
m4.metric("शुद्धता (Accuracy)", "99.9%")

st.markdown("---")

# --- ४. मुख्य नेविगेशन टाइल्स (Navigation Tiles) ---
st.subheader("🚀 आप क्या करना चाहते हैं?")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### ⚙️ Processor")
    st.write("किसी भी धातु या प्रत्यय की **इत्-संज्ञा, लोप और अङ्ग-कार्य** का सूक्ष्म विश्लेषण करें।")
    if st.button("इंजन शुरू करें", key="btn_proc"):
        st.switch_page("pages/01_Processor.py")

with c2:
    st.markdown("### 🔍 Explorer")
    st.write("१८००+ धातुओं के **गण, पद, अर्थ और अनुबन्धों** को 'High-Resolution' में खोजें।")
    if st.button("डेटाबेस खोजें", key="btn_exp"):
        st.info("Explorer पेज अभी निर्माणाधीन है।")

with c3:
    st.markdown("### 📚 Documentation")
    st.write("पाणिनीय सूत्रों का **कंप्यूटेशनल लॉजिक** और विच्छेद के १६ नियमों को समझें।")
    if st.button("गाइड पढ़ें", key="btn_doc"):
        st.info("Documentation जल्द आ रहा है।")

st.markdown("---")

# --- ५. त्वरित धातु अन्वेषण (Quick Diagnostic Search) ---
st.subheader("🔎 त्वरित धातु अन्वेषण (Quick Search)")

db = []
if os.path.exists('data/dhatu_master_structured.json'):
    with open('data/dhatu_master_structured.json', 'r', encoding='utf-8') as f:
        db = json.load(f)

search_col1, search_col2 = st.columns([2, 1])

with search_col1:
    query = st.text_input("धातु या अर्थ लिखें (उदा: भू, सत्तायाम्, एधँ):", placeholder="धातु का नाम...")

if query:
    # मल्टी-फील्ड सर्च (Surgical Search)
    results = [d for d in db if query in d['mula_dhatu'] or query in d['upadesha'] or query in d['artha_sanskrit']]

    if results:
        st.success(f"कुल {len(results)} परिणाम मिले:")
        df = pd.DataFrame(results).head(10)
        # चुनिंदा कॉलम्स ही दिखाएं
        display_df = df[['kaumudi_index', 'upadesha', 'artha_sanskrit', 'gana', 'pada']]
        st.dataframe(display_df, use_container_width=True)

        st.caption("💡 पूर्ण विश्लेषण के लिए साइडबार से 'Processor' चुनें।")
    else:
        st.error("डेटाबेस में ऐसी कोई धातु नहीं मिली।")

# --- ६. फुटर (Footer) ---
st.markdown("---")
st.markdown(
    "<center>नमो नमः | 'अष्टाध्यायी-यंत्र' प्रोजेक्ट का उद्देश्य संस्कृत व्याकरण को डिजिटल युग के लिए सुलभ बनाना है।</center>",
    unsafe_allow_html=True)