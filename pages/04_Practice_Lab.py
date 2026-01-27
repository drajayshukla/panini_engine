import streamlit as st
import json
import os
from core.phonology import sanskrit_varna_vichhed, sanskrit_varna_samyoga
from core.it_sanjna_engine import ItSanjnaEngine
from core.upadesha_registry import UpadeshaType

# --- १. पेज कॉन्फ़िगरेशन ---
st.set_page_config(page_title="Simulation Lab - अष्टाध्यायी-यंत्र", layout="wide")
st.title("🧪 पाणिनीय सिमुलेशन लैब: सूत्र-वार इत्-संज्ञा विश्लेषण")


# --- २. डेटा लोडिंग (Practice Set Integration) ---
@st.cache_data
def load_practice_set():
    path = 'data/it_sanjna_practice_set.json'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


practice_data = load_practice_set()

# --- ३. साइडबार: क्लिनिकल सेटिंग्स एवं प्रैक्टिस सेट ---
with st.sidebar:
    st.header("⚙️ डायग्नोस्टिक सेटिंग्स")

    if practice_data:
        st.subheader("📚 मास्टर प्रैक्टिस सेट")
        # कैटेगरी चयन
        categories = [c['name'] for c in practice_data['categories']]
        selected_cat_name = st.selectbox("अभ्यास श्रेणी चुनें:", options=categories)

        # सिलेक्टेड कैटेगरी का डेटा निकालना
        current_cat = next(c for c in practice_data['categories'] if c['name'] == selected_cat_name)

        # उदाहरण चयन
        example_names = [ex['input'] for ex in current_cat['examples']]
        selected_example_input = st.selectbox("उदाहरण चुनें:", options=example_names)

        # उदाहरण का विवरण (Metadata)
        example_detail = next(ex for ex in current_cat['examples'] if ex['input'] == selected_example_input)

        # ऑटो-कॉन्फ़िगरेशन (JSON के आधार पर)
        default_type = example_detail.get('type', 'Dhatu').upper()
        # Enum मैपिंग (धातु/प्रत्यय आदि)
        source_type_idx = 0
        if "PRATYAYA" in default_type:
            source_type_idx = 1
        elif "VIBHAKTI" in default_type:
            source_type_idx = 2
    else:
        st.error("Practice Set JSON नहीं मिला।")
        selected_example_input = "गाधृँ"
        source_type_idx = 0

    st.markdown("---")

    # मैन्युअल ओवरराइड (Manual Overrides)
    source_type_val = st.selectbox(
        "उपदेश का प्रकार (Source Type):",
        options=[e.value for e in UpadeshaType],
        index=source_type_idx
    )
    source_type = UpadeshaType(source_type_val)

    is_taddhita = False
    if source_type == UpadeshaType.PRATYAYA:
        # तद्धित का ऑटो-डिटेक्शन नोट से या मैन्युअल
        is_taddhita = st.checkbox("क्या यह तद्धित प्रत्यय है?", value=("तद्धित" in example_detail.get('note', '')))

# --- ४. मुख्य विश्लेषण लूप ---
input_val = st.text_input("संस्कृत उपदेश विश्लेषण:", value=selected_example_input)

if input_val:
    # सूत्र संकेत (JSON से)
    if practice_data:
        st.info(f"💡 **व्याकरणिक संकेत (Sutra Note):** {example_detail['note']}")

    # क. 'Gold Standard' विच्छेद
    v_list = sanskrit_varna_vichhed(input_val)
    st.markdown("### 🧬 विच्छेद विश्लेषण")
    st.code(" + ".join(v_list), language=None)

    # ख. इंजन द्वारा इत्-संज्ञा प्रक्रिया
    remaining, tags = ItSanjnaEngine.run_it_sanjna_prakaran(
        varna_list=v_list.copy(),
        original_input=input_val,
        source_type=source_type,
        is_taddhita=is_taddhita
    )

    st.markdown("---")

    # --- ५. सूत्र-वार 'Active/Inactive' विज़ुअलाइज़ेशन ---
    st.subheader("🚩 इत्-संज्ञा प्रकरण (Sutra-wise Status)")
    cols = st.columns(3)
    sutra_info = {
        "१.३.२": "उपदेशेऽजनुनासिक इत्",
        "१.३.३": "हलन्त्यम्",
        "१.३.५": "आदिर्ञिटुडवः",
        "१.३.६": "षः प्रत्ययस्य",
        "१.३.७": "चुट्टू",
        "१.३.८": "लशक्वतद्धिते"
    }

    for idx, (s_num, s_name) in enumerate(sutra_info.items()):
        is_active = any(s_num in tag for tag in tags)
        status_color = "#e6ffed" if is_active else "#f9f9f9"
        border_color = "#28a745" if is_active else "#d1d5db"

        with cols[idx % 3]:
            st.markdown(f"""
                <div style="border: 2px solid {border_color}; padding: 10px; border-radius: 8px; background-color: {status_color}; text-align: center;">
                    <span style="font-size: 0.8rem; color: #666;">{s_num}</span><br>
                    <span style="font-weight: bold;">{s_name}</span><br>
                    <span style="color: {border_color};">{'● ACTIVE' if is_active else '○ INACTIVE'}</span>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # --- ६. परिणाम विज़ुअलाइज़ेशन ---
    res_col1, res_col2 = st.columns(2)

    with res_col1:
        st.subheader("🔬 मार्क किया गया रूप")
        marked_display = []
        temp_rem = remaining.copy()
        for v in v_list:
            if v in temp_rem:
                marked_display.append(v)
                temp_rem.remove(v)
            else:
                marked_display.append(f"~~{v}~~")
        st.markdown(f"### {' + '.join(marked_display)}")

    with res_col2:
        st.subheader("✨ तस्य लोपः (१.३.९)")
        final_anga = sanskrit_varna_samyoga(remaining)
        st.markdown(f"### {final_anga}")
        st.success(f"अवशेष अङ्ग: **{final_anga}**")

    # ७. विशेष निषेध (1.3.4 & 1.3.8)
    if source_type == UpadeshaType.VIBHAKTI:
        st.warning("🛡️ **१.३.४ न विभक्तौ तुस्माः:** 'तु' (त-वर्ग), 'स्', 'म्' को विभक्ति के अंत में सुरक्षित रखा गया।")