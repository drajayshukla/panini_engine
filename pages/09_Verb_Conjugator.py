import streamlit as st
import json
import os

# --- १. पेज कॉन्फ़िगरेशन ---
st.set_page_config(page_title="Active Conjugator - अष्टाध्यायी-यंत्र", layout="wide", page_icon="📝")

st.markdown("""
    <style>
    .varna-box { background-color: #f8f9fa; padding: 12px; border-radius: 8px; text-align: center; border: 1px solid #dee2e6; font-size: 1.1em; color: #1a1a1a; }
    .purusha-label { font-weight: bold; color: #d32f2f; padding-top: 15px; font-size: 1.05em; }
    </style>
    """, unsafe_allow_html=True)

st.title("📝 धातु-रूप सिद्घि (Active/कर्तरि)")
st.caption("तिप्तस्झि... प्रक्रिया आधारित लकार-रूप विश्लेषण")


# --- २. डेटा लोडिंग ---
@st.cache_data
def load_panini_data():
    meta_path = os.path.join('data', 'dhatu_master_structured.json')
    roopa_path = os.path.join('data', 'active_voice.json')

    if not os.path.exists(meta_path) or not os.path.exists(roopa_path):
        return None, None

    with open(meta_path, 'r', encoding='utf-8') as f: meta = json.load(f)
    with open(roopa_path, 'r', encoding='utf-8') as f: roopa = json.load(f)
    return meta, roopa


db_metadata, db_active = load_panini_data()

# --- ३. डेटा प्रोसेसिंग (Normalization) ---
if db_metadata and db_active:
    clean_roopa = {str(k).strip(): v for k, v in db_active.items()}

    dhatu_list = []
    for d in db_metadata:
        d_id = str(d.get('identifier', '')).strip()
        if d_id in clean_roopa:
            d['label'] = f"[{d_id}] {d.get('upadesha', '???')} - {d.get('artha_sanskrit', 'N/A')}"
            dhatu_list.append(d)

    # --- ४. साइडबार ---
    with st.sidebar:
        st.header("🔍 अन्वेषण")
        search_term = st.text_input("धातु या अर्थ लिखें:")
        filtered_list = [d for d in dhatu_list if
                         search_term.lower() in d['label'].lower()] if search_term else dhatu_list
        st.metric("उपलब्ध धातु", len(dhatu_list))

    # --- ५. यूज़र इंटरफेस (Selection) ---
    c_sel1, c_sel2 = st.columns([2, 1])

    if filtered_list:
        with c_sel1:
            selected_dhatu_label = st.selectbox("धातु चुनें:", options=[d['label'] for d in filtered_list])
            target_entry = next(d for d in filtered_list if d['label'] == selected_dhatu_label)
            target_id = target_entry['identifier']
            target_roopa = clean_roopa[target_id]  # सिलेक्टेड धातु के सभी रूप
    else:
        st.error("कोई धातु नहीं मिली।")
        st.stop()

    lakara_labels = {
        "plat": "लट् (Present)", "plit": "लिट् (Perfect)", "plut": "लुट् (Future 1)",
        "plrut": "लृट् (Future 2)", "plot": "लोट् (Imperative)", "plang": "लङ् (Imperfect)",
        "pvidhiling": "विधिलिङ् (Potential)", "pashirling": "आशीर्लिङ् (Benedictive)",
        "plung": "लुङ् (Aorist)", "plrung": "लृङ् (Conditional)",
        "alat": "लट् (Atmanepada)", "alit": "लिट् (Atmanepada)", "alut": "लुट् (Atmanepada)",
        "alrut": "लृट् (Atmanepada)", "alot": "लोट् (Atmanepada)", "alang": "लङ् (Atmanepada)",
        "avidhiling": "विधिलिङ् (Atmanepada)", "aashirling": "आशीर्लिङ् (Atmanepada)",
        "alung": "लुङ् (Atmanepada)", "alrung": "लृङ् (Atmanepada)"
    }

    with c_sel2:
        available_lakaras = list(target_roopa.keys())
        selected_lakara = st.selectbox("लकार चुनें:", options=available_lakaras,
                                       format_func=lambda x: lakara_labels.get(x, x))

    # --- ६. विज़ुअलाइज़ेशन टैब्स (The Core Update) ---
    st.divider()
    tab1, tab2 = st.tabs(["📊 ३x३ मैट्रिक्स (Full Grid)", "🔍 लट्-लुट् सारांश (Prathama Ekavachana)"])

    with tab1:
        st.subheader(f"🛡️ {selected_dhatu_label} | {lakara_labels.get(selected_lakara, selected_lakara)}")
        grid = target_roopa[selected_lakara]

        # हेडर
        h_col = st.columns([1, 2, 2, 2])
        v_labels = ["एकवचन", "द्विवचन", "बहुवचन"]
        for i, v in enumerate(v_labels):
            h_col[i + 1].markdown(
                f"<div class='varna-box' style='background-color:#e9ecef; font-weight:bold;'>{v}</div>",
                unsafe_allow_html=True)

        # रोज़ (Rows)
        purushas = [("prathama", "प्रथम (III)"), ("madhyama", "मध्यम (II)"), ("uttama", "उत्तम (I)")]
        for p_key, p_name in purushas:
            r_col = st.columns([1, 2, 2, 2])
            r_col[0].markdown(f"<div class='purusha-label'>{p_name}</div>", unsafe_allow_html=True)
            p_data = grid.get(p_key, {})
            r_col[1].info(p_data.get('ekavachana', '-'))
            r_col[2].info(p_data.get('dvivachana', '-'))
            r_col[3].info(p_data.get('bahuvachana', '-'))

    with tab2:
        st.subheader(f"✨ {selected_dhatu_label} के सभी उपलब्ध लकारों का सारांश")
        summary_list = []
        for l_key, l_name in lakara_labels.items():
            if l_key in target_roopa:
                roop = target_roopa[l_key].get('prathama', {}).get('ekavachana', '-')
                summary_list.append({"लकार": l_name, "प्रथम पुरुष एकवचन": roop})

        if summary_list:
            st.table(summary_list)
        else:
            st.warning("सारांश के लिए डेटा उपलब्ध नहीं है।")

    with st.expander("📊 धातु मेटाडेटा"):
        st.json(target_entry)

else:
    st.error("🚨 'data/' फोल्डर में आवश्यक JSON फाइलें नहीं मिलीं।")

st.markdown("---")
st.caption("Paninian Engine v1.2 | Developed for Dr. Ajay Shukla")