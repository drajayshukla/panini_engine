import streamlit as st
from core.phonology import sanskrit_varna_vichhed, sanskrit_varna_samyoga
from core.it_sanjna_engine import ItSanjnaEngine
from core.upadesha_registry import UpadeshaType
from logic.pratipadika_engine import PratipadikaEngine
from logic.subanta_operations import apply_rutva_8_2_66, apply_visarga_8_3_15

st.set_page_config(page_title="Subant Siddhi Lab", layout="wide")

st.title("🔬 Subant Siddhi Lab: Sanskrit Word Generator")
st.markdown("---")

# १. Input Section
col1, col2 = st.columns([1, 1])

with col1:
    word_input = st.text_input("Enter Base Name (प्रातिपदिक)", value="राम")

with col2:
    # Pulling the 21 suffixes from the matrix in our engine
    sup_map = PratipadikaEngine.get_sup_vibhakti_map()
    vib_choice = st.selectbox("Select Vibhakti", list(sup_map.keys()))
    vac_choice = st.selectbox("Select Vachana", ["एकवचन", "द्विवचन", "बहुवचन"])
    selected_suffix = sup_map[vib_choice][vac_choice]

if word_input:
    # --- STEP 1: AUTOMATIC VERIFICATION (The Gatekeeper) ---
    base_info = PratipadikaEngine.identify_base(word_input)

    if base_info['is_pratipadika']:
        st.success(f"**Step 1: Identity Verified** - {base_info['sutra_applied']}")

        if 'metadata' in base_info:
            meta = base_info['metadata']
            st.caption(
                f"✨ **Database Match:** {meta.get('artha_hin') or meta.get('artha')} | Linga: {meta.get('linga')}")

        st.markdown("---")

        # --- STEP 2: SUFFIX INJECTION ---
        st.subheader(f"Step 2: Injection (Pratyaya: {selected_suffix})")
        combined_raw = word_input + selected_suffix
        varna_list = sanskrit_varna_vichhed(combined_raw)
        st.write(f"Varna Sequence: `{' + '.join([v.char for v in varna_list])}`")

        # --- STEP 3: IT-SANJNA ENGINE ---
        st.subheader("Step 3: It-Sanjna & Lopa (Cleaning)")
        # VIBHAKTI type triggers the 1.3.4 shield for endings like 's', 'm', 't-varga'
        clean_varnas, it_tags = ItSanjnaEngine.run_it_sanjna_prakaran(
            varna_list, combined_raw, source_type=UpadeshaType.VIBHAKTI
        )
        intermediate_word = sanskrit_varna_samyoga(clean_varnas)

        st.write(f"Post-Cleaning Form: `{intermediate_word}`")
        if it_tags:
            for tag in it_tags:
                st.caption(tag)
        else:
            st.caption("No It-markers found in this suffix.")

        # --- STEP 4 & 5: SUBANTA OPERATIONS ---
        final_processed_varnas = clean_varnas

        # Clinical Check: Apply Rutva-Visarga only if the word ends in 's'
        if intermediate_word.endswith('स्'):
            st.subheader("Step 4: Final Phonology (Rutva & Visarga)")

            # Rutva 8.2.66: ससजुषोः रुः (Converts 's' to 'ru')
            rutva_varnas, s66 = apply_rutva_8_2_66(clean_varnas)

            # Recursive Step: Clean 'ru' markers to get pure 'r'
            final_r_varnas, _ = ItSanjnaEngine.run_it_sanjna_prakaran(
                rutva_varnas, "रुँ", source_type=UpadeshaType.VIBHAKTI
            )
            st.write(f"Applied: {s66} → `{sanskrit_varna_samyoga(final_r_varnas)}`")

            # Visarga 8.3.15: खरवसानयोर्विसर्जनीयः (Converts 'r' to Visarga)
            final_processed_varnas, s15 = apply_visarga_8_3_15(final_r_varnas)
            st.write(f"Applied: {s15} → `{sanskrit_varna_samyoga(final_processed_varnas)}`")

        # --- FINAL OUTPUT ---
        final_output = sanskrit_varna_samyoga(final_processed_varnas)
        st.markdown("---")
        st.header(f"✅ Result: {final_output}")

        # Reference Comparison
        if 'metadata' in base_info and base_info['metadata'].get('forms'):
            with st.expander("View Reference Forms (From Database)"):
                st.write(base_info['metadata']['forms'])

    else:
        # --- REJECTION LOGIC (e.g. for 'एध्') ---
        st.error(f"❌ Rejection: {base_info['reason']}")
        if base_info.get('detected_as'):
            st.warning(f"Detected as: {base_info.get('detected_as')}")
        st.info("Sutra: १.२.४५ (अर्थवदधातुरप्रत्ययः प्रातिपदिकम्) - A Pratipadika cannot be a Dhatu or Pratyaya.")