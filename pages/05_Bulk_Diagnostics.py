import streamlit as st
import pandas as pd
import json
import os
from core.phonology import sanskrit_varna_vichhed, sanskrit_varna_samyoga
from core.it_sanjna_engine import ItSanjnaEngine
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

    # की-मैपिंग (Key Mapping)
    # डेटाबेस में 'upadesha' या 'pratyay' अलग-अलग नाम से हो सकते हैं
    search_key = ""
    if data_list:
        sample = data_list[0]
        search_key = 'upadesha' if 'upadesha' in sample else \
            ('pratyay' if 'pratyay' in sample else 'name')

    for entry in data_list:
        original = str(entry.get(search_key, ""))
        if not original: continue

        # १. विच्छेद
        v_list = sanskrit_varna_vichhed(original)

        # २. इत्-संज्ञा (कौमुदी क्रम)
        # तद्धित के लिए विशेष चेक
        is_taddhita = "तद्धित" in str(entry.get('note', '')) or "तद्धित" in str(entry.get('meaning', ''))

        remaining, tags = ItSanjnaEngine.run_it_sanjna_prakaran(
            varna_list=v_list.copy(),
            original_input=original,
            source_type=source_type,
            is_taddhita=is_taddhita
        )

        # ३. अङ्ग निर्माण
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