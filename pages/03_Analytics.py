import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(page_title="Analytics - अष्टाध्यायी-यंत्र", layout="wide")

st.title("📊 धातु-पाठ विश्लेषणात्मक डैशबोर्ड")

# डेटा लोड करना
@st.cache_data
def load_data():
    with open('data/dhatu_master_structured.json', 'r', encoding='utf-8') as f:
        return pd.DataFrame(json.load(f))

df = load_data()

# --- मुख्य सांख्यिकी (Metrics) ---
m1, m2, m3 = st.columns(3)
m1.metric("कुल धातुएं", len(df))
m2.metric("अद्वितीय गण", df['gana'].nunique())
m3.metric("सकर्मक अनुपात", f"{len(df[df['karmaka']=='सकर्मक'])/len(df)*100:.1f}%")

st.markdown("---")

# --- विज़ुअलाइज़ेशन (Old Repo Logic + New Data) ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("🎡 गणों का वितरण")
    # पुरानी रिपॉजिटरी का Pie Chart लॉजिक
    fig_gana = px.pie(df, names='gana', hole=0.4,
                      color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(fig_gana, use_container_width=True)

with c2:
    st.subheader("⚖️ पद (Voice) विश्लेषण")
    # पुरानी रिपॉजिटरी का Bar Chart लॉजिक
    fig_pada = px.bar(df['pada'].value_counts(),
                      color_discrete_sequence=['#636EFA'])
    st.plotly_chart(fig_pada, use_container_width=True)