# pages/18_Subantsiddhi2.py
import streamlit as st
from core.phonology import ad, sanskrit_varna_samyoga
from logic.it_engine import ItEngine
from core.upadesha_registry import UpadeshaType
from logic.pratipadika_engine import PratipadikaEngine
from logic.sanjna_rules import check_pada_sanjna_1_4_14

# Import Vidhi logic (Ensure these exist in your logic/vidhi_engine.py)
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


# --- 1.4.13 ANGA ENGINE (Local Helper) ---
class AngaEngine:
    """
    Sutra: यस्मात्प्रत्ययविधिस्तदादि प्रत्ययेऽङ्गम् (१.४.१३)
    Handles the identification of the Aṅga (Stem).
    """

    @staticmethod
    def identify_anga(full_varnas, pratyaya_len, manual_range=None):
        if manual_range:
            start_idx, end_idx = manual_range
            return full_varnas[start_idx:end_idx]

        # Default: Everything before the suffix is Anga
        if len(full_varnas) > pratyaya_len:
            return full_varnas[:-pratyaya_len]
        return full_varnas

    @staticmethod
    def get_anga_antya(anga_varnas):
        return anga_varnas[-1].char if anga_varnas else None


# --- UI CONFIG ---
st.set_page_config(page_title="Subant Siddhi Lab", layout="wide")
st.title("🔬 Subant Siddhi Lab: Sanskrit Word Generator")
st.caption("Prakriyā Visualizer for Sutra 4.1.2 (Svaujasamauṭ...)")
st.markdown("---")


# --- UI HELPERS ---
def highlight_diff(old_str, new_str):
    if old_str == new_str:
        return new_str
    return f":red[{new_str}]"


# --- INPUT SECTION ---
col1, col2 = st.columns([1, 1])

with col1:
    word_input = st.text_input("Enter Base Name (प्रातिपदिक)", value="राम",
                               help="Enter a valid Pratipadika (e.g. राम, क्रोष्टु, ज्ञान)")

with col2:
    sup_map = PratipadikaEngine.get_sup_vibhakti_map()
    vib_choice = st.selectbox("Select Vibhakti (Case)", list(sup_map.keys()))

    #

    vac_choice = st.selectbox("Select Vachana (Number)", ["एक", "द्वि", "बहु"])
    selected_suffix = sup_map[vib_choice][vac_choice]
    st.info(f"Selected Suffix: **{selected_suffix}**")

# --- PROCESSING ---
if word_input:
    # 1. PRATIPADIKA VALIDATION
    base_info = PratipadikaEngine.identify_base(word_input)

    if base_info['is_pratipadika']:
        st.success(f"**Step 1: Identity Verified** - {base_info['sutra_applied']}")

        # 2. VICHHED & CLEANING
        # Critical: Vichhed separately to avoid accidental Sandhi
        base_varnas = ad(word_input)
        suffix_varnas = ad(selected_suffix)

        # Clean Suffix (It-Prakaran)
        clean_suffix, it_trace = ItEngine.run_it_prakaran(suffix_varnas, UpadeshaType.PRATYAYA)

        # Combine
        combined_varnas = base_varnas + clean_suffix
        intermediate_word = sanskrit_varna_samyoga(combined_varnas)

        # 3. ANGA DEFINITION (1.4.13)
        st.subheader("✂️ Aṅga Definition (१.४.१३)")

        full_chars = [v.char for v in combined_varnas]
        suffix_len = len(clean_suffix)
        default_split = len(full_chars) - suffix_len

        varna_indices = list(range(len(full_chars) + 1))

        # Interactive Slider for Anga
        anga_indices = st.select_slider(
            "Verify Aṅga Boundary (Slide to adjust)",
            options=varna_indices,
            value=(0, default_split),
            format_func=lambda x: full_chars[x] if x < len(full_chars) else "|"
        )

        # Visual Feedback
        anga_part = "".join(full_chars[anga_indices[0]:anga_indices[1]])
        suffix_part = "".join(full_chars[anga_indices[1]:])
        st.markdown(f"**Aṅga:** `:blue[{anga_part}]` + **Suffix:** `:orange[{suffix_part}]`")

        # 4. PADA SANJNA CHECK
        is_pada, pada_msg = check_pada_sanjna_1_4_14(combined_varnas, UpadeshaType.VIBHAKTI)

        if is_pada:
            st.info(f"✨ **Step 5: Pada Sanjna established** - {pada_msg}")

            # --- DERIVATION HISTORY TRACKER ---
            history = []
            current_varnas = list(combined_varnas)
            prev_str = intermediate_word


            def add_history(sutra, varnas, p_str, change_desc):
                f_str = sanskrit_varna_samyoga(varnas)
                history.append({
                    "step": len(history) + 1,
                    "sutra": sutra,
                    "form": f_str,
                    "diff": highlight_diff(p_str, f_str),
                    "desc": change_desc
                })
                return f_str


            # Initial State
            add_history("Initial", current_varnas, prev_str, "Base + Suffix (Cleaned)")

            # Anga Analysis for Rules
            anga_segment = AngaEngine.identify_anga(current_varnas, suffix_len, anga_indices)
            antya_char = AngaEngine.get_anga_antya(anga_segment)

            # === VIDHI PIPELINE (BRANCHING LOGIC) ===

            # A. Irregular Bases (Apavada)
            if "क्रोष्टु" in word_input:
                current_varnas, s95 = apply_trijvadbhava_7_1_95(current_varnas)
                prev_str = add_history(s95, current_varnas, prev_str, "Trj-vadbhava (Becomes Kroṣṭṛ)")

                # Now it behaves like Karta/Pita (R-ending)
                current_varnas, s94 = apply_anang_7_1_94(current_varnas)
                prev_str = add_history(s94, current_varnas, prev_str, "Anang-Adesha (ṛ -> an)")

                # 1.3.3 Halantyam on 'ng' of Anang
                current_varnas = [v for v in current_varnas if v.char != 'ङ्']
                prev_str = add_history("१.३.३", current_varnas, prev_str, "It-Lopa (ṅ)")

                current_varnas, s11 = apply_upadha_dirgha_6_4_11(current_varnas)
                prev_str = add_history(s11, current_varnas, prev_str, "Upadha Dirgha (a -> ā)")

                current_varnas, s68 = apply_hal_nyab_6_1_68(current_varnas)
                prev_str = add_history(s68, current_varnas, prev_str, "Aprikta Lopa (Suffix s removed)")

                current_varnas, s7 = apply_nalopa_8_2_7(current_varnas)
                prev_str = add_history(s7, current_varnas, prev_str, "Nalopa (Final n removed)")

            # B. Kinship Terms (R-ending: Pitr, Matr)
            elif any(x in word_input for x in ["जामातृ", "पितृ", "भ्रातृ", "नृ", "मातृ", "स्वसृ", "धातृ", "कर्तृ"]):
                current_varnas, s94 = apply_anang_7_1_94(current_varnas)
                prev_str = add_history(s94, current_varnas, prev_str, "Anang-Adesha")

                # Cleaning 'Anang'
                current_varnas = [v for v in current_varnas if v.char != 'ङ्']
                prev_str = add_history("१.३.३", current_varnas, prev_str, "It-Lopa (ṅ)")

                if any(x in word_input for x in ["स्वसृ", "धातृ", "कर्तृ", "नप्तृ"]):
                    current_varnas, s11 = apply_upadha_dirgha_6_4_11(current_varnas)
                    prev_str = add_history(s11, current_varnas, prev_str, "Upadha Dirgha (Aptṛn...)")
                else:
                    current_varnas, s8 = apply_upadha_dirgha_6_4_8(current_varnas)
                    prev_str = add_history(s8, current_varnas, prev_str, "Upadha Dirgha (Sarvanamasthane...)")

                current_varnas, s68 = apply_hal_nyab_6_1_68(current_varnas)
                prev_str = add_history(s68, current_varnas, prev_str, "Hal-Nyabbhyo (Suffix Deleted)")

                current_varnas, s7 = apply_nalopa_8_2_7(current_varnas)
                prev_str = add_history(s7, current_varnas, prev_str, "Nalopa (Final n Deleted)")

            # C. Neuter Bases (Shripa - World Protector)
            elif word_input == "श्रीपा":
                current_varnas, s47 = apply_hrasva_napumsaka_1_2_47(current_varnas)
                prev_str = add_history(s47, current_varnas, prev_str, "Hrasva Napumsake")

                current_varnas, s24 = apply_ato_am_7_1_24(current_varnas)
                prev_str = add_history(s24, current_varnas, prev_str, "Ato'm (Su -> Am)")

                current_varnas, s107 = apply_ami_purvah_6_1_107(current_varnas)
                prev_str = add_history(s107, current_varnas, prev_str, "Ami Purvah (Sandhi)")

            # D. Pronouns (Tyadadi Gana)
            elif any(x == word_input for x in ["अन्य", "इतर", "कतर", "कतम", "तद्", "यद्"]):
                current_varnas, s25 = apply_add_7_1_25(current_varnas)
                prev_str = add_history(s25, current_varnas, prev_str, "Add-Adesha (Neuter)")

                current_varnas, s143 = apply_ti_lopa_6_4_143(current_varnas)
                prev_str = add_history(s143, current_varnas, prev_str, "Ti-Lopa")

                current_varnas, s56 = apply_chartva_8_4_56(current_varnas)
                prev_str = add_history(s56, current_varnas, prev_str, "Chartva (d -> t)")

            # E. Go / Rai (Irregular Vowels)
            elif word_input in ["गो", "रै"]:
                if word_input == "गो":
                    current_varnas, s90 = apply_goto_nit_7_1_90(current_varnas)
                    prev_str = add_history(s90, current_varnas, prev_str, "Goto Nit (Gauh)")
                    current_varnas, s115 = apply_vṛddhi_7_2_115(current_varnas)
                    prev_str = add_history(s115, current_varnas, prev_str, "Vriddhi")
                else:
                    current_varnas, s85 = apply_rayo_hali_7_2_85(current_varnas)
                    prev_str = add_history(s85, current_varnas, prev_str, "Rayo Hali (Rāh)")

                # Standard Visarga Finish
                current_varnas, s66 = apply_rutva_8_2_66(current_varnas)
                prev_str = add_history(s66, current_varnas, prev_str, "Sasajusho Ru (s -> ru)")

                current_varnas, _ = ItEngine.run_it_prakaran(current_varnas, UpadeshaType.VIBHAKTI)
                prev_str = add_history("१.३.२", current_varnas, prev_str, "Upadeshe'janunasika (u removed)")

                current_varnas, s15 = apply_visarga_8_3_15(current_varnas)
                prev_str = add_history(s15, current_varnas, prev_str, "Kharavasanayor (r -> ḥ)")

            # F. General Cases (Rama, Hari, Guru, Lata, Gauri)
            else:
                # 1. Neuter A-ending (Jñānam)
                if antya_char == 'अ' and word_input in ["ज्ञान", "फल", "वन", "पुष्प"]:
                    current_varnas, s24 = apply_ato_am_7_1_24(current_varnas)
                    prev_str = add_history(s24, current_varnas, prev_str, "Ato'm (Su -> Am)")
                    current_varnas, s107 = apply_ami_purvah_6_1_107(current_varnas)
                    prev_str = add_history(s107, current_varnas, prev_str, "Ami Purvah")

                # 2. Hal-Nyab Lopa (Feminities: Gauri, Lakshmi / Consonants: Rajan)
                # Logic: If suffix is 's' (Aprikta) and Stem ends in Hal or Ni/Ap
                elif clean_suffix and clean_suffix[0].char == 'स्' and len(clean_suffix) == 1:
                    # Check for 6.1.68 Applicability
                    is_halanta = ItEngine.is_halanta(anga_segment)  # Helper needs to exist
                    is_ni_ap = antya_char in ['ई', 'ऊ', 'आ']

                    if is_halanta or is_ni_ap:
                        # Exception: Lakshmi etc. do not take lopa
                        if word_input not in ["लक्ष्मी", "तन्त्री"]:
                            res_v, s68 = apply_hal_nyab_6_1_68(current_varnas)
                            if s68:
                                current_varnas = res_v
                                prev_str = add_history(s68, current_varnas, prev_str, "Hal-Nyabbhyo (Lopa)")

                # 3. Visarga Generation (Rama -> Ramah)
                # If 's' still exists at the end
                if current_varnas and current_varnas[-1].char == 'स्':
                    current_varnas, s66 = apply_rutva_8_2_66(current_varnas)
                    prev_str = add_history(s66, current_varnas, prev_str, "Sasajusho Ru (s -> ru)")

                    # Clean the 'u' from 'ru'
                    current_varnas, _ = ItEngine.run_it_prakaran(current_varnas, UpadeshaType.VIBHAKTI)
                    prev_str = add_history("१.३.२", current_varnas, prev_str, "Upadeshe... (u removed)")

                    current_varnas, s15 = apply_visarga_8_3_15(current_varnas)
                    prev_str = add_history(s15, current_varnas, prev_str, "Visarjaniya (r -> ḥ)")

            # --- RENDER TABLE ---
            st.subheader("🧪 Derivation Trace")
            st.table([
                {
                    "Step": x["step"],
                    "Sutra": x["sutra"],
                    "Form": x["form"],
                    "Description": x["desc"]
                } for x in history
            ])

            # Final Result
            final_output = sanskrit_varna_samyoga(current_varnas)
            st.success(f"### ✅ Final Result: {final_output}")
            st.balloons()

        else:
            st.warning(f"⚠️ **Pada Sanjna Not Established**: {pada_msg}")
    else:
        st.error(f"❌ **Rejection**: {base_info.get('reason', 'Invalid Pratipadika')}")