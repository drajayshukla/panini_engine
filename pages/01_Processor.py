import streamlit as st
import json
import pandas as pd
import os
import re

# कोर मॉड्यूल्स का इम्पोर्ट
from core.upadesha_registry import UpadeshaType
from core.it_sanjna_engine import ItSanjnaEngine
from core.analyzer import analyze_sanjna
from core.morph_rules import apply_ata_upadhayah_7_2_116


# --- १. व्याकरणिक सहायक (Surgical Helpers) ---

def sanskrit_varna_vichhed(text):
    """पाणिनीय १६-नियम विच्छेद (Granular Style)"""
    if not text: return []
    text = re.sub(r'[0-9०-९.]', '', text).strip()
    text = text.replace('क्ष', 'क्‌ष').replace('त्र', 'त्‌र').replace('ज्ञ', 'ज्‌ञ').replace('श्र', 'श्‌र')

    vowels_map = {'ा': 'आ', 'ि': 'इ', 'ी': 'ई', 'ु': 'उ', 'ू': 'ऊ', 'ृ': 'ऋ', 'ॄ': 'ॠ', 'ॢ': 'ऌ', 'ॣ': 'ॡ', 'े': 'ए',
                  'ै': 'ऐ', 'ो': 'ओ', 'ौ': 'औ'}
    independent_vowels = set('अआइईउऊऋॠऌॡएऐओऔ')

    res = []
    i = 0
    while i < len(text):
        char = text[i]
        if char in independent_vowels:
            res.append(char);
            i += 1
        elif '\u0915' <= char <= '\u0939' or char == 'ळ':
            res.append(char + '्');
            i += 1
            if i < len(text):
                if text[i] == '्':
                    i += 1
                elif text[i] in vowels_map:
                    res.append(vowels_map[text[i]]);
                    i += 1
                elif text[i] not in 'ंःँ':
                    res.append('अ')
            else:
                res.append('अ')
        elif char in 'ंःँ':
            res.append(char);
            i += 1
        else:
            i += 1
    return res


def sanskrit_varna_samyoga(varna_list):
    """वर्णों को जोड़कर शुद्ध रूप बनाना (ग् + आ -> गा)"""
    combined = ""
    vowels_map = {'आ': 'ा', 'इ': 'ि', 'ई': 'ी', 'उ': 'ु', 'ऊ': 'ू', 'ऋ': 'ृ', 'ॠ': 'ॄ', 'ऌ': 'ॢ', 'ॡ': 'ॣ', 'ए': 'े',
                  'ऐ': 'ै', 'ओ': 'ो', 'औ': 'ौ'}
    for varna in varna_list:
        if varna in vowels_map and combined.endswith('्'):
            combined = combined[:-1] + vowels_map[varna]
        elif varna == 'अ' and combined.endswith('्'):
            combined = combined[:-1]
        else:
            combined += varna
    return combined


# --- २. पेज सेटअप ---
st.set_page_config(page_title="इंजन - अष्टाध्यायी-यंत्र", layout="wide")
st.title("⚙️ पाणिनीय इंजन (Processor)")

# --- ३. साइड पैनल (Sidebar) - Examples & Settings ---
with st.sidebar:
    st.header("📚 अभ्यास एवं सेटिंग्स")

    # विद्यार्थियों के लिए उदाहरण (चुट्टू और षित् प्रत्यय)
    example_list = {
        "कस्टम": "",
        "गाधृँ (Dhatu)": "गाधृँ",
        "ष्वुन् (Shit-Krut)": "ष्वुन्",
        "ञ्युट् (Chuttu-Krut)": "ञ्युट्",
        "जस् (Vibhakti)": "जस्",
        "टाप् (Stri-Pratyaya)": "टाप्",
        "ष्यञ् (Shit-Taddhita)": "ष्यञ्"
    }
    selected_example = st.selectbox("प्रमुख उदाहरण चुनें:", options=list(example_list.keys()))

    st.markdown("---")
    source_type_input = st.selectbox(
        "उपदेश का प्रकार (Manual Override):",
        options=[e.value for e in UpadeshaType],
        index=0
    )
    manual_source_type = UpadeshaType(source_type_input)

# --- ४. मुख्य इनपुट प्रोसेसिंग ---
default_input = example_list[selected_example] if selected_example != "कस्टम" else "गाधृँ"
raw_input = st.text_input("संस्कृत उपदेश (धातु/प्रत्यय) लिखें:", value=default_input)

if raw_input:
    input_text = raw_input.strip()
    detected_type = UpadeshaType.auto_detect(input_text)
    source_type = detected_type if detected_type else manual_source_type

    # ऑटो-डिटेक्ट फीडबैक
    if detected_type:
        st.sidebar.success(f"✅ ऑटो-डिटेक्ट: {detected_type.value}")
    else:
        st.sidebar.info(f"ℹ️ मोड: {manual_source_type.value}")

    # १. विच्छेद
    original_varna_list = sanskrit_varna_vichhed(input_text)

    # २. इत्-संज्ञा इंजन (Identifying Indices)
    # इंजन अब लोप के बाद बचे वर्ण और टैग्स देता है
    remaining_varnas, it_tags = ItSanjnaEngine.run_it_sanjna_prakaran(
        original_varna_list.copy(), input_text, source_type
    )

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("१. इत्-संज्ञा (Identification)")
        # विज़ुअल मार्किंग: 'Index' आधारित स्ट्राइक-थ्रू (ज्यादा सटीक)
        marked_display = []
        temp_remaining = remaining_varnas.copy()

        # 'Remaining' लिस्ट का उपयोग करके लोप हुए वर्णों को पहचानना
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

        shuddha_anga = sanskrit_varna_samyoga(remaining_varnas)
        st.success(f"अन्तिम अङ्ग: **{shuddha_anga}**")

    # --- ५. संज्ञा विश्लेषण (Analytic View) ---
    st.markdown("---")
    st.subheader("🔍 ३. संज्ञा विश्लेषण (Sanjna Mapping)")
    analysis = analyze_sanjna(original_varna_list)
    cols = st.columns(len(original_varna_list) if original_varna_list else 1)

    # 'Remaining' को ट्रैक करने के लिए कॉपी
    tracking_remaining = remaining_varnas.copy()
    for idx, item in enumerate(analysis):
        with cols[idx]:
            # चेक करें कि क्या यह वर्ण लोप हो चुका है
            is_it = False
            if item['varna'] in tracking_remaining:
                tracking_remaining.remove(item['varna'])
            else:
                is_it = True

            box_style = "🔴" if is_it else "🔵"
            st.info(f"{box_style} **{item['varna']}**\n\n{', '.join(item['tags']) if item['tags'] else '-'}")

    # --- ६. विधि-सूत्र एवं सारांश ---
    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("🛠️ ४. विधि-सूत्र (Transformation)")
        final_varnas, is_applied = apply_ata_upadhayah_7_2_116(remaining_varnas.copy())
        if is_applied:
            st.success(f"परिवर्तित रूप: **{sanskrit_varna_samyoga(final_varnas)}**")
            st.caption("सूत्र: ७.२.११६ अत उपधायाः")
        else:
            st.write("कोई विधि-सूत्र लागू नहीं हुआ।")

    with col_b:
        st.subheader("📊 प्रक्रिया सारांश")
        steps = [
            {"क्रम": 1, "प्रक्रिया": "उपदेश (Original)", "स्थिति": input_text, "सूत्र": "-"},
            {"क्रम": 2, "प्रक्रिया": "इत्-संज्ञा (Marking)", "स्थिति": " + ".join(marked_display),
             "सूत्र": "१.३.२ - १.३.८"},
            {"क्रम": 3, "प्रक्रिया": "तस्य लोपः (Lopa)", "स्थिति": shuddha_anga, "सूत्र": "१.३.९"}
        ]
        st.table(steps)