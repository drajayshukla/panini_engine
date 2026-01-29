"""
FILE: logic/it_engine.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: It-Saṃjñā (Meta-Tag Scrubbing)
REFERENCE: १.३.२ to १.३.९
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
    Diagnoses 'It' markers and performs 'Tasya Lopah' (1.3.9).
    """

    @staticmethod
    def run_it_prakaran(varna_list, source_type=UpadeshaType.DHATU):
        """
        Executes the 1.3.x diagnostic pipeline.
        Returns: (cleaned_varna_list, list_of_trace_msgs)
        """
        if not varna_list:
            return [], []

        # 1. Initialize Set correctly (CRITICAL FIX: set() not {})
        it_indices = set()
        trace_log = []

        # =====================================================================
        # PHASE 1: BLOCKING RULES (Niyama) - Check what CANNOT be It
        # =====================================================================

        # 1.3.4 Na Vibhaktau Tusmah (Protects T-varga, s, m in Vibhakti)
        blocked_indices = apply_1_3_4_na_vibhaktau(varna_list, source_type)

        # =====================================================================
        # PHASE 2: DIAGNOSTIC RULES (Vidhi) - Identify markers
        # =====================================================================

        # 1.3.3 Halantyam (Final Consonant)
        # We pass the blocked indices so it doesn't accidentally mark protected chars
        hal_idx, hal_trace = apply_1_3_3_halantyam(varna_list, blocked_indices)
        if hal_idx:
            it_indices.update(hal_idx)
            trace_log.extend(hal_trace)

        # 1.3.2 Upadeshe'janunasika It (Nasal Vowels)
        aj_idx = apply_1_3_2_ajanunasika(varna_list)
        if aj_idx:
            it_indices.update(aj_idx)
            trace_log.append("१.३.२ उपदेशेऽजनुनासिक इत्")

        # 1.3.5 Adir Ñi-Tu-Davah (Initial Ñi, Tu, Du - Dhatus only)
        # The function internal logic usually handles the check, but checking source_type here is safer/clearer
        if source_type == UpadeshaType.DHATU:
            nit_idx, nit_trace = apply_1_3_5_adir_nitudavah(varna_list)
            if nit_idx:
                it_indices.update(nit_idx)
                trace_log.extend(nit_trace)

        # 1.3.6 Shah Pratyayasya (Initial Sh - Pratyayas only)
        sh_idx, sh_trace = apply_1_3_6_shah(varna_list, source_type)
        if sh_idx:
            it_indices.update(sh_idx)
            trace_log.extend(sh_trace)

        # 1.3.7 Chutu (Initial C-varga, T-varga - Pratyayas only)
        ch_idx, ch_trace = apply_1_3_7_chutu(varna_list, source_type)
        if ch_idx:
            it_indices.update(ch_idx)
            trace_log.extend(ch_trace)

        # 1.3.8 Lashakvataddhite (Initial L, S, K-varga - Non-Taddhita Pratyayas)
        # Need to know if it's Taddhita. For default Vibhakti/Pratyaya, we assume False (it is NOT Taddhita).
        is_taddhita = False
        la_idx, la_trace = apply_1_3_8_lashakva(varna_list, source_type, is_taddhita)
        if la_idx:
            it_indices.update(la_idx)
            trace_log.extend(la_trace)

        # =====================================================================
        # PHASE 3: SURGICAL REMOVAL (Tasya Lopah 1.3.9)
        # =====================================================================

        # Filter the list, keeping only indices NOT in it_indices
        cleaned_list = []
        for i, varna in enumerate(varna_list):
            if i in it_indices:
                # Mark as removed in the object itself for UI visualization (Ghost Tags)
                varna.sanjnas.add("इत्")
                varna.sanjnas.add("लोप")
            else:
                cleaned_list.append(varna)

        if it_indices:
            trace_log.append("१.३.९ तस्य लोपः (Removal of Markers)")

        return cleaned_list, trace_log