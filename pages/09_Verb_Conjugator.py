import streamlit as st
import json
import os

# --- १. पेज कॉन्फ़िगरेशन ---
st.set_page_config(page_title="Active Conjugator - अष्टाध्यायी-यंत्र", layout="wide", page_icon="📝")

# कस्टम CSS: पाणिनीय ३x३ ग्रिड को उभारने के लिए
st.markdown("""
    <style>
    .varna-box { background-color: #f8f9fa; padding: 12px; border-radius: 8px; text-align: center; border: 1px solid #dee2e6; font-size: 1.1em; color: #1a1a1a; }
    .purusha-label { font-weight: bold; color: #d32f2f; padding-top: 15px; font-size: 1.05em; }
    </style>
    """, unsafe_allow_html=True)

st.title("📝 धातु-रूप सिद्घि (Active/कर्तरि)")
st.caption("तिप्तस्झि... प्रक्रिया: ३x३ मैट्रिक्स आधारित कर्तरि प्रयोग विश्लेषण")


# --- २. डेटा लोडिंग (Safety Guards) ---
@st.cache_data
def load_panini_data():
    meta_path = os.path.join('data', 'dhatu_master_structured.json')
    roopa_path = os.path.join('data', 'active_voice.json')  # वापस 'active_voice' पर

    if not os.path.exists(meta_path) or not os.path.exists(roopa_path):
        return None, None

    with open(meta_path, 'r', encoding='utf-8') as f: meta = json.load(f)
    with open(roopa_path, 'r', encoding='utf-8') as f: roopa = json.load(f)
    return meta, roopa


db_metadata, db_active = load_panini_data()

# --- ३. डेटा प्रोसेसिंग (Normalization & Linking) ---
if db_metadata and db_active:
    # Keys को क्लीन करें ताकि "01.0001" सही से मैच हो
    clean_roopa = {str(k).strip(): v for k, v in db_active.items()}

    dhatu_list = []
    for d in db_metadata:
        d_id = str(d.get('identifier', '')).strip()
        if d_id in clean_roopa:
            # सर्च के लिए लेबल तैयार करना
            d['label'] = f"[{d_id}] {d.get('upadesha', '???')} - {d.get('artha_sanskrit', 'N/A')}"
            dhatu_list.append(d)

    # --- ४. साइडबार (Search & Statistics) ---
    with st.sidebar:
        st.header("🔍 अन्वेषण (Search)")
        search_term = st.text_input("धातु या अर्थ लिखें:", placeholder="उदा: भू या सत्तायाम्")

        filtered_list = [d for d in dhatu_list if
                         search_term.lower() in d['label'].lower()] if search_term else dhatu_list

        st.markdown("---")
        st.metric("उपलब्ध धातु (Active)", len(dhatu_list))
        st.metric("सर्च परिणाम", len(filtered_list))

    # --- ५. यूज़र इंटरफेस (Selection) ---
    c_sel1, c_sel2 = st.columns([2, 1])

    with c_sel1:
        if filtered_list:
            selected_dhatu_label = st.selectbox("धातु चुनें:", options=[d['label'] for d in filtered_list])
            target_entry = next(d for d in filtered_list if d['label'] == selected_dhatu_label)
            target_id = target_entry['identifier']
        else:
            st.error("कोई धातु नहीं मिली।")
            st.stop()

    # कर्तरि लकार मैपिंग
    lakara_labels = {
        "plat": "लट् (वर्तमान)", "plit": "लिट् (परोक्ष भूत)", "plut": "लुट् (अनद्यतन भविष्य)",
        "plrut": "लृट् (सामान्य भविष्य)", "plot": "लोट् (आज्ञा/आशीष)", "plang": "लङ् (अनद्यतन भूत)",
        "pvidhiling": "विधिलिङ् (विधि/संभावना)", "pashirling": "आशीर्लिङ् (आशीर्वाद)",
        "plung": "लुङ् (सामान्य भूत)", "plrung": "लृङ् (हेतुहेतुमद्भाव)",
        "alat": "लट् (Atmanepada)", "alit": "लिट् (Atmanepada)", "alut": "लुट् (Atmanepada)",
        "alrut": "लृट् (Atmanepada)", "alot": "लोट् (Atmanepada)", "alang": "लङ् (Atmanepada)",
        "avidhiling": "विधिलिङ् (Atmanepada)", "aashirling": "आशीर्लिङ् (Atmanepada)",
        "alung": "लुङ् (Atmanepada)", "alrung": "लृङ् (Atmanepada)"
    }

    available_lakaras = clean_roopa[target_id].keys()

    with c_sel2:
        selected_lakara = st.selectbox(
            "लकार (Tense/Mood):",
            options=list(available_lakaras),
            format_func=lambda x: lakara_labels.get(x, x)
        )

    # --- ६. ३x३ मैट्रिक्स रेंडरिंग (The Paninian Grid) ---
    st.divider()
    grid = clean_roopa[target_id][selected_lakara]

    st.subheader(f"🛡️ {selected_dhatu_label} | {lakara_labels.get(selected_lakara, selected_lakara)}")

    # मैट्रिक्स हेडर
    h_col = st.columns([1, 2, 2, 2])
    v_labels = ["एकवचन", "द्विवचन", "बहुवचन"]
    for i, v in enumerate(v_labels):
        h_col[i + 1].markdown(f"<div class='varna-box' style='background-color:#e9ecef; font-weight:bold;'>{v}</div>",
                              unsafe_allow_html=True)

    # पाणिनीय पुरुष क्रम
    purushas = [("prathama", "प्रथम (III)"), ("madhyama", "मध्यम (II)"), ("uttama", "उत्तम (I)")]

    for p_key, p_name in purushas:
        r_col = st.columns([1, 2, 2, 2])
        r_col[0].markdown(f"<div class='purusha-label'>{p_name}</div>", unsafe_allow_html=True)

        p_data = grid.get(p_key, {})
        r_col[1].info(p_data.get('ekavachana', '-'))
        r_col[2].info(p_data.get('dvivachana', '-'))
        r_col[3].info(p_data.get('bahuvachana', '-'))

    # --- ७. मेटा-डेटा ऑडिट ---
    with st.expander("📊 धातु गुण विवरण (Metadata Audit)"):
        st.json(target_entry)

else:
    st.error("🚨 'data/' फोल्डर में `active_voice.json` या मेटाडेटा फाइल नहीं मिली।")

# --- ८. फुटर ---
st.markdown("---")
st.caption("Paninian Engine v1.1 | Developed for Dr. Ajay Shukla")