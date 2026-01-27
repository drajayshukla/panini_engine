import streamlit as st
import json
import pandas as pd
import os
import re

# कोर मॉड्यूल्स का इम्पोर्ट (Phonology Integrated)
from core.phonology import sanskrit_varna_vichhed, sanskrit_varna_samyoga
from core.upadesha_registry import UpadeshaType
from core.it_sanjna_engine import ItSanjnaEngine
from core.analyzer import analyze_sanjna
from core.morph_rules import apply_ata_upadhayah_7_2_116

# --- १. पेज सेटअप ---
st.set_page_config(page_title="इंजन - अष्टाध्यायी-यंत्र", layout="wide")
st.title("⚙️ पाणिनीय इंजन (Processor)")

# --- २. साइड पैनल (Sidebar) ---
with st.sidebar:
    st.header("📚 अभ्यास एवं सेटिंग्स")
    example_list = {
        "कस्टम": "",
        "गाधृँ (Dhatu)": "गाधृँ",
        "ष्वुन् (Shit-Krut)": "ष्वुन्",
        "ञ्युट् (Chuttu-Krut)": "ञ्युट्",
        "जस् (Vibhakti)": "जस्",
        "टाप् (Stri-Pratyaya)": "टाप्",
        "ष्यञ् (Shit-Taddhita)": "ष्यञ्",
        "कन् (Taddhita)": "कन्",
        "एधँ (Dhatu)": "एधँ",
        "स्पर्धँ (Dhatu)": "स्पर्धँ"
    }
    selected_example = st.selectbox("प्रमुख उदाहरण चुनें:", options=list(example_list.keys()))

    st.markdown("---")
    source_type_input = st.selectbox(
        "उपदेश का प्रकार (Manual Override):",
        options=[e.value for e in UpadeshaType],
        index=0
    )
    manual_source_type = UpadeshaType(source_type_input)
    manual_taddhita = st.checkbox("Manual Taddhita Flag (Force)", value=False)

# --- ३. मुख्य इनपुट प्रोसेसिंग ---
default_input = example_list[selected_example] if selected_example != "कस्टम" else "गाधृँ"
raw_input = st.text_input("संस्कृत उपदेश (धातु/प्रत्यय) लिखें:", value=default_input)

if raw_input:
    input_text = raw_input.strip()

    # १. टुपल अनपैकिंग (Phonology and Registry Coordination)
    detected_type, is_taddhita_flag = UpadeshaType.auto_detect(input_text)

    # २. सोर्स टाइप और तद्धित फ्लैग का निर्धारण
    source_type = detected_type if detected_type else manual_source_type
    is_taddhita_final = is_taddhita_flag if detected_type else manual_taddhita

    # ३. 'Gold Standard' विच्छेद (Imported from core.phonology)
    original_varna_list = sanskrit_varna_vichhed(input_text)

    # ४. इत्-संज्ञा इंजन कॉल
    remaining_varnas, it_tags = ItSanjnaEngine.run_it_sanjna_prakaran(
        original_varna_list.copy(),
        input_text,
        source_type,
        is_taddhita=is_taddhita_final
    )

    # UI फीडबैक
    if detected_type:
        st.sidebar.success(f"✅ ऑटो-डिटेक्ट: {detected_type.value}")
    else:
        st.sidebar.info(f"ℹ️ मोड: {manual_source_type.value}")

    if is_taddhita_final:
        st.sidebar.warning("🛡️ तद्धित प्रत्यय पाया गया ($1.3.8$ निषेध सक्रिय)")

    # --- ४. विज़ुअलाइज़ेशन ---
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("१. इत्-संज्ञा (Identification)")
        marked_display = []
        temp_remaining = remaining_varnas.copy()
        for v in original_varna_list:
            if v in temp_remaining:
                marked_display.append(v)
                temp_remaining.remove(v)
            else:
                marked_display.append(f"~~{v}~~")

        st.markdown(f"**मार्क किया गया रूप (तस्य लोपः पूर्वम्):**")
        st.markdown(f"### {' + '.join(marked_display)}")
        if it_tags:
            for tag in it_tags: st.markdown(f"🚩 {tag}")
        else:
            st.info("कोई इत्-संज्ञा नहीं मिली।")

    with col2:
        st.subheader("२. तस्य लोपः (Execution)")
        st.markdown(f"**लोप के बाद (१.३.९):**")
        st.markdown(f"### {' + '.join(remaining_varnas)}")
        # 'Gold Standard' संयोग (Imported from core.phonology)
        shuddha_anga = sanskrit_varna_samyoga(remaining_varnas)
        st.success(f"अन्तिम अङ्ग: **{shuddha_anga}**")

    # --- ५. विश्लेषण और विधि-सूत्र ---
    st.markdown("---")
    st.subheader("🔍 ३. संज्ञा विश्लेषण एवं विधि-सूत्र")
    analysis_col, morph_col = st.columns([2, 1])

    with analysis_col:
        analysis = analyze_sanjna(original_varna_list)
        cols = st.columns(len(original_varna_list) if original_varna_list else 1)
        tracking_remaining = remaining_varnas.copy()
        for idx, item in enumerate(analysis):
            with cols[idx]:
                is_it = False
                if item['varna'] in tracking_remaining:
                    tracking_remaining.remove(item['varna'])
                else:
                    is_it = True
                box_style = "🔴" if is_it else "🔵"
                st.info(f"{box_style} **{item['varna']}**\n\n{', '.join(item['tags']) if item['tags'] else '-'}")

    with morph_col:
        st.write("**रूपांतरण (Morphology):**")
        final_varnas, is_applied = apply_ata_upadhayah_7_2_116(remaining_varnas.copy())
        if is_applied:
            st.success(f"परिवर्तित रूप: **{sanskrit_varna_samyoga(final_varnas)}**")
            st.caption("सूत्र: ७.२.११६ अत उपधायाः")
        else:
            st.write("कोई विधि-सूत्र लागू नहीं हुआ।")

    # --- ६. प्रक्रिया सारांश ---
    st.markdown("---")
    st.subheader("📊 प्रक्रिया सारांश (Workflow Summary)")
    steps = [
        {"क्रम": 1, "प्रक्रिया": "उपदेश (Input)", "status": input_text},
        {"क्रम": 2, "प्रक्रिया": "विच्छेद (Phonology)", "status": " + ".join(original_varna_list)},
        {"क्रम": 3, "प्रक्रिया": "तस्य लोपः (Lopa)", "status": shuddha_anga}
    ]
    st.table(steps)