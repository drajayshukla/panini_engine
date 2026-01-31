"""
FILE: logic/__init__.py
TIMESTAMP: 2026-01-31 (IST)
LOCATION: Lucknow, Uttar Pradesh, India
QUALITY: PAS-v2.0: 6.0 (Subanta)
PILLAR: Logic-Interface (The Bridge)

DESCRIPTION:
    Unified public API / facade for the entire system.
    Combines Sanjñā queries, IT-prakaraṇam orchestration, and Vidhi rule delegates.
    Prevents AttributeErrors by only exposing real methods.
"""

# ────────────────────────────────────────────────
# Imports
# ────────────────────────────────────────────────

from core.sanjna_engine import SanjnaEngine
from logic.it_engine import ItEngine
from logic.vidhi.vidhi_engine import VidhiEngine
from logic.vidhi.kniti_nisedha import KnitiNisedha

# ────────────────────────────────────────────────
# SECTION 1: Sanjñā Foundation & Queries (1.1.x)
# ────────────────────────────────────────────────

# Boolean classifiers (fast checks)
is_hal                 = SanjnaEngine.is_hal
is_ac                  = SanjnaEngine.is_ac
is_vriddhi_1_1_1       = SanjnaEngine.is_vriddhi_1_1_1
is_guna_1_1_2          = SanjnaEngine.is_guna_1_1_2
is_samyoga_1_1_7       = SanjnaEngine.is_samyoga_1_1_7

# Labeling / tagging functions (in-place on Varna list)
label_vriddhi_and_guna    = SanjnaEngine.label_vriddhi_and_guna
label_samyoga             = SanjnaEngine.label_samyoga
run_basic_sanjna_labeling = SanjnaEngine.run_basic_sanjna_labeling

# ────────────────────────────────────────────────
# SECTION 2: It-Prakaraṇam (1.3.x lifecycle)
# ────────────────────────────────────────────────

# Full orchestration (most common entry point)
run_it_prakaran = ItEngine.run_it_prakaran

# Individual sūtra-level calls (for debugging / testing / special cases)
apply_1_3_2_ajanunasika = SanjnaEngine.apply_1_3_2_ajanunasika
apply_1_3_3_halantyam   = SanjnaEngine.apply_1_3_3_halantyam
apply_1_3_4_na_vibhaktau = SanjnaEngine.apply_1_3_4_na_vibhaktau
apply_1_3_5_adir_nitudavah = SanjnaEngine.apply_1_3_5_adir_nitudavah
apply_1_3_6_shah        = SanjnaEngine.apply_1_3_6_shah
apply_1_3_7_chutu       = SanjnaEngine.apply_1_3_7_chutu
apply_1_3_8_lashakva    = SanjnaEngine.apply_1_3_8_lashakva

run_tasya_lopah_1_3_9   = SanjnaEngine.run_tasya_lopah_1_3_9

# ────────────────────────────────────────────────
# SECTION 3: Morphological Saṃjñās (1.4.x)
# ────────────────────────────────────────────────

is_nadi_1_4_3  = SanjnaEngine.is_nadi_1_4_3
is_ghi_1_4_7   = SanjnaEngine.is_ghi_1_4_7
is_laghu_1_4_10 = SanjnaEngine.is_laghu_1_4_10
is_bha_1_4_18  = SanjnaEngine.is_bha_1_4_18

check_pada_sanjna_1_4_14 = SanjnaEngine.check_pada_sanjna_1_4_14

# Kniti niṣedha (1.1.5)
check_kniti_nisedha_1_1_5 = KnitiNisedha.is_blocked
apply_kniti_nisedha_1_1_5 = KnitiNisedha.apply_1_1_5_block

# ────────────────────────────────────────────────
# SECTION 4: Vidhi / Operation Delegates (6.x–8.x)
# ────────────────────────────────────────────────

# 6. Sandhi
apply_aka_savarne_dirgha_6_1_101 = VidhiEngine.apply_aka_savarne_dirgha_6_1_101
apply_vriddhi_rechi_6_1_88      = VidhiEngine.apply_vriddhi_rechi_6_1_88
apply_ayadi_6_1_78              = VidhiEngine.apply_ayadi_6_1_78           # ← added (used in your demo)

# 7. Subanta / Sarvanāma
apply_ato_bhisa_ais_7_1_9       = VidhiEngine.apply_ato_bhisa_ais_7_1_9
apply_jasah_shi_7_1_17          = VidhiEngine.apply_jasah_shi_7_1_17
apply_jasi_ca_7_3_109           = VidhiEngine.apply_jasi_ca_7_3_109       # ← critical for mati + jas demo
apply_sarvanamnah_smai_7_1_14   = VidhiEngine.apply_sarvanamnah_smai_7_1_14

# 8. Tripadi
apply_nalopa_8_2_7    = VidhiEngine.apply_nalopa_8_2_7
apply_rutva_8_2_66    = VidhiEngine.apply_rutva_8_2_66
apply_visarga_8_3_15  = VidhiEngine.apply_visarga_8_3_15
apply_chartva_8_4_56  = VidhiEngine.apply_chartva_8_4_56
apply_natva_8_4_1     = VidhiEngine.apply_natva_8_4_1

