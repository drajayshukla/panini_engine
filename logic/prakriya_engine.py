"""
FILE: logic/prakriya_engine.py
PAS-v2.0: 5.0 (Siddha)
RATIO: ~55% Documentation | LIMIT: < 200 Lines
PURPOSE: The Master Orchestrator (प्रक्रिया-प्रबन्धकः) for word derivations.
"""

from core.phonology import ad, sanskrit_varna_samyoga
from core.upadesha_registry import UpadeshaType
from logic.it_engine import ItEngine
from logic.vidhi import VidhiEngine

class PrakriyaEngine:
    """
    [VṚTTI]: धातु-प्रातिपदिक-प्रत्ययानां संयोगे विधीनां क्रमिक-अनुप्रयोगः।
    This engine manages the sequential 'Recipes' for Sanskrit morphology.
    It acts as the bridge between raw input and the final Siddha-rupa.
    """

    def __init__(self):
        self.history = []

    def _log(self, step, rule, desc, anga, suffix):
        """[LOGIC]: Captures the snapshot of the word at each Sūtra application."""
        self.history.append({
            "step": step,
            "rule": rule,
            "description": desc,
            "form": sanskrit_varna_samyoga(anga + suffix)
        })

    def derive_ghanj(self, dhatu_input):
        """
        [RECIPE]: Root + Ghañ (घञ्) -> Action Noun (e.g., Pāka, Tyāga).
        [SŪTRAS]: 7.2.116 (Vriddhi), 7.3.52 (Kutva).
        """
        self.history = []
        # 1. Preparation: Clean Dhatu and Suffix (1.3.x Prakaran)
        anga, _ = ItEngine.run_it_prakaran(ad(dhatu_input), UpadeshaType.DHATU)
        suffix, _ = ItEngine.run_it_prakaran(ad("घञ्"), UpadeshaType.PRATYAYA)
        if suffix: suffix[0].sanjnas.update(["ghit", "ñit"]) # Tag transfer
        self._log("1", "Initial", "Root + Ghañ Cleaned", anga, suffix)

        # 2. Vriddhi: अत उपधायाः (7.2.116) - Penultimate short 'a' -> 'ā'
        anga, r_v = VidhiEngine.apply_ata_upadhayah_7_2_116(anga)
        if r_v: self._log("2", "७.२.११६", r_v, anga, suffix)

        # 3. Kutva: चजोः कु घिण्ण्यतोः (7.3.52) - c/j -> k/g
        anga, r_k = VidhiEngine.apply_chajo_ku_7_3_52(anga)
        if r_k: self._log("3", "७.३.५२", r_k, anga, suffix)

        return sanskrit_varna_samyoga(anga + suffix)

    def derive_nyanta(self, dhatu_text):
        """
        [RECIPE]: Root + Ṇic (णिच्) -> Causative Stem (e.g., Nāyi).
        [SŪTRAS]: 7.2.115 (Vriddhi), 6.1.78 (Ayādi).
        """
        self.history = []
        anga = ad(dhatu_text)
        suffix, _ = ItEngine.run_it_prakaran(ad("णिच्"), UpadeshaType.PRATYAYA)
        if suffix: suffix[0].sanjnas.add("ṇit")
        self._log("1", "Initial", "Base + Ṇic Prepared", anga, suffix)

        # Vriddhi (7.2.115) and Ayadi (6.1.78)
        anga, r_v = VidhiEngine.apply_aco_niti_7_2_115(anga, suffix)
        if r_v: self._log("2", "७.२.११५", r_v, anga, suffix)

        anga, r_a = VidhiEngine.apply_ayadi_6_1_78(anga, suffix)
        if r_a: self._log("3", "६.१.७८", r_a, anga, suffix)

        return sanskrit_varna_samyoga(anga + suffix)

    def derive_taddhita(self, base_text, pratyaya_text):
        """
        [RECIPE]: Pratipadika + Taddhita (e.g., Upagu + Aṇ -> Aupagava).
        [SŪTRAS]: 7.2.117 (Adi Vriddhi), 6.1.78 (Ayādi).
        """
        self.history = []
        anga = ad(base_text)
        suffix, _ = ItEngine.run_it_prakaran(ad(pratyaya_text), UpadeshaType.PRATYAYA)
        if "ण्" in pratyaya_text and suffix: suffix[0].sanjnas.add("ṇit")
        self._log("1", "Initial", "Taddhita Setup", anga, suffix)

        # Initial Vowel Vriddhi (7.2.117)
        anga, r_v = VidhiEngine.apply_taddhiteshu_acam_ade_7_2_117(anga, suffix)
        if r_v: self._log("2", "७.२.११७", r_v, anga, suffix)

        # Final Ayadi/Guna transformations
        anga, r_a = VidhiEngine.apply_ayadi_6_1_78(anga, suffix)
        if r_a: self._log("3", "६.१.७८", r_a, anga, suffix)

        return sanskrit_varna_samyoga(anga + suffix)