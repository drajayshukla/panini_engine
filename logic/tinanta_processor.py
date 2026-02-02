"""
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
