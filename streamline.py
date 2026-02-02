import os
import sys
from pathlib import Path


def fix_missing_tinanta_module():
    # 1. Ensure 'logic' package exists
    os.makedirs("logic", exist_ok=True)
    Path("logic/__init__.py").touch()

    # 2. CREATE THE MISSING FILE: logic/tinanta_processor.py
    tinanta_path = Path("logic/tinanta_processor.py")
    tinanta_code = r'''"""
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

        # B. Vikarana (Infix) Selection - Hardcoded Śap (a) for now
        vikarana = "अ" 
        self.log("3.1.68: Added Vikaraṇa 'Śap' (a)")

        # C. Guna (7.3.84 Sārvadhātukārdhadhātukayoḥ)
        root_varnas = ad(curr_root)
        if root_varnas:
            last_char = root_varnas[-1].char
            if last_char in ['इ', 'ई']:
                curr_root = curr_root[:-1] + "ए" # i -> e
                self.log("7.3.84: Guna (i -> e)")
            elif last_char in ['उ', 'ऊ']:
                curr_root = curr_root[:-1] + "ओ" # u -> o
                self.log("7.3.84: Guna (u -> o)")
            elif last_char in ['ऋ', 'ॠ']:
                curr_root = curr_root[:-1] + "अर्" # r -> ar
                self.log("7.3.84: Guna (ṛ -> ar)")

        # D. Ayadi Sandhi (6.1.78)
        if curr_root.endswith("ए"):
            curr_root = curr_root[:-1] + "अय्"
            self.log("6.1.78: Ayadi (e -> ay)")
        elif curr_root.endswith("ओ"):
            curr_root = curr_root[:-1] + "अव्"
            self.log("6.1.78: Ayadi (o -> av)")

        # E. Assembly
        return f"{curr_root}{vikarana}{curr_suffix}" # Example: Bhav + a + ti
'''
    tinanta_path.write_text(tinanta_code, encoding='utf-8')
    print("✅ Created missing file: logic/tinanta_processor.py")

    # 3. Add Path Fix to Pages
    # We prepend a sys.path hack to the top of the page files so they find 'logic'
    path_hack = r'''import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
'''

    # Update Page 1
    p1 = Path("pages/1_🧪_Dhatu_Lab.py")
    if p1.exists():
        content = p1.read_text(encoding='utf-8')
        if "sys.path.append" not in content:
            p1.write_text(path_hack + content, encoding='utf-8')
            print("✅ Patched Page 1 with system path fix.")

    # Update Page 2
    p2 = Path("pages/2_⚡_Tinanta_Lab.py")
    if p2.exists():
        content = p2.read_text(encoding='utf-8')
        if "sys.path.append" not in content:
            p2.write_text(path_hack + content, encoding='utf-8')
            print("✅ Patched Page 2 with system path fix.")


if __name__ == "__main__":
    fix_missing_tinanta_module()