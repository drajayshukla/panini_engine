"""
FILE: logic/__init__.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Logic-Interface
DESCRIPTION: Bridges modular engines to the rest of the application.
"""

from .vidhi import VidhiEngine
from .sanjna import SanjnaEngine

# =============================================================================
# SECTION 1: Foundation & Sanjñā Bridge
# =============================================================================

# 1.1 Foundation
apply_1_1_1_vriddhi = SanjnaEngine.apply_1_1_1_vriddhi
apply_1_1_2_guna = SanjnaEngine.is_guna_1_1_2
apply_1_1_2_guna_alias = SanjnaEngine.is_guna_1_1_2 # Alias for backward compatibility
apply_1_1_7_samyoga = SanjnaEngine.apply_1_1_7_samyoga

# 1.3 It-Prakaranam
apply_1_3_2_ajanunasika = SanjnaEngine.apply_1_3_2_ajanunasika
apply_1_3_3_halantyam = SanjnaEngine.apply_1_3_3_halantyam
apply_1_3_4_na_vibhaktau = SanjnaEngine.apply_1_3_4_na_vibhaktau
apply_1_3_5_adir_nitudavah = SanjnaEngine.apply_1_3_5_adir_nitudavah
apply_1_3_6_shah = SanjnaEngine.apply_1_3_6_shah
apply_1_3_7_chutu = SanjnaEngine.apply_1_3_7_chutu
apply_1_3_8_lashakva = SanjnaEngine.apply_1_3_8_lashakva

# 1.4 Morphology
is_nadi_1_4_3 = SanjnaEngine.is_nadi_1_4_3
is_ghi_1_4_7 = SanjnaEngine.is_ghi_1_4_7
is_laghu_1_4_10 = SanjnaEngine.is_laghu_1_4_10
check_pada_sanjna_1_4_14 = SanjnaEngine.check_pada_sanjna_1_4_14
apply_1_4_14_pada = SanjnaEngine.check_pada_sanjna_1_4_14
is_bha_1_4_18 = SanjnaEngine.is_bha_1_4_18

# =============================================================================
# SECTION 2: Vidhi (Operation) Bridge
# =============================================================================

# 6.x / 7.x Operations
apply_vṛddhi_7_2_115 = VidhiEngine.apply_aco_niti_7_2_115
apply_vṛddhi_7_2_117 = VidhiEngine.apply_taddhiteshu_acam_ade_7_2_117
apply_ata_upadhayah_7_2_116 = VidhiEngine.apply_ata_upadhayah_7_2_116
apply_chajo_ku_7_3_52 = VidhiEngine.apply_chajo_ku_7_3_52
apply_gher_niti_7_3_111 = VidhiEngine.apply_gher_niti_7_3_111

# 8.x Tripadi
apply_nalopa_8_2_7 = VidhiEngine.apply_nalopa_8_2_7
apply_rutva_8_2_66 = VidhiEngine.apply_rutva_8_2_66
apply_visarga_8_3_15 = VidhiEngine.apply_visarga_8_3_15
apply_chartva_8_4_56 = VidhiEngine.apply_chartva_8_4_56