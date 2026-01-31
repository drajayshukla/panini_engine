"""
FILE: logic/vidhi/vidhi_engine.py
TIMESTAMP: 2026-01-31 01:55:00 (IST)
LOCATION: Lucknow, Uttar Pradesh, India
QUALITY: PAS-v2.0: 6.0 (Subanta) | PILLAR: Master Interface (Facade)
DESCRIPTION: Central Gateway for all grammatical operations.
             Delegates to Sandhi, Tripadi, Subanta, and Sarvanama engines.
"""
from logic.vidhi.sandhi_engine import SandhiEngine
from logic.vidhi.tripadi import Tripadi
from logic.vidhi.subanta_vidhi import SubantaVidhi
from logic.vidhi.sarvanama_vidhi import SarvanamaVidhi

class VidhiEngine:
    """
    The Gateway for all Operational Rules (Vidhi).
    Centralizes the logic to ensure Strategy engines (like s_1_1.py)
    interact with a single interface.
    """

    # =========================================================
    # 1. SANDHI (Chapter 6)
    # =========================================================

    @staticmethod
    def apply_aka_savarne_dirgha_6_1_101(anga, suffix):
        return SandhiEngine.apply_aka_savarne_dirgha_6_1_101(anga, suffix)

    @staticmethod
    def apply_vriddhi_rechi_6_1_88(anga, suffix):
        return SandhiEngine.apply_vriddhi_rechi_6_1_88(anga, suffix)

    @staticmethod
    def apply_ami_purvah_6_1_107(stem, suffix):
        """[6.1.107] अमि पूर्वः - पूर्वरूपैकादेशः"""
        return SandhiEngine.apply_ami_purvah_6_1_107(stem, suffix)

    @staticmethod
    def apply_ayadi_6_1_78(stem, suffix):
        """[6.1.78] एचोऽयवायावः - अय्-आय्-अव्-आव् आदेशाः"""
        return SandhiEngine.apply_ayadi_6_1_78(stem, suffix)

    # =========================================================
    # 2. SUBANTA & SARVANAMA (Chapter 7)
    # =========================================================

    @staticmethod
    def apply_ato_bhisa_ais_7_1_9(stem, suffix):
        return SubantaVidhi.apply_ato_bhisa_ais_7_1_9(stem, suffix)

    @staticmethod
    def apply_ato_am_7_1_24(stem, suffix):
        """[7.1.24] अतोऽम् - सुँ-प्रत्ययस्य अम्-आदेशः"""
        return SubantaVidhi.apply_ato_am_7_1_24(stem, suffix)

    @staticmethod
    def apply_jasi_ca_7_3_109(stem, suffix):
        """[7.3.109] जसि च - इदुद्भ्यां गुणः"""
        return SubantaVidhi.apply_jasi_ca_7_3_109(stem, suffix)

    @staticmethod
    def apply_rto_ngi_sarvanamasthanayoh_7_3_110(stem, suffix):
        """[7.3.110] ऋतो ङिसर्वनामस्थानयोः - ऋकारस्य गुणः (अर्)"""
        return SubantaVidhi.apply_rto_ngi_sarvanamasthanayoh_7_3_110(stem, suffix)

    @staticmethod
    def apply_jasah_shi_7_1_17(stem, suffix):
        return SarvanamaVidhi.apply_jasah_shi_7_1_17(stem, suffix)

    @staticmethod
    def apply_sarvanamnah_smai_7_1_14(stem, suffix):
        return SarvanamaVidhi.apply_sarvanamnah_smai_7_1_14(stem, suffix)

    # =========================================================
    # 3. TRIPADI (Chapter 8)
    # =========================================================

    @staticmethod
    def apply_rutva_8_2_66(varnas):
        return Tripadi.apply_rutva_8_2_66(varnas)

    @staticmethod
    def apply_visarga_8_3_15(varnas):
        return Tripadi.apply_visarga_8_3_15(varnas)

    @staticmethod
    def apply_nalopa_8_2_7(varnas):
        return Tripadi.apply_nalopa_8_2_7(varnas)

    @staticmethod
    def apply_natva_8_4_1(varnas):
        return Tripadi.apply_natva_8_4_1(varnas)

    @staticmethod
    def apply_chartva_8_4_56(varnas):
        return Tripadi.apply_chartva_8_4_56(varnas)

    # =========================================================
    # 4. REMAINING STUBS & PLACEHOLDERS
    # =========================================================

    @staticmethod
    def apply_trijvadbhava_7_1_95(stem):
        return stem, "7.1.95 (Stub)"

    @staticmethod
    def apply_anang_7_1_94(stem):
        return stem, "7.1.94 (Stub)"

    @staticmethod
    def apply_hal_nyab_6_1_68(stem):
        return stem, "6.1.68 (Stub)"

    @staticmethod
    def apply_upadha_dirgha_6_4_11(stem):
        return stem, "6.4.11 (Stub)"

    @staticmethod
    def apply_upadha_dirgha_6_4_8(stem):
        return stem, "6.4.8 (Stub)"

    @staticmethod
    def apply_goto_nit_7_1_90(stem):
        return stem, "7.1.90 (Stub)"

    @staticmethod
    def apply_vṛddhi_7_2_115(stem, suffix):
        # Vriddhi logic (e.g. for Nayakah) should be moved to SubantaVidhi/Sandhi
        # Returning a stub until fully modularized in GunaVriddhi logic
        return stem, "7.2.115 (Stub)"

    @staticmethod
    def apply_rayo_hali_7_2_85(stem):
        return stem, "7.2.85 (Stub)"

    @staticmethod
    def apply_add_7_1_25(stem):
        return stem, "7.1.25 (Stub)"

    @staticmethod
    def apply_ti_lopa_6_4_143(stem):
        return stem, "6.4.143 (Stub)"

    @staticmethod
    def apply_hrasva_napumsaka_1_2_47(stem):
        return stem, "1.2.47 (Stub)"