"""
FILE: logic/prakriya_engine.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Prakriyā (Derivation Orchestration)
UPDATED: Added 'derive_ghanj' recipe.
"""

from core.phonology import ad, sanskrit_varna_samyoga
from core.upadesha_registry import UpadeshaType
from logic.it_engine import ItEngine
from logic.vidhi_engine import VidhiEngine

class PrakriyaEngine:
    """
    The Orchestrator.
    Manages the 'Recipe' of word formation sequences.
    """

    def __init__(self):
        self.history = []

    def log(self, step_name, anga, suffix, rule_code, description):
        """Centralized logging for UI."""
        current_form = sanskrit_varna_samyoga(anga + suffix)
        self.history.append({
            "step": step_name,
            "form": current_form,
            "rule": rule_code,
            "description": description,
            "components": f"{sanskrit_varna_samyoga(anga)} + {sanskrit_varna_samyoga(suffix)}"
        })

    def get_history(self):
        return self.history

    # =========================================================================
    # RECIPE 1: NYANTA (Causatives) - e.g. Nī -> Nāyi
    # =========================================================================
    def derive_nyanta(self, dhatu_text):
        self.history = []

        # 1. Prep
        raw_suffix = ad("णिच्")
        clean_suffix, _ = ItEngine.run_it_prakaran(raw_suffix, UpadeshaType.PRATYAYA)
        if clean_suffix: clean_suffix[0].sanjnas.add("ṇit")

        anga = ad(dhatu_text)
        self.log("1", anga, clean_suffix, "Initial", "Base + Suffix Prepared")

        # 2. Vriddhi (7.2.115)
        anga, rule_v = VidhiEngine.apply_vṛddhi_7_2_115(anga, clean_suffix)
        if rule_v: self.log("2", anga, clean_suffix, "७.२.११५", rule_v)

        # 3. Ayadi (6.1.78)
        anga, rule_a = VidhiEngine.apply_ayadi_6_1_78(anga, clean_suffix)
        if rule_a: self.log("3", anga, clean_suffix, "६.१.७८", rule_a)

        # 4. Output
        final_form = sanskrit_varna_samyoga(anga + clean_suffix)
        self.log("4", anga, clean_suffix, "३.१.३२", "सनाद्यन्ता धातवः")
        return final_form

    # =========================================================================
    # RECIPE 2: GHANJ (Action Nouns) - e.g. Pac -> Pāka, Tyaj -> Tyāga
    # =========================================================================
    def derive_ghanj(self, dhatu_input):
        """
        Derives Root + Ghañ (घञ्).
        Logic imported from tests/test_ghanj_random.py
        """
        self.history = []

        # --- STEP 1: PREPARATION ---
        # 1. Clean Root (Handle raw 'पचँ' input if necessary)
        raw_dhatu = ad(dhatu_input)
        clean_dhatu, _ = ItEngine.run_it_prakaran(raw_dhatu, UpadeshaType.DHATU)

        # 2. Clean Suffix (घञ् -> अ)
        raw_suffix = ad("घञ्")
        clean_suffix, _ = ItEngine.run_it_prakaran(raw_suffix, UpadeshaType.PRATYAYA)

        # [CRITICAL]: Transfer Tags (Ghit, Nit) manually as physical letters are gone
        if clean_suffix:
            clean_suffix[0].sanjnas.update(["ghit", "ñit"])

        self.log("1", clean_dhatu, clean_suffix, "Initial", "Root + Ghañ (Cleaned)")

        # --- STEP 2: VRIDDHI (7.2.116) ---
        # "Ata Upadhayah" - Penultimate 'a' becomes 'ā'
        # e.g. Pac -> Pāc
        clean_dhatu, rule_v = VidhiEngine.apply_ata_upadhayah_7_2_116(clean_dhatu)

        if rule_v:
            self.log("2", clean_dhatu, clean_suffix, "७.२.११६", rule_v)

        # --- STEP 3: KUTVA (7.3.52) ---
        # "Chajo Ku Ghinnyatoh" - Palatal (c/j) -> Velar (k/g)
        # e.g. Pāc -> Pāk, Tyāj -> Tyāg
        clean_dhatu, rule_k = VidhiEngine.apply_chajo_ku_7_3_52(clean_dhatu)

        if rule_k:
            self.log("3", clean_dhatu, clean_suffix, "७.३.५२", rule_k)

        # --- STEP 4: OUTPUT ---
        final_form = sanskrit_varna_samyoga(clean_dhatu + clean_suffix)
        self.log("4", clean_dhatu, clean_suffix, "३.१.९१", "धातोः (Final Form)")

        return final_form

    def derive_taddhita(self, pratipadika_text, pratyaya_text):
        """
        Derives Taddhita forms.
        Example: Upagu + Aṇ -> Aupagava
        """
        self.history = []

        # --- STEP 1: PREPARATION ---
        # 1. Clean Suffix (Aṇ -> a)
        raw_suffix = ad(pratyaya_text)
        clean_suffix, _ = ItEngine.run_it_prakaran(raw_suffix, UpadeshaType.PRATYAYA)

        # [MANUAL TAGGING]: Aṇ (अण्) is Ṇit (removes ṇ)
        if "ण्" in pratyaya_text and clean_suffix:
            clean_suffix[0].sanjnas.add("ṇit")

        # 2. Prepare Base
        anga = ad(pratipadika_text)

        self.log("1", anga, clean_suffix, "Initial", "Base + Taddhita Suffix")

        # --- STEP 2: ADI VRIDDHI (7.2.117) ---
        # Upagu -> Aupagu
        anga, rule_v = VidhiEngine.apply_taddhiteshu_acam_ade_7_2_117(anga, clean_suffix)
        if rule_v: self.log("2", anga, clean_suffix, "७.२.११७", rule_v)

        # --- STEP 3: ORGUNAH (6.4.146) ---
        # Aupagu -> Aupago
        anga, rule_o = VidhiEngine.apply_orgunah_6_4_146(anga, clean_suffix)
        if rule_o: self.log("3", anga, clean_suffix, "६.४.१४६", rule_o)

        # --- STEP 4: AYADI SANDHI (6.1.78) ---
        # Aupago + a -> Aupagav + a
        anga, rule_a = VidhiEngine.apply_ayadi_6_1_78(anga, clean_suffix)
        if rule_a: self.log("4", anga, clean_suffix, "६.१.७८", rule_a)

        # --- STEP 5: OUTPUT ---
        final_form = sanskrit_varna_samyoga(anga + clean_suffix)
        self.log("5", anga, clean_suffix, "४.१.७६", "तद्धिताः (Final Form)")

        return final_form