#pages/19_Sutra_Lab.py
import streamlit as st
import json
import os
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
# ==========================================
# ZONE 3: EXECUTION ENGINE (The logic mapping)
# ==========================================
from logic.vidhi.vidhi_engine import VidhiEngine
from core.sanjna_engine import SanjnaEngine


def run_sutra_logic(sutra_id, test_input_list):
    """
    Surgically routes Sutra IDs to the correct Engine Methods.
    Handles both Sanjna (Definitions) and Vidhi (Operations).
    """
    # Mapping for Zone 1: Sanjna Rules (Returns Boolean)
    sanjna_map = {
        "1.1.1": SanjnaEngine.is_vriddhi_1_1_1,
        "1.1.2": getattr(SanjnaEngine, "is_guna_1_1_2", None),
    }

    # Mapping for Zone 3: Vidhi Rules (Returns Modified List + Label)
    vidhi_map = {
        "1.2.47": VidhiEngine.apply_hrasva_napumsaka_1_2_47,
        "6.1.68": VidhiEngine.apply_hal_nyab_6_1_68,
        "6.1.107": VidhiEngine.apply_ami_purvah_6_1_107,
        "6.4.8": VidhiEngine.apply_upadha_dirgha_6_4_8,
        "6.4.143": VidhiEngine.apply_ti_lopa_6_4_143,
        "7.1.24": VidhiEngine.ato_am_7_1_24,
        "8.2.7": VidhiEngine.apply_nalopa_8_2_7,
        "8.2.66": VidhiEngine.apply_rutva_8_2_66,
        "8.3.15": VidhiEngine.apply_visarga_8_3_15,
    }

    # EXECUTION STEP
    if sutra_id in sanjna_map and sanjna_map[sutra_id]:
        # Sanjna rules take a single char/varna
        return sanjna_map[sutra_id](test_input_list[0].char), "Sanjna"

    if sutra_id in vidhi_map:
        # Vidhi rules take the full list and return (new_list, label)
        return vidhi_map[sutra_id](test_input_list), "Vidhi"

    return None, None

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