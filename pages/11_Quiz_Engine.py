import streamlit as st
import json
import os
import random

# --- १. पेज सेटअप ---
st.set_page_config(page_title="धातु-रूप क्विज - अष्टाध्यायी-यंत्र", layout="wide", page_icon="🎯")

st.title("🎯 पाणिनीय धातु-रूप क्विज")
st.caption("अपने ज्ञान का परीक्षण करें: डेटासेट आधारित रैंडम एमसीक्यू")


# --- २. डेटा लोडिंग ---
@st.cache_data
def load_quiz_data():
    meta_path = os.path.join('data', 'dhatu_master_structured.json')
    roopa_path = os.path.join('data', 'active_voice.json')
    if not os.path.exists(meta_path) or not os.path.exists(roopa_path):
        return None, None
    with open(meta_path, 'r', encoding='utf-8') as f: meta = json.load(f)
    with open(roopa_path, 'r', encoding='utf-8') as f: roopa = json.load(f)
    return meta, roopa


db_meta, db_roopa = load_quiz_data()

# --- ३. देवनागरी मैपिंग (The Clinical Nomenclature) ---
lakara_labels = {
    # परस्मैपद (Active/Parasmaipada)
    "plat": "लट् (वर्तमान)", "plit": "लिट् (परोक्ष भूत)", "plut": "लुट् (अनद्यतन भविष्य)",
    "plrut": "लृट् (सामान्य भविष्य)", "plot": "लोट् (आज्ञा)", "plang": "लङ् (अनद्यतन भूत)",
    "pvidhiling": "विधिलिङ् (संभावना)", "pashirling": "आशीर्लिङ् (आशीर्वाद)",
    "plung": "लुङ् (सामान्य भूत)", "plrung": "लृङ् (हेतुहेतुमद्भाव)",
    # आत्मनेपद (Atmanepada)
    "alat": "लट् (आत्मनेपद)", "alit": "लिट् (आत्मनेपद)", "alut": "लुट् (आत्मनेपद)",
    "alrut": "लृट् (आत्मनेपद)", "alot": "लोट् (आत्मनेपद)", "alang": "लङ् (आत्मनेपद)",
    "avidhiling": "विधिलिङ् (आत्मनेपद)", "aashirling": "आशीर्लिङ् (आत्मनेपद)",
    "alung": "लुङ् (आत्मनेपद)", "alrung": "लृङ् (आत्मनेपद)"
}

purusha_map = {
    "prathama": "प्रथम",
    "madhyama": "मध्यम",
    "uttama": "उत्तम"
}

vachana_map = {
    "ekavachana": "एकवचन",
    "dvivachana": "द्विवचन",
    "bahuvachana": "बहुवचन"
}


# --- ४. क्विज लॉजिक इंजन ---
def generate_question(metadata, roopa_db):
    clean_roopa_keys = list(roopa_db.keys())
    target_id = random.choice(clean_roopa_keys)

    meta_entry = next((d for d in metadata if str(d.get('identifier')).strip() == target_id), None)
    if not meta_entry: return None

    available_lakaras = list(roopa_db[target_id].keys())
    lak_code = random.choice(available_lakaras)
    pur_key = random.choice(["prathama", "madhyama", "uttama"])
    vac_key = random.choice(["ekavachana", "dvivachana", "bahuvachana"])

    correct_answer = roopa_db[target_id][lak_code][pur_key][vac_key]

    # गलत विकल्प तैयार करना (Smart Distractors)
    distractors = set()
    while len(distractors) < 3:
        random_id = random.choice(clean_roopa_keys)
        random_lak = random.choice(list(roopa_db[random_id].keys()))
        wrong_val = roopa_db[random_id][random_lak][pur_key][vac_key]
        if wrong_val != correct_answer:
            distractors.add(wrong_val)

    options = list(distractors) + [correct_answer]
    random.shuffle(options)

    return {
        "dhatu": meta_entry.get('upadesha'),
        "artha": meta_entry.get('artha_sanskrit'),
        "lakara": lakara_labels.get(lak_code, lak_code),
        "purusha": purusha_map.get(pur_key, pur_key),
        "vachana": vachana_map.get(vac_key, vac_key),
        "correct": correct_answer,
        "options": options
    }


# --- ५. सेशन स्टेट मैनेजमेंट ---
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total' not in st.session_state:
    st.session_state.total = 0

# --- ६. मुख्य इंटरफेस ---
if db_meta and db_roopa:
    st.sidebar.header("📊 प्रोग्रेस कार्ड")
    st.sidebar.metric("आपका स्कोर", f"{st.session_state.score} / {st.session_state.total}")

    if st.button("🔄 नया प्रश्न तैयार करें"):
        st.session_state.current_question = generate_question(db_meta, db_roopa)

    if st.session_state.current_question:
        q = st.session_state.current_question

        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 30px; border-radius: 15px; border-left: 10px solid #2e7d32; text-align: center; box-shadow: 2px 2px 10px rgba(0,0,0,0.1);">
            <h2 style="color: #2e7d32; font-family: 'Sanskrit Text', serif;">व्याकरण प्रश्न</h2>
            <p style="font-size: 1.5em; color: #333; line-height: 1.6;">
                धातु <b>'{q['dhatu']}'</b> ({q['artha']}) का <br>
                <span style="color: #d32f2f; font-weight: bold;">{q['lakara']}</span>, 
                <b>{q['purusha']} पुरुष</b>, 
                <b>{q['vachana']}</b> रूप क्या होगा?
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("---")
        user_choice = st.radio("शुद्ध विकल्प का चयन करें:", q['options'], index=None)

        if st.button("✅ उत्तर सबमिट करें") and user_choice:
            st.session_state.total += 1
            if user_choice == q['correct']:
                st.success(f"🚩 उत्तमम्! '{user_choice}' शुद्ध रूप है।")
                st.session_state.score += 1
            else:
                st.error(f"❌ अशुद्धम्। शुद्ध रूप है: **{q['correct']}**")

            st.info("अगले प्रश्न के लिए 'नया प्रश्न तैयार करें' बटन दबाएं।")
            st.session_state.current_question = None

    else:
        st.info("💡 क्विज शुरू करने के लिए ऊपर दिए गए बटन पर क्लिक करें।")

else:
    st.error("डेटाबेस (JSON) प्राप्त नहीं हुआ।")

# --- ७. फुटर ---
st.markdown("---")
st.caption("Paninian Quiz Engine v1.2 | Developed for Dr. Ajay Shukla")