"""
PAGE: Dhātu Laboratory
"""
import streamlit as st
import pandas as pd
import json
import os
from logic.dhatu_processor import DhatuDiagnostic

st.set_page_config(page_title="Dhātu Lab", page_icon="🧪", layout="wide")

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

st.title("🧪 Dhātu Prakriyā Laboratory")

mode = st.radio("Mode", ["Single Analysis", "Master Database Validator"], horizontal=True)

if mode == "Single Analysis":
    col1, col2 = st.columns([1, 2])
    with col1:
        raw_root = st.text_input("Enter Upadesha (e.g. डुकृञ्, षण्मुखाय)", value="डुकृञ्")
        is_sub = st.checkbox("Is Subdhātu (Nāmadhātu)?")

        if st.button("Run Diagnostics", type="primary"):
            diag = DhatuDiagnostic(raw_root, is_subdhatu=is_sub)

            st.markdown(f"""
            <div class="metric-card">
                <h4>Diagnosis</h4>
                <p>Input: <b>{diag.raw}</b></p>
                <p>Root: <b class="sanskrit" style="color:#d32f2f; font-size:1.5em;">{diag.get_final_root()}</b></p>
                <p>Voice: {diag.pada}</p>
            </div>
            """, unsafe_allow_html=True)

            st.subheader("🧬 It-Tags")
            st.write(diag.it_tags)

            st.session_state['dhatu_trace'] = diag.history

    with col2:
        if 'dhatu_trace' in st.session_state:
            st.subheader("📜 Step-by-Step Trace")
            trace_df = pd.DataFrame([s.split(": ", 1) for s in st.session_state['dhatu_trace']], columns=["Rule", "Operation"])
            st.table(trace_df)

elif mode == "Master Database Validator":
    # Load Data
    @st.cache_data
    def load_data():
        paths = ["data/dhatu_master_structured.json", "dhatu_master_structured.json"]
        for p in paths:
            if os.path.exists(p):
                with open(p, "r", encoding="utf-8") as f: return json.load(f)
        return []

    raw_db = load_data()

    if not raw_db:
        st.error("Database not found in 'data/' folder.")
    else:
        st.caption(f"Loaded {len(raw_db)} roots.")

        # Filters
        with st.expander("🔍 Filters"):
            col_f1, col_f2 = st.columns(2)
            sel_gana = col_f1.multiselect("Gana", sorted(list(set([x.get('gana') for x in raw_db if x.get('gana')]))))
            sel_pada = col_f2.multiselect("Pada", sorted(list(set([x.get('pada') for x in raw_db if x.get('pada')]))))

        # Process
        processed_rows = []
        # Optimization: Limit to first 100 if no filter, or all if filtered
        limit = 100 if not (sel_gana or sel_pada) else 5000

        count = 0
        for entry in raw_db:
            if sel_gana and entry.get('gana') not in sel_gana: continue
            if sel_pada and entry.get('pada') not in sel_pada: continue

            upadesha = entry.get('upadesha', '')
            if not upadesha: upadesha = entry.get('mula_dhatu', '')
            target = entry.get('mula_dhatu', '')

            diag = DhatuDiagnostic(upadesha)
            derived = diag.get_final_root()

            match = derived == target
            status = "✅" if match else "❌"

            # Voice Match Logic
            trad_voice = entry.get('pada', '')
            eng_voice = diag.pada
            voice_ok = "⚠️"
            if "Atmanepada" in eng_voice and "आत्मने" in trad_voice: voice_ok = "✅"
            elif "Parasmaipada" in eng_voice and "परस्मै" in trad_voice: voice_ok = "✅"
            elif "Ubhayapada" in eng_voice and "उभय" in trad_voice: voice_ok = "✅"

            processed_rows.append({
                "ID": entry.get('identifier', ''),
                "Upadesha": f"<span class='sanskrit'>{upadesha}</span>",
                "Target": f"<span class='sanskrit'>{target}</span>",
                "Output": f"<span class='sanskrit {'match-success' if match else 'match-fail'}'>{derived}</span>",
                "Status": status,
                "Voice (Engine)": f"{voice_ok} {eng_voice}",
                "Voice (JSON)": f"<span class='sanskrit'>{trad_voice}</span>",
                "Meaning": entry.get('artha_sanskrit', '')
            })
            count += 1
            if count >= limit: break

        df = pd.DataFrame(processed_rows)

        tab1, tab2 = st.tabs(["📊 Data Table", "❌ Mismatches Only"])
        with tab1:
            st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
        with tab2:
            mismatches = df[df["Status"] == "❌"]
            if not mismatches.empty:
                st.write(mismatches.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:
                st.success("No mismatches in this selection!")
