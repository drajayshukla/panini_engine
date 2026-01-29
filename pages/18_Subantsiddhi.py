import streamlit as st
from core.phonology import sanskrit_varna_vichhed, sanskrit_varna_samyoga
from core.it_sanjna_engine import ItSanjnaEngine
from core.upadesha_registry import UpadeshaType
from logic.pratipadika_engine import PratipadikaEngine
from logic.vidhi_engine import (
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


# --- 1.4.13 ANGA ENGINE ---
class AngaEngine:
    """
    Sutra: यस्मात्प्रत्ययविधिस्तदादि प्रत्ययेऽङ्गम् (१.४.१३)
    Handles the identification of the Aṅga (Stem) based on Paninian logic.
    """

    @staticmethod
    def yasmat_pratyaya_vidhi_1_4_13(full_varnas, pratyaya_len, manual_range=None):
        """Identifies the Aṅga segment of the varna list."""
        if manual_range:
            start_idx, end_idx = manual_range
            return full_varnas[start_idx:end_idx]
        return full_varnas[:-pratyaya_len] if len(full_varnas) > pratyaya_len else full_varnas

    @staticmethod
    def get_anga_antya(anga_varnas):
        """Extracts the final varna character of the Aṅga."""
        return anga_varnas[-1].char if anga_varnas else None


# --- UI HELPERS ---
def is_consonant(char):
    return char in "कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह"


def get_diff_highlight(old_str, new_str):
    if old_str == new_str:
        return new_str
    return f":red[{new_str}]"


st.set_page_config(page_title="Subant Siddhi Lab", layout="wide")
st.title("🔬 Subant Siddhi Lab: Sanskrit Word Generator")
st.markdown("---")

# १. Input Section
col1, col2 = st.columns([1, 1])
with col1:
    word_input = st.text_input("Enter Base Name (प्रातिपदिक)", value="राम")
with col2:
    sup_map = PratipadikaEngine.get_sup_vibhakti_map()
    vib_choice = st.selectbox("Select Vibhakti", list(sup_map.keys()))
    vac_choice = st.selectbox("Select Vachana", ["एकवचन", "द्विवचन", "बहुवचन"])
    selected_suffix = sup_map[vib_choice][vac_choice]

if word_input:
    base_info = PratipadikaEngine.identify_base(word_input)
    if base_info['is_pratipadika']:
        st.success(f"**Step 1: Identity Verified** - {base_info['sutra_applied']}")

        # STEP 2: SUFFIX & VICHHED
        combined_raw = word_input + selected_suffix
        varna_list = sanskrit_varna_vichhed(combined_raw)

        # STEP 3: IT-SANJNA & LOPA
        clean_varnas, it_tags = ItSanjnaEngine.run_it_sanjna_prakaran(
            varna_list, combined_raw, source_type=UpadeshaType.VIBHAKTI
        )
        intermediate_word = sanskrit_varna_samyoga(clean_varnas)

        # STEP 4: ANGA DEFINITION (Manual Override 1.4.13)
        st.subheader("✂️ Aṅga Definition (१.४.१३)")
        full_chars = [v.char for v in clean_varnas]
        suffix_len = len(sanskrit_varna_vichhed(selected_suffix))

        varna_indices = list(range(len(full_chars) + 1))
        anga_indices = st.select_slider(
            "Define Aṅga Boundary (यस्मात्प्रत्ययविधिस्तदादि प्रत्ययेऽङ्गम्)",
            options=varna_indices,
            value=(0, len(full_chars) - suffix_len),
            format_func=lambda x: full_chars[x] if x < len(full_chars) else "END"
        )

        # Display the split visually
        anga_display = "".join(full_chars[anga_indices[0]:anga_indices[1]])
        suffix_display = "".join(full_chars[anga_indices[1]:])
        st.markdown(f"**Aṅga:** `:blue[{anga_display}]` | **Suffix:** `:orange[{suffix_display}]`")

        # STEP 5: PADA SANJNA
        is_pada, pada_msg = check_pada_sanjna_1_4_14(clean_varnas, UpadeshaType.VIBHAKTI)

        if is_pada:
            st.info(f"✨ **Step 5: Pada Sanjna established** - {pada_msg}")
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


            prev_str = add_history("Initial", current_varnas, prev_str, "Post-Cleaning")

            # PROCESS ANGA ANTYA FOR GATING RULES
            anga_segment = AngaEngine.yasmat_pratyaya_vidhi_1_4_13(
                current_varnas, suffix_len, anga_indices
            )
            antya_char = AngaEngine.get_anga_antya(anga_segment)

            # --- BRANCHING LOGIC ---

            # CASE A: KROSTU
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

            # CASE B/C: KINSHIP & AGENT
            elif any(x in word_input for x in ["जामातृ", "पितृ", "भ्रातृ", "नृ", "मातृ", "स्वसृ", "धातृ", "कर्तृ"]):
                current_varnas, s94 = apply_anang_7_1_94(current_varnas)
                prev_str = add_history(s94, current_varnas, prev_str, "अनङ्-आदेशः")
                current_varnas = [v for v in current_varnas if v.char != 'ङ्']
                prev_str = add_history("१.३.३", current_varnas, prev_str, "ङ्-लोपः")

                if any(x in word_input for x in ["स्वसृ", "धातृ", "कर्तृ"]):
                    current_varnas, s11 = apply_upadha_dirgha_6_4_11(current_varnas)
                    prev_str = add_history(s11, current_varnas, prev_str, "उपधा-दीर्घः (६.४.११)")
                else:
                    current_varnas, s8 = apply_upadha_dirgha_6_4_8(current_varnas)
                    prev_str = add_history(s8, current_varnas, prev_str, "उपधा-दीर्घः (६.४.८)")

                current_varnas, s68 = apply_hal_nyab_6_1_68(current_varnas)
                prev_str = add_history(s68, current_varnas, prev_str, "सु-लोपः")
                current_varnas, s7 = apply_nalopa_8_2_7(current_varnas)
                prev_str = add_history(s7, current_varnas, prev_str, "न-लोपः")

            # CASE D: NEUTER LONG-VOWEL (श्रीपा)
            elif word_input == "श्रीपा":
                current_varnas, s47 = apply_hrasva_napumsaka_1_2_47(current_varnas)
                prev_str = add_history(s47, current_varnas, prev_str, "ह्रस्वो नपुंसके")
                current_varnas, s24 = apply_ato_am_7_1_24(current_varnas)
                prev_str = add_history(s24, current_varnas, prev_str, "अतोऽम्")
                current_varnas, s107 = apply_ami_purvah_6_1_107(current_varnas)
                prev_str = add_history(s107, current_varnas, prev_str, "पूर्वरूप एकादेशः")

            # CASE E: PRONOUN (अन्यत्)
            elif any(x == word_input for x in ["अन्य", "इतर", "कतर", "कतम"]):
                current_varnas, s25 = apply_add_7_1_25(current_varnas)
                prev_str = add_history(s25, current_varnas, prev_str, "अद्ड्-आदेशः")
                current_varnas, s143 = apply_ti_lopa_6_4_143(current_varnas)
                prev_str = add_history(s143, current_varnas, prev_str, "टेः (टि-लोपः)")
                current_varnas, s56 = apply_chartva_8_4_56(current_varnas)
                prev_str = add_history(s56, current_varnas, prev_str, "वाऽवसाने (चर्त्वम्)")

            # CASE F/G: GO & RAI
            elif word_input in ["गो", "रै"]:
                if word_input == "गो":
                    current_varnas, s90 = apply_goto_nit_7_1_90(current_varnas)
                    prev_str = add_history(s90, current_varnas, prev_str, "णिद्वद्भावः")
                    current_varnas, s115 = apply_vṛddhi_7_2_115(current_varnas)
                    prev_str = add_history(s115, current_varnas, prev_str, "वृद्धिः")
                else:
                    current_varnas, s85 = apply_rayo_hali_7_2_85(current_varnas)
                    prev_str = add_history(s85, current_varnas, prev_str, "आकारादेशः")

                current_varnas, s66 = apply_rutva_8_2_66(current_varnas)
                prev_str = add_history(s66, current_varnas, prev_str, "रुत्वम्")
                current_varnas, s15 = apply_visarga_8_3_15(current_varnas)
                prev_str = add_history(s15, current_varnas, prev_str, "विसर्गः")

            # CASE H: STANDARD (Rama, Gauri, Ramaa, Jnanam)
            else:
                # 1. Ato'm Check for Neuter a-anta
                if word_input in ["ज्ञान", "फल", "वन"]:
                    current_varnas, s24 = apply_ato_am_7_1_24(current_varnas)
                    prev_str = add_history(s24, current_varnas, prev_str, "अतोऽम्")
                    current_varnas, s107 = apply_ami_purvah_6_1_107(current_varnas)
                    prev_str = add_history(s107, current_varnas, prev_str, "पूर्वरूपम्")

                # 2. Strict Lopa Check based on Anga-Antya (6.1.68)
                elif antya_char in ['आ', 'ई', 'ऊ'] or is_consonant(antya_char):
                    if word_input not in ["लक्ष्मी", "तन्त्री", "तरी", "गोपा"]:
                        res_v, s68 = apply_hal_nyab_6_1_68(current_varnas)
                        if s68:
                            current_varnas = res_v
                            prev_str = add_history(s68, current_varnas, prev_str, "हल्ङ्याब्-लोपः")

                # 3. Visarga Path if suffix 's' survived (Rāma, Kavi)
                if current_varnas[-1].char == 'स्':
                    current_varnas, s66 = apply_rutva_8_2_66(current_varnas)
                    prev_str = add_history(s66, current_varnas, prev_str, "रुत्वम्")
                    current_varnas, _ = ItSanjnaEngine.run_it_sanjna_prakaran(
                        current_varnas, "रुँ", UpadeshaType.VIBHAKTI
                    )
                    prev_str = add_history("१.३.२", current_varnas, prev_str, "इत्-लोपः (रुँ->र्)")
                    current_varnas, s15 = apply_visarga_8_3_15(current_varnas)
                    prev_str = add_history(s15, current_varnas, prev_str, "विसर्गः")

            # --- FINAL UI RENDERING ---
            st.subheader("🧪 Step-by-Step Surgical Derivation")
            head_cols = st.columns([0.5, 1.5, 3, 1.5, 2])
            head_cols[0].caption("Step")
            head_cols[1].caption("Sutra")
            head_cols[2].caption("Varna Vichhed")
            head_cols[3].caption("Current Form")
            head_cols[4].caption("Transformation")
            st.divider()

            for row in history:
                with st.container():
                    cols = st.columns([0.5, 1.5, 3, 1.5, 2])
                    cols[0].write(f"**{row['step']}**")
                    cols[1].info(f"**{row['sutra']}**")
                    cols[2].markdown(row['vichhed'])
                    cols[3].subheader(row['highlighted'])
                    if row['change'] != "---":
                        cols[4].success(f"**{row['change']}**")
                    else:
                        cols[4].write("---")

            final_output = sanskrit_varna_samyoga(current_varnas)
            st.markdown("---")
            st.success(f"### ✅ Final Result: {final_output}")
            st.balloons()

        else:
            st.warning(f"⚠️ **Pada Sanjna Not Established**: {pada_msg}")
    else:
        st.error(f"❌ **Rejection**: {base_info.get('reason', 'Invalid Pratipadika')}")