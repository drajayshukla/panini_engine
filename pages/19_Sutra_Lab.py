import streamlit as st
import json
import os
from core.sanjna_engine import SanjnaEngine
from core.upadesha_registry import Upadesha
from core.phonology import sanskrit_varna_vichhed

# ==========================================
# ZONE 1: UI CONFIG & INITIALIZATION
# ==========================================
st.set_page_config(page_title="Pāṇini Sutra Lab", layout="wide")
st.title("🧪 Pāṇini Sutra Lab: Full Master Tester")


# ==========================================
# ZONE 2: DATA LOADING (Shastric Knowledge)
# ==========================================
@st.cache_data
def load_sutra_master():
    path = os.path.join("data", "panini_sutras_final.json")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


sutra_master = load_sutra_master()


# ==========================================
# ZONE 3: EXECUTION ENGINE (The logic mapping)
# ==========================================
def run_sutra_logic(sutra_id, test_input):
    """
    Surgically maps JSON IDs to Python Functions in SanjnaEngine.
    This is where we link Shastra to Code.
    """
    # Sanjna Logic Mapping
    if sutra_id == "1.1.1":
        return SanjnaEngine.is_vriddhi_1_1_1(test_input)
    if sutra_id == "1.1.2":
        # Assuming we add is_guna_1_1_2 to SanjnaEngine
        return getattr(SanjnaEngine, "is_guna_1_1_2", lambda x: False)(test_input)

    # Placeholder for non-implemented logic
    return None


# ==========================================
# ZONE 4: SEARCH & SELECTION UI
# ==========================================
with st.sidebar:
    st.header("🔍 Sutra Navigator")
    search_query = st.text_input("Search by Number or Name (e.g. 1.1.1)")

    # Filtered List
    filtered_sutras = {k: v for k, v in sutra_master.items()
                       if search_query in k or search_query in v.get('sutra', '')}

    selected_id = st.selectbox("Select Sutra", list(filtered_sutras.keys()) if filtered_sutras else ["None"])

# ==========================================
# ZONE 5: SURGICAL TRACE & RESULTS
# ==========================================
if selected_id != "None" and selected_id in sutra_master:
    s_data = sutra_master[selected_id]

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader(f"Sūtra {selected_id}")
        st.info(f"**{s_data.get('sutra', '')}**")
        st.markdown(f"**Vṛtti:** {s_data.get('vritti', 'No vritti available.')}")
        st.caption(f"Type: {s_data.get('type', 'Unknown')}")

    with col2:
        st.subheader("🔬 Live Test Bench")
        test_val = st.text_input("Enter Varna to test:", value="आ")

        if test_val:
            result = run_sutra_logic(selected_id, test_val)

            if result is True:
                st.success(f"✅ VALID: '{test_val}' satisfies {selected_id}")
            elif result is False:
                st.error(f"❌ INVALID: '{test_val}' fails {selected_id}")
            else:
                st.warning("⚠️ Logic not yet implemented in SanjnaEngine.")

    st.divider()

    # ZONE 6: OBJECT DNA INSPECTOR
    st.subheader("🧬 Varna DNA Inspector")
    if test_val:
        v_obj = Upadesha(test_val, selected_id)
        st.json({
            "Character": v_obj.char,
            "Address": v_obj.sutra_origin,
            "Is Pratyaya (3.1.1)": v_obj.is_pratyaya,
            "Is Para (3.1.2)": v_obj.is_para,
            "Phonetic Breakdown": [v.char for v in sanskrit_varna_vichhed(test_val)]
        })