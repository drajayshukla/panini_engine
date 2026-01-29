#pages/
import streamlit as st
import pandas as pd
import os
import json

# 'Gold Standard' Modules
from core.phonology import sanskrit_varna_vichhed, sanskrit_varna_samyoga
from logic.it_engine import ItSanjnaEngine
from core.upadesha_registry import UpadeshaType

# --- १. पेज कॉन्फ़िगरेशन एवं स्टाइल ---
st.set_page_config(page_title="Explorer - अष्टाध्यायी-यंत्र", layout="wide", page_icon="🔍")

st.title("🔍 व्याकरण डेटाबेस एक्सप्लोरर")
st.markdown("---")


# --- २. लोप गणना इंजन (Cashed for Performance) ---
@st.cache_data
def calculate_lopa(upadesha, u_type=UpadeshaType.DHATU):
    if not upadesha or upadesha == "०": return "०"
    try:
        v_list = sanskrit_varna_vichhed(upadesha)
        _, is_taddhita = UpadeshaType.auto_detect(upadesha)
        remaining, _ = ItSanjnaEngine.run_it_sanjna_prakaran(
            varna_list=v_list.copy(),
            original_input=upadesha,
            source_type=u_type,
            is_taddhita=is_taddhita
        )
        return sanskrit_varna_samyoga(remaining)
    except:
        return upadesha


# --- ३. डेटा लोडिंग ---
@st.cache_data
def load_json(filename):
    path = f'data/{filename}'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


# --- ४. साइडबार फिल्टर्स (The Diagnostic Matrix) ---
st.sidebar.header("🎯 सूक्ष्म फिल्टर (Filters)")
search_query = st.sidebar.text_input("वैश्विक खोज (Global Search):", placeholder="धातु या अर्थ लिखें...")

# --- ५. टैब आधारित डेटा विज़ुअलाइज़ेशन ---
tabs = st.tabs(["💎 धातु-पाठ", "📦 कृत् प्रत्यय", "🔱 विभक्ति/तिङ्", "📊 सांख्यिकी"])

# --- TAB 1: धातु-पाठ (Enhanced with Filtering) ---
with tabs[0]:
    dhatu_data = load_json('dhatu_master_structured.json')
    if dhatu_data:
        df = pd.DataFrame(dhatu_data)

        # फिल्टर्स का ग्रिड
        f1, f2, f3 = st.columns(3)
        with f1:
            gana_filter = st.multiselect("गण (Gana):", options=df['gana'].unique())
        with f2:
            pada_filter = st.multiselect("पद (Pada):", options=df['pada'].unique())
        with f3:
            it_filter = st.multiselect("इट्-प्रकार (It-type):", options=df['it_type'].unique())

        # डेटा फिल्टरिंग लॉजिक
        if gana_filter: df = df[df['gana'].isin(gana_filter)]
        if pada_filter: df = df[df['pada'].isin(pada_filter)]
        if it_filter: df = df[df['it_type'].isin(it_filter)]
        if search_query:
            df = df[df.apply(lambda row: search_query in str(row.values), axis=1)]

        # १. लाइव गणना चेकबॉक्स
        live_calc = st.checkbox("🔄 लाइव अनुबन्ध-लोप (Shuddha Anga) लागू करें", value=True)
        if live_calc:
            with st.spinner("पाणिनीय गणना जारी..."):
                df['shuddha_anga'] = df['upadesha'].apply(lambda x: calculate_lopa(x, UpadeshaType.DHATU))

        # २. मास्टर डिस्प्ले मैपिंग (सभी संभावित कॉलम्स)
        master_display_map = {
            'kaumudi_index': 'ID',
            'upadesha': 'उपदेश',
            'shuddha_anga': 'शुद्ध अङ्ग',
            'artha_sanskrit': 'अर्थ (Sanskrit)',
            'gana': 'गण',
            'pada': 'पद'
        }

        # ३. उपलब्ध कॉलम्स की पहचान (Dynamic Filtering)
        # यह केवल उन्हीं कॉलम्स को चुनेगा जो DataFrame में वास्तव में मौजूद हैं
        available_cols = {k: v for k, v in master_display_map.items() if k in df.columns}

        # ४. सुरक्षित विज़ुअलाइज़ेशन
        st.dataframe(
            df[list(available_cols.keys())].rename(columns=available_cols),
            use_container_width=True,
            height=500,
            column_config={
                "शुद्ध अङ्ग": st.column_config.TextColumn(
                    "शुद्ध अङ्ग",
                    help="इत्-संज्ञा और लोप के बाद का रूप",
                    width="medium"
                )
            }
        )

        # ५. डाउनलोड बटन (फिल्टर किए गए डेटा के साथ)
        st.download_button(
            label="📥 फिल्टर किया गया डेटा डाउनलोड करें",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="filtered_dhatus.csv",
            mime="text/csv"
        )

# --- TAB 2: कृत् प्रत्यय ---
with tabs[1]:
    krit_data = load_json('krut_pratyayas.json')
    if krit_data:
        df_k = pd.DataFrame(krit_data.get('data', krit_data))
        df_k['shuddha'] = df_k['pratyay'].apply(lambda x: calculate_lopa(x, UpadeshaType.PRATYAYA))
        st.dataframe(df_k, use_container_width=True)

# --- TAB 3: विभक्ति/तिङ् ---
with tabs[2]:
    v_data = load_json('vibhaktipatha.json')
    if v_data:
        c1, c2 = st.columns(2)
        with c1:
            st.info("**सुप् प्रत्यय**")
            st.table(v_data.get('sup_pratyayas', []))
        with c2:
            st.info("**तिङ् प्रत्यय**")
            st.table(v_data.get('tin_pratyayas', []))

# --- TAB 4: सांख्यिकी (Analytics) ---
with tabs[3]:
    if dhatu_data:
        st.subheader("📊 धातुपाठ का सांख्यिकीय विश्लेषण")
        df_stats = pd.DataFrame(dhatu_data)

        col1, col2 = st.columns(2)

        with col1:
            st.write("**गणों के अनुसार वितरण**")
            st.bar_chart(df_stats['gana'].value_counts())

        with col2:
            st.write("**पद के अनुसार वितरण**")

            # वर्शन-सेफ चार्टिंग (Version-Safe Charting)
            data = df_stats['pada'].value_counts()

            # तरीका १: यदि स्ट्रीमलिट नया है (>= 1.34.0)
            if hasattr(st, "pie_chart"):
                st.pie_chart(data)

            # तरीका २: पुराने वर्शन के लिए फॉलबैक (Plotly या Matplotlib)
            else:
                try:
                    import plotly.express as px

                    fig = px.pie(values=data.values, names=data.index)
                    st.plotly_chart(fig, use_container_width=True)
                except ImportError:
                    # यदि Plotly भी नहीं है, तो Matplotlib का उपयोग करें
                    import matplotlib.pyplot as plt

                    fig, ax = plt.subplots()
                    ax.pie(data, labels=data.index, autopct='%1.1f%%')
                    st.pyplot(fig)