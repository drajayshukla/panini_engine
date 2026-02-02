import os
from pathlib import Path


def integrate_master_data():
    app_path = Path("app.py")

    code = r'''"""
FILE: app.py
PAS-v12.1 (Master Data Integration)
"""
import streamlit as st
import pandas as pd
import json
from logic.dhatu_processor import DhatuDiagnostic

st.set_page_config(page_title="Panini Engine", layout="wide", page_icon="🕉️")

# --- CSS Styling ---
st.markdown("""
<style>
    .sanskrit { font-family: 'Sanskrit 2003', 'Adobe Devanagari', sans-serif; font-size: 1.15em; }
    .tag-badge { 
        background-color: #e3f2fd; 
        color: #1565c0; 
        padding: 2px 8px; 
        border-radius: 12px; 
        font-size: 0.85em; 
        border: 1px solid #90caf9;
        margin-right: 4px;
    }
    .action-root { color: #d32f2f; font-weight: bold; }
    .voice-match { color: #2e7d32; font-weight: bold; }
    .voice-mismatch { color: #c62828; font-weight: bold; }
    .metric-box {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #673ab7;
    }
</style>
""", unsafe_allow_html=True)

st.title("🕉️ Pāṇinian Engine: Master Data Validator")
st.markdown("---")

# --- Load & Cache Data ---
@st.cache_data
def load_and_process_db():
    try:
        # Load the Master JSON
        with open("data/Dhatu_master_structured.json", "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        # Process Logic for ALL roots (Batch Processing)
        processed_data = []
        for entry in raw_data:
            # Run the Engine
            upadesha = entry.get('upadesha', '')
            diag = DhatuDiagnostic(upadesha)

            # Derived Properties
            derived_root = diag.get_final_root()
            derived_voice = diag.pada

            # Format Tags for UI
            tags_str = " ".join([f"<span class='tag-badge'>{t.split('-')[0]}</span>" for t in diag.it_tags])

            # Traditional vs Derived Check
            trad_voice = entry.get('pada', 'Unknown')
            # Normalize strings for comparison (simple check)
            match_status = "✅" if (("Atmanepada" in derived_voice and "आत्मने" in trad_voice) or 
                                   ("Parasmaipada" in derived_voice and "परस्मै" in trad_voice) or
                                   ("Ubhayapada" in derived_voice and "उभय" in trad_voice)) else "⚠️"

            processed_data.append({
                "ID": entry.get('identifier', entry.get('kaumudi_index')),
                "Upadesha (Input)": f"<span class='sanskrit'>{upadesha}</span>",
                "Meaning": f"<span class='sanskrit'>{entry.get('artha_sanskrit', '')}</span>",
                "Gana": entry.get('gana', ''),
                "Engine Output": f"<span class='sanskrit action-root'>{derived_root}</span>",
                "Genetic Tags": tags_str,
                "Voice (Tradition)": f"<span class='sanskrit'>{trad_voice}</span>",
                "Voice (Engine)": f"{match_status} {derived_voice}"
            })

        return pd.DataFrame(processed_data)

    except FileNotFoundError:
        st.error("File 'data/Dhatu_master_structured.json' not found. Please ensure data exists.")
        return pd.DataFrame()

# --- Main Layout ---
mode = st.sidebar.radio("Select Laboratory", ["Master Database", "Surgical Analysis"])

if mode == "Master Database":
    df = load_and_process_db()

    if not df.empty:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.header("📚 Dhātu-Pāṭha Ledger")
            st.caption(f"Loaded {len(df)} roots. The Engine has calculated derivations for ALL of them.")

        with col2:
            query = st.text_input("🔍 Search (Root/ID/Meaning)", "")

        # Filtering
        if query:
            mask = df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)
            display_df = df[mask]
        else:
            display_df = df

        # Render HTML Table
        st.write(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)
    else:
        st.info("Please place your 'Dhatu_master_structured.json' in the 'data/' folder.")

elif mode == "Surgical Analysis":
    st.header("🧪 Single Root Diagnostics")

    col1, col2 = st.columns([1, 2])
    with col1:
        raw_root = st.text_input("Enter Upadesha (e.g. डुकृञ्)", value="डुकृञ्")
        if st.button("Run Prakriyā", type="primary"):
            diag = DhatuDiagnostic(raw_root)

            st.markdown(f"""
            <div class="metric-box">
                <h4>Diagnosis</h4>
                <p>Input: <b>{diag.raw}</b></p>
                <p>Root: <b class="sanskrit" style="color:#d32f2f; font-size:1.5em;">{diag.get_final_root()}</b></p>
                <p>Voice: {diag.pada}</p>
            </div>
            """, unsafe_allow_html=True)

            st.subheader("🧬 It-Tags Detected")
            st.write(diag.it_tags)

    with col2:
        if 'diag' in locals():
            st.subheader("📜 Step-by-Step Trace")
            trace = pd.DataFrame([s.split(": ", 1) for s in diag.history], columns=["Rule", "Operation"])
            st.table(trace)
'''
    app_path.write_text(code, encoding='utf-8')
    print("✅ App Updated: Linked to 'data/Dhatu_master_structured.json'.")


if __name__ == "__main__":
    integrate_master_data()