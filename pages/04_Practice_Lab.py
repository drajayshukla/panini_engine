#pages/04_Practice_Lab.py
import streamlit as st
import json
import os
from core.phonology import sanskrit_varna_vichhed, sanskrit_varna_samyoga
from logic.it_engine import ItSanjnaEngine
from core.upadesha_registry import UpadeshaType


# ==============================================================================
# FEATURE LIST (LAB CAPABILITIES):
# 1. Phonology Integration: Gold-standard varna-vichhed handling implicit vowels.
# 2. Multi-Database Support: Loads Dhatu, Krit, Taddhita, and Vibhakti JSONs.
# 3. All-Sutra Category: Aggregates all practice examples into a single list.
# 4. Auto-Detection: Automatically identifies Upadesha type (Dhatu/Pratyaya, etc.).
# 5. Visual Sutra Matrix: Real-time status of sutras 1.3.2 to 1.3.8.
# 6. Surgical Strikethrough: Red line-through visualization for deleted characters.
# 7. It-Sanjna Labeling: Dynamic generation of Paninian labels (e.g., Kit, Nit, Lit).
# 8. Protection Alerts: Warnings for 1.3.4 (Vibhakti) and 1.3.8 (Taddhita) blocks.
# 9. Workflow Summary: Tabular summary of the clinical transformation.
# ==============================================================================
# 10. Manual Input Support: Direct typing or pasting of any Sanskrit word.
# 11. Hybrid Selection Logic: Priority given to manual input over database selection.
# ==============================================================================

# --- १. पाणिनीय संज्ञा मैपिंग ---
def get_it_labels(varna_list, remaining_list):
    removed_varnas = []
    temp_rem = remaining_list.copy()
    for v in varna_list:
        if v in temp_rem:
            temp_rem.remove(v)
        else:
            clean_v = v.replace('्', '')
            removed_varnas.append(clean_v)
    labels = [f"{v}ित्" for v in removed_varnas if v.strip()]
    return sorted(list(set(labels)))


# --- २. पेज सेटअप ---
st.set_page_config(page_title="Universal Panini Lab", layout="wide", page_icon="🧪")
st.title("🧪 पाणिनीय महा-सिमुलेशन लैब")
st.caption("अष्टाध्यायी-यंत्र: इत्-संज्ञा एवं अनुबन्ध-संज्ञा (Labels) विश्लेषण")


# --- ३. वृहद् डेटा लोडर ---
@st.cache_data
def load_panini_ecosystem():
    files = {
        "🎯 मास्टर अभ्यास माला": "it_sanjna_practice_set.json",
        "💎 धातु-पाठ (Master)": "dhatu_master_structured.json",
        "📦 कृत् प्रत्यय (Krit)": "krit_pratyayas.json",
        "🏷️ तद्धित प्रत्यय (Taddhita)": "taddhita_master_data.json",
        "🔱 विभक्ति/तिङ् (Vibhakti)": "vibhaktipatha.json",
        "⚙️ चुट्टू विशिष्ट (1.3.7)": "chuttu_pratyayas.json",
        "🛡️ शित् विशिष्ट (1.3.6)": "shit_pratyaya.json"
    }
    data_store = {}
    for label, fname in files.items():
        path = f'data/{fname}'
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data_store[label] = json.load(f)
    return data_store


all_data = load_panini_ecosystem()

# --- ४. साइडबार: क्लिनिकल कंट्रोल्स ---
with st.sidebar:
    st.header("⚙️ लैब कंट्रोल्स")

    # NEW: टाइपिंग या डेटाबेस के बीच चयन
    input_mode = st.radio("इनपुट मोड चुनें:", ["डेटाबेस से चुनें", "सीधे टाइप/पेस्ट करें"])

    selected_val = ""
    note_hint = ""

    if input_mode == "डेटाबेस से चुनें":
        db_choice = st.selectbox("डेटाबेस चुनें:", options=list(all_data.keys()))
        selected_db = all_data[db_choice]

        if db_choice == "🎯 मास्टर अभ्यास माला":
            sub_cats = ["ऑल इट सूत्र (1.3.2 - 1.3.8)"] + [c['name'] for c in selected_db['categories']]
            sub_choice = st.selectbox("उप-श्रेणी:", sub_cats)
            if sub_choice == "ऑल इट सूत्र (1.3.2 - 1.3.8)":
                all_ex = []
                for cat in selected_db['categories']: all_ex.extend(cat['examples'])
                examples = sorted({ex['input']: ex for ex in all_ex}.values(), key=lambda x: x['input'])
            else:
                examples = next(c for c in selected_db['categories'] if c['name'] == sub_choice)['examples']
            obj = st.selectbox("उदाहरण चुनें:", options=examples,
                               format_func=lambda x: f"{x['input']} ({x.get('type', '')})")
            selected_val = obj['input']
            note_hint = obj['note']
        elif isinstance(selected_db, list):
            search_key = 'upadesha' if 'upadesha' in selected_db[0] else (
                'pratyay' if 'pratyay' in selected_db[0] else 'name')
            obj = st.selectbox("उदाहरण चुनें:", options=selected_db, format_func=lambda x: str(x.get(search_key, "")))
            selected_val = str(obj.get(search_key, ""))
            note_hint = obj.get('artha_sanskrit', obj.get('meaning', obj.get('note', "")))
    else:
        # MANUAL TYPING MODE
        selected_val = st.text_input("संस्कृत उपदेश टाइप/पेस्ट करें (जैसे: डुकृञ्, क्त्वा):", value="डुकृञ्")
        note_hint = "Manual Entry: System will auto-detect rules."

    st.markdown("---")
    # ऑटो-डिटेक्ट लॉजिक
    detected_type, is_taddhita_auto = UpadeshaType.auto_detect(selected_val)
    source_type_val = st.selectbox("उपदेश प्रकार (Sutra 1.3.4-8 हेतु):",
                                   options=[e.value for e in UpadeshaType],
                                   index=[e.value for e in UpadeshaType].index(
                                       detected_type.value) if detected_type else 0)
    source_type = UpadeshaType(source_type_val)
    is_taddhita = st.checkbox("तद्धित प्रत्यय निषेध (1.3.8)", value=is_taddhita_auto)

# --- ५. मुख्य विश्लेषण पैनल ---

st.subheader(f"🔍 डायग्नोस्टिक विश्लेषण: {selected_val}")

if selected_val:
    if note_hint: st.info(f"📚 **व्याकरणिक संदर्भ:** {note_hint}")

    # १. विच्छेद
    v_list = sanskrit_varna_vichhed(selected_val)
    st.markdown("### 🧬 १. वर्ण-विच्छेद")
    st.code(" + ".join(v_list), language=None)

    # २. इत्-संज्ञा इंजन
    remaining, tags = ItSanjnaEngine.run_it_sanjna_prakaran(
        varna_list=v_list.copy(), original_input=selected_val,
        source_type=source_type, is_taddhita=is_taddhita
    )

    # ३. संज्ञा जनरेशन
    it_labels = get_it_labels(v_list, remaining)
    if it_labels:
        label_cols = st.columns(len(it_labels))
        for idx, label in enumerate(it_labels):
            label_cols[idx].markdown(
                f"<div style='background-color: #6366f1; color: white; padding: 10px; border-radius: 50px; text-align: center; font-weight: bold;'>{label}</div>",
                unsafe_allow_html=True)

    # ४. सुव्यवस्थित 'Sutra-Matrix'
    st.markdown("---")
    st.subheader("🚩 २. सक्रिय इत्-संज्ञा सूत्र")
    sutra_map = {"१.३.२": "अजनुनासिक", "१.३.३": "हलन्त्यम्", "१.३.४": "न विभक्तौ", "१.३.५": "आदिर्ञिटु", "१.३.६": "षः",
                 "१.३.७": "चुट्टू", "१.३.८": "लशक्व"}
    s_cols = st.columns(len(sutra_map))
    for i, (num, name) in enumerate(sutra_map.items()):
        is_active = any(num in tag for tag in tags)
        color = "#28a745" if is_active else "#6c757d"
        bg = "#e6ffed" if is_active else "#f8f9fa"
        s_cols[i].markdown(
            f"<div style='border: 2px solid {color}; background-color: {bg}; padding: 10px; border-radius: 8px; text-align: center; min-height: 100px; display: flex; flex-direction: column; justify-content: center;'><b style='color: {color}; font-size: 0.8rem;'>{num}</b><br><span style='font-size: 0.7rem;'>{name}</span></div>",
            unsafe_allow_html=True)

    st.markdown("---")

    # ५. विज़ुअल परिणाम
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔬 ३. इत्-संज्ञा चिह्नीकरण")
        marked = []
        temp_rem = remaining.copy()
        for v in v_list:
            if v in temp_rem:
                marked.append(v); temp_rem.remove(v)
            else:
                marked.append(f"<span style='color: #ff4b4b; text-decoration: line-through;'>{v}</span>")
        st.markdown(f"### {' + '.join(marked)}", unsafe_allow_html=True)
        if tags:
            for tag in tags: st.warning(f"🚩 {tag}")

    with col2:
        st.subheader("✨ ४. तस्य लोपः (अन्तिम रूप)")
        final = sanskrit_varna_samyoga(remaining)
        st.markdown(f"<div style='font-size: 3rem; color: #28a745; font-weight: bold;'>{final}</div>",
                    unsafe_allow_html=True)
        st.success(f"अन्तिम अङ्ग: {final}")

    # ६. सारांश टेबल
    st.subheader("📊 ५. प्रक्रिया सारांश")
    workflow = [
        {"क्रम": 1, "प्रक्रिया": "विच्छेद", "परिणाम": " + ".join(v_list)},
        {"क्रम": 2, "प्रक्रिया": "संज्ञा", "परिणाम": ", ".join(it_labels) if it_labels else "None"},
        {"क्रम": 3, "प्रक्रिया": "लोप", "परिणाम": final}
    ]
    st.table(workflow)