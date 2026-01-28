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
    apply_vṛddhi_7_2_115,
    apply_rayo_hali_7_2_85,
    apply_ato_am_7_1_24,
    apply_ami_purvah_6_1_107,
apply_add_7_1_25,
apply_ti_lopa_6_4_143,
apply_chartva_8_4_56,
apply_hrasva_napumsaka_1_2_47
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


            def add_history(sutra, varnas, p_str, change_desc="---"):
                f_str = sanskrit_varna_samyoga(varnas)
                history.append({
                    "step": len(history),
                    "sutra": sutra if sutra else "Initial",
                    "vichhed": " + ".join([f"`{v.char}`" for v in varnas]),
                    "form": f_str,
                    "highlighted": get_diff_highlight(p_str, f_str),
                    "change": change_desc
                })
                return f_str


            # Initial State
            prev_str = add_history("Initial", current_varnas, prev_str, "Post-Cleaning")

            # --- BRANCHING LOGIC ---

            # CASE A: KROSTU (7.1.95)
            if "क्रोष्टु" in word_input:
                current_varnas, s95 = apply_trijvadbhava_7_1_95(current_varnas)
                prev_str = add_history(s95, current_varnas, prev_str, "त्रिज्वद्भावः")
                current_varnas, s94 = apply_anang_7_1_94(current_varnas)
                prev_str = add_history(s94, current_varnas, prev_str, "अनङ्-आदेशः")
                current_varnas = [v for v in current_varnas if v.char != 'ङ्']
                prev_str = add_history("१.३.३", current_varnas, prev_str, "इत्-लोपः (ङ्)")
                current_varnas, s11 = apply_upadha_dirgha_6_4_11(current_varnas)
                prev_str = add_history(s11, current_varnas, prev_str, "उपधा-दीर्घः")
                current_varnas, s68 = apply_hal_nyab_6_1_68(current_varnas)
                prev_str = add_history(s68, current_varnas, prev_str, "अपृक्त-लोपः")
                current_varnas, s7 = apply_nalopa_8_2_7(current_varnas)
                prev_str = add_history(s7, current_varnas, prev_str, "न-लोपः")

            # CASE B: KINSHIP TERMS (6.4.8)
            elif any(x in word_input for x in ["जामातृ", "पितृ", "भ्रातृ", "नृ", "मातृ"]):
                current_varnas, s94 = apply_anang_7_1_94(current_varnas)
                prev_str = add_history(s94, current_varnas, prev_str, "अनङ्-आदेशः")
                current_varnas = [v for v in current_varnas if v.char != 'ङ्']
                prev_str = add_history("१.३.३", current_varnas, prev_str, "इत्-लोपः (ङ्)")
                current_varnas, s8 = apply_upadha_dirgha_6_4_8(current_varnas)
                prev_str = add_history(s8, current_varnas, prev_str, "उपधा-दीर्घः")
                current_varnas, s68 = apply_hal_nyab_6_1_68(current_varnas)
                prev_str = add_history(s68, current_varnas, prev_str, "सु-लोपः")
                current_varnas, s7 = apply_nalopa_8_2_7(current_varnas)
                prev_str = add_history(s7, current_varnas, prev_str, "न-लोपः")

            # CASE C: AGENT NOUNS & SVASR (6.4.11)
            elif any(x in word_input for x in ["स्वसृ", "धातृ", "कर्तृ", "नप्तृ", "नेष्टृ"]):
                current_varnas, s94 = apply_anang_7_1_94(current_varnas)
                prev_str = add_history(s94, current_varnas, prev_str, "अनङ्-आदेशः")
                current_varnas = [v for v in current_varnas if v.char != 'ङ्']
                prev_str = add_history("१.३.३", current_varnas, prev_str, "इत्-लोपः (ङ्)")
                current_varnas, s11 = apply_upadha_dirgha_6_4_11(current_varnas)
                prev_str = add_history(s11, current_varnas, prev_str, "उपधा-दीर्घः")
                current_varnas, s68 = apply_hal_nyab_6_1_68(current_varnas)
                prev_str = add_history(s68, current_varnas, prev_str, "सु-लोपः")
                current_varnas, s7 = apply_nalopa_8_2_7(current_varnas)
                prev_str = add_history(s7, current_varnas, prev_str, "न-लोपः")

            # CASE D: NEUTER (Ato'm)
            elif word_input in ["ज्ञान", "फल", "वन", "पुष्प"]:
                current_varnas, s24 = apply_ato_am_7_1_24(current_varnas)
                prev_str = add_history(s24, current_varnas, prev_str, "सुँ -> अम् आदेशः")
                current_varnas, s107 = apply_ami_purvah_6_1_107(current_varnas)
                prev_str = add_history(s107, current_varnas, prev_str, "पूर्वरूप एकादेशः")

            # CASE E: GO (O-kanta)
            elif word_input == "गो":
                current_varnas, s90 = apply_goto_nit_7_1_90(current_varnas)
                prev_str = add_history(s90, current_varnas, prev_str, "णिद्वद्भावः")
                current_varnas, s115 = apply_vṛddhi_7_2_115(current_varnas)
                prev_str = add_history(s115, current_varnas, prev_str, "वृद्धिः (ओ->औ)")
                current_varnas, s66 = apply_rutva_8_2_66(current_varnas)
                prev_str = add_history(s66, current_varnas, prev_str, "रुत्वम्")
                current_varnas, s15 = apply_visarga_8_3_15(current_varnas)
                prev_str = add_history(s15, current_varnas, prev_str, "विसर्गः")

            # CASE F: RAI (Ai-kanta)
            elif word_input == "रै":
                current_varnas, s85 = apply_rayo_hali_7_2_85(current_varnas)
                prev_str = add_history(s85, current_varnas, prev_str, "आकारादेशः")
                current_varnas, s66 = apply_rutva_8_2_66(current_varnas)
                prev_str = add_history(s66, current_varnas, prev_str, "रुत्वम्")
                current_varnas, s15 = apply_visarga_8_3_15(current_varnas)
                prev_str = add_history(s15, current_varnas, prev_str, "विसर्गः")

            # CASE G: NON-NYAB ROOT NOUNS (Gopa, Lakshmi, Tantri)
            elif any(x == word_input for x in ["गोपा", "लक्ष्मी", "तन्त्री", "तरी"]):
                current_varnas, s66 = apply_rutva_8_2_66(current_varnas)
                prev_str = add_history(s66, current_varnas, prev_str, "रुत्वम्")
                current_varnas, s15 = apply_visarga_8_3_15(current_varnas)
                prev_str = add_history(s15, current_varnas, prev_str, "विसर्गः")
                # --- BRANCH O: NEUTER LONG-VOWEL STEMS (श्रीपा, प्रधी) ---
            elif word_input == "श्रीपा":
                # 1. 1.2.47 (श्रीपा -> श्रीप)
                current_varnas, s47 = apply_hrasva_napumsaka_1_2_47(current_varnas)
                prev_str = add_history(s47, current_varnas, prev_str, "ह्रस्वो नपुंसके")

                # 2. 7.1.24 (सुँ -> अम्)
                current_varnas, s24 = apply_ato_am_7_1_24(current_varnas)
                prev_str = add_history(s24, current_varnas, prev_str, "अतोऽम् (सुँ -> अम्)")

                # 3. 6.1.107 (अ + अ -> अ)
                current_varnas, s107 = apply_ami_purvah_6_1_107(current_varnas)
                prev_str = add_history(s107, current_varnas, prev_str, "अमि पूर्वः (पूर्वरूपम्)")
                # --- BRANCH N: PRONOUN SPECIAL (अन्य, इतर, कतर) ---
            elif any(x == word_input for x in ["अन्य", "इतर", "कतर", "कतम", "अन्यतर"]):
                # 1. 7.1.25 (सुँ -> अद्ड्)
                current_varnas, s25 = apply_add_7_1_25(current_varnas)
                prev_str = add_history(s25, current_varnas, prev_str, "सुँ -> अद्ड् आदेशः")

                # 2. 1.3.3 (ड्-लोपः)
                current_varnas = [v for v in current_varnas if v.char != 'ड्']
                prev_str = add_history("१.३.३", current_varnas, prev_str, "हलन्त्यम् - ड् लोपः")

                # 3. 6.4.143 (Ti-Lopa: अन्य + अद् -> अन्य् + अद्)
                current_varnas, s143 = apply_ti_lopa_6_4_143(current_varnas)
                prev_str = add_history(s143, current_varnas, prev_str, "टेः (टि-लोपः)")

                # 4. 8.4.56 (चर्त्वम्: द -> त)
                current_varnas, s56 = apply_chartva_8_4_56(current_varnas)
                prev_str = add_history(s56, current_varnas, prev_str, "वाऽवसाने (चर्त्वम्)")

            # CASE H: STANDARD (Rama, Gauri, Ramaa)
            else:
                res_v, s68 = apply_hal_nyab_6_1_68(current_varnas)
                if s68:
                    current_varnas = res_v
                    prev_str = add_history(s68, current_varnas, prev_str, "हल्ङ्याब्-लोपः")
                else:
                    current_varnas, s66 = apply_rutva_8_2_66(current_varnas)
                    prev_str = add_history(s66, current_varnas, prev_str, "रुत्वम्")
                    current_varnas, s15 = apply_visarga_8_3_15(current_varnas)
                    prev_str = add_history(s15, current_varnas, prev_str, "विसर्गः")

            # --- BEAUTIFUL UI RENDERING (Correctly Indented) ---
            st.subheader("🧪 Step-by-Step Surgical Derivation")

            # Header Row
            head_cols = st.columns([0.5, 1.5, 3, 1.5, 2])
            head_cols[0].caption("Step")
            head_cols[1].caption("Sutra")
            head_cols[2].caption("Varna Vichhed (Decomposition)")
            head_cols[3].caption("Current Form")
            head_cols[4].caption("Transformation")
            st.divider()

            # Iterate through history
            for row in history:
                with st.container():
                    cols = st.columns([0.5, 1.5, 3, 1.5, 2])
                    cols[0].write(f"**{row['step']}**")
                    cols[1].info(f"**{row['sutra']}**")
                    cols[2].markdown(row['vichhed'])
                    cols[3].subheader(row['highlighted'])

                    if row['change'] and row['change'] != "---":
                        cols[4].success(f"**{row['change']}**")
                    else:
                        cols[4].write("---")

            # --- FINAL RESULT AREA ---
            final_output = sanskrit_varna_samyoga(current_varnas)
            st.markdown("---")
            st.success(f"### ✅ Final Result: {final_output}")
            st.balloons()

        else:
            st.warning("⚠️ **Pada Sanjna Not Established**: The current combination does not satisfy 1.4.14.")
    else:
        st.error(f"❌ **Rejection**: {base_info.get('reason', 'Input is not a valid Pratipadika.')}")