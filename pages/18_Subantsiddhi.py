import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Subant Siddhi Lab", page_icon="🔬", layout="wide")

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
    return sanskrit_varna_samyoga(varna_list)


def get_diff_highlight(old_str, new_str):
    if old_str == new_str: return new_str
    return f":red[{new_str}]"


# --- 4. EXTENDED VIDHI (Local Extensions) ---
class ExtendedVidhi(VidhiEngine):
    @staticmethod
    def apply_ami_purvah_6_1_107(varna_list):
        if len(varna_list) > 1 and varna_list[-1].char == 'अ' and varna_list[-2].char == 'अ':
            varna_list.pop()
            return varna_list, "६.१.१०७ (अमि पूर्वः)"
        return varna_list, None

    @staticmethod
    def apply_nalopa_8_2_7(varna_list):
        if varna_list and varna_list[-1].char == 'न्':
            varna_list.pop()
            return varna_list, "८.२.७ (न-लोपः)"
        return varna_list, None


# --- 5. MAIN APP LOGIC ---
st.title("🔬 Subant Siddhi Lab: Sanskrit Word Generator")
st.markdown("### PAS-5.0 Engine | Zone 3 (Morphology)")
st.markdown("---")

col1, col2 = st.columns([1, 1])
with col1:
    word_input = st.text_input("Enter Base Name (प्रातिपदिक)", value="गीत")
with col2:
    sup_map = PratipadikaEngine.get_sup_vibhakti_map()
    vib_choice = st.selectbox("Select Vibhakti", list(sup_map.keys()))
    vac_choice = st.selectbox("Select Vachana", ["एक", "द्वि", "बहु"])
    try:
        selected_suffix = sup_map[vib_choice][vac_choice]
    except:
        selected_suffix = "सुँ"

if word_input:
    # A. VALIDATION
    base_info = PratipadikaEngine.identify_base(word_input)

    if base_info['is_pratipadika']:
        st.success(f"**Step 1: Identity Verified** - {base_info['sutra_applied']}")

        # --- B. ARCHITECTURAL FIX: SPLIT PROCESSING ---
        # 1. Base: Raw Phonology ONLY (No It-Sanjna)
        # [CRITICAL]: This protects 'Geeta' from 1.3.8 Lashakvataddhite
        base_varnas = ad(word_input)

        # 2. Suffix: Phonology + It-Sanjna (Cleaning)
        # [CRITICAL]: 1.3.8 applies HERE
        suffix_raw_varnas = ad(selected_suffix)
        clean_suffix, it_tags = ItEngine.run_it_prakaran(
            suffix_raw_varnas, source_type=UpadeshaType.VIBHAKTI
        )

        # 3. Combine Clean Parts
        combined_varnas = base_varnas + clean_suffix

        # --- C. HISTORY & TRACING ---
        history = []

        # Show Split View
        base_disp = get_readable_form(base_varnas)
        suffix_clean_disp = get_readable_form(clean_suffix)

        history.append({
            "step": 1,
            "sutra": "Samyoga (Joining)",
            "vichhed": f"{base_disp} + {suffix_clean_disp}",
            "form": get_readable_form(combined_varnas),
            "highlighted": get_readable_form(combined_varnas),
            "change": "Base + Clean Suffix"
        })

        current_varnas = list(combined_varnas)
        prev_str = get_readable_form(current_varnas)


        def add_trace(sutra, varnas, prev_s, change_desc):
            curr_s = get_readable_form(varnas)
            vichhed_disp = " + ".join([f"{v.char}" for v in varnas])
            history.append({
                "step": len(history) + 1,
                "sutra": sutra,
                "vichhed": vichhed_disp,
                "form": curr_s,
                "highlighted": get_diff_highlight(prev_s, curr_s),
                "change": change_desc
            })
            return curr_s


        # D. ANGA DEFINITION
        st.subheader("✂️ Aṅga Definition (१.४.१३)")
        split_index = len(base_varnas)
        full_chars = [v.char for v in current_varnas]

        c1, c2 = st.columns([2, 1])
        with c1:
            user_indices = st.slider("Aṅga Boundary", 0, len(full_chars), (0, split_index))

        anga_part = current_varnas[user_indices[0]:user_indices[1]]
        suffix_part = current_varnas[user_indices[1]:]

        with c2:
            st.markdown(f"**Aṅga:** `:blue[{get_readable_form(anga_part)}]`")
            st.markdown(f"**Suffix:** `:orange[{get_readable_form(suffix_part)}]`")

        # E. PADA SANJNA & VIDHI
        is_pada, pada_msg = apply_1_4_14_pada(current_varnas, UpadeshaType.VIBHAKTI)

        if is_pada:
            process_list = list(current_varnas)

            # 1. 7.1.24 Ato Am (Neut)
            if word_input in ["फल", "ज्ञान", "वन", "गीत"] and selected_suffix in ["सुँ", "अम्"]:
                process_list, s24 = VidhiEngine.ato_am_7_1_24(process_list)
                if s24: prev_str = add_trace("७.१.२४", process_list, prev_str, "अतोऽम्")
                process_list, s107 = ExtendedVidhi.apply_ami_purvah_6_1_107(process_list)
                if s107: prev_str = add_trace("६.१.१०७", process_list, prev_str, "पूर्वरूपम्")

            # 2. 6.1.107 Ami Purvah (Masc Acc)
            if selected_suffix == "अम्" and not s24:  # Avoid double fire
                process_list, s107 = ExtendedVidhi.apply_ami_purvah_6_1_107(process_list)
                if s107: prev_str = add_trace("६.१.१०७", process_list, prev_str, "अमि पूर्वः")

            # 3. 6.4.8 Upadha Dirgha
            if "राजन्" in word_input or word_input.endswith("न्"):
                if selected_suffix in ["सुँ", "औ", "जस्", "अम्", "औट्"]:
                    process_list, s8 = VidhiEngine.apply_upadha_dirgha_6_4_8(process_list)
                    if s8: prev_str = add_trace("६.४.८", process_list, prev_str, "उपधा-दीर्घः")

            # 4. 6.1.68 Hal-Nyab-Lopa
            stem_ends_in_hal = not anga_part[-1].is_vowel if anga_part else False
            stem_ends_in_fem = anga_part[-1].char in ['आ', 'ई', 'ऊ'] if anga_part else False

            if (stem_ends_in_hal or stem_ends_in_fem) and word_input not in ["लक्ष्मी"]:
                if suffix_part and len(suffix_part) == 1 and suffix_part[0].char == 'स्':
                    process_list, s68 = VidhiEngine.apply_hal_nyab_6_1_68(process_list)
                    if s68: prev_str = add_trace("६.१.६८", process_list, prev_str, "हल्ङ्याब्-लोपः")

            # 5. 8.2.7 Nalopa
            process_list, s7 = ExtendedVidhi.apply_nalopa_8_2_7(process_list)
            if s7: prev_str = add_trace("८.२.७", process_list, prev_str, "न-लोपः")

            # 6. 8.2.66 Rutva
            if process_list and process_list[-1].char == 'स्':
                process_list, s66 = VidhiEngine.apply_rutva_8_2_66(process_list)
                if s66: prev_str = add_trace("८.२.६६", process_list, prev_str, "ससजुषोः रुः")

            # 7. 8.3.15 Visarga
            if process_list and process_list[-1].char == 'र्':
                process_list, s15 = VidhiEngine.apply_visarga_8_3_15(process_list)
                if s15: prev_str = add_trace("८.३.१५", process_list, prev_str, "खरवसानयोर्विसर्जनीयः")

            # --- RENDER ---
            st.subheader("🧪 Step-by-Step Surgical Derivation")
            if history:
                h_cols = st.columns([0.5, 1, 3, 1.5, 2])
                h_cols[0].markdown("**#**")
                h_cols[1].markdown("**Sutra**")
                h_cols[2].markdown("**Vichhed**")
                h_cols[3].markdown("**Form**")
                h_cols[4].markdown("**Change**")
                st.divider()
                for row in history:
                    with st.container():
                        c = st.columns([0.5, 1, 3, 1.5, 2])
                        c[0].write(f"{row['step']}")
                        c[1].info(f"{row['sutra']}")
                        c[2].code(row['vichhed'], language="text")
                        c[3].markdown(f"### {row['highlighted']}")
                        c[4].success(row['change'])
                        st.divider()

            final_output = get_readable_form(process_list)
            st.markdown("---")
            r1, r2 = st.columns(2)
            r1.metric("Input", word_input)
            r2.metric("Siddha Output", final_output)
            st.balloons()

    else:
        st.error(f"❌ Rejection: {base_info.get('reason')}")