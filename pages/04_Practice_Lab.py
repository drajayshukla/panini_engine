import streamlit as st
import json
import os
import re
import pandas as pd
from core.phonology import sanskrit_varna_vichhed, sanskrit_varna_samyoga
from core.it_sanjna_engine import ItSanjnaEngine
from core.upadesha_registry import UpadeshaType

# --- १. पेज कॉन्फ़िगरेशन ---
st.set_page_config(page_title="Universal Panini Lab", layout="wide", page_icon="🧪")
st.title("🧪 पाणिनीय महा-सिमुलेशन लैब")
st.caption("अष्टाध्यायी-यंत्र: इत्-संज्ञा प्रकरण का पूर्ण 'Step-by-Step' विश्लेषण")


# --- २. वृहद् डेटा लोडर ---
@st.cache_data
def load_panini_ecosystem():
    files = {
        "🎯 मास्टर अभ्यास माला": "it_sanjna_practice_set.json",
        "💎 धातु-पाठ (Master)": "dhatu_master_structured.json",
        "📦 कृत् प्रत्यय (Krit)": "krit_pratyayas.json",
        "🏷️ तद्धित प्रत्यय (Taddhita)": "taddhita_master_data.json",
        "🔱 विभक्ति/तिङ् (Vibhakti)": "vibhaktipatha.json",
        "⚙️ चुट्टू विशिष्ट (1.3.7)": "chuttu_pratyayas.json",
        "🛡️ शित् विशिष्ट (1.3.6)": "shit_pratyayas_addition.json"
    }
    data_store = {}
    for label, fname in files.items():
        path = f'data/{fname}'
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data_store[label] = json.load(f)
    return data_store


all_data = load_panini_ecosystem()

# --- ३. साइडबार: क्लिनिकल कंट्रोल्स ---
with st.sidebar:
    st.header("⚙️ लैब कंट्रोल्स")
    db_choice = st.selectbox("डेटाबेस चुनें:", options=list(all_data.keys()))
    selected_db = all_data[db_choice]

    example_input = ""
    note_hint = ""

    if db_choice == "🎯 मास्टर अभ्यास माला":
        # 'ऑल इट सूत्र' को उप-श्रेणी में जोड़ना
        sub_cats = ["ऑल इट सूत्र (1.3.2 - 1.3.8)"] + [c['name'] for c in selected_db['categories']]
        sub_choice = st.selectbox("उप-श्रेणी (Category):", sub_cats)

        if sub_choice == "ऑल इट सूत्र (1.3.2 - 1.3.8)":
            all_examples = []
            for cat in selected_db['categories']:
                all_examples.extend(cat['examples'])
            # यूनिक उदाहरण सुनिश्चित करना
            examples = sorted({ex['input']: ex for ex in all_examples}.values(), key=lambda x: x['input'])
        else:
            examples = next(c for c in selected_db['categories'] if c['name'] == sub_choice)['examples']

        obj = st.selectbox("उदाहरण चुनें:", options=examples,
                           format_func=lambda x: f"{x['input']} ({x.get('type', '')})")
        example_input = obj['input']
        note_hint = obj['note']

    elif isinstance(selected_db, list):
        search_key = 'upadesha' if 'upadesha' in selected_db[0] else \
            ('pratyay' if 'pratyay' in selected_db[0] else 'name')
        obj = st.selectbox("उदाहरण चुनें:", options=selected_db, format_func=lambda x: str(x.get(search_key, "")))
        example_input = str(obj.get(search_key, ""))
        note_hint = obj.get('artha_sanskrit', obj.get('meaning', obj.get('note', "")))

    st.markdown("---")
    detected_type, is_taddhita_auto = UpadeshaType.auto_detect(example_input)
    source_type_val = st.selectbox("उपदेश प्रकार (Sutra 1.3.4-8 हेतु):",
                                   options=[e.value for e in UpadeshaType],
                                   index=[e.value for e in UpadeshaType].index(
                                       detected_type.value) if detected_type else 0)
    source_type = UpadeshaType(source_type_val)
    is_taddhita = st.checkbox("तद्धित प्रत्यय निषेध (Sutra 1.3.8)", value=is_taddhita_auto)

# --- ४. मुख्य विश्लेषण पैनल ---

st.subheader(f"🔍 डायग्नोस्टिक विश्लेषण: {example_input}")

if example_input:
    if note_hint: st.info(f"📚 **व्याकरणिक संदर्भ:** {note_hint}")

    # १. विच्छेद
    v_list = sanskrit_varna_vichhed(example_input)
    st.markdown("### 🧬 १. वर्ण-विच्छेद")
    st.code(" + ".join(v_list), language=None)

    # २. इत्-संज्ञा इंजन
    remaining, tags = ItSanjnaEngine.run_it_sanjna_prakaran(
        varna_list=v_list.copy(),
        original_input=example_input,
        source_type=source_type,
        is_taddhita=is_taddhita
    )

    # ३. सुव्यवस्थित 'Sutra-Matrix'
    st.markdown("---")
    st.subheader("🚩 २. सक्रिय इत्-संज्ञा सूत्र")
    sutra_map = {
        "१.३.२": "उपदेशेऽजनुनासिक इत्", "१.३.३": "हलन्त्यम्",
        "१.३.४": "न विभक्तौ तुस्माः", "१.३.५": "आदिर्ञिटुडवः",
        "१.३.६": "षः प्रत्ययस्य", "१.३.७": "चुट्टू", "१.३.८": "लशक्वतद्धिते"
    }

    s_cols = st.columns(len(sutra_map))
    for i, (num, name) in enumerate(sutra_map.items()):
        is_active = any(num in tag for tag in tags)
        color = "#28a745" if is_active else "#6c757d"
        bg = "#e6ffed" if is_active else "#f8f9fa"
        s_cols[i].markdown(f"""
            <div style="border: 2px solid {color}; background-color: {bg}; padding: 10px; border-radius: 8px; text-align: center; min-height: 110px; display: flex; flex-direction: column; justify-content: center;">
                <b style="color: {color}; font-size: 0.9rem;">{num}</b><br>
                <span style="font-size: 0.75rem; font-weight: 500;">{name}</span><br>
                <span style="font-size: 0.7rem; color: {color};">{'● ACTIVE' if is_active else '○ INACTIVE'}</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ४. विज़ुअल ट्रेस
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔬 ३. इत्-संज्ञा चिह्नीकरण")
        marked_display = []
        temp_rem = remaining.copy()
        for v in v_list:
            if v in temp_rem:
                marked_display.append(v); temp_rem.remove(v)
            else:
                marked_display.append(f"<span style='color: #ff4b4b; text-decoration: line-through;'>{v}</span>")

        st.markdown(f"<div style='font-size: 2rem; letter-spacing: 5px;'>{' + '.join(marked_display)}</div>",
                    unsafe_allow_html=True)
        if tags:
            for tag in tags: st.warning(f"🚩 {tag}")
        else:
            st.info("कोई इत्-संज्ञा सूत्र लागू नहीं हुआ।")

    with col2:
        st.subheader("✨ ४. तस्य लोपः (अन्तिम रूप)")
        final_anga = sanskrit_varna_samyoga(remaining)
        st.markdown(f"<div style='font-size: 3rem; color: #28a745; font-weight: bold;'>{final_anga}</div>",
                    unsafe_allow_html=True)
        st.success(f"अन्तिम अङ्ग (सूत्र १.३.९ द्वारा): {final_anga}")

    # ५. विशेष अलर्ट्स
    st.markdown("---")
    if source_type == UpadeshaType.VIBHAKTI:
        st.warning("🛡️ **विभक्ति सुरक्षा कवच (१.३.४):** अन्त्य 'त-वर्ग', 'स्' और 'म्' सुरक्षित रहे।")
    if is_taddhita:
        st.error("🚫 **तद्धित निषेध (१.३.८):** तद्धित प्रत्यय होने के कारण आदि 'ल-श-कु' की इत्-संज्ञा बाधित।")

    # ६. सारांश टेबल
    st.subheader("📊 ५. प्रक्रिया सारांश")
    workflow_data = [
        {"क्रम": 1, "प्रक्रिया": "विच्छेद", "परिणाम": " + ".join(v_list), "सूत्र": "Phonology"},
        {"क्रम": 2, "प्रक्रिया": "इत्-संज्ञा",
         "परिणाम": " + ".join([re.sub('<[^<]+?>', '', m) for m in marked_display]), "सूत्र": "१.३.२ - १.३.८"},
        {"क्रम": 3, "प्रक्रिया": "तस्य लोपः", "परिणाम": final_anga, "सूत्र": "१.३.९"}
    ]
    st.table(workflow_data)