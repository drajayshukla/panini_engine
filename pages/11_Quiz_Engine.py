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

# लकारों के नाम
lakara_labels = {
    "plat": "लट् (Present)", "plit": "लिट् (Perfect)", "plut": "लुट् (Future 1)",
    "plrut": "लृट् (Future 2)", "plot": "लोट् (Imperative)", "plang": "लङ् (Imperfect)",
    "pvidhiling": "विधिलिङ् (Potential)", "pashirling": "आशीर्लिङ् (Benedictive)",
    "plung": "लुङ् (Aorist)", "plrung": "लृङ् (Conditional)"
}


# --- ३. क्विज लॉजिक इंजन ---
def generate_question(metadata, roopa_db):
    """रैंडम प्रश्न जनरेटर"""
    # १. एक ऐसी धातु चुनें जिसके रूप मौजूद हों
    clean_roopa_keys = list(roopa_db.keys())
    target_id = random.choice(clean_roopa_keys)

    # २. उस धातु का मेटाडेटा निकालें
    meta_entry = next((d for d in metadata if str(d.get('identifier')).strip() == target_id), None)
    if not meta_entry: return None

    # ३. रैंडम लकार, पुरुष और वचन चुनें
    available_lakaras = list(roopa_db[target_id].keys())
    lak_code = random.choice(available_lakaras)
    pur = random.choice(["prathama", "madhyama", "uttama"])
    vac = random.choice(["ekavachana", "dvivachana", "bahuvachana"])

    correct_answer = roopa_db[target_id][lak_code][pur][vac]

    # ४. गलत विकल्प तैयार करना (Distractors)
    # अन्य रैंडम धातुओं के रूप उठाना
    distractors = set()
    while len(distractors) < 3:
        random_id = random.choice(clean_roopa_keys)
        random_lak = random.choice(list(roopa_db[random_id].keys()))
        wrong_val = roopa_db[random_id][random_lak][pur][vac]
        if wrong_val != correct_answer:
            distractors.add(wrong_val)

    options = list(distractors) + [correct_answer]
    random.shuffle(options)

    return {
        "dhatu": meta_entry.get('upadesha'),
        "artha": meta_entry.get('artha_sanskrit'),
        "lakara": lakara_labels.get(lak_code, lak_code),
        "purusha": pur,
        "vachana": vac,
        "correct": correct_answer,
        "options": options
    }


# --- ४. सेशन स्टेट मैनेजमेंट (UI Persistence) ---
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total' not in st.session_state:
    st.session_state.total = 0

# --- ५. मुख्य इंटरफेस ---
if db_meta and db_roopa:

    st.sidebar.header("📊 प्रोग्रेस कार्ड")
    st.sidebar.metric("आपका स्कोर", f"{st.session_state.score} / {st.session_state.total}")

    if st.button("🔄 नया प्रश्न तैयार करें"):
        st.session_state.current_question = generate_question(db_meta, db_roopa)
        st.session_state.answered = False

    if st.session_state.current_question:
        q = st.session_state.current_question

        st.markdown(f"""
        <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; border-left: 5px solid #FF4B4B;">
            <h3>प्रश्न:</h3>
            <p style="font-size: 1.2em;">धातु <b>'{q['dhatu']}'</b> ({q['artha']}) का <b>{q['lakara']}</b>, 
            <b>{q['purusha'].capitalize()} पुरुष</b>, <b>{q['vachana'].capitalize()}</b> रूप क्या होगा?</p>
        </div>
        """, unsafe_allow_html=True)

        # विकल्प दिखाना
        user_choice = st.radio("सही विकल्प चुनें:", q['options'], index=None)

        if st.button("✅ उत्तर सबमिट करें") and user_choice:
            st.session_state.total += 1
            if user_choice == q['correct']:
                st.success(f"अति सुंदर! '{user_choice}' सही उत्तर है।")
                st.session_state.score += 1
            else:
                st.error(f"गलत जवाब। सही उत्तर था: **{q['correct']}**")

            # प्रश्न रीसेट करने के लिए गाइड
            st.info("अगले प्रश्न के लिए 'नया प्रश्न तैयार करें' बटन दबाएं।")
            st.session_state.current_question = None  # उत्तर देने के बाद प्रश्न साफ़ करें

    else:
        st.write("क्विज शुरू करने के लिए ऊपर दिए गए बटन पर क्लिक करें।")

else:
    st.error("डेटाबेस लोड नहीं हो सका।")

st.markdown("---")
st.caption("Quiz Engine v1.0 | Based on Paninian Dataset | Dr. Ajay Shukla Edition")