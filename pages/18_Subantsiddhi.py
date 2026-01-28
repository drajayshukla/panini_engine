import streamlit as st
from core.phonology import sanskrit_varna_vichhed, sanskrit_varna_samyoga
from core.it_sanjna_engine import ItSanjnaEngine
from core.upadesha_registry import UpadeshaType
from logic.pratipadika_engine import PratipadikaEngine
from logic.subanta_operations import apply_rutva_8_2_66, apply_visarga_8_3_15
from utils.data_loader import get_all_vibhakti

st.set_page_config(page_title="Subant Siddhi Lab", layout="wide")

st.title("🔬 Subant Siddhi Lab: रामः Process")

# १. Input & Base Identification
word_input = st.text_input("Enter Base (e.g., राम)", value="राम")

if word_input:
    # Step 1: Base Identification (1.2.45 / 1.2.46)
    base_info = PratipadikaEngine.identify_base(word_input)

    if base_info['is_pratipadika']:
        st.info(
            f"**Step 1: Pratipadika Sanjna** - {base_info['sutra_applied']} applied. '{word_input}' is now a valid base.")
        with st.expander("Sutra Description"):
            st.write(base_info['description'])

        # २. Suffix Selection (4.1.2)
        st.subheader("Step 2: Vibhakti Injection (४.१.२)")
        # In a full app, you can use get_all_vibhakti() to populate a selectbox
        selected_suffix = "सुँ"  # Hardcoded for the 'रामः' case study
        st.success(f"Selected Suffix: **{selected_suffix}** (Prathama Ekavachana)")

        # ३. It-Sanjna & Lopa (1.3.2)
        st.subheader("Step 3: It-Sanjna & Cleaning")
        combined_raw = word_input + selected_suffix
        varna_list = sanskrit_varna_vichhed(combined_raw)

        # Applying It-Sanjna Engine (Results in 'रामस्')
        clean_varnas, it_tags = ItSanjnaEngine.run_it_sanjna_prakaran(
            varna_list, combined_raw, source_type=UpadeshaType.VIBHAKTI
        )

        st.write(f"After It-Lopa: `{sanskrit_varna_samyoga(clean_varnas)}`")
        for tag in it_tags:
            st.caption(f"Applied: {tag}")

        # ४. Rutva (8.2.66)
        st.subheader("Step 4: Rutva (८.२.६६)")
        # Converts 'रामस्' to 'रामरुँ'
        rutva_varnas, rutva_sutra = apply_rutva_8_2_66(clean_varnas)

        # Step 5: Second It-Lopa (Cleaning the 'रुँ' into 'र्')
        # Panini's process requires cleaning newly added Upadesha markers
        final_r_varnas, r_tags = ItSanjnaEngine.run_it_sanjna_prakaran(
            rutva_varnas, "रुँ", source_type=UpadeshaType.VIBHAKTI
        )

        st.write(f"After Rutva ({rutva_sutra}): `{sanskrit_varna_samyoga(final_r_varnas)}`")

        # ६. Visarga (8.3.15)
        st.subheader("Step 5: Visarga (८.३.१५)")
        # Converts 'रामर्' to 'रामः' in Avasana
        final_varnas, visarga_sutra = apply_visarga_8_3_15(final_r_varnas)
        final_word = sanskrit_varna_samyoga(final_varnas)

        st.header(f"✅ Final Siddhi: {final_word}")
        st.balloons()

    else:
        # Error handling if the input is already a Dhatu or Pratyaya
        st.error(f"Error: {base_info['reason']}")