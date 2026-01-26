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
    """पाणिनीय १६-नियम विच्छेद - Granular Style"""
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
    """वर्णों को जोड़कर शुद्ध रूप बनाना (भ् + ऊ -> भू)"""
    vowels_map = {'आ': 'ा', 'इ': 'ि', 'ई': 'ी', 'उ': 'ु', 'ऊ': 'ू', 'ऋ': 'ृ', 'ॠ': 'ॄ', 'ऌ': 'ॢ', 'ॡ': 'ॡ', 'ए': 'े',
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


def apply_it_logic_processor(varna_list, input_text, source_type):
    """
    इत्-संज्ञा का 'Clean' लॉजिक:
    १. 'ँ' मिले तो अच् के साथ बॉन्डिंग लोप।
    २. 'हलन्त्यम्' की सुरक्षा (केवल मूल हलन्त पर)।
    """
    ach_list = set('अआइईउऊऋॠऌॡएऐओऔ')
    # मूल स्थिति की जाँच
    is_originally_halant = varna_list[-1].endswith('्') if varna_list else False

    # क. बॉन्डिंग लोप (Bonded Lopa)
    it_tags = []
    indices_to_remove = set()
    for idx, v in enumerate(varna_list):
        if v == 'ँ':
            indices_to_remove.add(idx)
            it_tags.append("[१.३.२ उपदेशेऽजनुनासिक इत्](https://ashtadhyayi.com/sutraani/1/3/2)")
            if idx > 0 and varna_list[idx - 1] in ach_list:
                indices_to_remove.add(idx - 1)

    bonded_list = [v for i, v in enumerate(varna_list) if i not in indices_to_remove]

    # ख. मुख्य इंजन प्रक्रिया
    remaining_varnas, engine_tags = ItSanjnaEngine.run_it_sanjna_prakaran(
        bonded_list, input_text, source_type
    )

    # ग. हलन्त्यम् फिल्टर (Clinical Filter)
    valid_engine_tags = []
    for tag in engine_tags:
        if "१.३.३ हलन्त्यम्" in tag and not is_originally_halant:
            continue
        valid_engine_tags.append(tag)

    return remaining_varnas, list(set(it_tags + valid_engine_tags))


# --- २. पेज सेटअप ---
st.set_page_config(page_title="इंजन - अष्टाध्यायी-यंत्र", layout="wide")
st.title("⚙️ पाणिनीय इंजन (Processor)")

with st.sidebar:
    st.header("🎯 इंजन सेटिंग्स")
    source_type_input = st.selectbox("उपदेश का प्रकार (Manual):",
                                     options=[e.value for e in UpadeshaType], index=0)
    source_type = UpadeshaType(source_type_input)

raw_input = st.text_input("संस्कृत उपदेश (धातु/प्रत्यय) लिखें:", value="गाधृँ")

if raw_input:
    input_text = raw_input.strip()
    varna_list = sanskrit_varna_vichhed(input_text)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("१. वर्ण-विच्छेद")
        st.code(" + ".join(varna_list), language=None)

    # --- Step 2: रिफाइंड इत्-संज्ञा प्रक्रिया ---
    remaining_varnas, it_tags = apply_it_logic_processor(varna_list, input_text, source_type)
    shuddha_anga = sanskrit_varna_samyoga(remaining_varnas)

    with col2:
        st.subheader("२. इत्-संज्ञा")
        if it_tags:
            for tag in it_tags: st.markdown(f"🚩 {tag}")
            st.success(f"शुद्ध अङ्ग: **{shuddha_anga}**")
        else:
            st.warning("कोई इत् वर्ण नहीं मिला।")

    # --- Step 3: संज्ञा विश्लेषण ---
    st.markdown("---")
    st.subheader("🔍 ३. संज्ञा विश्लेषण")
    analysis = analyze_sanjna(varna_list)
    cols = st.columns(len(varna_list) if varna_list else 1)
    for idx, item in enumerate(analysis):
        with cols[idx]:
            st.info(f"**{item['varna']}**\n\n{', '.join(item['tags']) if item['tags'] else '-'}")

    # --- Step 4: विधि-सूत्र (7.2.116 आदि) ---
    result_varnas = remaining_varnas.copy()
    is_applied = False
    if len(remaining_varnas) >= 2:
        st.markdown("---")
        st.subheader("🛠️ ४. विधि-सूत्र")
        result_varnas, is_applied = apply_ata_upadhayah_7_2_116(remaining_varnas.copy())
        if is_applied:
            final_form = sanskrit_varna_samyoga(result_varnas)
            st.success(f"परिवर्तित रूप: **{final_form}** (७.२.११६ अत उपधायाः)")

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