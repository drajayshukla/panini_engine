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
                    res.append(vowels_map[text[i]]); i += 1
                elif text[i] not in 'ंःँ':
                    res.append('अ')
            else:
                res.append('अ')
        elif char in 'ंःँ':
            res.append(char); i += 1
        else:
            i += 1
    return res


def sanskrit_varna_samyoga(varna_list):
    """वर्णों को जोड़कर शुद्ध रूप बनाना (ग् + आ -> गा)"""
    vowels_map = {'आ': 'ा', 'इ': 'ि', 'ई': 'ी', 'उ': 'ु', 'ऊ': 'ू', 'ऋ': 'ृ', 'ॠ': 'ॄ', 'ऌ': 'ॢ', 'ॡ': 'ॣ', 'ए': 'े',
                  'ऐ': 'ै', 'ओ': 'ो', 'औ': 'ौ'}
    combined = ""
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

raw_input = st.text_input("संस्कृत उपदेश (धातु/प्रत्यय) लिखें:", value="गाधृँ")

if raw_input:
    input_text = raw_input.strip()
    source_type = UpadeshaType.auto_detect(input_text) or UpadeshaType.DHATU

    # १. विच्छेद (Original Form)
    original_varna_list = sanskrit_varna_vichhed(input_text)

    # २. इत्-संज्ञा (Identification)
    # इंजन अब 'Marking' के बाद 'तस्य लोपः' करके रिज़ल्ट देता है
    remaining_varnas, it_tags = ItSanjnaEngine.run_it_sanjna_prakaran(
        original_varna_list.copy(), input_text, source_type
    )

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("१. इत्-संज्ञा (Identification)")
        # विज़ुअल मार्किंग: इत् वर्णों को Strikethrough (~~) दिखाना
        marked_display = []
        # 'remaining' में जो नहीं है, वह 'इत्' है
        temp_remaining = remaining_varnas.copy()

        for v in original_varna_list:
            if v in temp_remaining:
                marked_display.append(v)
                temp_remaining.remove(v)
            else:
                marked_display.append(f"~~{v}~~")  # इत् वर्ण पर काट (Lopa Mark)

        st.markdown(f"**मार्क किया गया रूप:** {' + '.join(marked_display)}")

        if it_tags:
            for tag in it_tags: st.markdown(f"🚩 {tag}")
        else:
            st.info("कोई इत्-संज्ञा नहीं हुई।")

    with col2:
        st.subheader("२. तस्य लोपः (Execution)")
        st.markdown(f"**लोप के बाद (१.३.९):** {' + '.join(remaining_varnas)}")

        # शुद्ध अङ्ग का निर्माण
        shuddha_anga = sanskrit_varna_samyoga(remaining_varnas)
        st.success(f"अन्तिम अङ्ग: **{shuddha_anga}**")

    # --- ३. संज्ञा विश्लेषण (Analytic View) ---
    st.markdown("---")
    st.subheader("🔍 ३. संज्ञा विश्लेषण (Sanjna Mapping)")
    analysis = analyze_sanjna(original_varna_list)
    cols = st.columns(len(original_varna_list) if original_varna_list else 1)
    for idx, item in enumerate(analysis):
        with cols[idx]:
            # यदि वर्ण 'इत्' मार्क किया गया है तो उसका बैकग्राउंड अलग दिखाएं
            is_it = item['varna'] not in remaining_varnas
            box_style = "🔴" if is_it else "🔵"
            st.info(f"{box_style} **{item['varna']}**\n\n{', '.join(item['tags']) if item['tags'] else '-'}")

    # --- ४. विधि-सूत्र (Transformation) ---
    st.markdown("---")
    st.subheader("🛠️ ४. विधि-सूत्र (Transformation)")
    final_varnas, is_applied = apply_ata_upadhayah_7_2_116(remaining_varnas.copy())

    c1, c2 = st.columns(2)
    with c1:
        if is_applied:
            st.success(f"परिवर्तित रूप: **{sanskrit_varna_samyoga(final_varnas)}**")
            st.caption("सूत्र: ७.२.११६ अत उपधायाः")
        else:
            st.write("कोई विधि-सूत्र लागू नहीं हुआ।")

    # --- ५. प्रक्रिया सारांश (Final Report) ---
    st.markdown("---")
    st.subheader("📊 प्रक्रिया सारांश (Workflow)")
    steps = [
        {"क्रम": 1, "प्रक्रिया": "उपदेश (Original)", "स्थिति": input_text, "सूत्र": "-"},
        {"क्रम": 2, "प्रक्रिया": "इत्-संज्ञा (Identification)", "स्थिति": " + ".join(marked_display),
         "सूत्र": "१.३.२ - १.३.८"},
        {"क्रम": 3, "प्रक्रिया": "तस्य लोपः (Lopa)", "स्थिति": shuddha_anga, "सूत्र": "१.३.९"},
    ]
    if is_applied:
        steps.append({"क्रम": 4, "प्रक्रिया": "अङ्ग-कार्य (Morphology)", "स्थिति": sanskrit_varna_samyoga(final_varnas),
                      "सूत्र": "७.२.११६"})

    st.table(steps)