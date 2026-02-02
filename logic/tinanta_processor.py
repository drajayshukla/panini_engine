import os
from pathlib import Path


def initialize_tinanta_engine():
    # Create the new Logic Module
    processor_path = Path("logic/tinanta_processor.py")

    code = r'''"""
FILE: logic/tinanta_processor.py - PAS-v18.0 (The Conjugation Engine)
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga
from logic.dhatu_processor import DhatuDiagnostic

# --- The 18 Tiṅ Suffixes (3.4.78) ---
TIN_PRATYAYA = {
    "Parasmaipada": [
        ["तिप्", "तस्", "झि"],   # Prathama (3rd Person)
        ["सिप्", "थस्", "थ"],    # Madhyama (2nd Person)
        ["मिप्", "वस्", "मस्"]   # Uttama (1st Person)
    ],
    "Atmanepada": [
        ["त", "आताम्", "झ"],     # Prathama
        ["थास्", "आथाम्", "ध्वम्"], # Madhyama
        ["इड्", "वहि", "महिङ्"]   # Uttama
    ]
}

class TinantaDiagnostic:
    def __init__(self, upadesha, lakara="Lat", purusha=1, vacana=1):
        """
        upadesha: Raw root (e.g. 'डुकृञ्')
        lakara: Tense/Mood (e.g. 'Lat')
        purusha: 1=Prathama, 2=Madhyama, 3=Uttama (Paninian Indexing)
        vacana: 1=Eka, 2=Dvi, 3=Bahu
        """
        self.raw_root = upadesha
        self.lakara = lakara
        self.purusha = purusha - 1 # 0-indexed
        self.vacana = vacana - 1   # 0-indexed

        self.history = []
        self.derivation = []

        # Step 1: Process Root (Dhātu-Pāṭha Logic)
        self.dhatu_obj = DhatuDiagnostic(upadesha)
        self.root = self.dhatu_obj.get_final_root()
        self.pada_type = self.dhatu_obj.pada # Parasmai/Atmane

        self.log(f"Root Prepared: {self.root} ({self.pada_type})")

        # Step 2: Select Suffix (Tiṅ Selection)
        self.suffix = self._select_tin()
        self.log(f"Suffix Selected: {self.suffix} ({self.lakara})")

        # Step 3: Run Prakriya
        self.final_form = self._run_prakriya()

    def log(self, message):
        self.history.append(message)

    def _select_tin(self):
        # 1.3.12/78: Determine Voice
        # Simple Logic: If Engine says Atmanepada, use Atmane set. Else Parasmai.
        # (Enhancement: User override vivakṣā needed later)

        voice = "Atmanepada" if "Atmanepada" in self.pada_type else "Parasmaipada"
        selection = TIN_PRATYAYA[voice][self.purusha][self.vacana]

        # Basic IT removal for suffixes (P in Tip/Mip/Sip is It)
        if selection.endswith("प्") and len(selection) > 1:
            selection = selection[:-2] + "ि" # Tip -> Ti

        return selection

    def _run_prakriya(self):
        """
        The Core Assembly Line:
        Root + Vikarana + Suffix -> Anga-Karya -> Sandhi -> Pada
        """
        # A. Current State
        curr_root = self.root
        curr_suffix = self.suffix

        # B. Vikarana (Infix) Selection
        # Currently hardcoded for Bhvādi (Kartari Śap - 3.1.68)
        # TODO: Lookup Gana from DB to decide Śap, Śyan, Śnu, etc.
        vikarana = "अ" # Śap -> a
        self.log("3.1.68: Added Vikaraṇa 'Śap' (a)")

        # C. Guna (7.3.84 Sārvadhātukārdhadhātukayoḥ)
        # If root ends in Ik, Guna happens before 'a'
        root_varnas = ad(curr_root)
        if root_varnas:
            last_char = root_varnas[-1].char
            if last_char in ['इ', 'ई']:
                curr_root = curr_root[:-1] + "ए" # i -> e
                self.log("7.3.84: Guna (i -> e)")
            elif last_char in ['उ', 'ऊ']:
                curr_root = curr_root[:-1] + "ओ" # u -> o
                self.log("7.3.84: Guna (u -> o)")

        # D. Ayadi Sandhi (6.1.78)
        # e + a -> ay, o + a -> av
        if curr_root.endswith("ए"):
            curr_root = curr_root[:-1] + "अय्"
            self.log("6.1.78: Ayadi (e -> ay)")
        elif curr_root.endswith("ओ"):
            curr_root = curr_root[:-1] + "अव्"
            self.log("6.1.78: Ayadi (o -> av)")

        # E. Assembly
        return f"{curr_root}{vikarana}{curr_suffix}" # Example: Bhav + a + ti

'''
    processor_path.write_text(code, encoding='utf-8')

    # Update App to show Tiṅanta Lab
    app_path = Path("app.py")
    app_code = r'''"""
FILE: app.py
PAS-v18.0 (Tiṅanta Laboratory)
"""
import streamlit as st
import pandas as pd
from logic.tinanta_processor import TinantaDiagnostic

st.set_page_config(page_title="Panini Engine", layout="wide", page_icon="🕉️")

st.title("🕉️ Pāṇinian Engine: The Digital Ashtadhyayi")
st.markdown("---")

mode = st.sidebar.radio("Select Laboratory", ["Tiṅanta (Verbs)", "Dhātu (Roots)", "Subanta (Nouns)"])

if mode == "Tiṅanta (Verbs)":
    st.header("⚡ Tiṅanta Prakriyā (Verb Conjugation)")

    col1, col2 = st.columns([1, 2])

    with col1:
        root_input = st.text_input("Root (Upadesha)", value="भू")
        lakara = st.selectbox("Lakāra", ["Lat (Present)", "Lit (Perfect)", "Lrt (Future)"])
        purusha = st.selectbox("Purusha", ["Prathama (3rd)", "Madhyama (2nd)", "Uttama (1st)"])
        vacana = st.selectbox("Vacana", ["Eka (Singular)", "Dvi (Dual)", "Bahu (Plural)"])

        if st.button("Generate Form"):
            # Map inputs to indices
            p_map = {"Prathama (3rd)": 1, "Madhyama (2nd)": 2, "Uttama (1st)": 3}
            v_map = {"Eka (Singular)": 1, "Dvi (Dual)": 2, "Bahu (Plural)": 3}

            tin = TinantaDiagnostic(root_input, lakara.split()[0], p_map[purusha], v_map[vacana])

            st.session_state['tin_result'] = tin

    with col2:
        if 'tin_result' in st.session_state:
            res = st.session_state['tin_result']

            st.markdown(f"""
            <div style="background:#e8f5e9;padding:20px;border-radius:10px;border-left:5px solid #2e7d32;">
                <h3>🏁 Final Form: <span style="color:#d32f2f;font-size:1.5em;">{res.final_form}</span></h3>
                <p><strong>Root:</strong> {res.root} | <strong>Voice:</strong> {res.pada_type}</p>
            </div>
            """, unsafe_allow_html=True)

            st.subheader("📜 Derivation History")
            for step in res.history:
                st.write(f"- {step}")

elif mode == "Dhātu (Roots)":
    st.info("Dhātu Logic is 100% Siddha. Use 'tests' to verify.")
'''
    app_path.write_text(app_code, encoding='utf-8')
    print("✅ Tiṅanta Engine Initialized: v18.0 Live.")


if __name__ == "__main__":
    initialize_tinanta_engine()