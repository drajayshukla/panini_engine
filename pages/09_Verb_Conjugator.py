import streamlit as st
import json
import os
import pandas as pd

# --- १. पेज कॉन्फ़िगरेशन ---
st.set_page_config(page_title="Passive Conjugator - अष्टाध्यायी-यंत्र", layout="wide", page_icon="📝")

# कस्टम CSS (Matrix को सुंदर बनाने के लिए)
st.markdown("""
    <style>
    .varna-box { background-color: #f0f2f6; padding: 10px; border-radius: 5px; text-align: center; border: 1px solid #d1d1d1; }
    .purusha-label { font-weight: bold; color: #1f77b4; padding-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📝 धातु-रूप सिद्घि (Passive/भावकर्मणोः)")
st.caption("अष्टाध्यायी प्रक्रिया: ३x३ मैट्रिक्स आधारित कर्मवाच्य विश्लेषण")


# --- २. डेटा लोडिंग (Safety Guards के साथ) ---
@st.cache_data
def load_panini_data():
    meta_path = os.path.join('data', 'dhatu_master_structured.json')
    # आपने इसे passive_voice.json नाम दिया है
    roopa_path = os.path.join('data', 'passive_voice.json')

    if not os.path.exists(meta_path) or not os.path.exists(roopa_path):
        return None, None

    with open(meta_path, 'r', encoding='utf-8') as f: meta = json.load(f)
    with open(roopa_path, 'r', encoding='utf-8') as f: roopa = json.load(f)
    return meta, roopa


db_metadata, db_passive = load_panini_data()

# --- ३. डेटा प्रोसेसिंग और सर्च (Advanced Filtering) ---
if db_metadata and db_passive:
    # क्लिन डेटा मैपिंग
    clean_roopa = {str(k).strip(): v for k, v in db_passive.items()}

    # सर्च योग्य डेटाबेस बनाना (Surgical Search)
    dhatu_list = []
    for d in db_metadata:
        d_id = str(d.get('identifier', '')).strip()
        if d_id in clean_roopa:
            d['label'] = f"[{d_id}] {d.get('upadesha', '???')} - {d.get('artha_sanskrit', 'N/A')}"
            dhatu_list.append(d)

    # --- ४. साइडबार फिल्टर्स (The Diagnostic Control) ---
    with st.sidebar:
        st.header("🔍 अन्वेषण (Search)")
        search_term = st.text_input("धातु या अर्थ लिखें:", placeholder="उदा: भू या सत्तायाम्")

        # सर्च लॉजिक
        filtered_list = [d for d in dhatu_list if
                         search_term.lower() in d['label'].lower()] if search_term else dhatu_list

        st.markdown("---")
        st.metric("उपलब्ध धातु (Passive)", len(dhatu_list))
        st.metric("सर्च परिणाम", len(filtered_list))

    # --- ५. यूज़र इंटरफेस (Selection) ---
    c_sel1, c_sel2 = st.columns([2, 1])

    with c_sel1:
        if filtered_list:
            selected_dhatu = st.selectbox("धातु चुनें:", options=[d['label'] for d in filtered_list])
            # सिलेक्टेड धातु का मेटाडेटा निकालना
            target_entry = next(d for d in filtered_list if d['label'] == selected_dhatu)
            target_id = target_entry['identifier']
        else:
            st.error("कोई धातु नहीं मिली।")
            st.stop()

    # लकार मैपिंग (Clinical Labels)
    lakara_labels = {
        "alat": "लट् (Present Passive)", "alit": "लिट् (Perfect Passive)", "alut": "लुट् (Future Passive 1)",
        "alrut": "लृट् (Future Passive 2)", "alot": "लोट् (Imperative Passive)", "alang": "लङ् (Imperfect Passive)",
        "avidhiling": "विधिलिङ् (Potential Passive)", "aashirling": "आशीर्लिङ् (Benedictive Passive)",
        "alung": "लुङ् (Aorist Passive)", "alrung": "लृङ् (Conditional Passive)"
    }

    with c_sel2:
        available_lakaras = clean_roopa[target_id].keys()
        selected_lakara = st.selectbox(
            "लकार (Tense/Mood):",
            options=list(available_lakaras),
            format_func=lambda x: lakara_labels.get(x, x)
        )

    # --- ६. ३x३ मैट्रिक्स रेंडरिंग (The Lab View) ---
    st.divider()
    grid = clean_roopa[target_id][selected_lakara]

    st.subheader(f"🛡️ {selected_dhatu} | {lakara_labels.get(selected_lakara, selected_lakara)}")

    # मैट्रिक्स लेआउट
    h_col = st.columns([1, 2, 2, 2])
    v_labels = ["एकवचन", "द्विवचन", "बहुवचन"]
    for i, v in enumerate(v_labels):
        h_col[i + 1].markdown(f"<div class='varna-box' style='background-color:#e1e4e8; font-weight:bold;'>{v}</div>",
                              unsafe_allow_html=True)

    purushas = [("prathama", "प्रथम (III)"), ("madhyama", "मध्यम (II)"), ("uttama", "उत्तम (I)")]

    for p_key, p_name in purushas:
        r_col = st.columns([1, 2, 2, 2])
        r_col[0].markdown(f"<div class='purusha-label'>{p_name}</div>", unsafe_allow_html=True)

        # सुरक्षित रूप से डेटा रिट्रीवल
        p_data = grid.get(p_key, {})
        r_col[1].info(p_data.get('ekavachana', '-'))
        r_col[2].info(p_data.get('dvivachana', '-'))
        r_col[3].info(p_data.get('bahuvachana', '-'))

    # --- ७. प्रक्रिया ऑडिट (Audit Trail) ---
    with st.expander("📊 धातु गुण विवरण (Meta-Audit)"):
        st.json(target_entry)

else:
    st.error("🚨 `passive_voice.json` या मेटाडेटा फाइल `data/` में नहीं मिली।")

# --- ८. फुटर ---
st.markdown("---")
st.caption("Developed for Dr. Ajay Shukla | Paninian Engine: Passive Voice Module")