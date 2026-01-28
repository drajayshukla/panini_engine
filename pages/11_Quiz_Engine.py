import streamlit as st
import json
import os
import random

# --- १. पेज सेटअप ---
st.set_page_config(page_title="Analytical Quiz - अष्टाध्यायी-यंत्र", layout="wide", page_icon="🎯")

st.title("🎯 पाणिनीय धातु-रूप क्विज (Single Dhatu Mode)")
st.caption("एक ही धातु के विभिन्न रूपों के बीच सूक्ष्म अंतर को पहचानें")


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

# --- ३. देवनागरी मैपिंग ---
lakara_labels = {
    "plat": "लट् (वर्तमान)", "plit": "लिट् (परोक्ष भूत)", "plut": "लुट् (भविष्य १)",
    "plrut": "लृट् (सामान्य भविष्य)", "plot": "लोट् (आज्ञा)", "plang": "लङ् (अनद्यतन भूत)",
    "pvidhiling": "विधिलिङ् (संभावना)", "pashirling": "आशीर्लिङ् (आशीर्वाद)",
    "plung": "लुङ् (सामान्य भूत)", "plrung": "लृङ् (हेतुहेतुमद्भाव)",
    "alat": "लट् (आत्मनेपद)", "alit": "लिट् (आत्मनेपद)", "alut": "लुट् (आत्मनेपद)",
    "alrut": "लृट् (आत्मनेपद)", "alot": "लोट् (आत्मनेपद)", "alang": "लङ् (आत्मनेपद)",
    "avidhiling": "विधिलिङ् (आत्मनेपद)", "aashirling": "आशीर्लिङ् (आत्मनेपद)",
    "alung": "लुङ् (आत्मनेपद)", "alrung": "लृङ् (आत्मनेपद)"
}
purusha_map = {"prathama": "प्रथम", "madhyama": "मध्यम", "uttama": "उत्तम"}
vachana_map = {"ekavachana": "एकवचन", "dvivachana": "द्विवचन", "bahuvachana": "बहुवचन"}


# --- ४. Diagnostic Logic Engine ---
def get_grammatical_rule(lak_code, pur, vac):
    is_atmanepada = lak_code.startswith('a')
    pada_text = "आत्मनेपद" if is_atmanepada else "परस्मैपद"
    rules = {
        "plat": "लट्। वर्तमान काल। विकरण: शप् (अ)।",
        "plit": "लिट्। परोक्ष भूत। धातु द्वित्व (Reduplication)।",
        "plut": "लुट्। अनद्यतन भविष्य। 'ता' (Taa) विकरण।",
        "plrut": "लृट्। सामान्य भविष्य। 'स्य/इष्य' विकरण।",
        "plot": "लोट्। आज्ञा/प्रार्थना।",
        "plang": "लङ्। अनद्यतन भूत। 'अ' उपसर्ग (अट्-आगम)।",
        "plung": "लुङ्। सामान्य भूत। 'अ' उपसर्ग + 'सिच/अ' विकरण।",
    }
    base_key = 'p' + lak_code[1:] if is_atmanepada else lak_code
    diagnostic = rules.get(base_key, "व्याकरणिक प्रक्रिया विश्लेषण।")
    return f"**Surgical Diagnosis:** {diagnostic} | पद: {pada_text} | स्थान: {purusha_map.get(pur)} - {vachana_map.get(vac)}"


# --- ५. क्विज लॉजिक इंजन (Single Dhatu Option Generation) ---
def generate_question(metadata, roopa_db):
    clean_roopa_keys = list(roopa_db.keys())
    target_id = random.choice(clean_roopa_keys)
    meta_entry = next((d for d in metadata if str(d.get('identifier')).strip() == target_id), None)

    if not meta_entry: return None

    # सही उत्तर का चयन
    all_dhatu_forms = roopa_db[target_id]
    available_lakaras = list(all_dhatu_forms.keys())

    lak_code = random.choice(available_lakaras)
    pur_key = random.choice(["prathama", "madhyama", "uttama"])
    vac_key = random.choice(["ekavachana", "dvivachana", "bahuvachana"])
    correct_answer = all_dhatu_forms[lak_code][pur_key][vac_key]

    # --- स्मार्ट डिस्ट्रैक्टर लॉजिक (सभी विकल्प एक ही धातु से) ---
    distractors = set()
    attempts = 0
    while len(distractors) < 3 and attempts < 100:
        # उसी धातु के किसी भी रैंडम लकार/पुरुष/वचन से रूप उठाएं
        r_lak = random.choice(available_lakaras)
        r_pur = random.choice(["prathama", "madhyama", "uttama"])
        r_vac = random.choice(["ekavachana", "dvivachana", "bahuvachana"])
        wrong_val = all_dhatu_forms[r_lak][r_pur][r_vac]

        if wrong_val != correct_answer and wrong_val not in distractors:
            distractors.add(wrong_val)
        attempts += 1

    options = list(distractors) + [correct_answer]
    random.shuffle(options)

    return {
        "dhatu": meta_entry.get('upadesha'),
        "artha": meta_entry.get('artha_sanskrit'),
        "lakara": lakara_labels.get(lak_code, lak_code),
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

    if st.button("🔄 नया प्रश्न तैयार करें"):
        st.session_state.q = generate_question(db_meta, db_roopa)
        st.session_state.answered = False
        st.rerun()

    if st.session_state.q:
        q = st.session_state.q
        st.markdown(f"""
        <div style="background-color: #f0f4f8; padding: 25px; border-radius: 12px; border-left: 10px solid #1a73e8; text-align: center;">
            <p style="font-size: 1.3em;">धातु <b>'{q['dhatu']}'</b> ({q['artha']}) का</p>
            <h3 style="color: #d32f2f;">{q['lakara']}, {q['purusha']} पुरुष, {q['vachana']}</h3>
            <p>रूप क्या होगा?</p>
        </div>
        """, unsafe_allow_html=True)

        user_choice = st.radio("शुद्ध विकल्प चुनें:", q['options'], index=None, disabled=st.session_state.answered)

        if not st.session_state.answered and st.button("✅ उत्तर सबमिट करें"):
            if user_choice:
                st.session_state.total += 1
                st.session_state.answered = True
                if user_choice == q['correct']:
                    st.success(f"🚩 उत्तमम्! '{user_choice}' शुद्ध रूप है।")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ अशुद्धम्। शुद्ध रूप था: '{q['correct']}'")
                st.rerun()

        if st.session_state.answered:
            st.warning(get_grammatical_rule(q.get('lak_code'), q.get('pur_key'), q.get('vac_key')))
            st.divider()
            st.subheader(f"📊 '{q['dhatu']}' ({q['lakara']}) मैट्रिक्स")
            # मैट्रिक्स डिस्प्ले
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