import streamlit as st
import json
import pandas as pd
import os
import re

# अपने कोर मॉड्यूल्स का इम्पोर्ट
from core.upadesha_registry import UpadeshaType
from core.it_sanjna_engine import ItSanjnaEngine
from core.analyzer import analyze_sanjna
from core.morph_rules import apply_ata_upadhayah_7_2_116


# --- १. व्याकरणिक सहायक (Surgical Helpers) ---

def sanskrit_varna_vichhed(text):
    """पाणिनीय १६-नियम विच्छेद"""
    if not text: return []
    # सफाई: नंबर्स और ZWNJ हटाना
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
    """वर्णों को जोड़कर शुद्ध रूप बनाना (ग् + आ -> गा)"""
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


def apply_bonded_lopa(varna_list):
    """Ach + Anunasika Bonding (१.३.२)"""
    ach_list = set('अआइईउऊऋॠऌॡएऐओऔ')
    temp_list = varna_list.copy()
    indices_to_remove = set()
    for idx, v in enumerate(temp_list):
        if v == 'ँ':
            indices_to_remove.add(idx)
            if idx > 0 and temp_list[idx - 1] in ach_list:
                indices_to_remove.add(idx - 1)
    return [v for i, v in enumerate(temp_list) if i not in indices_to_remove]


# --- २. पेज सेटअप ---
st.set_page_config(page_title="इंजन - अष्टाध्यायी-यंत्र", layout="wide")
st.title("⚙️ पाणिनीय इंजन (Processor)")

with st.sidebar:
    st.header("🎯 इंजन सेटिंग्स")
    source_type_input = st.selectbox("उपदेश का प्रकार (Manual):",
                                     options=[e.value for e in UpadeshaType], index=0)
    manual_source_type = UpadeshaType(source_type_input)

raw_input = st.text_input("संस्कृत उपदेश (धातु/प्रत्यय) लिखें:", value="गाधृँ")

if raw_input:
    input_text = raw_input.strip()
    detected_type = UpadeshaType.auto_detect(input_text)
    source_type = detected_type if detected_type else manual_source_type

    # --- Step 1: विच्छेद ---
    varna_list = sanskrit_varna_vichhed(input_text)

    # --- महत्वपूर्ण: मूल अवस्था की जाँच (Fix for 1.3.3) ---
    # यहाँ हम देख रहे हैं कि क्या वास्तव में मूल शब्द हलन्त था?
    is_originally_halant = varna_list[-1].endswith('्') if varna_list else False

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("१. वर्ण-विच्छेद")
        st.code(" + ".join(varna_list), language=None)

    # --- Step 2: इत्-संज्ञा प्रक्रिया (With Original Halant Check) ---
    # क. बॉन्डिंग लोप (१.३.२)
    bonded_list = apply_bonded_lopa(varna_list)

    # ख. इंजन द्वारा प्रक्रिया
    # हमने इंजन को 'original_input' भेजा है ताकि वह १.३.४ (विभक्ति) भी चेक कर सके
    remaining_varnas, it_tags = ItSanjnaEngine.run_it_sanjna_prakaran(
        bonded_list, input_text, source_type
    )

    # ग. शुद्ध अङ्ग का निर्माण
    shuddha_anga = sanskrit_varna_samyoga(remaining_varnas)

    with col2:
        st.subheader("२. इत्-संज्ञा")
        if it_tags:
            # यहाँ फिल्टर: केवल वही टैग दिखाएं जो जायज हैं
            for tag in it_tags:
                # यदि हलन्त्यम् लगा है पर मूल शब्द हलन्त नहीं था, तो उसे इग्नोर करें
                if "१.३.३ हलन्त्यम्" in tag and not is_originally_halant:
                    continue
                st.markdown(f"🚩 {tag}")
            st.success(f"अन्तिम अङ्ग: **{shuddha_anga}**")
        else:
            st.warning("कोई इत् वर्ण नहीं मिला।")

    # --- बाकी विश्लेषण और सारांश (पूर्ववत) ---
    st.markdown("---")
    st.subheader("🔍 ३. संज्ञा विश्लेषण")
    analysis = analyze_sanjna(varna_list)
    cols = st.columns(len(varna_list) if len(varna_list) > 0 else 1)
    for idx, item in enumerate(analysis):
        with cols[idx]:
            st.info(f"**{item['varna']}**\n\n{', '.join(item['tags']) if item['tags'] else '-'}")

    # ... (विधि-सूत्र और सारांश तालिका का कोड वही रहेगा)

    # --- Step 4: विधि-सूत्र (7.2.116 आदि) ---
    result_varnas = remaining_varnas.copy()
    is_applied = False
    if len(remaining_varnas) >= 2:
        st.markdown("---")
        st.subheader("🛠️ ४. विधि-सूत्र")
        result_varnas, is_applied = apply_ata_upadhayah_7_2_116(remaining_varnas.copy())
        if is_applied:
            final_form = sanskrit_varna_samyoga(result_varnas)
            st.success(f"परिवर्तित रूप: **{final_form}**")
            st.info("सूत्र: ७.२.११६ अत उपधायाः")

    # --- Step 5: सारांश तालिका ---
    st.markdown("---")
    st.subheader("📊 प्रक्रिया सारांश")
    steps = [
        {"क्रम": 1, "प्रक्रिया": "मूल रूप", "स्थिति": input_text, "सूत्र": "-"},
        {"क्रम": 2, "प्रक्रिया": "इत्-लोप (Bonded)", "स्थिति": shuddha_anga, "सूत्र": "1.3.x"},
        {"क्रम": 3, "प्रक्रिया": "वृद्धि/अन्य",
         "स्थिति": sanskrit_varna_samyoga(result_varnas) if is_applied else "यथावत्", "सूत्र": "7.2.116"}
    ]
    st.table(steps)