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
    # --- STEP 1: AUTOMATIC VERIFICATION ---
    base_info = PratipadikaEngine.identify_base(word_input)

    if base_info['is_pratipadika']:
        st.success(f"**Step 1: Identity Verified** - {base_info['sutra_applied']}")

        # Display metadata if found in shabdroop.json
        if 'metadata' in base_info:
            meta = base_info['metadata']
            st.caption(f"✨ **Database Match Found:** Meaning: {meta.get('artha_hin')} | Gender: {meta.get('linga')}")

        st.markdown("---")

        # --- STEP 2: SUFFIX INJECTION ---
        st.subheader(f"Step 2: Injection (Pratyaya: {selected_suffix})")
        combined_raw = word_input + selected_suffix
        varna_list = sanskrit_varna_vichhed(combined_raw)
        st.write(f"Initial Sequence: `{combined_raw}`")

        # --- STEP 3: IT-SANJNA ENGINE ---
        st.subheader("Step 3: It-Sanjna & Lopa (Cleaning)")
        clean_varnas, it_tags = ItSanjnaEngine.run_it_sanjna_prakaran(
            varna_list, combined_raw, source_type=UpadeshaType.VIBHAKTI
        )
        intermediate_word = sanskrit_varna_samyoga(clean_varnas)
        st.write(f"Post-Cleaning Form: `{intermediate_word}`")
        for tag in it_tags:
            st.caption(tag)

        # --- STEP 4 & 5: SUBANTA OPERATIONS (Logic for Prathama Ekavachana) ---
        # Note: These operations currently handle 's' -> 'r' -> 'h'
        final_processed_varnas = clean_varnas

        if intermediate_word.endswith('स्'):
            st.subheader("Step 4: Rutva & Visarga (Final Operations)")

            # Rutva 8.2.66
            rutva_varnas, s66 = apply_rutva_8_2_66(clean_varnas)
            st.write(f"Applying Rutva ({s66})...")

            # Clean newly added 'रुँ'
            final_r_varnas, _ = ItSanjnaEngine.run_it_sanjna_prakaran(
                rutva_varnas, "रुँ", source_type=UpadeshaType.VIBHAKTI
            )

            # Visarga 8.3.15
            final_processed_varnas, s15 = apply_visarga_8_3_15(final_r_varnas)
            st.write(f"Applying Visarga ({s15})...")

        # --- FINAL OUTPUT ---
        final_output = sanskrit_varna_samyoga(final_processed_varnas)
        st.markdown("---")
        st.header(f"✅ Final Siddhi Form: {final_output}")

        # Reference Check (If available in JSON)
        if 'metadata' in base_info:
            st.info(f"**Reference Check:** In database, forms for this word are: {base_info['metadata'].get('forms')}")

    else:
        st.error(f"❌ Rejection: {base_info['reason']}")
        st.warning("According to Panini 1.2.45, a Pratipadika cannot be a Dhatu or a Pratyaya.")