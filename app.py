import streamlit as st
import pandas as pd
import json
import os

# --- IMPORTING THE PAS-5.0 ENGINE ---
from core.phonology import ad
from core.controller import process_word_full_cycle
from core.upadesha_registry import UpadeshaType
from core.pratyahara_engine import PratyaharaEngine
from logic.sthana_rules import STHANA_MAP

# Initialize Engines
pe = PratyaharaEngine()

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="अष्टाध्यायी-यंत्र | Paninian Engine",
    page_icon="🕉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CUSTOM CSS (The Clinical Aesthetic) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 10px; }
    .varna-box {
        border: 2px solid #4CAF50;
        border-radius: 5px;
        padding: 10px;
        text-align: center;
        background-color: white;
        margin: 2px;
        display: inline-block;
        min-width: 60px;
    }
    .varna-removed {
        border: 2px dashed #ff4b4b;
        background-color: #ffebee;
        text-decoration: line-through;
        opacity: 0.7;
    }
    .sutra-tag {
        font-size: 0.8em;
        color: #1565C0;
        background-color: #e3f2fd;
        padding: 2px 5px;
        border-radius: 4px;
        margin-top: 5px;
        display: block;
    }
    </style>
    """, unsafe_allow_html=True)


# --- 3. HELPER: DATA LOADER (Fail-safe) ---
@st.cache_data
def load_dhatu_data():
    """Loads Dhatu data safely for the dashboard."""
    path = os.path.join("data", "dhatu_master_structured.json")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, list) else data.get('dhatus', [])
    return []


# --- 4. VIEWS ---

def view_dashboard():
    """The Landing Page"""
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Om_symbol.svg/200px-Om_symbol.svg.png",
                 width=80)
    with col2:
        st.title("अष्टाध्यायी-यंत्र (The Paninian Engine)")
        st.markdown("**PAS-5.0 (Siddha)** | *Computational Linguistics for Sanskrit Grammar*")

    st.markdown("---")

    # Metrics
    dhatus = load_dhatu_data()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("कुल धातु (Total Roots)", f"{len(dhatus)}" if dhatus else "Offline")
    m2.metric("अष्टाध्यायी सूत्र", "3981")
    m3.metric("सक्रिय इंजन", "PAS-5.0")
    m4.metric("Engine Status", "🟢 Online")

    st.markdown("---")
    st.subheader("🔎 त्वरित धातु अन्वेषण (Quick Search)")
    query = st.text_input("Search Dhatupatha (e.g., 'भू', 'एधँ', 'Gam')", placeholder="Type a root...")

    if query and dhatus:
        results = [d for d in dhatus if query in str(d.get('mula_dhatu', '')) or query in str(d.get('upadesha', ''))]
        if results:
            st.success(f"Found {len(results)} matches.")
            df = pd.DataFrame(results)[['kaumudi_index', 'upadesha', 'artha_sanskrit', 'gana', 'pada']]
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("No matches found in database.")


def view_processor():
    """The Clinical Lab (Where the Engine runs)"""
    st.title("🔬 Clinical Lab (Processor)")
    st.markdown("Run the **Full Diagnostic Cycle** on any Sanskrit word.")

    # 1. Input
    c1, c2 = st.columns([3, 1])
    with c1:
        text_input = st.text_input("Enter Sanskrit Word (Upadesha):", value="गाधृँ")
    with c2:
        source_type = st.selectbox("Source Type", ["Dhatu", "Pratyaya", "Vibhakti", "Auto-Detect"])

    # 2. Controls
    run_btn = st.button("🚀 Run Diagnosis", type="primary")

    if run_btn and text_input:
        # A. Detect Type
        s_type = UpadeshaType.DHATU  # Default
        if source_type == "Auto-Detect":
            detected, is_t, origin = UpadeshaType.auto_detect(text_input)
            if detected:
                s_type = detected
                st.info(f"🤖 Auto-Detected: **{s_type.name}** (Ref: {origin})")
            else:
                st.warning("Could not auto-detect type. Defaulting to DHATU.")
        else:
            s_type = getattr(UpadeshaType, source_type.upper(), UpadeshaType.DHATU)

        # B. RUN THE ENGINE
        try:
            result = process_word_full_cycle(text_input, "User Input", s_type)

            # C. VISUALIZATION
            st.markdown("### 1. वर्ण-विच्छेद (Phonological MRI)")
            st.caption("Decomposition into Varna objects with Sthana/Prayatna DNA.")

            cols = st.columns(len(result['original_varnas']))
            for i, v in enumerate(result['original_varnas']):
                with cols[i]:
                    sthana_str = "+".join(v.sthana) if v.sthana else "N/A"
                    st.markdown(f"""
                    <div class="varna-box">
                        <div style="font-size: 1.5em; font-weight: bold;">{v.char}</div>
                        <div style="font-size: 0.8em; color: gray;">{sthana_str}</div>
                        <div style="font-size: 0.7em; color: #666;">{v.prayatna or ''}</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("### 2. इत्-संज्ञा & लोप (Surgical Scrub)")
            st.caption("Application of 1.3.2 - 1.3.9 to remove meta-tags.")

            # Logic to verify which indices were removed
            original_chars = [v.char for v in result['original_varnas']]
            remaining_chars = [v.char for v in result['remaining_varnas']]

            # Simple visual differencing (Clinical View)
            # We reconstruct the display based on the 'trace' inside the original objects

            p_cols = st.columns(len(result['original_varnas']))
            for i, v in enumerate(result['original_varnas']):
                is_removed = "इत्" in v.sanjnas
                css_class = "varna-box varna-removed" if is_removed else "varna-box"

                with p_cols[i]:
                    tags_html = "".join([f"<span class='sutra-tag'>{t}</span>" for t in v.trace if "1.3." in t])
                    st.markdown(f"""
                    <div class="{css_class}">
                        <div style="font-size: 1.5em; font-weight: bold;">{v.char}</div>
                        {tags_html}
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("### 3. परिणाम (Final Synthesis)")
            c_res1, c_res2 = st.columns(2)
            with c_res1:
                st.metric("Raw Input", text_input)
            with c_res2:
                st.metric("Siddha Output", result['final_result'])

            # Full Trace Log
            with st.expander("📂 Full Clinical Trace Log (Debug Data)"):
                st.json({
                    "Original": str(result['original_varnas']),
                    "Sanjna Analysis": str(result['analysis']),
                    "It Tags": result['it_tags'],
                    "Remaining": str(result['remaining_varnas'])
                })

        except Exception as e:
            st.error(f"Surgical Error: {e}")
            st.exception(e)


def view_calculator():
    """Pratyahara Calculator"""
    st.title("🧮 Pratyahara Calculator")
    st.markdown("Test the Algebraic Engine (1.1.71).")

    p_input = st.text_input("Enter Pratyahara (e.g., अच्, हल्, झल्):", "अच्")
    if st.button("Calculate Set"):
        varnas = pe.get_varnas(p_input)
        if varnas:
            st.success(f"**{p_input}** contains {len(varnas)} varnas.")
            st.write(varnas)
            st.info("Expanded (Savarṇa) check enabled.")
        else:
            st.error("Invalid Pratyahara.")


# --- 5. MAIN NAVIGATION ---
def main():
    with st.sidebar:
        st.header("Navigation")
        mode = st.radio("Go to:", ["Dashboard", "Processor (Clinical Lab)", "Calculator"])

        st.markdown("---")
        st.info("Running PAS-v5.0 Core")

    if mode == "Dashboard":
        view_dashboard()
    elif mode == "Processor (Clinical Lab)":
        view_processor()
    elif mode == "Calculator":
        view_calculator()


if __name__ == "__main__":
    main()