import streamlit as st
import json
import os

# --- १. पेज कॉन्फ़िगरेशन ---
st.set_page_config(page_title="रूप-सिद्धि - अष्टाध्यायी-यंत्र", layout="wide", page_icon="📝")

st.title("📝 धातु-रूप सिद्घि (Verb Conjugator)")
st.caption("पाणिनीय ३x३ मैट्रिक्स आधारित लकार-रूप विश्लेषण")


# --- २. डेटा लोडिंग (Master Active Voice JSON) ---
@st.cache_data
def load_conjugation_data():
    path = 'data/active_voice.json'  # आपकी रिफाइंड फाइल
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


@st.cache_data
def load_dhatu_metadata():
    path = 'data/dhatu_master_structured.json'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


db_conjugation = load_conjugation_data()
db_metadata = load_dhatu_metadata()

# --- ३. सिलेक्शन इंटरफेस (Surgical Selection) ---
dhatu_map = {f"{d['upadesha']} ({d['artha_sanskrit']})": d['kaumudi_index'] for d in db_metadata}

col_s1, col_s2 = st.columns([2, 1])

with col_s1:
    selected_name = st.selectbox("धातु चुनें:", options=list(dhatu_map.keys()), index=0)
    dhatu_id = dhatu_map[selected_name]

# --- ४. लकार चयन ---
# लकार की मैपिंग (Human Readable)
lakara_map = {
    "plat": "लट् (Present)", "plit": "लिट् (Perfect)", "plut": "लुट् (Periphrastic Future)",
    "plrut": "लृट् (Simple Future)", "plot": "लोट् (Imperative)", "plang": "लङ् (Imperfect)",
    "pvidhiling": "विधिलिङ् (Potential)", "pashirling": "आशीर्लिङ् (Benedictive)",
    "plung": "लुङ् (Aorist)", "plrung": "लृङ् (Conditional)",
    "alat": "लट् (Atmanepada)", "alit": "लिट् (Atmanepada)",  # यदि उपलब्ध हों
}

if dhatu_id in db_conjugation:
    available_lakaras = db_conjugation[dhatu_id].keys()
    # केवल वही लकार दिखाएं जो डेटा में मौजूद हैं
    display_lakaras = {lakara_map.get(k, k): k for k in available_lakaras}

    with col_s2:
        selected_lakara_label = st.selectbox("लकार चुनें:", options=list(display_lakaras.keys()))
        lakara_key = display_lakaras[selected_lakara_label]

    # --- ५. ३x३ मैट्रिक्स रेंडरिंग (The Paninian Grid) ---
    st.markdown("---")
    st.subheader(f"🛡️ {selected_name} - {selected_lakara_label}")

    lakara_data = db_conjugation[dhatu_id][lakara_key]

    # यदि डेटा सही 3x3 फॉर्मेट में है
    if isinstance(lakara_data, dict) and "prathama" in lakara_data:
        # टेबल का हेडर
        h1, h2, h3, h4 = st.columns([1, 2, 2, 2])
        h2.markdown("<h4 style='text-align: center;'>एकवचन</h4>", unsafe_allow_html=True)
        h3.markdown("<h4 style='text-align: center;'>द्विवचन</h4>", unsafe_allow_html=True)
        h4.markdown("<h4 style='text-align: center;'>बहुवचन</h4>", unsafe_allow_html=True)

        purushas = [("prathama", "प्रथम (III)"), ("madhyama", "मध्यम (II)"), ("uttama", "उत्तम (I)")]
        vachanas = ["ekavachana", "dvivachana", "bahuvachana"]

        for p_key, p_label in purushas:
            r1, r2, r3, r4 = st.columns([1, 2, 2, 2])
            r1.markdown(f"**{p_label}**")

            # रूपों को कोड ब्लॉक में दिखाना ताकि कॉपी करना आसान हो
            r2.info(lakara_data[p_key][vachanas[0]])
            r3.info(lakara_data[p_key][vachanas[1]])
            r4.info(lakara_data[p_key][vachanas[2]])

    else:
        # फॉलबैक: यदि रूप मैट्रिक्स फॉर्मेट में नहीं हैं
        st.write("रूप सूची:", lakara_data)

else:
    st.error("इस धातु के लिए रूप डेटाबेस में उपलब्ध नहीं हैं।")

# --- ६. फुटर नोट ---
st.markdown("---")
st.caption("💡 सूचना: ये रूप 'dhatu_roopa_active.json' से लाइव रेंडर हो रहे हैं।")