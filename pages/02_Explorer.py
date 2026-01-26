import streamlit as st
import json
import pandas as pd
import os

st.set_page_config(page_title="Explorer - अष्टाध्यायी-यंत्र", layout="wide")

st.title("🔍 व्याकरण डेटाबेस एक्सप्लोरर")

tabs = st.tabs(["💎 धातु-पाठ", "📦 कृत् प्रत्यय", "🏷️ तद्धित प्रत्यय"])

def load_json(filename):
    path = f'data/{filename}'
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

with tabs[0]:
    st.subheader("1500+ धातु मास्टर लिस्ट")
    dhatu_data = load_json('dhatu_master_structured.json')
    if dhatu_data:
        df_dhatu = pd.DataFrame(dhatu_data)
        st.dataframe(df_dhatu, use_container_width=True)

with tabs[1]:
    st.subheader("कृत् प्रत्यय सूची")
    krit_data = load_json('krut_pratyayas.json')
    if krit_data:
        # अगर डेटा 'data' की के अंदर है तो:
        list_to_show = krit_data.get('data', krit_data)
        st.table(list_to_show)

with tabs[2]:
    st.subheader("तद्धित प्रत्यय सूची")
    taddhita_data = load_json('taddhita_pratyayas.json')
    if taddhita_data:
        st.json(taddhita_data)