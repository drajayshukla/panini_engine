import os
from pathlib import Path

def build_sanjna_prakaran():
    print("🏷️ BUILDING PHASE 3: SANJNA PRAKARANA (IT-KARYA)...")

    # ====================================================
    # 1. UPGRADE CORE: shared/anubandha.py
    # ====================================================
    # We add logic for 1.3.5 (Adirñi...), 1.3.7 (Cutu), 1.3.8 (Lashaku...)
    Path("shared/anubandha.py").write_text(r'''"""
FILE: shared/anubandha.py
PURPOSE: The "It-Sanjna" Engine. Identifies and removes meta-markers.
"""
from shared.varnas import Varna

class AnubandhaEngine:
    @staticmethod
    def process(varnas, context="General"):
        """
        Input: List of Varna objects
        Output: (Cleaned Varnas, Trace Log)
        """
        if not varnas: return [], []
        
        # Working copy
        res = list(varnas)
        trace = []
        
        # --- RULE 1.3.2: Upadeśe'janunāsika it ---
        # (Nasal Vowels are It)
        # Note: In our 'ad' function, we merged 'u~' into single units.
        # We just check for the nasal marker.
        temp_res = []
        for v in res:
            if 'ँ' in v.char:
                trace.append(f"1.3.2 Upadeśe'janunāsika it: {v.char} is It-Sanjna.")
                trace.append(f"1.3.9 Tasya Lopaḥ: {v.char} removed.")
                # Lopa (Do not add to temp_res)
            else:
                temp_res.append(v)
        res = temp_res
        
        # --- RULE 1.3.3: Halantyam ---
        # (Final Consonant is It)
        if res and res[-1].is_consonant:
            last = res[-1].char
            
            # EXCEPTION 1.3.4: Na Vibhaktau Tusmāḥ
            # (t, th, d, dh, n, s, m are NOT It in Vibhakti)
            tusma = ['त्', 'थ्', 'द्', 'ध्', 'न्', 'स्', 'म्']
            if context == "Vibhakti" and last in tusma:
                trace.append(f"1.3.4 Na Vibhaktau Tusmāḥ: {last} is SAVED from It-Sanjna.")
            else:
                trace.append(f"1.3.3 Halantyam: {last} is It-Sanjna.")
                trace.append(f"1.3.9 Tasya Lopaḥ: {last} removed.")
                res.pop() # Remove last

        # --- INITIAL RULES (Adi) ---
        if res:
            first = res[0].char.replace('्', '') # Remove virama for checking
            
            # RULE 1.3.5: Ādirñiṭuḍavaḥ (ñi, ṭu, ḍu at start of Dhatu)
            if context == "Dhatu":
                if first == 'ञ' and len(res)>1 and 'इ' in res[1].char:
                     # e.g., Ñi-Dhrish
                     trace.append(f"1.3.5 Ādirñiṭuḍavaḥ: Ñi is It-Sanjna.")
                     res = res[2:] # Remove Ñi
                elif first == 'ट' and len(res)>1 and 'उ' in res[1].char:
                     trace.append(f"1.3.5 Ādirñiṭuḍavaḥ: Ṭu is It-Sanjna.")
                     res = res[2:]
                elif first == 'ड' and len(res)>1 and 'उ' in res[1].char:
                     trace.append(f"1.3.5 Ādirñiṭuḍavaḥ: Ḍu is It-Sanjna (e.g. Ḍukṛñ).")
                     res = res[2:] # Remove Du

            # RULE 1.3.7: Cuṭū (Cu, Tu at start of Pratyaya)
            elif context == "Pratyaya":
                # Cu = c, ch, j, jh, ñ
                # Tu = ṭ, ṭh, ḍ, ḍh, ṇ
                cu_group = ['च', 'छ', 'ज', 'झ', 'ञ']
                tu_group = ['ट', 'ठ', 'ड', 'ढ', 'ण']
                
                if first in cu_group or first in tu_group:
                    trace.append(f"1.3.7 Cuṭū: {res[0].char} is It-Sanjna.")
                    trace.append(f"1.3.9 Tasya Lopaḥ: {res[0].char} removed.")
                    res.pop(0)

            # RULE 1.3.8: Laśakvataddhite (L, S, K-varga at start of Pratyaya)
            # Exception: Taddhita pratyayas are excluded (not handled here yet)
            if context == "Pratyaya" and res:
                # Re-check first after potential 1.3.7 removal
                first = res[0].char.replace('्', '')
                ku_group = ['क', 'ख', 'ग', 'घ', 'ङ']
                if first == 'ल' or first == 'श' or first in ku_group:
                    trace.append(f"1.3.8 Laśakvataddhite: {res[0].char} is It-Sanjna.")
                    trace.append(f"1.3.9 Tasya Lopaḥ: {res[0].char} removed.")
                    res.pop(0)

        return res, trace
''', encoding='utf-8')
    print("✅ UPDATED: shared/anubandha.py (Added Rules 1.3.4, 1.3.5, 1.3.7, 1.3.8)")

    # ====================================================
    # 2. CREATE PAGE: pages/3_🏷️_Sanjna_Lab.py
    # ====================================================
    page_code = r'''import streamlit as st
import sys
import os

# --- PATH HACK ---
sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared.varnas import ad, join
from shared.anubandha import AnubandhaEngine

st.set_page_config(page_title="Sanjna Lab", page_icon="🏷️", layout="wide")

st.markdown("""
<style>
    .it-box { background:#ffebee; padding:10px; border-radius:5px; border-left:4px solid #c62828; margin-bottom:5px; }
    .save-box { background:#e8f5e9; padding:10px; border-radius:5px; border-left:4px solid #2e7d32; margin-bottom:5px; }
    .final-res { font-size:1.5em; font-weight:bold; color:#2c3e50; }
</style>
""", unsafe_allow_html=True)

st.title("🏷️ Sanjñā Prakaraṇa (It-Kārya)")
st.caption("The Machine that Cleans the Code: It-Tagging & Lopa")

# 1. INPUT
c1, c2 = st.columns([2, 1])
with c1:
    raw_input = st.text_input("Upadeśa (Raw Input)", value="डुकृञ्")
    st.caption("Examples: डुकृञ् (Dhatu), जस् (Pratyaya), सुँ (Pratyaya), शप् (Vikarna)")

with c2:
    context = st.selectbox("Context (Sanjna Scope)", 
                           ["Dhatu", "Pratyaya", "Vibhakti", "General"],
                           index=0)
    st.caption("Different rules apply to Dhatus vs Pratyayas.")

if st.button("Run It-Prakriyā", type="primary"):
    # A. Varna Viccheda
    varnas = ad(raw_input)
    
    st.subheader("1. Atomic Analysis")
    st.code(f"{[v.char for v in varnas]}", language="json")

    # B. Run Engine
    clean_varnas, trace = AnubandhaEngine.process(varnas, context)
    
    # C. Display Trace
    st.subheader("2. Rule Application")
    if not trace:
        st.info("No It-Sanjna rules applied.")
    else:
        for t in trace:
            style = "save-box" if "SAVED" in t else "it-box"
            st.markdown(f'<div class="{style}">{t}</div>', unsafe_allow_html=True)

    # D. Final Result
    st.subheader("3. Final Result (Nirubandha)")
    final_str = join(clean_varnas)
    st.markdown(f'<div class="final-res">{final_str}</div>', unsafe_allow_html=True)
    
    if final_str == "कृ":
        st.success("Correct derivation for Ḍukṛñ!")
    if final_str == "अ" and raw_input == "जस्":
        st.success("Correct derivation for Jas (as -> a)!")

'''
    (Path("pages") / "3_🏷️_Sanjna_Lab.py").write_text(page_code, encoding='utf-8')
    print("✅ CREATED: pages/3_🏷️_Sanjna_Lab.py")

if __name__ == "__main__":
    build_sanjna_prakaran()