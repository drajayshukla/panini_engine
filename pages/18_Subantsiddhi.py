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
    apply_nalopa_8_2_7
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
    # --- STEP 1: AUTOMATIC VERIFICATION ---
    base_info = PratipadikaEngine.identify_base(word_input)

    if base_info['is_pratipadika']:
        st.success(f"**Step 1: Identity Verified** - {base_info['sutra_applied']}")
        if 'metadata' in base_info:
            meta = base_info['metadata']
            st.caption(
                f"✨ **Database Match:** {meta.get('artha_hin') or meta.get('artha')} | Linga: {meta.get('linga')}")

        st.markdown("---")

        # --- STEP 2: SUFFIX INJECTION (4.1.2) ---
        st.subheader(f"Step 2: Injection (Pratyaya: {selected_suffix})")
        combined_raw = word_input + selected_suffix
        varna_list = sanskrit_varna_vichhed(combined_raw)
        st.write(f"**{word_input} + {selected_suffix}** [४.१.२ स्वौजसमौट्...]")

        # --- STEP 3: IT-SANJNA & LOPA (1.3.2, 1.3.9) ---
        st.subheader("Step 3: It-Sanjna & Lopa (Cleaning)")
        clean_varnas, it_tags = ItSanjnaEngine.run_it_sanjna_prakaran(
            varna_list, combined_raw, source_type=UpadeshaType.VIBHAKTI
        )
        intermediate_word = sanskrit_varna_samyoga(clean_varnas)
        st.write(f"**→ {intermediate_word}** [१.३.२, १.३.९]")

        # --- STEP 4: PADA SANJNA (1.4.14) ---
        is_pada, pada_msg = check_pada_sanjna_1_4_14(clean_varnas, UpadeshaType.VIBHAKTI)

        if is_pada:
            st.info(f"✨ **Step 4: Pada Sanjna** - {pada_msg}")

            # --- STEP 5: FINAL PHONOLOGY & DEBUGGER ---
            st.subheader("Step 5: Process Tracing (Varna Debugger)")
            history = []
            current_varnas = list(clean_varnas)
            prev_str = intermediate_word

            # Initial State Entry
            history.append({
                "Sutra": "Initial (Post-Cleaning)",
                "Vichhed": [v.char for v in current_varnas],
                "Form": intermediate_word
            })

            # --- BRANCH A: SPECIAL STEM (Kroṣṭu Case) ---
            if "क्रोष्टु" in word_input:
                # 5a. Trijvadbhava (7.1.95)
                current_varnas, s95 = apply_trijvadbhava_7_1_95(current_varnas)
                new_str = sanskrit_varna_samyoga(current_varnas)
                history.append({"Sutra": s95, "Vichhed": [v.char for v in current_varnas],
                                "Form": get_diff_highlight(prev_str, new_str)})
                prev_str = new_str

                # 5b. Anang Substitution (7.1.94)
                current_varnas, s94 = apply_anang_7_1_94(current_varnas)
                new_str = sanskrit_varna_samyoga(current_varnas)
                history.append({"Sutra": s94, "Vichhed": [v.char for v in current_varnas],
                                "Form": get_diff_highlight(prev_str, new_str)})
                prev_str = new_str

                # 5c. Surgical ṅ removal (1.3.3)
                for i, v in enumerate(current_varnas):
                    if v.char == 'ङ्':
                        current_varnas.pop(i)
                        break
                new_str = sanskrit_varna_samyoga(current_varnas)
                history.append({"Sutra": "१.३.३ (हलन्त्यम् - ङ् इत्-लोपः)", "Vichhed": [v.char for v in current_varnas],
                                "Form": get_diff_highlight(prev_str, new_str)})
                prev_str = new_str

                # 5d. Upadha Dirgha (6.4.11)
                current_varnas, s11 = apply_upadha_dirgha_6_4_11(current_varnas)
                new_str = sanskrit_varna_samyoga(current_varnas)
                history.append({"Sutra": s11, "Vichhed": [v.char for v in current_varnas],
                                "Form": get_diff_highlight(prev_str, new_str)})
                prev_str = new_str

                # 5e. Apṛkta Lopa (6.1.68)
                current_varnas, s68 = apply_hal_nyab_6_1_68(current_varnas)
                new_str = sanskrit_varna_samyoga(current_varnas)
                history.append({"Sutra": s68, "Vichhed": [v.char for v in current_varnas],
                                "Form": get_diff_highlight(prev_str, new_str)})
                prev_str = new_str

                # 5f. N-Lopa (8.2.7)
                current_varnas, s7 = apply_nalopa_8_2_7(current_varnas)
                new_str = sanskrit_varna_samyoga(current_varnas)
                history.append({"Sutra": s7, "Vichhed": [v.char for v in current_varnas],
                                "Form": get_diff_highlight(prev_str, new_str)})

            # --- BRANCH B: APRUKTA LOPA (Bahuśreyasī Case) ---
            else:
                lopa_varnas, s68 = apply_hal_nyab_6_1_68(list(current_varnas))
                if s68:
                    current_varnas = lopa_varnas
                    new_str = sanskrit_varna_samyoga(current_varnas)
                    history.append({"Sutra": s68, "Vichhed": [v.char for v in current_varnas],
                                    "Form": get_diff_highlight(prev_str, new_str)})

                # --- BRANCH C: RUTVA & VISARGA (Standard Rāma Case) ---
                elif intermediate_word.endswith('स्'):
                    # 5g. Rutva (8.2.66)
                    current_varnas, s66 = apply_rutva_8_2_66(current_varnas)
                    new_str = sanskrit_varna_samyoga(current_varnas)
                    history.append({"Sutra": s66, "Vichhed": [v.char for v in current_varnas],
                                    "Form": get_diff_highlight(prev_str, new_str)})
                    prev_str = new_str

                    # 5h. ruँ-Lopa
                    current_varnas, _ = ItSanjnaEngine.run_it_sanjna_prakaran(current_varnas, "रुँ",
                                                                              UpadeshaType.VIBHAKTI)
                    new_str = sanskrit_varna_samyoga(current_varnas)
                    history.append({"Sutra": "१.३.२ (रुँ-लोपः)", "Vichhed": [v.char for v in current_varnas],
                                    "Form": get_diff_highlight(prev_str, new_str)})
                    prev_str = new_str

                    # 5i. Visarga (8.3.15)
                    current_varnas, s15 = apply_visarga_8_3_15(current_varnas)
                    new_str = sanskrit_varna_samyoga(current_varnas)
                    history.append({"Sutra": s15, "Vichhed": [v.char for v in current_varnas],
                                    "Form": get_diff_highlight(prev_str, new_str)})

            # Render the final Table
            st.table(history)

            final_output = sanskrit_varna_samyoga(current_varnas)
            st.markdown("---")
            st.header(f"✅ Final Result: {final_output}")
            st.balloons()
        else:
            st.warning("Could not establish Pada Sanjna. Word is still a Base/Pratyaya.")
    else:
        st.error(f"❌ Rejection: {base_info['reason']}")