import streamlit as st
import json
import os
import re
import pandas as pd
from core.phonology import sanskrit_varna_vichhed, sanskrit_varna_samyoga
from core.it_sanjna_engine import ItSanjnaEngine
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

# --- १. पाणिनीय संज्ञा मैपिंग (It-Label Logic) ---
def get_it_labels(varna_list, remaining_list):
    """
    हटाए गए वर्णों के आधार पर पाणिनीय संज्ञाएं (Labels) बनाना।
    जैसे: 'ल्' हटा -> 'लित्', 'ङ्' हटा -> 'ङित्'
    """
    removed_varnas = []
    temp_rem = remaining_list.copy()
    for v in varna_list:
        if v in temp_rem:
            temp_rem.remove(v)
        else:
            # हलन्त हटाकर शुद्ध वर्ण आधार प्राप्त करना
            clean_v = v.replace('्', '')
            removed_varnas.append(clean_v)

    # पाणिनीय प्रारूप में 'ित्' जोड़ना
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

# --- ४. साइडबार: क्लिनिकल कंट्रोल्स ---
with st.sidebar:
    st.header("⚙️ लैब कंट्रोल्स")
    db_choice = st.selectbox("डेटाबेस चुनें:", options=list(all_data.keys()))
    selected_db = all_data[db_choice]

    example_input = ""
    note_hint = ""

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
    source_type_val = st.selectbox("उपदेश प्रकार:", options=[e.value for e in UpadeshaType],
                                   index=[e.value for e in UpadeshaType].index(
                                       detected_type.value) if detected_type else 0)
    source_type = UpadeshaType(source_type_val)
    is_taddhita = st.checkbox("तद्धित प्रत्यय निषेध (1.3.8)", value=is_taddhita_auto)

# --- ५. मुख्य विश्लेषण पैनल ---


if example_input:
    if note_hint: st.info(f"📚 **व्याकरणिक संदर्भ:** {note_hint}")

    v_list = sanskrit_varna_vichhed(example_input)
    remaining, tags = ItSanjnaEngine.run_it_sanjna_prakaran(
        varna_list=v_list.copy(), original_input=example_input,
        source_type=source_type, is_taddhita=is_taddhita
    )

    # १. संज्ञा जनरेशन (Sangya Generation)
    it_labels = get_it_labels(v_list, remaining)

    st.subheader(f"🔍 डायग्नोस्टिक विश्लेषण: {example_input}")

    # २. पाणिनीय लेबल्स का डिस्प्ले
    if it_labels:
        label_cols = st.columns(len(it_labels))
        for idx, label in enumerate(it_labels):
            label_cols[idx].markdown(f"""
                <div style="background-color: #6366f1; color: white; padding: 10px; border-radius: 50px; text-align: center; font-weight: bold; font-size: 1.1rem; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); margin-bottom: 20px;">
                    {label}
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ३. विज़ुअल 'Sutra-Matrix'
    st.subheader("🚩 सक्रिय इत्-संज्ञा सूत्र")
    sutra_map = {"१.३.२": "अजनुनासिक", "१.३.३": "हलन्त्यम्", "१.३.४": "न विभक्तौ", "१.३.५": "आदिर्ञिटु", "१.३.६": "षः",
                 "१.३.७": "चुट्टू", "१.३.८": "लशक्व"}
    s_cols = st.columns(len(sutra_map))
    for i, (num, name) in enumerate(sutra_map.items()):
        active = any(num in tag for tag in tags)
        color = "#28a745" if active else "#6c757d"
        bg = "#e6ffed" if active else "#f8f9fa"
        s_cols[i].markdown(f"""
            <div style="border: 2px solid {color}; background-color: {bg}; padding: 10px; border-radius: 8px; text-align: center; height: 100px; display: flex; flex-direction: column; justify-content: center;">
                <b style="color: {color}; font-size: 0.8rem;">{num}</b><br>
                <span style="font-size: 0.7rem;">{name}</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # ४. विज़ुअल परिणाम (चिह्नीकरण एवं लोप)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔬 इत्-संज्ञा चिह्नीकरण")
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
        st.subheader("✨ अवशेष अङ्ग (१.३.९)")
        final = sanskrit_varna_samyoga(remaining)
        st.markdown(f"<div style='font-size: 3rem; color: #28a745; font-weight: bold;'>{final}</div>",
                    unsafe_allow_html=True)
        st.success(f"अन्तिम अङ्ग: {final}")

    # ५. विशेष निषेध अलर्ट्स
    st.markdown("---")
    if source_type == UpadeshaType.VIBHAKTI:
        st.warning("🛡️ **विभक्ति सुरक्षा कवच (१.३.४):** अन्त्य 'त-वर्ग', 'स्' और 'म्' सुरक्षित रहे।")
    if is_taddhita:
        st.error("🚫 **तद्धित निषेध (१.३.८):** आदि 'ल-श-कु' की इत्-संज्ञा बाधित।")

    # ६. सारांश टेबल
    st.subheader("📊 प्रक्रिया सारांश")
    workflow = [
        {"क्रम": 1, "प्रक्रिया": "विच्छेद", "परिणाम": " + ".join(v_list)},
        {"क्रम": 2, "प्रक्रिया": "संज्ञा", "परिणाम": ", ".join(it_labels) if it_labels else "None"},
        {"क्रम": 3, "प्रक्रिया": "लोप", "परिणाम": final}
    ]
    st.table(workflow)