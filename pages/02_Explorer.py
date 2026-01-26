import streamlit as st
import json
import pandas as pd
import os
import re  # नियम ६, ७ के लिए अनिवार्य

# अपने कोर मॉड्यूल्स का इम्पोर्ट
from core.it_sanjna_engine import ItSanjnaEngine
from core.upadesha_registry import UpadeshaType

# --- १. पेज कॉन्फ़िगरेशन ---
st.set_page_config(page_title="Explorer - अष्टाध्यायी-यंत्र", layout="wide")

st.title("🔍 व्याकरण डेटाबेस एक्सप्लोरर")
st.caption("पाणिनीय 16-नियम विच्छेद और सजीव अनुबन्ध-लोप (Anubandha Lopa) विश्लेषण")


# --- २. वर्ण विच्छेद (Sanskrit Varna Vichhed - 16 Rules) ---

def sanskrit_varna_vichhed(text):
    """
    पाणिनीय अष्टाध्यायी के 16 नियमों पर आधारित पूर्ण शुद्ध कोड।
    'लो, ली, लू, लाँ' जैसी समस्याओं का स्थायी समाधान।
    """
    if not text:
        return []

    # नियम 16: ॐ का विशिष्ट विच्छेद
    if text == "ॐ":
        return ["अ", "उ", "म्"]

    # नियम 3, 12, 13: विशिष्ट संयुक्ताक्षर और अवग्रह
    text = text.replace('क्ष', 'क्‌ष').replace('त्र', 'त्‌र').replace('ज्ञ', 'ज्‌ञ').replace('श्र', 'श्‌र').replace('ऽ',
                                                                                                                    'अ')

    # नियम 6, 7: पञ्चम वर्ण और अनुस्वार नियम
    text = re.sub(r'ं(?=[कखगघ])', 'ङ्', text)
    text = re.sub(r'ं(?=[चछजझ])', 'ञ्', text)
    text = re.sub(r'ं(?=[टठडढ])', 'ण्', text)
    text = re.sub(r'ं(?=[तथदध])', 'न्', text)
    text = re.sub(r'ं(?=[पफबभ])', 'म्', text)

    # नियम 16 (Standard): अंत में आने वाला अनुस्वार 'म्' में बदलना
    if text.endswith('ं'):
        text = text[:-1] + 'म्'

    vowels_map = {
        'ा': 'आ', 'ि': 'इ', 'ी': 'ई', 'ु': 'उ', 'ू': 'ऊ',
        'ृ': 'ऋ', 'ॄ': 'ॠ', 'ॢ': 'ऌ', 'ॣ': 'ॡ',
        'े': 'ए', 'ै': 'ऐ', 'ो': 'ओ', 'ौ': 'औ'
    }
    independent_vowels = set('अआइईउऊऋॠऌॡएऐओऔ')

    res = []
    i = 0
    while i < len(text):
        char = text[i]

        # स्वतंत्र स्वर प्रबंधन
        if char in independent_vowels:
            res.append(char)
            i += 1
            if i < len(text) and text[i] == '३':
                res[-1] += '३'
                i += 1
            while i < len(text) and text[i] in 'ंःँ':
                res.append(text[i])
                i += 1
            continue

        # व्यंजन प्रबंधन
        elif '\u0915' <= char <= '\u0939' or char == 'ळ':
            res.append(char + '्')
            i += 1
            found_vowel = False
            if i < len(text):
                if text[i] == '्':
                    i += 1
                    found_vowel = True
                elif text[i] in vowels_map:
                    res.append(vowels_map[text[i]])
                    i += 1
                    found_vowel = True
                elif text[i] in 'ंःँ':
                    res.append('अ')
                    found_vowel = True

            if not found_vowel:
                res.append('अ')

            while i < len(text) and text[i] in 'ंःँ':
                res.append(text[i])
                i += 1
            continue

        elif char in 'ᳲᳳ':
            res.append(char)
            i += 1
        else:
            i += 1
    return res


# --- ३. वर्ण संयोग (Varna Samyoga - Fix for 'भऊ' vs 'भू') ---

def sanskrit_varna_samyoga(varna_list):
    """
    विच्छेदित वर्णों को वापस जोड़ना (['भ्', 'ऊ'] -> 'भू')।
    """
    vowels_map = {
        'आ': 'ा', 'इ': 'ि', 'ई': 'ी', 'उ': 'ु', 'ऊ': 'ू',
        'ऋ': 'ृ', 'ॠ': 'ॄ', 'ऌ': 'ॢ', 'ॡ': 'ॣ',
        'ए': 'े', 'ऐ': 'ै', 'ओ': 'ो', 'औ': 'ौ'
    }
    combined = ""
    for varna in varna_list:
        if varna in vowels_map and combined.endswith('्'):
            combined = combined[:-1] + vowels_map[varna]
        elif varna == 'अ' and combined.endswith('्'):
            combined = combined[:-1]
        else:
            combined += varna
    return combined


# --- ४. अनुबन्ध लोप गणना इंजन (Lopa Calculation Engine) ---

def calculate_lopa(upadesha, u_type=UpadeshaType.DHATU):
    """लाइव लोप की गणना: विच्छेद -> इंजन प्रक्रिया -> संयोग"""
    if not upadesha or upadesha == "०": return "०"
    try:
        # क. विच्छेद
        v_list = sanskrit_varna_vichhed(upadesha)
        # ख. इंजन द्वारा इत्-संज्ञा हटाना
        remaining, _ = ItSanjnaEngine.run_it_sanjna_prakaran(v_list, upadesha, u_type)
        # ग. संयोग (शुद्ध रूप निर्माण)
        return sanskrit_varna_samyoga(remaining)
    except Exception as e:
        return upadesha


# --- ५. डेटा लोडिंग और UI ---

@st.cache_data
def load_json(filename):
    path = f'data/{filename}'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


tabs = st.tabs(["💎 धातु-पाठ", "📦 कृत् प्रत्यय", "🏷️ तद्धित प्रत्यय", "🔱 विभक्ति/तिङ्"])

# --- TAB 1: धातु-पाठ ---
with tabs[0]:
    st.subheader("1500+ धातु मास्टर लिस्ट (Live It-Lopa)")
    dhatu_data = load_json('dhatu_master_structured.json')

    if dhatu_data:
        df_dhatu = pd.DataFrame(dhatu_data)

        if st.checkbox("🔄 लाइव अनुबन्ध-लोप (Anubandha Lopa) दिखाएँ", value=True):
            with st.spinner("पाणिनीय गणना की जा रही है..."):
                df_dhatu['shuddha_anga'] = df_dhatu['upadesha'].apply(lambda x: calculate_lopa(x, UpadeshaType.DHATU))

        display_cols = {
            'identifier': 'ID',
            'mula_dhatu': 'मूल धातु',
            'upadesha': 'उपदेश',
            'shuddha_anga': 'शुद्ध अङ्ग',
            'gana': 'गण',
            'artha_sanskrit': 'अर्थ (संस्कृत)'
        }

        # केवल मौजूद कॉलम दिखाएँ
        cols_to_show = [c for c in display_cols.keys() if c in df_dhatu.columns]
        st.dataframe(df_dhatu[cols_to_show].rename(columns=display_cols), use_container_width=True, height=600)

# --- TAB 2: कृत् प्रत्यय ---
with tabs[1]:
    st.subheader("कृत् प्रत्यय विश्लेषण")
    krit_data = load_json('krut_pratyayas.json')
    if krit_data:
        df_krit = pd.DataFrame(krit_data.get('data', krit_data))
        if st.checkbox("प्रत्यय का अवशेष (Lopa) गणना करें", key="krit_lopa"):
            df_krit['shuddha_pratyaya'] = df_krit['pratyay'].apply(lambda x: calculate_lopa(x, UpadeshaType.PRATYAYA))
        st.dataframe(df_krit, use_container_width=True)

# --- TAB 3: तद्धित प्रत्यय ---
with tabs[2]:
    st.subheader("तद्धित प्रत्यय सूची")
    taddhita_data = load_json('taddhita_pratyayas.json')
    if taddhita_data:
        st.json(taddhita_data)

# --- TAB 4: विभक्ति/तिङ् ---
with tabs[3]:
    st.subheader("विभक्ति और तिङ् प्रत्यय")
    v_data = load_json('vibhakti_master.json')
    if v_data:
        c1, c2 = st.columns(2)
        with c1:
            st.write("**सुप् प्रत्यय (Declension)**")
            st.dataframe(pd.DataFrame(v_data['sup_pratyayas']))
        with c2:
            st.write("**तिङ् प्रत्यय (Conjugation)**")
            st.dataframe(pd.DataFrame(v_data['tin_pratyayas']))