#pages/11_Quiz_Engine.py
import streamlit as st
import json
import os
import random

# --- १. पेज सेटअप ---
st.set_page_config(page_title="Analytical Quiz - अष्टाध्यायी-यंत्र", layout="wide", page_icon="🎯")

st.title("🎯 पाणिनीय धातु-रूप क्विज (कर्तरि प्रयोग)")
st.caption("पाणिनीय व्याकरण आधारित 'कर्तरि' रूप विश्लेषण एवं परीक्षण")


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

# --- ३. देवनागरी मैपिंग (शुद्ध कर्तरि लेबल्स) ---
lakara_labels = {
    "plat": "कर्तरि लट् (वर्तमान)", "plit": "कर्तरि लिट् (परोक्ष भूत)", "plut": "कर्तरि लुट् (भविष्य १)",
    "plrut": "कर्तरि लृट् (सामान्य भविष्य)", "plot": "कर्तरि लोट् (आज्ञा)", "plang": "कर्तरि लङ् (अनद्यतन भूत)",
    "pvidhiling": "कर्तरि विधिलिङ् (संभावना)", "pashirling": "कर्तरि आशीर्लिङ् (आशीर्वाद)",
    "plung": "कर्तरि लुङ् (सामान्य भूत)", "plrung": "कर्तरि लृङ् (हेतुहेतुमद्भाव)",
    "alat": "कर्तरि लट् (आत्मनेपद)", "alit": "कर्तरि लिट् (आत्मनेपद)", "alut": "कर्तरि लुट् (आत्मनेपद)",
    "alrut": "कर्तरि लृट् (आत्मनेपद)", "alot": "कर्तरि लोट् (आत्मनेपद)", "alang": "कर्तरि लङ् (आत्मनेपद)",
    "avidhiling": "कर्तरि विधिलिङ् (आत्मनेपद)", "aashirling": "कर्तरि आशीर्लिङ् (आत्मनेपद)",
    "alung": "कर्तरि लुङ् (आत्मनेपद)", "alrung": "कर्तरि लृङ् (आत्मनेपद)"
}
purusha_map = {"prathama": "प्रथम", "madhyama": "मध्यम", "uttama": "उत्तम"}
vachana_map = {"ekavachana": "एकवचन", "dvivachana": "द्विवचन", "bahuvachana": "बहुवचन"}


# --- ४. Diagnostic Logic ---
def get_grammatical_rule(lak_code, pur, vac):
    is_atmanepada = lak_code.startswith('a')
    pada_text = "आत्मनेपद" if is_atmanepada else "परस्मैपद"
    base_key = 'p' + lak_code[1:] if is_atmanepada else lak_code

    rules = {
        "plat": "कर्तरि लट्। विकरण: शप् (अ)।",
        "plit": "कर्तरि लिट्। धातु द्वित्व (Reduplication)।",
        "plut": "कर्तरि लुट्। 'ता' (Taa) विकरण।",
        "plrut": "कर्तरि लृट्। 'स्य/इष्य' विकरण।",
        "plot": "कर्तरि लोट्। आज्ञा/प्रार्थना।",
        "plang": "कर्तरि लङ्। 'अ' उपसर्ग (अट्-आगम)।",
        "plung": "कर्तरि लुङ्। 'अ' उपसर्ग + 'सिच' विकरण।",
        "plrung": "कर्तरि लृङ्। भविष्य-भूत (Conditional)।"
    }

    diagnostic = rules.get(base_key, "कर्तरि व्याकरणिक प्रक्रिया विश्लेषण।")
    return f"**Diagnosis:** {diagnostic} | पद: {pada_text} | स्थान: {purusha_map.get(pur)} - {vachana_map.get(vac)}"


# --- ५. क्विज लॉजिक इंजन ---
def generate_question(metadata, roopa_db):
    clean_roopa_keys = list(roopa_db.keys())
    target_id = random.choice(clean_roopa_keys)
    meta_entry = next((d for d in metadata if str(d.get('identifier')).strip() == target_id), None)

    if not meta_entry: return None

    all_dhatu_forms = roopa_db[target_id]
    lak_code = random.choice(list(all_dhatu_forms.keys()))
    pur_key = random.choice(["prathama", "madhyama", "uttama"])
    vac_key = random.choice(["ekavachana", "dvivachana", "bahuvachana"])
    correct_answer = all_dhatu_forms[lak_code][pur_key][vac_key]

    # एक ही धातु से विकल्प बनाना
    distractors = set()
    attempts = 0
    while len(distractors) < 3 and attempts < 100:
        r_lak = random.choice(list(all_dhatu_forms.keys()))
        wrong_val = all_dhatu_forms[r_lak][random.choice(["prathama", "madhyama", "uttama"])][
            random.choice(["ekavachana", "dvivachana", "bahuvachana"])]
        if wrong_val != correct_answer: distractors.add(wrong_val)
        attempts += 1

    options = list(distractors) + [correct_answer]
    random.shuffle(options)

    return {
        "dhatu": meta_entry.get('upadesha'),
        "artha": meta_entry.get('artha_sanskrit'),
        "full_lakara_name": lakara_labels.get(lak_code, lak_code),  # "कर्तरि लृङ् (आत्मनेपद)"
        "lak_code": lak_code,
        "purusha": purusha_map[pur_key],
        "pur_key": pur_key,
        "vachana": vachana_map[vac_key],
        "vac_key": vac_key,
        "correct": correct_answer,
        "options": options,
        "full_grid": all_dhatu_forms[lak_code]
    }


# --- ६. मुख्य इंटरफेस ---
if 'q' not in st.session_state: st.session_state.q = None
if 'score' not in st.session_state: st.session_state.score = 0
if 'total' not in st.session_state: st.session_state.total = 0
if 'answered' not in st.session_state: st.session_state.answered = False

if db_meta and db_roopa:
    st.sidebar.metric("आपका स्कोर", f"{st.session_state.score} / {st.session_state.total}")

    if st.button("🔄 नया कर्तरि प्रश्न तैयार करें"):
        st.session_state.q = generate_question(db_meta, db_roopa)
        st.session_state.answered = False
        st.rerun()

    if st.session_state.q:
        q = st.session_state.q
        st.markdown(f"""
        <div style="background-color: #f0f4f8; padding: 25px; border-radius: 12px; border-left: 10px solid #1a73e8; text-align: center;">
            <p style="font-size: 1.3em;">धातु <b>'{q['dhatu']}'</b> ({q['artha']}) का</p>
            <h3 style="color: #d32f2f; font-family: 'Sanskrit Text', serif;">{q['full_lakara_name']}, {q['purusha']} पुरुष, {q['vachana']}</h3>
            <p>रूप क्या होगा?</p>
        </div>
        """, unsafe_allow_html=True)

        user_choice = st.radio("शुद्ध विकल्प चुनें:", q['options'], index=None, disabled=st.session_state.answered)

        if not st.session_state.answered and st.button("✅ उत्तर सबमिट करें"):
            if user_choice:
                st.session_state.total += 1
                st.session_state.answered = True
                if user_choice == q['correct']:
                    st.success(f"🚩 उत्तमम्! '{user_choice}' शुद्ध **कर्तरि** रूप है।")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ अशुद्धम्। शुद्ध **कर्तरि** रूप था: '{q['correct']}'")
                st.rerun()

        if st.session_state.answered:
            st.warning(get_grammatical_rule(q.get('lak_code'), q.get('pur_key'), q.get('vac_key')))
            st.divider()
            st.subheader(f"📊 '{q['dhatu']}' ({q['full_lakara_name']}) मैट्रिक्स")
            cols = st.columns([1, 2, 2, 2])
            for i, v in enumerate(["एकवचन", "द्विवचन", "बहुवचन"]): cols[i + 1].write(f"**{v}**")
            for p_k, p_n in [("prathama", "प्रथम"), ("madhyama", "मध्यम"), ("uttama", "उत्तम")]:
                r_c = st.columns([1, 2, 2, 2])
                r_c[0].write(f"**{p_n}**")
                for i, v_k in enumerate(["ekavachana", "dvivachana", "bahuvachana"]):
                    val = q['full_grid'][p_k][v_k]
                    if val == q['correct']:
                        r_c[i + 1].success(val)
                    else:
                        r_c[i + 1].code(val)
else:
    st.error("डेटाबेस त्रुटि।")