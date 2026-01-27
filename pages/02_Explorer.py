import streamlit as st
import json
import pandas as pd
import os

# 'Gold Standard' Modules
from core.phonology import sanskrit_varna_vichhed, sanskrit_varna_samyoga
from core.it_sanjna_engine import ItSanjnaEngine
from core.upadesha_registry import UpadeshaType

# --- १. पेज कॉन्फ़िगरेशन ---
st.set_page_config(page_title="Explorer - अष्टाध्यायी-यंत्र", layout="wide")

st.title("🔍 व्याकरण डेटाबेस एक्सप्लोरर")
st.caption("पाणिनीय शुद्धिकरण: एकीकृत Engine आधारित अनुबन्ध-लोप विश्लेषण")


# --- २. लोप गणना इंजन (Simplified & Integrated) ---
def calculate_lopa(upadesha, u_type=UpadeshaType.DHATU):
    """
    लाइव लोप गणना:
    विच्छेद -> इंजन (सभी इत्-संज्ञा सूत्र) -> संयोग
    """
    if not upadesha or upadesha == "०":
        return "०"

    try:
        # क. विच्छेद (Gold Standard)
        v_list = sanskrit_varna_vichhed(upadesha)

        # ख. तद्धित फ्लैग डिटेक्शन (Sutra 1.3.8 के लिए आवश्यक)
        _, is_taddhita = UpadeshaType.auto_detect(upadesha)

        # ग. एकीकृत इंजन प्रक्रिया (१.३.२ से १.३.८ तक के सभी नियम यहीं समाहित हैं)
        # अब मैन्युअल apply_bonded_lopa की आवश्यकता नहीं है
        remaining, _ = ItSanjnaEngine.run_it_sanjna_prakaran(
            varna_list=v_list.copy(),
            original_input=upadesha,
            source_type=u_type,
            is_taddhita=is_taddhita
        )

        # घ. संयोग (शुद्ध रूप निर्माण)
        return sanskrit_varna_samyoga(remaining)

    except Exception:
        return upadesha


# --- ३. डेटा लोडिंग ---
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
    st.subheader("1500+ धातु मास्टर लिस्ट")
    dhatu_data = load_json('dhatu_master_structured.json')
    if dhatu_data:
        df_dhatu = pd.DataFrame(dhatu_data)
        if st.checkbox("🔄 लाइव अनुबन्ध-लोप दिखाएँ", value=True, key="dhatu_live"):
            with st.spinner("पाणिनीय गणना जारी..."):
                df_dhatu['shuddha_anga'] = df_dhatu['upadesha'].apply(
                    lambda x: calculate_lopa(x, UpadeshaType.DHATU)
                )

        display_cols = {
            'identifier': 'ID',
            'mula_dhatu': 'मूल धातु',
            'upadesha': 'उपदेश',
            'shuddha_anga': 'शुद्ध अङ्ग',
            'gana': 'गण',
            'artha_sanskrit': 'अर्थ'
        }
        actual_cols = [c for c in display_cols.keys() if c in df_dhatu.columns]
        st.dataframe(df_dhatu[actual_cols].rename(columns=display_cols), use_container_width=True, height=600)

# --- TAB 2: कृत् प्रत्यय ---
with tabs[1]:
    st.subheader("कृत् प्रत्यय विश्लेषण")
    krit_data = load_json('krut_pratyayas.json')
    if krit_data:
        df_krit = pd.DataFrame(krit_data.get('data', krit_data))
        if st.checkbox("प्रत्यय का अवशेष (Lopa) गणना करें", key="krit_lopa"):
            df_krit['shuddha_pratyaya'] = df_krit['pratyay'].apply(
                lambda x: calculate_lopa(x, UpadeshaType.PRATYAYA)
            )
        st.dataframe(df_krit, use_container_width=True)

# --- TAB 3: तद्धित प्रत्यय ---
with tabs[2]:
    st.subheader("तद्धित प्रत्यय सूची")
    taddhita_data = load_json('taddhita_master_data.json')
    if taddhita_data:
        st.json(taddhita_data)

# --- TAB 4: विभक्ति/तिङ् ---
with tabs[3]:
    st.subheader("विभक्ति और तिङ् प्रत्यय")
    v_data = load_json('vibhaktipatha.json')
    if v_data:
        c1, c2 = st.columns(2)
        with c1:
            st.write("**सुप् प्रत्यय (Declension)**")
            st.dataframe(pd.DataFrame(v_data.get('sup_pratyayas', [])))
        with c2:
            st.write("**तिङ् प्रत्यय (Conjugation)**")
            st.dataframe(pd.DataFrame(v_data.get('tin_pratyayas', [])))