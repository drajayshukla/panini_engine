import streamlit as st
import json
import pandas as pd
import os
from core.it_sanjna_engine import ItSanjnaEngine
from core.phonology import sanskrit_varna_vichhed
from core.upadesha_registry import UpadeshaType

# पेज सेटअप
st.set_page_config(page_title="Explorer - अष्टाध्यायी-यंत्र", layout="wide")

st.title("🔍 व्याकरण डेटाबेस एक्सप्लोरर")
st.caption("धातु और प्रत्ययों का सजीव अनुबन्ध-लोप विश्लेषण")


# डेटा लोड करने का फंक्शन
@st.cache_data
def load_json(filename):
    path = f'data/{filename}'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def calculate_lopa(upadesha, u_type=UpadeshaType.DHATU):
    """इंजन का उपयोग करके लाइव अनुबन्ध-लोप करना"""
    if not upadesha or upadesha == "०": return "०"
    try:
        varna_list = sanskrit_varna_vichhed(upadesha)
        remaining, _ = ItSanjnaEngine.run_it_sanjna_prakaran(varna_list, upadesha, u_type)
        return "".join(remaining).replace('्', '')
    except:
        return upadesha


tabs = st.tabs(["💎 धातु-पाठ", "📦 कृत् प्रत्यय", "🏷️ तद्धित प्रत्यय", "🔱 विभक्ति/तिङ्"])

# --- TAB 1: धातु-पाठ ---
with tabs[0]:
    st.subheader("1500+ धातु मास्टर लिस्ट")
    dhatu_data = load_json('dhatu_master_structured.json')

    if dhatu_data:
        df_dhatu = pd.DataFrame(dhatu_data)

        col_opts = st.columns([2, 1])
        with col_opts[0]:
            show_lopa = st.checkbox("🔄 लाइव अनुबन्ध-लोप (Anubandha Lopa) दिखाएँ", value=True)

        if show_lopa:
            with st.spinner("पाणिनीय गणना की जा रही है..."):
                df_dhatu['shuddha_anga'] = df_dhatu['upadesha'].apply(lambda x: calculate_lopa(x, UpadeshaType.DHATU))

        # कॉलम रीऑर्डर और रीनेम
        display_cols = {
            'identifier': 'ID',
            'mula_dhatu': 'मूल धातु',
            'upadesha': 'उपदेश',
            'shuddha_anga': 'शुद्ध अङ्ग',
            'gana': 'गण',
            'artha_sanskrit': 'अर्थ (संस्कृत)',
            'tags': 'इत्-टैग्स'
        }

        actual_display = [c for c in display_cols.keys() if c in df_dhatu.columns]

        st.dataframe(
            df_dhatu[actual_display].rename(columns=display_cols),
            use_container_width=True,
            height=600
        )

# --- TAB 2: कृत् प्रत्यय ---
with tabs[1]:
    st.subheader("कृत् प्रत्यय विश्लेषण")
    krit_data = load_json('krut_pratyayas.json')
    if krit_data:
        k_list = krit_data.get('data', krit_data)
        df_krit = pd.DataFrame(k_list)

        if st.checkbox("प्रत्यय का अवशेष (Lopa) गणना करें", key="krit_lopa"):
            df_krit['lopa_form'] = df_krit['pratyay'].apply(lambda x: calculate_lopa(x, UpadeshaType.PRATYAYA))

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