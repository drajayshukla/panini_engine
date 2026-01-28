import streamlit as st
import json
import os

# --- १. पेज कॉन्फ़िगरेशन ---
st.set_page_config(page_title="रूप-सिद्धि - अष्टाध्यायी-यंत्र", layout="wide", page_icon="📝")

st.title("📝 धातु-रूप सिद्घि (Verb Conjugator)")
st.caption("पाणिनीय ३x३ मैट्रिक्स आधारित लकार-रूप विश्लेषण")


# --- २. डेटा लोडिंग ---
@st.cache_data
def load_json(filename):
    path = f'data/{filename}'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


# रूप डेटा और मेटाडेटा लोड करें
db_conjugation = load_json('active_voice.json')
db_metadata = load_json('dhatu_master_structured.json')  # यहाँ सही फाइल का उपयोग किया गया है

# --- ३. सिलेक्शन इंटरफेस ---

# सुरक्षित मैप तैयार करें: मेटाडेटा से उपदेश और अर्थ उठाएं
dhatu_map = {}
if isinstance(db_metadata, list):
    for d in db_metadata:
        if isinstance(d, dict) and 'kaumudi_index' in d:
            idx = d['kaumudi_index']
            # केवल वही धातु दिखाएं जिसके रूप active_voice.json में मौजूद हैं
            if idx in db_conjugation:
                label = f"{d.get('upadesha', 'Unknown')} ({d.get('artha_sanskrit', 'N/A')})"
                dhatu_map[label] = idx

# सिलेक्शन कॉलम
col_s1, col_s2 = st.columns([2, 1])

with col_s1:
    available_options = list(dhatu_map.keys())
    if available_options:
        selected_name = st.selectbox("धातु चुनें:", options=available_options, index=0)
        dhatu_id = dhatu_map[selected_name]
    else:
        st.error("डेटाबेस में कोई वैध धातु या रूप नहीं मिले। कृपया JSON फाइलें जांचें।")
        st.stop()

# --- ४. लकार चयन ---
lakara_map = {
    "plat": "लट् (Present)", "plit": "लिट् (Perfect)", "plut": "लुट् (Periphrastic Future)",
    "plrut": "लृट् (Simple Future)", "plot": "लोट् (Imperative)", "plang": "लङ् (Imperfect)",
    "pvidhiling": "विधिलिङ् (Potential)", "pashirling": "आशीर्लिङ् (Benedictive)",
    "plung": "लुङ् (Aorist)", "plrung": "लृङ् (Conditional)",
    "alat": "लट् (Atmanepada)", "alit": "लिट् (Atmanepada)",
    "alut": "लुट् (Atmanepada)", "alrut": "लृट् (Atmanepada)",
    "alot": "लोट् (Atmanepada)", "alang": "लङ् (Atmanepada)",
    "avidhiling": "विधिलिङ् (Atmanepada)", "aashirling": "आशीर्लिङ् (Atmanepada)",
    "alung": "लुङ् (Atmanepada)", "alrung": "लृङ् (Atmanepada)"
}

if dhatu_id in db_conjugation:
    available_lakaras = db_conjugation[dhatu_id].keys()
    display_lakaras = {lakara_map.get(k, k): k for k in available_lakaras}

    with col_s2:
        selected_lakara_label = st.selectbox("लकार चुनें:", options=list(display_lakaras.keys()))
        lakara_key = display_lakaras[selected_lakara_label]

    # --- ५. ३x३ मैट्रिक्स रेंडरिंग ---
    st.markdown("---")
    st.subheader(f"🛡️ {selected_name} - {selected_lakara_label}")

    lakara_data = db_conjugation[dhatu_id][lakara_key]

    if isinstance(lakara_data, dict) and "prathama" in lakara_data:
        # टेबल का हेडर
        h1, h2, h3, h4 = st.columns([1, 2, 2, 2])
        h2.markdown("<h4 style='text-align: center; color: #FF4B4B;'>एकवचन</h4>", unsafe_allow_html=True)
        h3.markdown("<h4 style='text-align: center; color: #FF4B4B;'>द्विवचन</h4>", unsafe_allow_html=True)
        h4.markdown("<h4 style='text-align: center; color: #FF4B4B;'>बहुवचन</h4>", unsafe_allow_html=True)

        purushas = [("prathama", "प्रथम (III)"), ("madhyama", "मध्यम (II)"), ("uttama", "उत्तम (I)")]
        vachanas = ["ekavachana", "dvivachana", "bahuvachana"]

        for p_key, p_label in purushas:
            r1, r2, r3, r4 = st.columns([1, 2, 2, 2])
            r1.markdown(f"**{p_label}**")

            # रूपों को सुंदर ढंग से रेंडर करना
            r2.info(lakara_data[p_key].get(vachanas[0], "-"))
            r3.info(lakara_data[p_key].get(vachanas[1], "-"))
            r4.info(lakara_data[p_key].get(vachanas[2], "-"))
    else:
        st.warning("इस लकार का डेटा मैट्रिक्स फॉर्मेट में नहीं है।")
else:
    st.error("इस धातु के लिए कोई रूप नहीं मिले।")

# --- ६. फुटर नोट ---
st.markdown("---")
st.caption(f"💡 डेटा सोर्स: active_voice.json | इंडेक्स: {dhatu_id}")