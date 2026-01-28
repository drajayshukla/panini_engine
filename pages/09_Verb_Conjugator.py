import streamlit as st
import json
import os

# --- १. पेज सेटअप ---
st.set_page_config(page_title="रूप-सिद्धि - अष्टाध्यायी-यंत्र", layout="wide", page_icon="📝")

st.title("📝 धातु-रूप सिद्घि (Verb Conjugator)")
st.caption("पाणिनीय ३x३ मैट्रिक्स आधारित लकार-रूप विश्लेषण")


# --- २. डेटा लोडिंग (Robust Logic) ---
@st.cache_data
def load_all_data():
    meta_path = os.path.join('data', 'dhatu_master_structured.json')
    roopa_path = os.path.join('data', 'active_voice.json')

    if not os.path.exists(meta_path) or not os.path.exists(roopa_path):
        return None, None

    with open(meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)
    with open(roopa_path, 'r', encoding='utf-8') as f:
        roopa = json.load(f)

    return meta, roopa


db_metadata, db_conjugation = load_all_data()

# --- ३. डेटा सिंकिंग (Clinical Normalization) ---
if db_metadata and db_conjugation:
    dhatu_map = {}

    # रूप डेटाबेस की चाबियों को क्लीन करें (जैसे " 01.0001 " -> "01.0001")
    clean_roopa = {str(k).strip(): v for k, v in db_conjugation.items()}

    for entry in db_metadata:
        # 'identifier' ही '01.0001' के बराबर है
        d_id = str(entry.get('identifier', '')).strip()

        if d_id in clean_roopa:
            label = f"[{d_id}] {entry.get('upadesha', '???')} ({entry.get('artha_sanskrit', 'N/A')})"
            dhatu_map[label] = {
                "id": d_id,
                "forms": clean_roopa[d_id]
            }

    if not dhatu_map:
        st.warning("⚠️ 'identifier' और रूप डेटाबेस की Keys मैच नहीं हो रही हैं। कृपया डेटा फॉर्मेट चेक करें।")
        st.stop()

    # --- ४. यूज़र इंटरफेस (Selection) ---
    col_sel1, col_sel2 = st.columns([2, 1])

    with col_sel1:
        selected_label = st.selectbox("पाणिनीय क्रम के अनुसार धातु चुनें:", options=list(dhatu_map.keys()))
        target_data = dhatu_map[selected_label]

    # लकार मैपिंग (Human Readable)
    lakara_labels = {
        "plat": "लट् (वर्तमान)", "plit": "लिट् (परोक्ष भूत)", "plut": "लुट् (अनद्यतन भविष्य)",
        "plrut": "लृट् (सामान्य भविष्य)", "plot": "लोट् (आज्ञा/आशीष)", "plang": "लङ् (अनद्यतन भूत)",
        "pvidhiling": "विधिलिङ् (संभावना)", "pashirling": "आशीर्लिङ् (आशीर्वाद)",
        "plung": "लुङ् (सामान्य भूत)", "plrung": "लृङ् (हेतुहेतुमद्भाव)",
        "alat": "लट् (Atmanepada)", "alit": "लिट् (Atmanepada)", "alut": "लुट् (Atmanepada)",
        "alrut": "लृट् (Atmanepada)", "alot": "लोट् (Atmanepada)", "alang": "लङ् (Atmanepada)",
        "avidhiling": "विधिलिङ् (Atmanepada)", "aashirling": "आशीर्लिङ् (Atmanepada)",
        "alung": "लुङ् (Atmanepada)", "alrung": "लृङ् (Atmanepada)"
    }

    available_lakaras = target_data["forms"].keys()

    with col_sel2:
        selected_lakara = st.selectbox(
            "लकार चुनें:",
            options=list(available_lakaras),
            format_func=lambda x: lakara_labels.get(x, x)
        )

    # --- ५. ३x३ मैट्रिक्स रेंडरिंग ---
    st.divider()
    st.subheader(f"🛡️ {selected_label} - {lakara_labels.get(selected_lakara, selected_lakara)}")

    grid = target_data["forms"][selected_lakara]

    # ग्रिड हेडर
    h_col1, h_col2, h_col3, h_col4 = st.columns([1, 2, 2, 2])
    h_col2.markdown("<center><b>एकवचन</b></center>", unsafe_allow_html=True)
    h_col3.markdown("<center><b>द्विवचन</b></center>", unsafe_allow_html=True)
    h_col4.markdown("<center><b>बहुवचन</b></center>", unsafe_allow_html=True)

    purushas = [("prathama", "प्रथम (III)"), ("madhyama", "मध्यम (II)"), ("uttama", "उत्तम (I)")]
    vachanas = ["ekavachana", "dvivachana", "bahuvachana"]

    for p_key, p_name in purushas:
        r_col1, r_col2, r_col3, r_col4 = st.columns([1, 2, 2, 2])
        r_col1.markdown(f"**{p_name}**")

        # सुरक्षित डेटा फेचिंग
        row_data = grid.get(p_key, {})
        r_col2.info(row_data.get('ekavachana', '-'))
        r_col3.info(row_data.get('dvivachana', '-'))
        r_col4.info(row_data.get('bahuvachana', '-'))

else:
    st.error("🚨 'data/' फोल्डर में आवश्यक JSON फाइलें (dhatu_master_structured.json / active_voice.json) नहीं मिलीं।")

# --- ६. फुटर ---
st.markdown("---")
st.caption("Developed for Dr. Ajay Shukla | Paninian Engine v1.0")