"""
FILE: logic/vidhi/__init__.py
PAS-v2.0: 5.2 (Siddha) | PILLAR: Vidhi-Vinyāsa (Orchestrator)
TIMESTAMP: 2026-01-30 20:30:00
"""
from .meta_rules import MetaRules
from .sandhi_engine import SandhiEngine
from .anga_transform import AngaTransform
from .tripadi import Tripadi
from .kniti_nisedha import KnitiNisedha

# --- MODULAR IMPORTS (Mandatory for 5.2 Architecture) ---
from .vriddhi_7_2 import Vriddhi72
from .guna_7_3 import Guna73
from .guna_misc import GunaMisc
from .gv_kutva import GvKutva  # Mandatory for Ghanj tests

# --- OPTIONAL IMPORTS ---
try:
    from .gv_taddhita import GvTaddhita
except ImportError:
    class GvTaddhita: pass

class VidhiEngine(
    MetaRules,
    SandhiEngine,
    AngaTransform,
    Tripadi,
    KnitiNisedha,
    Vriddhi72,
    Guna73,
    GunaMisc,
    GvKutva,
    GvTaddhita
):
    """
    [VṚTTI]: विधि-विन्द्यासस्य मुख्यपीठम्।
    The Universal Rule Executor: Coordinates all operational sūtras.
    """
    pass

# =============================================================================
# SŪTRA ALIASES (Mapping Tests to Logic)
# =============================================================================

# --- 1. Prohibitions (Niṣedha) ---
VidhiEngine.is_blocked_by_kniti_1_1_5 = KnitiNisedha.is_blocked

# --- 2. Sandhi ---
VidhiEngine.apply_iko_yan_achi_6_1_77 = SandhiEngine.apply_iko_yan_achi_6_1_77
VidhiEngine.apply_ayadi_6_1_78 = SandhiEngine.apply_ayadi_6_1_78
VidhiEngine.apply_aka_savarne_dirgha_6_1_101 = SandhiEngine.apply_aka_savarne_dirgha_6_1_101

# --- 3. Anga Operations (Stem Transformations) ---
VidhiEngine.apply_div_aut_7_1_84 = AngaTransform.apply_div_aut_7_1_84
VidhiEngine.apply_goto_nit_7_1_90 = MetaRules.apply_goto_nit_7_1_90
VidhiEngine.apply_haladi_shesha_7_4_60 = AngaTransform.apply_haladi_shesha_7_4_60
VidhiEngine.apply_urat_7_4_66 = AngaTransform.apply_urat_7_4_66
VidhiEngine.apply_rīk_āgama_7_4_90 = AngaTransform.apply_rik_agama_7_4_90
# Alias for spelling variant found in some tests
VidhiEngine.apply_rik_agama_7_4_90 = AngaTransform.apply_rik_agama_7_4_90

# --- 4. Vṛddhi (Chapter 7.2) ---
VidhiEngine.apply_mṛjer_vṛddhiḥ_7_2_114 = Vriddhi72.apply_mṛjer_vṛddhiḥ_7_2_114
VidhiEngine.apply_vṛddhi_7_2_114 = Vriddhi72.apply_mṛjer_vṛddhiḥ_7_2_114
VidhiEngine.apply_aco_niti_7_2_115 = Vriddhi72.apply_aco_niti_7_2_115
VidhiEngine.apply_ata_upadhayah_7_2_116 = Vriddhi72.apply_ata_upadhayah_7_2_116

# --- 5. Guṇa (Chapter 7.3 & 7.4) ---
VidhiEngine.apply_mider_gunah_7_3_82 = Guna73.apply_mider_gunah_7_3_82
VidhiEngine.apply_sarvadhatukardhadhatukayoh_7_3_84 = Guna73.apply_sarvadhatuka_ardhadhatuka_7_3_84
VidhiEngine.apply_guna_7_3_84 = Guna73.apply_sarvadhatuka_ardhadhatuka_7_3_84
VidhiEngine.apply_puganta_laghupadhasya_7_3_86 = Guna73.apply_puganta_laghupadhasya_7_3_86

VidhiEngine.apply_jasi_ca_7_3_109 = GunaMisc.apply_jasi_ca_7_3_109
VidhiEngine.apply_rto_ngi_sarvanamasthanayoh_7_3_110 = GunaMisc.apply_rto_ngi_sarvanamasthanayoh_7_3_110
VidhiEngine.apply_gher_niti_7_3_111 = GunaMisc.apply_gher_niti_7_3_111
VidhiEngine.apply_guno_yanlukoh_7_4_82 = GunaMisc.apply_guno_yanlukoh_7_4_82

# --- 6. Kutva (Velarization) ---
# Mandatory mapping for Ghanj tests
VidhiEngine.apply_chajo_ku_7_3_52 = GvKutva.apply_chajo_ku_7_3_52

# --- 7. Tripadi (Final Phonology) ---
VidhiEngine.apply_rutva_8_2_66 = Tripadi.apply_rutva_8_2_66
VidhiEngine.apply_visarga_8_3_15 = Tripadi.apply_visarga_8_3_15
VidhiEngine.apply_chartva_8_4_56 = Tripadi.apply_chartva_8_4_56
VidhiEngine.apply_natva_8_4_1 = Tripadi.apply_natva_8_4_1

# --- 8. Taddhita (Optional) ---
if hasattr(GvTaddhita, 'apply_vriddhi_7_2_117'):
    VidhiEngine.apply_taddhiteshu_acam_ade_7_2_117 = GvTaddhita.apply_vriddhi_7_2_117