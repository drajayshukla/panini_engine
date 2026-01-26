import streamlit as st
import json
import pandas as pd
import os
import re

# कोर मॉड्यूल्स
from core.upadesha_registry import UpadeshaType
from core.it_sanjna_engine import ItSanjnaEngine
from core.analyzer import analyze_sanjna
from core.morph_rules import apply_ata_upadhayah_7_2_116


# --- १. व्याकरणिक सहायक (Refined Helpers) ---

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
    """वर्णों को जोड़कर शुद्ध रूप बनाना (ग् + आ + ध् -> गाध्)"""
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


def apply_bonded_lopa_fixed(varna_list):
    """
    Surgical Fix: १.३.२ के तहत केवल 'अच् + ँ' का लोप।
    यह सुनिश्चित करता है कि 'हल्' (व्यंजन) सुरक्षित रहे।
    """
    ach_list = set('अआइईउऊऋॠऌॡएऐओऔ')
    temp_list = varna_list.copy()
    indices_to_remove = set()

    for idx, v in enumerate(temp_list):
        if v == 'ँ':
            # १. 'ँ' स्वयं इत् है
            indices_to_remove.add(idx)
            # २. केवल यदि पिछला वर्ण स्वर (Ach) है, तो ही उसे हटाओ
            if idx > 0 and temp_list[idx - 1] in ach_list:
                indices_to_remove.add(idx - 1)
            # यदि पिछला वर्ण हल् (जैसे ध्) है, तो उसे टच मत करो!

    return [v for i, v in enumerate(temp_list) if i not in indices_to_remove]


# --- २. पेज सेटअप ---
st.set_page_config(page_title="इंजन - अष्टाध्यायी-यंत्र", layout="wide")
st.title("⚙️ पाणिनीय इंजन (Processor)")

raw_input = st.text_input("संस्कृत उपदेश लिखें:", value="गाधृँ")

if raw_input:
    input_text = raw_input.strip()
    source_type = UpadeshaType.auto_detect(input_text) or UpadeshaType.DHATU

    # १. विच्छेद
    varna_list = sanskrit_varna_vichhed(input_text)

    # २. रिफाइंड बॉन्डिंग लोप (Fix for Consonant Removal)
    bonded_list = apply_bonded_lopa_fixed(varna_list)

    # ३. इंजन प्रक्रिया (हलन्त्यम् सुरक्षा के साथ)
    remaining_varnas, it_tags = ItSanjnaEngine.run_it_sanjna_prakaran(
        bonded_list, input_text, source_type
    )

    # ४. शुद्ध रूप
    shuddha_anga = sanskrit_varna_samyoga(remaining_varnas)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("१. वर्ण-विच्छेद")
        st.code(" + ".join(varna_list), language=None)

    with col2:
        st.subheader("२. इत्-संज्ञा")
        # अनुनासिक टैग मैन्युअल जोड़ें क्योंकि हमने उसे इंजन से पहले प्रोसेस किया है
        if 'ँ' in varna_list:
            st.markdown("🚩 [१.३.२ उपदेशेऽजनुनासिक इत्](https://ashtadhyayi.com/sutraani/1/3/2)")

        for tag in it_tags:
            # यहाँ सुरक्षा: यदि मूल शब्द हलन्त नहीं था, तो हलन्त्यम् टैग न दिखाएँ
            if "१.३.३ हलन्त्यम्" in tag and not varna_list[-1].endswith('्'):
                continue
            st.markdown(f"🚩 {tag}")

        st.success(f"शुद्ध अङ्ग: **{shuddha_anga}**")

    # --- ३. संज्ञा विश्लेषण ---
    st.markdown("---")
    st.subheader("🔍 ३. संज्ञा विश्लेषण")
    analysis = analyze_sanjna(varna_list)
    cols = st.columns(len(varna_list) if varna_list else 1)
    for idx, item in enumerate(analysis):
        with cols[idx]:
            st.info(f"**{item['varna']}**\n\n{', '.join(item['tags']) if item['tags'] else '-'}")