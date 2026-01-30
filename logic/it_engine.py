"""
FILE: logic/it_engine.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: It-Prakaraṇam (Meta-Data & Cleaning)
UPDATED: Added Tag Inheritance (Kit/Nit/Shit properties transfer to survivors).
"""

from core.upadesha_registry import UpadeshaType

# Import rule logic directly from Sanjna Rules (Zone 1)
from logic.sanjna_rules import (
    apply_1_3_2_ajanunasika,
    apply_1_3_3_halantyam,
    apply_1_3_4_na_vibhaktau,
    apply_1_3_5_adir_nitudavah,
    apply_1_3_6_shah,
    apply_1_3_7_chutu,
    apply_1_3_8_lashakva
)

class ItEngine:
    """
    इत्-संज्ञा सञ्चालक: (The Marker Removal Engine)
    Diagnoses 'It' markers, preserves their grammatical tags, and performs 'Tasya Lopah'.
    """

    @staticmethod
    def run_it_prakaran(varna_list, source_type=UpadeshaType.DHATU):
        """
        Executes the entire It-Sanjna pipeline (1.3.2 to 1.3.9).
        RETURNS: (cleaned_varna_list, log_of_rules_applied)
        """
        if not varna_list:
            return [], []

        it_indices = set()
        trace_log = []

        # =====================================================================
        # PHASE 1: IDENTIFICATION (Diagnose Markers)
        # =====================================================================

        # 1.3.2 Upadeshe'janunasika It
        indices, log = apply_1_3_2_ajanunasika(varna_list)
        if indices:
            it_indices.update(indices)
            trace_log.extend(log)

        # 1.3.3 Halantyam (Final Consonant)
        # Note: We must check 1.3.4 (Blocking) immediately after.
        indices, log = apply_1_3_3_halantyam(varna_list, blocked_indices=it_indices)
        if indices:
            # Check 1.3.4 Na Vibhaktau (Blocker)
            blocked = apply_1_3_4_na_vibhaktau(varna_list, source_type)
            final_indices = indices - blocked
            if final_indices:
                it_indices.update(final_indices)
                trace_log.extend(log)

        # 1.3.5 Adir Nitudavah (Initial Ñi, Tu, Du)
        if source_type == UpadeshaType.DHATU:
            indices, log = apply_1_3_5_adir_nitudavah(varna_list)
            if indices:
                it_indices.update(indices)
                trace_log.extend(log)

        # 1.3.6 Shah Pratyayasya (Initial Sh)
        indices, log = apply_1_3_6_shah(varna_list, source_type)
        if indices:
            it_indices.update(indices)
            trace_log.extend(log)

        # 1.3.7 Chutu (Initial C-varga, T-varga)
        indices, log = apply_1_3_7_chutu(varna_list, source_type)
        if indices:
            it_indices.update(indices)
            trace_log.extend(log)

        # 1.3.8 Lashakvataddhite (Initial L, S, K-varga)
        # Assumption: Not Taddhita by default unless specified
        is_taddhita = False
        indices, log = apply_1_3_8_lashakva(varna_list, source_type, is_taddhita)
        if indices:
            it_indices.update(indices)
            trace_log.extend(log)

        # =====================================================================
        # PHASE 2: TAG INHERITANCE (CRITICAL FIX)
        # =====================================================================
        # Identify the grammatical property of the marker (Kit, Nit, etc.)
        # and store it to transfer to the survivor.

        inherited_tags = set()
        for idx in it_indices:
            char = varna_list[idx].char

            # Map marker char to grammatical tag
            if 'क्' in char: inherited_tags.add("kit")
            if 'ग्' in char: inherited_tags.add("gnit")
            if 'ङ्' in char: inherited_tags.add("ngit")
            if 'ञ्' in char: inherited_tags.add("ñit")
            if 'ण्' in char: inherited_tags.add("ṇit")
            if 'न्' in char: inherited_tags.add("nit")
            if 'श्' in char: inherited_tags.add("śit")
            if 'ष्' in char: inherited_tags.add("ṣit")
            if 'प्' in char: inherited_tags.add("pit")
            if 'र्' in char: inherited_tags.add("rit")

        # =====================================================================
        # PHASE 3: SURGICAL REMOVAL (Tasya Lopah 1.3.9)
        # =====================================================================

        if it_indices:
            trace_log.append("१.३.९ तस्य लोपः (Removal of Markers)")

            # Create new list excluding markers
            cleaned_list = []
            for i, v in enumerate(varna_list):
                if i not in it_indices:
                    cleaned_list.append(v)

            # Apply inherited tags to the first remaining letter (the representative)
            if cleaned_list:
                cleaned_list[0].sanjnas.update(inherited_tags)

            return cleaned_list, trace_log

        return varna_list, trace_log