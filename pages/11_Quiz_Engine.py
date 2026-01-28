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

# देवनागरी मैपिंग (Translation Dictionary)
lakara_labels = {
    "plat": "लट् (वर्तमान)", "plit": "लिट् (परोक्ष भूत)", "plut": "लुट् (अनद्यतन भविष्य)",
    "plrut": "लृट् (सामान्य भविष्य)", "plot": "लोट् (आज्ञा)", "plang": "लङ् (अनद्यतन भूत)",
    "pvidhiling": "विधिलिङ् (संभावना)", "pashirling": "आशीर्लिङ् (आशीर्वाद)",
    "plung": "लुङ् (सामान्य भूत)", "plrung": "लृङ् (हेतुहेतुमद्भाव)"
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


# --- ३. क्विज लॉजिक इंजन ---
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

    # Distractors (गलत विकल्प)
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
        "purusha": purusha_map[pur_key],  # देवनागरी
        "vachana": vachana_map[vac_key],  # देवनागरी
        "correct": correct_answer,
        "options": options
    }


# --- ४. सेशन स्टेट ---
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total' not in st.session_state:
    st.session_state.total = 0

# --- ५. मुख्य इंटरफेस ---
if db_meta and db_roopa:
    st.sidebar.header("📊 प्रोग्रेस")
    st.sidebar.metric("स्कोर", f"{st.session_state.score} / {st.session_state.total}")

    if st.button("🔄 नया प्रश्न"):
        st.session_state.current_question = generate_question(db_meta, db_roopa)

    if st.session_state.current_question:
        q = st.session_state.current_question

        st.markdown(f"""
        <div style="background-color: #f0f4f8; padding: 25px; border-radius: 12px; border-right: 8px solid #1a73e8; border-left: 8px solid #1a73e8; text-align: center;">
            <h3 style="color: #1a73e8;">प्रश्न विश्लेषण</h3>
            <p style="font-size: 1.4em; color: #333;">
                धातु <b>'{q['dhatu']}'</b> ({q['artha']}) का <br>
                <span style="color: #d32f2f;">{q['lakara']}</span>, 
                <b>{q['purusha']} पुरुष</b>, 
                <b>{q['vachana']}</b> रूप क्या होगा?
            </p>
        </div>
        """, unsafe_allow_html=True)

        user_choice = st.radio("विकल्प चुनें:", q['options'], index=None)

        if st.button("✅ उत्तर दें") and user_choice:
            st.session_state.total += 1
            if user_choice == q['correct']:
                st.success(f"उत्तमम्! '{user_choice}' शुद्ध रूप है।")
                st.session_state.score += 1
            else:
                st.error(f"अशुद्धम्। शुद्ध रूप है: **{q['correct']}**")
            st.session_state.current_question = None  # उत्तर के बाद साफ़ करें
    else:
        st.info("क्विज शुरू करने के लिए 'नया प्रश्न' बटन दबाएं।")

else:
    st.error("डेटाबेस अनुपलब्ध।")