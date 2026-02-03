"""
FILE: subanta/declension.py
PURPOSE: Derives Noun Forms using the Shared Core.
"""
from shared.varnas import ad, join
from shared.anubandha import AnubandhaEngine
from shared.sandhi import SandhiEngine

class SubantaGenerator:
    def __init__(self):
        # 4.1.2 The 21 Suffixes (Sup)
        self.SUP = {
            (1,1): "सुँ", (1,2): "औ", (1,3): "जस्",
            (2,1): "अम्", (2,2): "औट्", (2,3): "शस्",
            (3,1): "टा", (3,2): "भ्याम्", (3,3): "भिस्",
            # ... add others as we implement them
        }

    def log(self, step, result):
        self.history.append({"step": step, "result": result})

    def derive(self, stem, vibhakti, vacana):
        self.history = []
        
        # Step 1: Input Analysis
        if stem.endswith("a"): stem = stem[:-1] + "अ" # Basic transliteration fix
        
        # Step 2: Pratyaya Selection (4.1.2)
        pratyaya_raw = self.SUP.get((vibhakti, vacana), "")
        if not pratyaya_raw: return "WIP"
        
        # Step 0: Varna-Viccheda (ALWAYS FIRST)
        stem_varnas = ad(stem)
        prat_varnas = ad(pratyaya_raw)
        
        # Merge for display
        full_split = stem_varnas + prat_varnas
        self.log("Varna-Viccheda", join(full_split))
        self.log(f"4.1.2 Svaujasamaut...", f"{stem} + {pratyaya_raw}")

        # --- IT KARYA (Cleaning the Suffix) ---
        # Use the Shared Anubandha Engine
        clean_prat, tags = AnubandhaEngine.process(prat_varnas, context="Pratyaya")
        
        # Log the cleaning
        if len(clean_prat) != len(prat_varnas):
            for t in tags:
                self.log(f"It-Sanjna & Lopa ({t})", f"{stem} + {join(clean_prat)}")

        # --- SPECIFIC DERIVATIONS ---
        
        # Case 1.1: Rama + s (The detailed flow you requested)
        if vibhakti == 1 and vacana == 1:
            # 1.4.14 Suptingantam Padam
            self.log("1.4.14 Suptingantam Padam", f"{stem}{join(clean_prat)}")
            
            # 8.2.66 Sasajusho Ruh (s -> ru~)
            # We explicitly simulate the 's' -> 'ru~' change
            clean_prat = ad("रुँ")
            self.log("8.2.66 Sasajusho Ruh", f"{stem}रुँ")
            
            # Clean the 'ru~' (Remove u~)
            clean_prat, tags = AnubandhaEngine.process(clean_prat, context="General")
            self.log("1.3.2 Upadeshe'janunasika It", f"{stem}र्")
            
            # 8.3.15 Kharavasanayor Visarjaniyah (r -> h)
            clean_prat = ad("ः")
            final = f"{stem}ः"
            self.log("8.3.15 Kharavasanayor Visarjaniyah", final)
            return final, self.history

        return "Logic Pending", self.history
