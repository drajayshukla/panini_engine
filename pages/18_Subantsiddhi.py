import streamlit as st
from core.phonology import sanskrit_varna_vichhed, sanskrit_varna_samyoga
from core.it_sanjna_engine import ItSanjnaEngine
from core.upadesha_registry import UpadeshaType
from logic.pratipadika_engine import PratipadikaEngine
from logic.subanta_operations import (
    apply_rutva_8_2_66,
    apply_visarga_8_3_15,
    apply_hal_nyab_6_1_68,
    apply_trijvadbhava_7_1_95,
    apply_anang_7_1_94,
    apply_upadha_dirgha_6_4_11,
    apply_upadha_dirgha_6_4_8,
    apply_nalopa_8_2_7,
apply_goto_nit_7_1_90,
apply_vṛddhi_7_2_115
)
from logic.sanjna_rules import check_pada_sanjna_1_4_14


# --- Helper for Highlighted Debugging ---
def get_diff_highlight(old_str, new_str):
    """Highlights changes in red for the debugger table."""
    if old_str == new_str:
        return new_str
    return f":red[{new_str}]"


st.set_page_config(page_title="Subant Siddhi Lab", layout="wide")
st.title("🔬 Subant Siddhi Lab: Sanskrit Word Generator")
st.markdown("---")

# १. Input Section
col1, col2 = st.columns([1, 1])
with col1:
    word_input = st.text_input("Enter Base Name (प्रातिपदिक)", value="क्रोष्टु")
with col2:
    sup_map = PratipadikaEngine.get_sup_vibhakti_map()
    vib_choice = st.selectbox("Select Vibhakti", list(sup_map.keys()))
    vac_choice = st.selectbox("Select Vachana", ["एकवचन", "द्विवचन", "बहुवचन"])
    selected_suffix = sup_map[vib_choice][vac_choice]

if word_input:
    base_info = PratipadikaEngine.identify_base(word_input)
    if base_info['is_pratipadika']:
        st.success(f"**Step 1: Identity Verified** - {base_info['sutra_applied']}")

        # --- STEP 2: SUFFIX INJECTION ---
        combined_raw = word_input + selected_suffix
        varna_list = sanskrit_varna_vichhed(combined_raw)

        # --- STEP 3: IT-SANJNA & LOPA ---
        clean_varnas, it_tags = ItSanjnaEngine.run_it_sanjna_prakaran(
            varna_list, combined_raw, source_type=UpadeshaType.VIBHAKTI
        )
        intermediate_word = sanskrit_varna_samyoga(clean_varnas)

        # --- STEP 4: PADA SANJNA ---
        is_pada, pada_msg = check_pada_sanjna_1_4_14(clean_varnas, UpadeshaType.VIBHAKTI)

        if is_pada:
            st.info(f"✨ **Step 4: Pada Sanjna** - {pada_msg}")
            history = []
            current_varnas = list(clean_varnas)
            prev_str = intermediate_word


            def add_history(sutra, varnas, p_str):
                f_str = sanskrit_varna_samyoga(varnas)
                history.append({
                    "Sutra": sutra if sutra else "---",
                    "Vichhed": [v.char for v in varnas],
                    "Form": get_diff_highlight(p_str, f_str)
                })
                return f_str


            prev_str = add_history("Initial (Post-Cleaning)", current_varnas, prev_str)

            # --- BRANCHING LOGIC FOR DIFFERENT STEM TYPES ---

            # CASE A: KROSTU
            if "क्रोष्टु" in word_input:
                current_varnas, s95 = apply_trijvadbhava_7_1_95(current_varnas)
                prev_str = add_history(s95, current_varnas, prev_str)
                current_varnas, s94 = apply_anang_7_1_94(current_varnas)
                prev_str = add_history(s94, current_varnas, prev_str)
                current_varnas = [v for v in current_varnas if v.char != 'ङ्']
                prev_str = add_history("१.३.३ (इत्-लोपः)", current_varnas, prev_str)
                current_varnas, s11 = apply_upadha_dirgha_6_4_11(current_varnas)
                prev_str = add_history(s11, current_varnas, prev_str)
                current_varnas, s68 = apply_hal_nyab_6_1_68(current_varnas)
                prev_str = add_history(s68 if s68 else "६.१.६८ (Manual)", current_varnas, prev_str)
                current_varnas, s7 = apply_nalopa_8_2_7(current_varnas)
                prev_str = add_history(s7 if s7 else "८.२.७ (Manual)", current_varnas, prev_str)

            # CASE B: JAMATR
                # --- BRANCH B: KINSHIP TERMS (जामातृ, पितृ, भ्रातृ etc.) ---
            elif any(x in word_input for x in ["जामातृ", "पितृ", "भ्रातृ", "नृ"]):
                # 1. 7.1.94 (अनङ्-आदेशः: ऋ -> अन्)
                current_varnas, s94 = apply_anang_7_1_94(current_varnas)
                prev_str = add_history(s94, current_varnas, prev_str)

                # 2. 1.3.3 (इत्-लोपः: ङ् removal)
                current_varnas = [v for v in current_varnas if v.char != 'ङ्']
                prev_str = add_history("१.३.३ (हलन्त्यम् - ङ् लोपः)", current_varnas, prev_str)

                # 3. 6.4.8 (उपधा दीर्घ: अ -> आ specifically for kinship/N-anta)
                current_varnas, s8 = apply_upadha_dirgha_6_4_8(current_varnas)
                prev_str = add_history(s8, current_varnas, prev_str)

                # 4. 6.1.68 (S-LOPA: पितान्स् -> पितान्)
                res_v5, s68 = apply_hal_nyab_6_1_68(current_varnas)
                current_varnas = res_v5
                prev_str = add_history(s68 if s68 else "६.१.६८ (S-Removal)", current_varnas, prev_str)

                # 5. 8.2.7 (N-LOPA: पितान् -> पिता)
                res_v6, s7 = apply_nalopa_8_2_7(current_varnas)
                current_varnas = res_v6
                prev_str = add_history(s7 if s7 else "८.२.७ (N-Removal)", current_varnas, prev_str)

            # CASE C: DHATR / KARTR (Agent Nouns)
            elif any(x in word_input for x in ["धातृ", "कर्तृ", "हर्तृ"]):
                current_varnas, s94 = apply_anang_7_1_94(current_varnas)
                prev_str = add_history(s94, current_varnas, prev_str)
                current_varnas = [v for v in current_varnas if v.char != 'ङ्']
                prev_str = add_history("१.३.३ (हलन्त्यम् - ङ् लोपः)", current_varnas, prev_str)
                current_varnas, s11 = apply_upadha_dirgha_6_4_11(current_varnas)
                prev_str = add_history(s11, current_varnas, prev_str)
                current_varnas, s68 = apply_hal_nyab_6_1_68(current_varnas)
                prev_str = add_history(s68 if s68 else "६.१.६८ (S-Removal)", current_varnas, prev_str)
                current_varnas, s7 = apply_nalopa_8_2_7(current_varnas)
                prev_str = add_history(s7 if s7 else "८.२.७ (N-Removal)", current_varnas, prev_str)
                # --- BRANCH F: GO SPECIAL (ओकारान्त) ---
            elif word_input == "गो":
                # 1. 7.1.90 (णिद्वद्भावः)
                current_varnas, s90 = apply_goto_nit_7_1_90(current_varnas)
                prev_str = add_history(s90, current_varnas, prev_str)

                # 2. 7.2.115 (ओ -> औ वृद्धिः)
                current_varnas, s115 = apply_vṛddhi_7_2_115(current_varnas)
                prev_str = add_history(s115, current_varnas, prev_str)

                # 3. 8.2.66 (स् -> रुँ)
                current_varnas, s66 = apply_rutva_8_2_66(current_varnas)
                prev_str = add_history(s66, current_varnas, prev_str)

                # 4. 1.3.2 (रुँ -> र् cleaning)
                current_varnas, _ = ItSanjnaEngine.run_it_sanjna_prakaran(
                    current_varnas, "रुँ", UpadeshaType.VIBHAKTI
                )
                prev_str = add_history("१.३.२ (रुँ-लोपः)", current_varnas, prev_str)

                # 5. 8.3.15 (र् -> विसर्ग)
                current_varnas, s15 = apply_visarga_8_3_15(current_varnas)
                prev_str = add_history(s15, current_varnas, prev_str)

            # CASE D: STANDARD (RAMA / BAHUSHREYASI)
            else:
                res_v, s68 = apply_hal_nyab_6_1_68(list(current_varnas))
                if s68:
                    current_varnas = res_v
                    prev_str = add_history(s68, current_varnas, prev_str)
                elif intermediate_word.endswith('स्'):
                    current_varnas, s66 = apply_rutva_8_2_66(current_varnas)
                    prev_str = add_history(s66, current_varnas, prev_str)
                    current_varnas, _ = ItSanjnaEngine.run_it_sanjna_prakaran(
                        current_varnas, "रुँ", UpadeshaType.VIBHAKTI
                    )
                    prev_str = add_history("१.३.२ (रुँ-लोपः)", current_varnas, prev_str)
                    current_varnas, s15 = apply_visarga_8_3_15(current_varnas)
                    prev_str = add_history(s15, current_varnas, prev_str)

            # --- FINAL RENDERING ---
            st.table(history)
            final_output = sanskrit_varna_samyoga(current_varnas)
            st.markdown("---")
            st.header(f"✅ Final Result: {final_output}")
            st.balloons()
        else:
            st.warning("Could not establish Pada Sanjna.")
    else:
        st.error(f"❌ Rejection: {base_info['reason']}")