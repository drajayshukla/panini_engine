import streamlit as st
import json
import os
from core.pratyahara_engine import PratyaharaGenerator

# --- १. पेज कॉन्फ़िगरेशन ---
st.set_page_config(page_title="Pratyahara Lab - Panini Engine", layout="wide")
st.title("🎼 प्रत्याहार निर्माण प्रयोगशाला (SK2 Lab)")
st.caption("सूत्र: आदिरन्त्येन सहेता (१.१.७१) - प्रत्याहार जनरेटर")


# --- २. माहेश्वर सूत्र लोडर ---
@st.cache_data
def load_shiva_sutras():
    path = 'data/shiva_sutras.json'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)['shiva_sutras']
    return []


shiva_sutras = load_shiva_sutras()

if not shiva_sutras:
    st.error("माहेश्वर सूत्र डेटा (shiva_sutras.json) नहीं मिला!")
    st.stop()

# --- ३. डेटा प्रोसेसिंग (आदि और अन्त्य वर्णों की सूची) ---
all_adis = []
all_its = []
for sutra in shiva_sutras:
    all_adis.extend(sutra['varnas'])
    all_its.append(sutra['it_varna'])

# --- ४. यूआई डिजाइन (Selection Panel) ---
st.markdown("### 🛠️ प्रत्याहार पैरामीटर्स")
col1, col2, col3 = st.columns([2, 2, 3])

with col1:
    adi_val = st.selectbox("आदि वर्ण (Start):", options=all_adis, index=0)
with col2:
    # डिफ़ॉल्ट 'च्' (अच् के लिए)
    default_it_idx = all_its.index("च्") if "च्" in all_its else 0
    it_val = st.selectbox("अन्त्य इत् (End):", options=all_its, index=default_it_idx)

# ५. प्रत्याहार जनरेशन (Logic Execution)
pratyahara_name = f"{adi_val}{it_val}"
result_varnas = PratyaharaGenerator.generate(adi_val, it_val, shiva_sutras)

# --- ५. रिज़ल्ट डिस्प्ले ---
st.markdown("---")
st.header(f"💠 प्रत्याहार: **{pratyahara_name}**")

if not result_varnas or (adi_val not in result_varnas):
    st.error("⚠️ अमान्य संयोजन: सुनिश्चित करें कि आदि वर्ण माहेश्वर सूत्रों में अन्त्य इत् से पहले आता है।")
else:
    # विज़ुअलाइज़ेशन
    st.subheader("📚 शामिल वर्ण (Varnas):")
    varna_html = "".join([
                             f"<div style='display:inline-block; background-color:#f0f2f6; border-radius:10px; padding:10px 20px; margin:5px; font-size:1.5rem; border:1px solid #d1d5db; font-weight:bold;'>{v}</div>"
                             for v in result_varnas])
    st.markdown(varna_html, unsafe_allow_html=True)

    st.info(f"कुल वर्णों की संख्या: **{len(result_varnas)}**")

# --- ६. माहेश्वर सूत्र संदर्भ (Reference Table) ---
st.markdown("---")
with st.expander("🕉️ माहेश्वर सूत्र संदर्भ तालिका (Shiva Sutras Reference)"):
    # सूत्रों को हाइलाइट करना
    highlighted_sutras = []
    for s in shiva_sutras:
        style = ""
        if adi_val in s['varnas'] or s['it_varna'] == it_val:
            style = "background-color: #e8f0fe;"

        highlighted_sutras.append({
            "क्रम": s['id'],
            "सूत्र": s['sutra'],
            "वर्ण": ", ".join(s['varnas']),
            "इत्": s['it_varna']
        })
    st.table(highlighted_sutras)

# --- ७. क्लिनिकल नोट (Educational) ---
st.sidebar.markdown("### 🔬 क्लिनिकल अंतर्दृष्टि")
st.sidebar.info("""
**आदिरन्त्येन सहेता** के अनुसार:
- **आदि वर्ण:** अपना भी बोध कराता है।
- **अन्त्य इत्:** केवल सीमा (Boundary) निर्धारित करता है, समूह में शामिल नहीं होता।
- **मध्य वर्ण:** आदि और अन्त्य के बीच के सभी वर्ण शामिल होते हैं।
""")