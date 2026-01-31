"""
FILE: logic/it_engine.py
TIMESTAMP: 2026-01-31 08:45:00 (IST)
PILLAR: It-Prakaraṇam (Orchestrator)
QUALITY: PAS-v2.0: 6.0 (Subanta/Siddha)
DESCRIPTION:
    The Master Engine for marker identification and removal.
    - Orchestrates Sañjñā rules (1.3.2 - 1.3.8) in valid sequence.
    - Harvests metadata (DNA/Tags) from markers before deletion.
    - Performs physical removal (1.3.9 Lopa) via SanjnaEngine.
"""
from core.upadesha_registry import UpadeshaType
from core.phonology import Varna, sanskrit_varna_samyoga

class ItEngine:
    """
    The Gateway for marker processing.
    Diagnoses markers, transfers metadata tags (like Kit/Nit),
    and performs the physical deletion to allow Sandhi engines to see junctions.
    """

    @staticmethod
    def run_it_prakaran(varna_list, source_type=UpadeshaType.DHATU, is_taddhita=False):
        """
        Executes the full It-Sanjna and Lopa pipeline.

        Args:
            varna_list (list[Varna]): The phonological input list.
            source_type (UpadeshaType): Context (Dhatu, Pratyaya, Vibhakti, etc.).
            is_taddhita (bool): Specific flag for rule 1.3.8.

        Returns:
            tuple: (cleaned_varna_list, list[trace_log_strings])
        """
        if not varna_list:
            return [], []

        # Local Import to prevent Circular Dependency with logic/__init__.py
        from logic.sanjna import SanjnaEngine

        it_indices = set()
        trace_log = []

        # =========================================================
        # PHASE 1: IDENTIFICATION (Sañjñā Identification)
        # =========================================================

        # 1.3.2: Upadeshe'janunasika (Nasalized vowels)
        idx, rule = SanjnaEngine.apply_1_3_2_ajanunasika(varna_list)
        if idx:
            it_indices.update(idx)
            trace_log.append(rule)

        # Context-Specific Initial Markers
        if source_type == UpadeshaType.DHATU:
            # 1.3.5: Adir Ñi-Tu-Du
            idx, rule = SanjnaEngine.apply_1_3_5_adir_nitudavah(varna_list)
            if idx:
                it_indices.update(idx)
                trace_log.append(rule)

        elif source_type in [UpadeshaType.PRATYAYA, UpadeshaType.VIBHAKTI]:
            # 1.3.6: Shah Pratyayasya
            idx, rule = SanjnaEngine.apply_1_3_6_shah(varna_list, source_type)
            if idx:
                it_indices.update(idx)
                trace_log.append(rule)

            # 1.3.7: Cutu (Initial Palatals/Cerebrals)
            idx, rule = SanjnaEngine.apply_1_3_7_chutu(varna_list, source_type)
            if idx:
                it_indices.update(idx)
                trace_log.append(rule)

            # 1.3.8: Lashakva Taddhite
            idx, rule = SanjnaEngine.apply_1_3_8_lashakva(varna_list, source_type, is_taddhita)
            if idx:
                it_indices.update(idx)
                trace_log.append(rule)

        # 1.3.3: Halantyam (Run last to allow 1.3.4 'Na Vibhaktau' blocks inside 1.3.3)
        idx, rule = SanjnaEngine.apply_1_3_3_halantyam(varna_list, source_type, it_indices)
        if idx:
            it_indices.update(idx)
            trace_log.append(rule)

        # =========================================================
        # PHASE 2: METADATA HARVEST & LOPA (1.3.9)
        # =========================================================
        # Physically filters the list and transfers 'DNA' (tags) to the segment.
        cleaned_list = SanjnaEngine.run_tasya_lopah_1_3_9(varna_list, it_indices)

        if it_indices:
            removed_chars = [varna_list[i].char for i in sorted(it_indices)]
            trace_log.append(f"1.3.9 तस्य लोपः (Removed: {removed_chars})")

        return cleaned_list, trace_log

    # =========================================================
    # UTILITY METHODS (Logic Helpers)
    # =========================================================

    @staticmethod
    def is_halanta(varnas):
        """Checks if the list ends in a consonant (Hal)."""
        if not varnas: return False
        return varnas[-1].is_consonant

    @staticmethod
    def is_ajanta(varnas):
        """Checks if the list ends in a vowel (Ac)."""
        if not varnas: return False
        return varnas[-1].is_vowel