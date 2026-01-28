import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

# --- १. पेज कॉन्फ़िगरेशन ---
st.set_page_config(page_title="Analytics - अष्टाध्यायी-यंत्र", layout="wide", page_icon="📊")

st.title("📊 धातु-पाठ विश्लेषणात्मक डैशबोर्ड")
st.caption("Clinical Diagnostics: डेटा अखंडता और सांख्यिकीय विश्लेषण")


# --- २. रोबस्ट डेटा लोडिंग (Diagnostic Layer) ---
@st.cache_data
def load_data():
    file_path = 'data/dhatu_master_structured.json'

    # फाइल की मौजूदगी की जाँच
    if not os.path.exists(file_path):
        return pd.DataFrame()

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            df = pd.DataFrame(data)

            # डेटा सैनिटाइजेशन (Data Sanitization)
            # स्ट्रिंग्स से अनचाहे स्पेस हटाना ताकि चार्ट्स में 'Duplicates' न आएं
            string_cols = df.select_dtypes(include=['object']).columns
            for col in string_cols:
                df[col] = df[col].astype(str).str.strip()

            return df
    except (json.JSONDecodeError, KeyError, Exception) as e:
        st.error(f"डेटा लोड करने में त्रुटि: {e}")
        return pd.DataFrame()


df_raw = load_data()

# --- ३. 'Empty State' हैंडलिंग ---
if df_raw.empty:
    st.warning("⚠️ डेटा उपलब्ध नहीं है या फाइल 'data/dhatu_master_structured.json' दूषित है।")
    st.stop()

# --- ४. साइडबार फिल्टर्स (The Surgical Filters) ---
st.sidebar.header("🎯 डेटा फ़िल्टरिंग")
selected_gana = st.sidebar.multiselect(
    "गण (Gana) चुनें:",
    options=sorted(df_raw['gana'].unique()),
    default=sorted(df_raw['gana'].unique())
)

# फिल्टर लागू करना
df = df_raw[df_raw['gana'].isin(selected_gana)]

# --- ५. मुख्य सांख्यिकी (Metrics Matrix) ---
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("कुल धातुएं", len(df))
with m2:
    st.metric("अद्वितीय गण", df['gana'].nunique())
with m3:
    karmaka_ratio = (len(df[df['karmaka'] == 'सकर्मक']) / len(df) * 100) if len(df) > 0 else 0
    st.metric("सकर्मक अनुपात", f"{karmaka_ratio:.1f}%")
with m4:
    # नई सांख्यिकी: उभयपदी धातुओं की संख्या
    ubhayapadi = len(df[df['pada'] == 'उभयपदी'])
    st.metric("उभयपदी धातु", ubhayapadi)

st.markdown("---")

# --- ६. विज़ुअलाइज़ेशन (Advanced Visualization) ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("🎡 गणों का वितरण (Distribution)")
    if not df.empty:
        fig_gana = px.pie(
            df,
            names='gana',
            hole=0.4,
            title="धातु वितरण प्रति गण",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_gana.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_gana, use_container_width=True)
    else:
        st.info("चयनित गणों के लिए डेटा उपलब्ध नहीं है।")

with c2:
    st.subheader("⚖️ पद (Voice) विश्लेषण")
    if not df.empty:
        # डेटा को एग्रीगेट करना
        pada_counts = df['pada'].value_counts().reset_index()
        pada_counts.columns = ['pada', 'count']

        fig_pada = px.bar(
            pada_counts,
            x='pada',
            y='count',
            color='pada',
            text='count',
            labels={'pada': 'पद प्रकार', 'count': 'संख्या'},
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_pada.update_layout(showlegend=False)
        st.plotly_chart(fig_pada, use_container_width=True)

# --- ७. डेटा ऑडिट टेबल (Deep Dive) ---
st.markdown("---")
with st.expander("🔍 विस्तृत डेटा ऑडिट (Raw Data View)"):
    st.dataframe(df, use_container_width=True)