#pages/05_Bulk_Diagnostics.py
import streamlit as st
import pandas as pd
import json
import os
from core.phonology import sanskrit_varna_vichhed, sanskrit_varna_samyoga
from logic.it_engine import ItSanjnaEngine
from core.upadesha_registry import UpadeshaType

# --- १. पेज सेटअप ---
st.set_page_config(page_title="Bulk Diagnostics - अष्टाध्यायी-यंत्र", layout="wide")
st.title("📊 वृहद् व्याकरणिक परीक्षण (Bulk Diagnostics)")
st.caption("२०००+ उपदेशों का एक साथ इत्-संज्ञा एवं अङ्ग-प्राप्ति विश्लेषण")


# --- २. डेटा लोडर ---
@st.cache_data
def load_all_datasets():
    files = {
        "Dhatupatha": "dhatu_master_structured.json",
        "Krit Pratyaya": "krit_pratyayas.json",
        "Taddhita Pratyaya": "taddhita_master_data.json",
        "Vibhakti": "vibhaktipatha.json"
    }
    loaded = {}
    for label, fname in files.items():
        path = f'data/{fname}'
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                loaded[label] = json.load(f)
    return loaded


all_datasets = load_all_datasets()


# --- ३. विश्लेषण इंजन (Batch Processor) ---
def run_bulk_test(data_list, source_type):
    report = []

    # १. एम्पटी चेक (Clinical Safety Check)
    if not data_list:
        st.warning("चुना गया डेटासेट खाली है।")
        return pd.DataFrame()

    # २. अभ्यास माला (Nested Structure) का विशेष हैंडलिंग
    actual_list = []
    if isinstance(data_list, dict) and 'categories' in data_list:
        # सभी कैटेगरीज के उदाहरणों को एक समतल सूची (Flat List) में लाना
        for cat in data_list['categories']:
            actual_list.extend(cat['examples'])
    elif isinstance(data_list, list):
        actual_list = data_list
    else:
        st.error("डेटा स्ट्रक्चर अज्ञात है।")
        return pd.DataFrame()

    # ३. की-मैपिंग (Key Mapping)
    if not actual_list:
        return pd.DataFrame()

    sample = actual_list[0]
    search_key = 'input' if 'input' in sample else \
        ('upadesha' if 'upadesha' in sample else \
             ('pratyay' if 'pratyay' in sample else 'name'))

    # ४. प्रोसेसिंग लूप
    for entry in actual_list:
        original = str(entry.get(search_key, ""))
        if not original: continue

        v_list = sanskrit_varna_vichhed(original)

        # तद्धित ऑटो-डिटेक्शन (Critical for 1.3.8)
        is_taddhita = "तद्धित" in str(entry.get('note', '')) or \
                      "तद्धित" in str(entry.get('meaning', ''))

        remaining, tags = ItSanjnaEngine.run_it_sanjna_prakaran(
            varna_list=v_list.copy(),
            original_input=original,
            source_type=source_type,
            is_taddhita=is_taddhita
        )

        final_anga = sanskrit_varna_samyoga(remaining)

        report.append({
            "Original (उपदेश)": original,
            "Type": source_type.value,
            "Anga (अङ्ग)": final_anga,
            "Sutras Applied": ", ".join(tags) if tags else "None",
            "Meaning": entry.get('meaning', entry.get('artha_sanskrit', '-'))
        })

    return pd.DataFrame(report)


# --- ४. यूआई कंट्रोल्स (UI Controls) ---
if not all_datasets:
    st.error("डेटा फोल्डर में कोई JSON फाइल नहीं मिली।")
else:
    db_choice = st.selectbox("परीक्षण के लिए डेटाबेस चुनें:", options=list(all_datasets.keys()))

    # टाइप मैपिंग
    type_map = {
        "Dhatupatha": UpadeshaType.DHATU,
        "Krit Pratyaya": UpadeshaType.PRATYAYA,
        "Taddhita Pratyaya": UpadeshaType.PRATYAYA,
        "Vibhakti": UpadeshaType.VIBHAKTI
    }

    if st.button(f"🚀 {db_choice} का परीक्षण शुरू करें"):
        with st.spinner(f"{db_choice} के उदाहरणों को स्कैन किया जा रहा है..."):
            df_report = run_bulk_test(all_datasets[db_choice], type_map[db_choice])

            st.success(f"कुल {len(df_report)} उदाहरणों का परीक्षण सफल रहा!")

            # ५. मेट्रिक्स और फिल्टर्स
            st.subheader("📈 परीक्षण मेट्रिक्स")
            c1, c2, c3 = st.columns(3)
            c1.metric("कुल उदाहरण", len(df_report))
            # कितने शब्दों में इत्-संज्ञा हुई
            it_count = len(df_report[df_report['Sutras Applied'] != "None"])
            c2.metric("इत्-संज्ञा वाले शब्द", it_count)
            c3.metric("अपरिवर्तित शब्द", len(df_report) - it_count)

            # ६. परिणाम तालिका (Interactive Table)
            st.markdown("### 📋 विस्तृत रिपोर्ट")
            st.dataframe(df_report, use_container_width=True)

            # ७. डाउनलोड बटन (Excel/CSV Export)
            csv = df_report.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 परीक्षण रिपोर्ट डाउनलोड करें (CSV)",
                data=csv,
                file_name=f"Panini_Bulk_Test_{db_choice}.csv",
                mime='text/csv',
            )