import streamlit as st
import json
import os
import random

# --- १. पेज सेटअप ---
st.set_page_config(page_title="Analytical Quiz - अष्टाध्यायी-यंत्र", layout="wide", page_icon="🎯")

st.title("🎯 पाणिनीय धातु-रूप क्विज (With Diagnostic Rules)")
st.caption("रूप पहचानें और उनके पीछे के ९० 'Rule-in/Rule-out' मानकों को समझें")


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
    "plat": "लट् (Present)", "plit": "लिट् (Perfect)", "plut": "लुट् (Future 1)",
    "plrut": "लृट् (Future 2)", "plot": "लोट् (Imperative)", "plang": "लङ् (Imperfect)",
    "pvidhiling": "विधिलिङ् (Potential)", "pashirling": "आशीर्लिङ् (Benedictive)",
    "plung": "लुङ् (Aorist)", "plrung": "लृङ् (Conditional)"
}
purusha_map = {"prathama": "प्रथम", "madhyama": "मध्यम", "uttama": "उत्तम"}
vachana_map = {"ekavachana": "एकवचन", "dvivachana": "द्विवचन", "bahuvachana": "बहुवचन"}


# --- ४. Diagnostic Logic Engine (Robust Version) ---
def get_grammatical_rule(lak_code, pur, vac):
    rules = {
        "plat": "वर्तमान काल। लक्षण: ति-तस्-झि प्रत्यय।",
        "plit": "परोक्ष भूत। लक्षण: धातु द्वित्व (Reduplication)।",
        "plut": "अनद्यतन भविष्य। लक्षण: 'ता' (Taa) विकरण का प्रयोग।",
        "plrut": "सामान्य भविष्य। लक्षण: 'स्य/इष्य' विकरण।",
        "plot": "आज्ञा/प्रार्थना। लक्षण: तु-ताम्-न्तु प्रत्यय।",
        "plang": "अनद्यतन भूत। लक्षण: 'अ' उपसर्ग (अट्-आगम) + हलन्त अंत।",
        "pvidhiling": "संभावना/विधि। लक्षण: 'ए' (E) स्वर का बाहुल्य।",
        "pashirling": "आशीर्वाद। लक्षण: 'यात्/यास्ताम्' का प्रयोग।",
        "plung": "सामान्य भूत। लक्षण: 'अ' उपसर्ग + 'स्' विकरण (सिच्)।",
        "plrung": "हेतुहेतुमद्भाव। लक्षण: 'अ' उपसर्ग + 'स्य' विकरण।"
    }

    suffix_logic = f"। स्थान: {purusha_map.get(pur, pur)} पुरुष, {vachana_map.get(vac, vac)}।"
    return f"**Diagnostic Criteria:** {rules.get(lak_code, 'नियम उपलब्ध नहीं')} {suffix_logic}"


# --- ५. क्विज लॉजिक इंजन ---
def generate_question(metadata, roopa_db):
    clean_roopa_keys = list(roopa_db.keys())
    target_id = random.choice(clean_roopa_keys)
    meta_entry = next((d for d in metadata if str(d.get('identifier')).strip() == target_id), None)

    if not meta_entry: return None

    # केवल वही लकार चुनें जो हमारी मैपिंग में हैं
    available_lakaras = [l for l in roopa_db[target_id].keys() if l in lakara_labels]
    if not available_lakaras: return None

    lak_code = random.choice(available_lakaras)
    pur_key = random.choice(["prathama", "madhyama", "uttama"])
    vac_key = random.choice(["ekavachana", "dvivachana", "bahuvachana"])

    correct_answer = roopa_db[target_id][lak_code][pur_key][vac_key]

    distractors = set()
    while len(distractors) < 3:
        random_id = random.choice(clean_roopa_keys)
        # सुरक्षित रैंडम सिलेक्शन
        r_laks = list(roopa_db[random_id].keys())
        random_lak = random.choice(r_laks)
        wrong_val = roopa_db[random_id][random_lak][random.choice(["prathama", "madhyama", "uttama"])][
            random.choice(["ekavachana", "dvivachana", "bahuvachana"])]
        if wrong_val != correct_answer: distractors.add(wrong_val)

    options = list(distractors) + [correct_answer]
    random.shuffle(options)

    return {
        "dhatu": meta_entry.get('upadesha'),
        "artha": meta_entry.get('artha_sanskrit'),
        "lakara": lakara_labels[lak_code],
        "lak_code": lak_code,
        "purusha": purusha_map[pur_key],
        "pur_key": pur_key,
        "vachana": vachana_map[vac_key],
        "vac_key": vac_key,
        "correct": correct_answer,
        "options": options,
        "full_grid": roopa_db[target_id][lak_code]
    }


# --- ६. मुख्य इंटरफेस ---
if 'q' not in st.session_state: st.session_state.q = None
if 'score' not in st.session_state: st.session_state.score = 0
if 'total' not in st.session_state: st.session_state.total = 0
if 'answered' not in st.session_state: st.session_state.answered = False

if db_meta and db_roopa:
    st.sidebar.metric("स्कोर", f"{st.session_state.score} / {st.session_state.total}")

    if st.button("🔄 नया प्रश्न तैयार करें"):
        st.session_state.q = generate_question(db_meta, db_roopa)
        st.session_state.answered = False
        st.rerun()  # KeyError से बचने के लिए तुरंत रिफ्रेश

    if st.session_state.q:
        q = st.session_state.q
        st.info(
            f"धातु **'{q['dhatu']}'** ({q['artha']}) का **{q['lakara']}**, **{q['purusha']} पुरुष**, **{q['vachana']}** चुनें।")

        user_choice = st.radio("विकल्प:", q['options'], index=None, disabled=st.session_state.answered)

        if not st.session_state.answered and st.button("✅ सबमिट"):
            if user_choice:
                st.session_state.total += 1
                st.session_state.answered = True
                if user_choice == q['correct']:
                    st.success(f"🚩 शुद्धम्! {q['correct']}")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ अशुद्धम्। सही उत्तर: {q['correct']}")
                st.rerun()

        if st.session_state.answered:
            # सुरक्षित रूप से नियम प्राप्त करें
            rule_text = get_grammatical_rule(q.get('lak_code'), q.get('pur_key'), q.get('vac_key'))
            st.warning(rule_text)

            st.divider()
            # ३x३ मैट्रिक्स
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