import streamlit as st
import pandas as pd
from core.phonology import ad
from core.upadesha_registry import UpadeshaType
from logic.pratipadika_engine import PratipadikaEngine
from logic.it_engine import ItEngine
from logic.anga_engine import AngaEngine
from logic.vidhi_engine import VidhiEngine
from logic.sanjna_rules import apply_1_4_14_pada

# --- UI CONFIG ---
st.set_page_config(
    page_title="Subant Siddhi Lab",
    page_icon="🔬",
    layout="wide"
)


# --- HELPER FUNCTIONS ---
def join_varnas(varna_list):
    """Reconstructs string from Varna objects."""
    return "".join([v.char for v in varna_list])


def get_diff_highlight(old_str, new_str):
    """Visualizes the mutation."""
    if old_str == new_str:
        return new_str
    return f":red[{new_str}]"


# --- EXTENDED VIDHI WRAPPER (For Demo Specifics) ---
# Some specific rules (Kroshtu, Rai, etc.) might not be in the main engine yet.
# We define them here to ensure the page runs smoothly for all examples.
class ExtendedVidhi(VidhiEngine):

    @staticmethod
    def apply_ami_purvah_6_1_107(varna_list):
        """६.१.१०७ अमि पूर्वः (Sandhi for Am)"""
        # Logic: If 'a' + 'a' of Am -> 'a' (Purvarupa)
        # Simplified for demo: merge last two if they are 'a' and 'a'
        if len(varna_list) > 1:
            if varna_list[-1].char == 'अ' and varna_list[-2].char == 'अ':
                varna_list.pop()
                return varna_list, "६.१.१०७ (अमि पूर्वः)"
        return varna_list, None

    @staticmethod
    def apply_nalopa_8_2_7(varna_list):
        """८.२.७ नलोपः प्रातिपदिकान्तस्य"""
        if varna_list and varna_list[-1].char == 'न्':
            varna_list.pop()
            return varna_list, "८.२.७ (न-लोपः)"
        return varna_list, None


# --- MAIN APP LOGIC ---

st.title("🔬 Subant Siddhi Lab: Sanskrit Word Generator")
st.markdown("### PAS-5.0 Engine | Zone 3 (Morphology)")
st.markdown("---")

# 1. INPUT SECTION
col1, col2 = st.columns([1, 1])
with col1:
    word_input = st.text_input("Enter Base Name (प्रातिपदिक)", value="राम")
with col2:
    sup_map = PratipadikaEngine.get_sup_vibhakti_map()
    # Flattening logic for UI
    vib_options = list(sup_map.keys())
    vib_choice = st.selectbox("Select Vibhakti", vib_options)

    vac_choice = st.selectbox("Select Vachana", ["एक", "द्वि", "बहु"])

    # Safe retrieval
    try:
        selected_suffix = sup_map[vib_choice][vac_choice]
    except KeyError:
        selected_suffix = "सुँ"  # Fallback

if word_input:
    # A. PRATIPADIKA VALIDATION
    base_info = PratipadikaEngine.identify_base(word_input)

    if base_info['is_pratipadika']:
        st.success(f"**Step 1: Identity Verified** - {base_info['sutra_applied']}")

        # B. PHONOLOGICAL ASSEMBLY (Varna-Vichhed)
        # We combine Base + Suffix (e.g., Ram + Su)
        combined_raw = word_input + selected_suffix

        # Use PAS-5 'ad' engine
        varna_list = ad(combined_raw)

        # Track history for UI
        history = []
        prev_str = join_varnas(varna_list)


        def add_trace(sutra, varnas, prev_s, change_desc):
            curr_s = join_varnas(varnas)
            history.append({
                "step": len(history) + 1,
                "sutra": sutra,
                "vichhed": " + ".join([f"`{v.char}`" for v in varnas]),
                "form": curr_s,
                "highlighted": get_diff_highlight(prev_s, curr_s),
                "change": change_desc
            })
            return curr_s


        # Initial State
        prev_str = add_trace("Initial", varna_list, prev_str, "Varna Vichhed")

        # C. IT-SANJNA & LOPA (The Scrubber)
        # We assume the suffix part needs scrubbing.
        # Ideally, we scrub only the suffix, but ItEngine handles Vibhakti context globally.

        clean_varnas, it_tags = ItEngine.run_it_prakaran(
            varna_list, source_type=UpadeshaType.VIBHAKTI
        )

        # Log It-Sanjna steps
        if len(clean_varnas) < len(varna_list):
            prev_str = add_trace("१.३.२ - १.३.९", clean_varnas, prev_str, "इत्-लोपः (Marker Removal)")

        current_varnas = list(clean_varnas)

        # D. ANGA DEFINITION (1.4.13)
        st.subheader("✂️ Aṅga Definition (१.४.१३)")

        # Use AngaEngine to auto-detect
        anga_indices = AngaEngine.identify_boundary_indices(current_varnas)

        # Allow user to see/adjust
        full_chars = [v.char for v in current_varnas]
        start, end = anga_indices

        c_slide, c_vis = st.columns([2, 1])
        with c_slide:
            user_indices = st.slider(
                "Aṅga Boundary (Stem | Suffix)",
                0, len(full_chars), (0, end)
            )

        # Separate lists based on slider
        anga_part = current_varnas[user_indices[0]:user_indices[1]]
        suffix_part = current_varnas[user_indices[1]:]

        with c_vis:
            st.markdown(f"**Aṅga:** `:blue[{join_varnas(anga_part)}]`")
            st.markdown(f"**Suffix:** `:orange[{join_varnas(suffix_part)}]`")

        # E. PADA SANJNA (1.4.14)
        # Pass the full list to check if it qualifies
        is_pada = True  # Subanta is generally Pada
        if is_pada:
            # st.info(f"✨ **Step 4: Pada Sanjna established** (१.४.१४)")

            # --- F. SURGICAL DERIVATION (Vidhi) ---
            # We reconstruct the list for processing: Anga + Suffix
            process_list = anga_part + suffix_part

            # 1. 7.1.24 Ato Am (Rama + Am)
            # Conditions: Anga ends in 'a', Suffix is 'Am' (replaces Su)
            if word_input.endswith("अ") and selected_suffix in ["अम्", "सुँ"]:
                # Check if it's Neuter (Phalam) -> 7.1.24
                if word_input in ["फल", "ज्ञान", "वन"]:
                    process_list, s24 = VidhiEngine.ato_am_7_1_24(process_list)  # Wrapper handles logic
                    if s24: prev_str = add_trace("७.१.२४", process_list, prev_str, "अतोऽम्")

                    process_list, s107 = ExtendedVidhi.apply_ami_purvah_6_1_107(process_list)
                    if s107: prev_str = add_trace("६.१.१०७", process_list, prev_str, "पूर्वरूपम्")

            # 2. 6.4.8 Upadha Dirgha (Rajan + Su/Au)
            if "राजन्" in word_input or word_input.endswith("न्"):
                # Check for Sarvanamasthana (Su, Au, Jas, Am, Aut)
                if selected_suffix in ["सुँ", "औ", "जस्", "अम्", "औट्"]:
                    process_list, s8 = VidhiEngine.apply_upadha_dirgha_6_4_8(process_list)
                    if s8: prev_str = add_trace("६.४.८", process_list, prev_str, "उपधा-दीर्घः")

                # 8.2.7 Nalopa (Raja) - Only if Padanta (End of word) implies Su-Lopa happened
                # But for Rajan + Su -> Raja, we need Hal-Nyab-Lopa first.

            # 3. 7.1.94 Anang (Pitr -> Pitan)
            if word_input.endswith("ऋ"):
                if selected_suffix == "सुँ":
                    process_list, s94 = VidhiEngine.apply_anang_7_1_94(process_list)
                    if s94:
                        prev_str = add_trace("७.१.९४", process_list, prev_str, "अनङ्-आदेशः")
                        # Remove 'ng' marker immediately
                        process_list = [v for v in process_list if v.char != 'ङ्']

                    # 6.4.8 Upadha Dirgha applies to 'an' ending now (Pitan -> Pitaan)
                    process_list, s8 = VidhiEngine.apply_upadha_dirgha_6_4_8(process_list)
                    if s8: prev_str = add_trace("६.४.८", process_list, prev_str, "उपधा-दीर्घः")

            # 4. 6.1.68 Hal-Nyab-Lopa (Removal of Su)
            # Triggers for: Raja(n)+s, Pita(n)+s, Ramaa+s, Nadi+s
            # We assume current state has 's' at end.
            process_list, s68 = VidhiEngine.apply_hal_nyab_6_1_68(process_list)
            if s68: prev_str = add_trace("६.१.६८", process_list, prev_str, "हल्ङ्याब्-लोपः (Su-Lopa)")

            # 5. 8.2.7 Nalopa (Rajan -> Raja)
            # Applies if 'n' is final after Su-Lopa
            process_list, s7 = ExtendedVidhi.apply_nalopa_8_2_7(process_list)
            if s7: prev_str = add_trace("८.२.७", process_list, prev_str, "न-लोपः")

            # 6. 8.2.66 Rutva & 8.3.15 Visarga (Rama + s -> Ramah)
            # If 's' remains (e.g. Ramas), it becomes Ru -> Visarga
            if process_list and process_list[-1].char == 'स्':
                process_list, s66 = VidhiEngine.apply_rutva_8_2_66(process_list)
                if s66:
                    prev_str = add_trace("८.२.६६", process_list, prev_str, "ससजुषोः रुः")
                    # Remove 'u' marker
                    process_list = [v for v in process_list if v.char != 'उँ']

                process_list, s15 = VidhiEngine.apply_visarga_8_3_15(process_list)
                if s15: prev_str = add_trace("८.३.१५", process_list, prev_str, "खरवसानयोर्विसर्जनीयः")

            # --- G. RENDER HISTORY ---
            st.subheader("🧪 Step-by-Step Surgical Derivation")

            # Using standard dataframe for clean look
            df_history = pd.DataFrame(history)
            if not df_history.empty:
                # Custom HTML table for better control
                for i, row in df_history.iterrows():
                    with st.container():
                        c_step = st.columns([0.5, 1, 3, 1.5, 2])
                        c_step[0].write(f"**{row['step']}**")
                        c_step[1].info(f"{row['sutra']}")
                        c_step[2].text(row['vichhed'])
                        c_step[3].markdown(f"**{row['highlighted']}**")
                        c_step[4].success(row['change'])
                        st.divider()

            final_output = join_varnas(process_list)
            st.markdown("---")

            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.metric("Input (Pratipadika)", word_input)
            with res_col2:
                st.metric("Siddha Output (Subanta)", final_output)

            st.balloons()

    else:
        st.error(f"❌ **Rejection**: {base_info.get('reason', 'Invalid Pratipadika')}")