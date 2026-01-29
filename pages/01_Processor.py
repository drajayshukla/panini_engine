# panini_app/pages/1_Processor.py

import streamlit as st
import pandas as pd

# Core Paninian Modules (Surgically Integrated)
from core.phonology import ad, sanskrit_varna_samyoga
from core.upadesha_registry import UpadeshaType
from logic.it_engine import ItEngine
from core.analyzer import analyze_sanjna
from utils.data_loader import get_all_dhatus

# --- १. Page Configuration & Styling ---
st.set_page_config(
    page_title="इंजन - अष्टाध्यायी-यंत्र",
    layout="wide",
    page_icon="⚙️"
)

st.title("⚙️ पाणिनीय इंजन (Panini Processor)")
st.markdown("""
यह अनुभाग उपदेशों की **इत्-संज्ञा** और **वर्ण-विश्लेषण** के लिए समर्पित है। 
यह 'Surgical Trace' के साथ प्रक्रिया को दृश्यमान बनाता है।
---
""")


# --- २. Data Loading (Master Dhatupatha) ---
@st.cache_data
def load_dhatu_data():
    all_dhatus = get_all_dhatus()
    # Creating a searchable map: Display Name -> Raw Upadesha
    return {f"{d['upadesha']} ({d['artha_sanskrit']})": d['upadesha'] for d in all_dhatus}


dhatu_options_map = load_dhatu_data()

# --- ३. Sidebar Panel (Surgical Settings) ---
with st.sidebar:
    st.header("📚 उपदेश चयन (Input Context)")

    # Master Search Box for 1800+ Dhatus
    search_input = st.selectbox(
        "धातुपाठ से धातु खोजें:",
        options=[""] + list(dhatu_options_map.keys()),
        index=0,
        help="यहाँ १८००+ पाणिनीय धातुओं में से चयन करें"
    )

    st.markdown("---")

    # Manual Context Overrides
    st.subheader("⚙️ मैनुअल सेटिंग्स")
    manual_source_type = st.selectbox(
        "उपदेश प्रकार (Override):",
        options=[e.value for e in UpadeshaType],
        index=0,
        help="यदि ऑटो-डिटेक्शन विफल हो, तो यहाँ से प्रकार चुनें।"
    )

    manual_taddhita = st.checkbox("Manual Taddhita Flag", value=False)
    st.info("नोट: धातु चयन करने पर सिस्टम 'Adhikāra' के आधार पर ऑटो-डिटेक्ट करेगा।")

# --- ४. Input Processing Block ---
# Logic: Priority to Search Selection -> then to Manual Text Input
default_val = dhatu_options_map[search_input] if search_input else "गाधृँ"
raw_input = st.text_input("संस्कृत उपदेश (धातु/प्रत्यय/आगम) यहाँ लिखें:", value=default_val)

if raw_input:
    input_text = raw_input.strip()

    # १. Auto-Detection (Upadesha Registry Upgrade)
    detected_type, is_taddhita_flag, sutra_origin = UpadeshaType.auto_detect(input_text)

    # Final Parameter Determination
    source_type = detected_type if detected_type else UpadeshaType(manual_source_type)
    is_taddhita_final = is_taddhita_flag if detected_type else manual_taddhita

    # २. Varna Vichheda (Physiological Decomposition via 'ad')
    # Returns a list of Varna Objects with Kāla, Sthāna, and Svara metadata
    varna_list = ad(input_text)

    # ३. It-Engine Execution (Surgical Scrub)
    # Identifies markers and performs तस्य लोपः (1.3.9)
    remaining_varnas, it_tags = ItEngine.run_it_prakaran(
        varna_list,
        source_type=source_type,
        is_taddhita=is_taddhita_final
    )

    # UI Feedback (Sidebar)
    if detected_type:
        st.sidebar.success(f"✅ ऑटो-डिटेक्ट: {detected_type.value}")
        st.sidebar.caption(f"मूल सूत्र: {sutra_origin}")
    if is_taddhita_final:
        st.sidebar.warning("🛡️ तद्धित निषेध (१.३.८) सक्रिय")

    # --- ५. Visualization (Main Display) ---
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🔬 १. इत्-संज्ञा (Identification)")
        # Visualizing elision with strikethrough logic
        marked_display = []
        for v in varna_list:
            if v in remaining_varnas:
                marked_display.append(f"**{v.char}**")
            else:
                marked_display.append(f"~~{v.char}~~")

        st.markdown(f"**प्रक्रिया अवस्था (मार्क किया गया रूप):**")
        st.markdown(f"<div style='font-size: 2.5rem; letter-spacing: 5px;'>{' + '.join(marked_display)}</div>",
                    unsafe_allow_html=True)

        if it_tags:
            for tag in it_tags:
                st.markdown(f"🚩 {tag}")
        else:
            st.info("कोई इत्-संज्ञा (Marker) प्राप्त नहीं हुई।")

    with col2:
        st.subheader("✂️ २. तस्य लोपः (Execution)")
        st.markdown(f"**लोप के बाद का स्वरूप (१.३.९):**")
        st.markdown(
            f"<div style='font-size: 2.5rem; color: #4CAF50;'>{' + '.join([v.char for v in remaining_varnas])}</div>",
            unsafe_allow_html=True)

        # Final samyoga (Synthesis)
        shuddha_anga = sanskrit_varna_samyoga(remaining_varnas)
        st.success(f"शुद्ध अङ्ग / आधार: **{shuddha_anga}**")

    # --- ६. Varna-Analysis Matrix (The DNA Grid) ---
    st.markdown("---")
    st.subheader("🔍 ३. वर्ण-विश्लेषण एवं संज्ञा मैट्रिक्स (DNA Matrix)")

    # Diagnostic Data from Zone 1 Analyzer
    analysis_data = analyze_sanjna(varna_list)

    # Creating dynamic columns for each character in the input
    cols = st.columns(len(varna_list) if varna_list else 1)

    for idx, item in enumerate(analysis_data):
        with cols[idx]:
            # Color coding based on 'It' status
            is_it = varna_list[idx] not in remaining_varnas
            box_style = "🔴 IT" if is_it else "🔵 AL"

            st.markdown(f"### {item['varna']}")
            st.code(box_style)

            # Displaying technical Sanjnas (Guna, Vriddhi, Samyoga)
            if item['tags']:
                for t in item['tags']:
                    st.caption(f"🏷️ {t}")
            else:
                st.caption("-")

            # Phonetic Birthplace (Sthana)
            st.markdown(f"**स्थान:**\n{item.get('sthana', 'Unknown')}")

    # --- ७. Workflow Audit Table ---
    st.markdown("---")
    st.subheader("📊 प्रक्रिया सारांश (Workflow Summary)")

    summary_data = [
        {"चरण": "१. उपदेश", "विवरण": input_text, "स्थिति": source_type.value},
        {"चरण": "२. विच्छेद", "विवरण": " + ".join([v.char for v in varna_list]), "स्थिति": "Completed"},
        {"चरण": "३. इत्-लोप", "विवरण": " + ".join([v.char for v in remaining_varnas]),
         "स्थिति": f"{len(it_tags)} markers removed"},
        {"चरण": "४. अन्तिम रूप", "विवरण": shuddha_anga, "स्थिति": "Ready for Vidhi"}
    ]
    st.table(pd.DataFrame(summary_data))

    # --- ८. Quick Export (Surgical Trace) ---
    st.download_button(
        label="Download Process Trace (JSON)",
        data=str({"input": input_text, "it_tags": it_tags, "final": shuddha_anga}),
        file_name=f"panini_trace_{input_text}.json",
        mime="application/json"
    )

else:
    st.warning("कृपया ऊपर एक उपदेश लिखें या बाईं ओर से धातु चुनें।")