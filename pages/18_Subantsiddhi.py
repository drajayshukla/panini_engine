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
    # 1.2.45 Logic
    base_info = PratipadikaEngine.identify_base(word_input)
    st.info(f"**Step 1: Pratipadika Sanjna** - {base_info['sutra']} applied. '{word_input}' is now a valid base.")

    # २. Suffix Selection (4.1.2)
    st.subheader("Step 2: Vibhakti Injection (४.१.२)")
    vibhaktis = get_all_vibhakti()  # Loaded from vibhaktipatha.json
    selected_suffix = "सुँ"  # For 'रामः' specifically
    st.success(f"Selected Suffix: **{selected_suffix}** (Prathama Ekavachana)")

    # ३. It-Sanjna & Lopa (1.3.2)
    st.subheader("Step 3: It-Sanjna & Cleaning")
    combined_raw = word_input + selected_suffix
    varna_list = sanskrit_varna_vichhed(combined_raw)

    clean_varnas, it_tags = ItSanjnaEngine.run_it_sanjna_prakaran(
        varna_list, combined_raw, source_type=UpadeshaType.VIBHAKTI
    )
    st.write(f"Cleaned Stem: `{sanskrit_varna_samyoga(clean_varnas)}`")
    for tag in it_tags:
        st.caption(f"Applied: {tag}")

    # ४. Rutva (8.2.66)
    st.subheader("Step 4: Rutva (८.२.६६)")
    rutva_varnas, rutva_sutra = apply_rutva_8_2_66(clean_varnas)

    # Run It-Sanjna again specifically for 'रुँ' to get 'र्'
    final_r_varnas, _ = ItSanjnaEngine.run_it_sanjna_prakaran(
        rutva_varnas, "रुँ", source_type=UpadeshaType.VIBHAKTI
    )
    st.write(f"After Rutva: `{sanskrit_varna_samyoga(final_r_varnas)}` ({rutva_sutra})")

    # ५. Visarga (8.3.15)
    st.subheader("Step 5: Visarga (८.३.१५)")
    final_varnas, visarga_sutra = apply_visarga_8_3_15(final_r_varnas)
    final_word = sanskrit_varna_samyoga(final_varnas)

    st.header(f"✅ Final Siddhi: {final_word}")
    st.balloons()