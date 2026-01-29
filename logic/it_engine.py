"""
FILE: logic/it_engine.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: It-Saṃjñā & Lopa (The Surgical Scrubber)
REFERENCE: १.३.२ to १.३.९
"""

from core.upadesha_registry import UpadeshaType
import logic.sanjna_rules as rules


class ItEngine:
    """
    इत्-सञ्चालक: The Marker Removal Engine.
    Executes the 'It' identification (Diagnosis) and 'Lopa' (Removal) cycle.
    """

    @staticmethod
    def run_it_prakaran(varna_list, source_type=UpadeshaType.DHATU, is_taddhita=False):
        """
        [CYCLE]: Diagnosis (1.3.2-8) -> Prescription (1.3.9).
        Returns: (Cleaned Varna List, List of Tags applied)
        """
        if not varna_list:
            return [], []

        # 1. DIAGNOSIS PHASE (Identify the markers)
        # We collect indices of all chars that get the 'It' label.
        it_indices = set()
        trace_log = []

        # A. 1.3.2 Upadeshe'janunasika It (Vowels)
        # Check specific nasal vowels (e.g., 'ँ' in 'गाधृँ')
        nasal_indices = rules.apply_1_3_2_ajanunasika(varna_list)
        if nasal_indices:
            it_indices.update(nasal_indices)
            trace_log.append(f"1.3.2 Applied on indices: {nasal_indices}")

        # B. 1.3.3 Halantyam (Final Consonant)
        # CRITICAL: 1.3.4 (Na Vibhaktau) acts as a blocking antibody.
        blocked_indices = rules.apply_1_3_4_na_vibhaktau(varna_list, source_type)
        if blocked_indices:
            trace_log.append(f"1.3.4 Blocked Halantyam on indices: {blocked_indices}")

        hal_indices = rules.apply_1_3_3_halantyam(varna_list, blocked_indices)
        if hal_indices:
            it_indices.update(hal_indices)
            trace_log.append(f"1.3.3 Applied on indices: {hal_indices}")

        # C. Initial Markers (1.3.5 - 1.3.8)
        # 1.3.5 Adir Ñitudavah (Dhatu only)
        if source_type == UpadeshaType.DHATU:
            indices_135 = rules.apply_1_3_5_adir_nitudavah(varna_list)
            if indices_135:
                it_indices.update(indices_135)
                trace_log.append("1.3.5 Applied (Ñi/Tu/Du)")

        # 1.3.6 - 1.3.8 (Pratyayas only)
        if source_type in [UpadeshaType.PRATYAYA, UpadeshaType.VIBHAKTI]:
            # 1.3.6 Shah Pratyayasya
            # Note: Ensure these functions exist in your logic/sanjna_rules.py
            if hasattr(rules, 'apply_1_3_6_shah'):
                indices_136 = rules.apply_1_3_6_shah(varna_list, source_type)
                if indices_136:
                    it_indices.update(indices_136)
                    trace_log.append("1.3.6 Applied (Ṣah)")

            # 1.3.7 Chutu
            if hasattr(rules, 'apply_1_3_7_chutu'):
                indices_137 = rules.apply_1_3_7_chutu(varna_list, source_type)
                if indices_137:
                    it_indices.update(indices_137)
                    trace_log.append("1.3.7 Applied (Cu/Tu)")

            # 1.3.8 Lashakvataddhite (Not for Taddhitas)
            indices_138 = rules.apply_1_3_8_lashakva(varna_list, source_type, is_taddhita)
            if indices_138:
                it_indices.update(indices_138)
                trace_log.append("1.3.8 Applied (L/Ś/Ku)")

        # 2. SURGICAL PHASE (1.3.9 Tasya Lopah)
        # We rebuild the list excluding the identified 'It' markers.
        cleaned_list = []
        for i, v in enumerate(varna_list):
            if i in it_indices:
                # MARKER FOUND: We do not add it to cleaned_list.
                # But we MUST preserve its 'Ghost' properties (1.1.56 idea)
                v.sanjnas.add("इत्")
                v.trace.append("१.३.९ तस्य लोपः (Removed)")
            else:
                cleaned_list.append(v)

        return cleaned_list, trace_log