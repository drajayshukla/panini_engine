import os
from pathlib import Path


def fix_database_path():
    app_path = Path("app.py")

    code = r'''"""
FILE: app.py
PAS-v12.3 (Path Correction)
"""
import streamlit as st
import pandas as pd
import json
import os
from logic.dhatu_processor import DhatuDiagnostic

st.set_page_config(page_title="Panini Engine", layout="wide", page_icon="🕉️")

# --- CSS Styling ---
st.markdown("""
<style>
    .sanskrit { font-family: 'Sanskrit 2003', 'Adobe Devanagari', sans-serif; font-size: 1.1em; }
    .tag-badge { 
        background-color: #e3f2fd; color: #1565c0; padding: 2px 8px; 
        border-radius: 12px; font-size: 0.8em; border: 1px solid #90caf9; margin-right: 4px;
    }
    .match-success { color: #2e7d32; font-weight: bold; }
    .match-fail { color: #c62828; font-weight: bold; }
    .metric-card {
        background-color: #f8f9fa; border-left: 4px solid #673ab7;
        padding: 15px; border-radius: 8px; margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🕉️ Pāṇinian Engine: Master Analytics Dashboard")
st.markdown("---")

# --- Load Data (Robust) ---
@st.cache_data
def load_data():
    # List of probable filenames to check
    possible_paths = [
        "data/dhatu_master_structured.json",  # Lowercase (User provided)
        "data/Dhatu_master_structured.json",  # Uppercase
        "dhatu_master_structured.json"        # Root dir fallback
    ]

    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                st.error(f"Error reading {path}: {e}")
                return []

    return []

raw_db = load_data()

if not raw_db:
    st.error("❌ Database Not Found! Please ensure 'data/dhatu_master_structured.json' exists.")
    # Debug info
    st.text(f"Current Working Directory: {os.getcwd()}")
    st.text(f"Files in 'data' folder: {os.listdir('data') if os.path.exists('data') else 'Data folder missing'}")
    st.stop()

# --- Sidebar Filters ---
st.sidebar.header("🔍 Filter Database")

# 1. Gana Filter
all_ganas = sorted(list(set([item.get('gana', 'Unknown') for item in raw_db])))
selected_gana = st.sidebar.multiselect("Select Gana", all_ganas, default=all_ganas[:1] if all_ganas else None)

# 2. Pada Filter
all_padas = sorted(list(set([item.get('pada', 'Unknown') for item in raw_db])))
selected_pada = st.sidebar.multiselect("Select Pada", all_padas, default=all_padas)

# 3. It-Type Filter
all_it_types = sorted(list(set([item.get('it_type', 'Unknown') for item in raw_db])))
selected_it = st.sidebar.multiselect("Select It-Type", all_it_types, default=all_it_types)

# --- Processing & Logic ---
processed_rows = []

# Apply Filters
filtered_db = [
    item for item in raw_db 
    if (not selected_gana or item.get('gana') in selected_gana) and
       (not selected_pada or item.get('pada') in selected_pada) and
       (not selected_it or item.get('it_type') in selected_it)
]

if filtered_db:
    st.caption(f"Analyzing {len(filtered_db)} roots based on selection...")
    progress_bar = st.progress(0)

    for i, entry in enumerate(filtered_db):
        upadesha = entry.get('upadesha', '')
        # Fallback to 'mula_dhatu' if 'upadesha' is missing, or vice versa
        if not upadesha: upadesha = entry.get('mula_dhatu', '')

        expected_root = entry.get('mula_dhatu', '') 

        # Run Engine
        diag = DhatuDiagnostic(upadesha)
        derived_root = diag.get_final_root()
        derived_voice = diag.pada

        # Comparison Logic
        root_match = derived_root == expected_root

        # Voice Matching
        trad_voice = entry.get('pada', '')
        voice_match = False
        if "Atmanepada" in derived_voice and "आत्मने" in trad_voice: voice_match = True
        elif "Parasmaipada" in derived_voice and "परस्मै" in trad_voice: voice_match = True
        elif "Ubhayapada" in derived_voice and "उभय" in trad_voice: voice_match = True

        # Tags Formatting
        tags_html = "".join([f"<span class='tag-badge'>{t.split('-')[0]}</span>" for t in diag.it_tags])

        processed_rows.append({
            "ID": entry.get('identifier', entry.get('kaumudi_index')),
            "Upadesha (Input)": f"<span class='sanskrit'>{upadesha}</span>",
            "Target (JSON)": f"<span class='sanskrit'>{expected_root}</span>",
            "Engine Output": f"<span class='sanskrit {'match-success' if root_match else 'match-fail'}'>{derived_root}</span>",
            "Status": "✅" if root_match else "❌",
            "Voice (Engine)": f"{'✅' if voice_match else '⚠️'} {derived_voice}",
            "Voice (JSON)": f"<span class='sanskrit'>{trad_voice}</span>",
            "It-Tags": tags_html,
            "Meaning": f"<span class='sanskrit'>{entry.get('artha_sanskrit', '')}</span>"
        })

        if i % 50 == 0: progress_bar.progress(min(i / len(filtered_db), 1.0))

    progress_bar.empty()

    # --- Visualization & Stats ---
    df = pd.DataFrame(processed_rows)

    col1, col2, col3 = st.columns(3)

    total = len(df)
    passed = len(df[df["Status"] == "✅"])
    accuracy = (passed / total) * 100 if total > 0 else 0

    col1.metric("Total Roots", total)
    col2.metric("Accuracy", f"{accuracy:.1f}%")
    col3.metric("Mismatches", total - passed)

    tab1, tab2 = st.tabs(["📊 Data Table", "❌ Mismatches Only"])

    with tab1:
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)

    with tab2:
        mismatches = df[df["Status"] == "❌"]
        if not mismatches.empty:
            st.warning("These roots differ from the JSON expectation.")
            st.write(mismatches.to_html(escape=False, index=False), unsafe_allow_html=True)
        else:
            st.success("No mismatches found! 🎉")

else:
    st.info("No data matches your filters.")
'''
    app_path.write_text(code, encoding='utf-8')
    print("✅ App Repaired: Now searching for 'data/dhatu_master_structured.json' correctly.")


if __name__ == "__main__":
    fix_database_path()