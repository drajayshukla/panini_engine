import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION (Must be first) ---
st.set_page_config(
    page_title="Subant Siddhi Lab",
    page_icon="🔬",
    layout="wide"
)

# --- 2. PAS-5.0 IMPORTS ---
from core.phonology import ad, sanskrit_varna_samyoga
from core.upadesha_registry import UpadeshaType
from logic.pratipadika_engine import PratipadikaEngine
from logic.it_engine import ItEngine
from logic.anga_engine import AngaEngine
from logic.vidhi_engine import VidhiEngine
from logic.sanjna_rules import apply_1_4_14_pada


# --- 3. HELPER FUNCTIONS ---
def get_readable_form(varna_list):
    """
    Uses the Samyoga Engine to create a readable Devanagari string
    (Ligatures applied) instead of raw concatenation.
    """
    return sanskrit_varna_samyoga(varna_list)


def get_diff_highlight(old_str, new_str):
    """Visualizes the mutation."""
    if old_str == new_str:
        return new_str
    return f":red[{new_str}]"


# --- 4. EXTENDED VIDHI WRAPPER (Local Logic) ---
class ExtendedVidhi(VidhiEngine):
    """
    Extensions for specific rules needed for this demo page.
    """

    @staticmethod
    def apply_ami_purvah_6_1_107(varna_list):
        """[SUTRA]: अमि पूर्वः (६.१.१०७)"""
        if len(varna_list) > 1:
            if varna_list[-1].char == 'अ' and varna_list[-2].char == 'अ':
                varna_list.pop()
                return varna_list, "६.१.१०७ (अमि पूर्वः)"
        return varna_list, None

    @staticmethod
    def apply_nalopa_8_2_7(varna_list):
        """[SUTRA]: नलोपः प्रातिपदिकान्तस्य (८.२.७)"""
        if varna_list and varna_list[-1].char == 'न्':
            varna_list.pop()
            return varna_list, "८.२.७ (न-लोपः)"
        return varna_list, None


# --- 5. MAIN APP LOGIC ---

st.title("🔬 Subant Siddhi Lab: Sanskrit Word Generator")
st.markdown("### PAS-5.0 Engine | Zone 3 (Morphology)")
st.markdown("---")

# INPUT SECTION
col1, col2 = st.columns([1, 1])
with col1:
    word_input = st.text_input("Enter Base Name (प्रातिपदिक)", value="राम")
with col2:
    sup_map = PratipadikaEngine.get_sup_vibhakti_map()
    vib_choice = st.selectbox("Select Vibhakti", list(sup_map.keys()))
    vac_choice = st.selectbox("Select Vachana", ["एक", "द्वि", "बहु"])

    try:
        selected_suffix = sup_map[vib_choice][vac_choice]
    except KeyError:
        selected_suffix = "सुँ"

if word_input:
    # A. PRATIPADIKA VALIDATION
    base_info = PratipadikaEngine.identify_base(word_input)

    if base_info['is_pratipadika']:
        st.success(f"**Step 1: Identity Verified** - {base_info['sutra_applied']}")

        # B. PHONOLOGICAL ASSEMBLY (Varna-Vichhed)
        combined_raw = word_input + selected_suffix
        varna_list = ad(combined_raw)

        # History Tracking
        history = []
        # [VISUAL FIX]: Initialize with Readable Form (e.g. रामसुँ)
        prev_str = get_readable_form(varna_list)


        def add_trace(sutra, varnas, prev_s, change_desc):
            # [VISUAL FIX]: Use Samyoga for the 'Form' column so it looks like 'रामस्' not 'र्आम्अस्'
            curr_s = get_readable_form(varnas)

            # Create a clean visual split for the Vichhed column
            vichhed_display = " + ".join([f"{v.char}" for v in varnas])

            history.append({
                "step": len(history) + 1,
                "sutra": sutra,
                "vichhed": vichhed_display,
                "form": curr_s,
                "highlighted": get_diff_highlight(prev_s, curr_s),
                "change": change_desc
            })
            return curr_s


        prev_str = add_trace("Initial", varna_list, prev_str, "Varna Vichhed")

        # C. IT-SANJNA & LOPA (The Scrubber)
        clean_varnas, it_tags = ItEngine.run_it_prakaran(
            varna_list, source_type=UpadeshaType.VIBHAKTI
        )

        if len(clean_varnas) < len(varna_list):
            prev_str = add_trace("१.३.२ - १.३.९", clean_varnas, prev_str, "इत्-लोपः")

        current_varnas = list(clean_varnas)

        # D. ANGA DEFINITION (1.4.13)
        st.subheader("✂️ Aṅga Definition (१.४.१३)")

        # Auto-detect boundary
        start_idx, end_idx = AngaEngine.identify_boundary_indices(current_varnas)
        full_chars = [v.char for v in current_varnas]

        c_slide, c_vis = st.columns([2, 1])
        with c_slide:
            user_indices = st.slider(
                "Aṅga Boundary (Stem | Suffix)",
                0, len(full_chars), (0, end_idx)
            )

        anga_part = current_varnas[user_indices[0]:user_indices[1]]
        suffix_part = current_varnas[user_indices[1]:]

        with c_vis:
            # Join parts for display
            anga_str = get_readable_form(anga_part)
            suffix_str = get_readable_form(suffix_part)
            st.markdown(f"**Aṅga:** `:blue[{anga_str}]`")
            st.markdown(f"**Suffix:** `:orange[{suffix_str}]`")

        # E. PADA SANJNA (1.4.14)
        is_pada, pada_msg = apply_1_4_14_pada(current_varnas, UpadeshaType.VIBHAKTI)

        if is_pada:
            # --- F. SURGICAL DERIVATION (Vidhi) ---
            process_list = list(current_varnas)

            # --- RULE 1: 7.1.24 Ato Am ---
            if word_input.endswith("अ") and selected_suffix in ["अम्"]:
                if word_input in ["फल", "ज्ञान", "वन"]:
                    process_list, s24 = VidhiEngine.ato_am_7_1_24(process_list)
                    if s24: prev_str = add_trace("७.१.२४", process_list, prev_str, "अतोऽम्")

                    process_list, s107 = ExtendedVidhi.apply_ami_purvah_6_1_107(process_list)
                    if s107: prev_str = add_trace("६.१.१०७", process_list, prev_str, "पूर्वरूपम्")

            # --- RULE 2: 6.1.107 Ami Purvah ---
            if selected_suffix == "अम्":
                process_list, s107 = ExtendedVidhi.apply_ami_purvah_6_1_107(process_list)
                if s107: prev_str = add_trace("६.१.१०७", process_list, prev_str, "अमि पूर्वः")

            # --- RULE 3: 6.4.8 Upadha Dirgha ---
            if "राजन्" in word_input or word_input.endswith("न्"):
                if selected_suffix in ["सुँ", "औ", "जस्", "अम्", "औट्"]:
                    process_list, s8 = VidhiEngine.apply_upadha_dirgha_6_4_8(process_list)
                    if s8: prev_str = add_trace("६.४.८", process_list, prev_str, "उपधा-दीर्घः")

            # --- RULE 4: 6.1.68 Hal-Nyab-Lopa ---
            stem_ends_in_consonant = not anga_part[-1].is_vowel if anga_part else False
            stem_ends_in_fem = anga_part[-1].char in ['आ', 'ई', 'ऊ'] if anga_part else False

            if stem_ends_in_consonant or stem_ends_in_fem:
                if suffix_part and len(suffix_part) == 1 and suffix_part[0].char == 'स्':
                    process_list, s68 = VidhiEngine.apply_hal_nyab_6_1_68(process_list)
                    if s68: prev_str = add_trace("६.१.६८", process_list, prev_str, "हल्ङ्याब्-लोपः")

            # --- RULE 5: 8.2.7 Nalopa ---
            process_list, s7 = ExtendedVidhi.apply_nalopa_8_2_7(process_list)
            if s7: prev_str = add_trace("८.२.७", process_list, prev_str, "न-लोपः")

            # --- RULE 6: 8.2.66 Sasajusho Ru ---
            if process_list and process_list[-1].char == 'स्':
                process_list, s66 = VidhiEngine.apply_rutva_8_2_66(process_list)
                if s66:
                    prev_str = add_trace("८.२.६६", process_list, prev_str, "ससजुषोः रुः")

            # --- RULE 7: 8.3.15 Kharavasanayor Visarjaniyah ---
            if process_list and process_list[-1].char == 'र्':
                process_list, s15 = VidhiEngine.apply_visarga_8_3_15(process_list)
                if s15: prev_str = add_trace("८.३.१५", process_list, prev_str, "खरवसानयोर्विसर्जनीयः")

            # --- G. RENDER HISTORY ---
            st.subheader("🧪 Step-by-Step Surgical Derivation")
            df_history = pd.DataFrame(history)

            if not df_history.empty:
                # [Visual Tweak]: Use Styler or simpler Column layout
                # Here we use Streamlit columns for a clean look

                # Header
                h_cols = st.columns([0.5, 1, 3, 1.5, 2])
                h_cols[0].markdown("**#**")
                h_cols[1].markdown("**Sutra**")
                h_cols[2].markdown("**Vichhed (Split)**")
                h_cols[3].markdown("**Form (Joined)**")
                h_cols[4].markdown("**Change**")
                st.divider()

                for i, row in df_history.iterrows():
                    with st.container():
                        c_step = st.columns([0.5, 1, 3, 1.5, 2])
                        c_step[0].write(f"{row['step']}")
                        c_step[1].info(f"{row['sutra']}")
                        c_step[2].code(row['vichhed'], language="text")  # Code block for clear separation
                        c_step[3].markdown(f"### {row['highlighted']}")  # Bigger font for form
                        c_step[4].success(row['change'])
                        st.divider()

            final_output = sanskrit_varna_samyoga(process_list)
            st.markdown("---")

            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.metric("Input (Pratipadika)", word_input)
            with res_col2:
                st.metric("Siddha Output (Subanta)", final_output)

            st.balloons()

    else:
        st.error(f"❌ **Rejection**: {base_info.get('reason', 'Invalid Pratipadika')}")