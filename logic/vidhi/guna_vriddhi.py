"""
FILE: logic/vidhi/guna_vriddhi.py
PAS-v2.0: 5.0 (Siddha) | RATIO: ~70% Doc | LIMIT: < 200 Lines
TIMESTAMP: 2026-01-30 09:45:00
DESCRIPTION: Proxy Router for Guṇa-Vṛddhi Prakaraṇam.
"""
from .gv_final_ac import GvFinalAc
from .gv_penultimate import GvPenultimate
from .gv_taddhita import GvTaddhita
from .gv_kutva import GvKutva

class GunaVriddhi(GvFinalAc, GvPenultimate, GvTaddhita, GvKutva):
    """
    [VṚTTI]: गुणानां वृद्धीनां च सङ्ग्रहः।
    This class acts as a central proxy. It inherits from all specialized
    Guṇa-Vṛddhi sub-modules to maintain backward compatibility.

    [STRUCTURE]:
    - Final Vowels -> gv_final_ac.py
    - Penultimate -> gv_penultimate.py
    - Taddhita -> gv_taddhita.py
    - Kutva -> gv_kutva.py
    """

    @staticmethod
    def apply_aco_niti_7_2_115(anga, suffix):
        return GvFinalAc.apply_aco_niti_7_2_115(anga, suffix)

    @staticmethod
    def apply_ata_upadhayah_7_2_116(anga, manual_range=None):
        return GvPenultimate.apply_ata_upadhayah_7_2_116(anga, manual_range)

    @staticmethod
    def apply_sarvadhatukardhadhatukayoh_7_3_84(anga, suffix, context=None):
        return GvFinalAc.apply_sarvadhatukardhadhatukayoh_7_3_84(anga, suffix, context)

    @staticmethod
    def apply_puganta_laghupadhasya_7_3_86(anga, suffix, context=None):
        return GvPenultimate.apply_puganta_laghupadhasya_7_3_86(anga, suffix, context)

    @staticmethod
    def apply_chajo_ku_7_3_52(anga, manual_range=None):
        return GvKutva.apply_chajo_ku_7_3_52(anga, manual_range)