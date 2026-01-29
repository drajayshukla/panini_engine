"""
FILE: logic/vidhi_engine.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Vidhi-Prakaraṇam (Operational Rules)
UPDATED: Fixed Upadha Index Calculation (limit - 2).
"""

from core.phonology import Varna, ad
from core.pratyahara_engine import PratyaharaEngine
from core.paribhasha_manager import ParibhashaManager
from core.upadesha_registry import UpadeshaType
from logic.sanjna_rules import is_ghi_1_4_7, is_nadi_1_4_3

pe = PratyaharaEngine()

class VidhiEngine:
    """
    विधि-सञ्चालक: (The Rule Executor)
    Contains operational rules for transformation (Adesha).
    Organized strictly by Ashtadhyayi Sutra Order.
    """

    # =========================================================================
    # BOOK 1: Definitions & Extensions
    # =========================================================================

    @staticmethod
    def apply_hrasva_napumsaka_1_2_47(varna_list):
        """[SUTRA]: ह्रस्वो नपुंसके प्रातिपदिकस्य (१.२.४७)"""
        if not varna_list: return varna_list, None
        last = varna_list[-1]
        mapping = {'आ': 'अ', 'ई': 'इ', 'ऊ': 'उ'}
        if last.char in mapping:
            old = last.char
            last.char = mapping[old]
            return varna_list, f"१.२.४७ ({old}->{last.char})"
        return varna_list, None

    # =========================================================================
    # BOOK 6: Anga & Sandhi Operations
    # =========================================================================

    @staticmethod
    def apply_hal_nyab_6_1_68(varna_list):
        """[SUTRA]: हल्ङ्याब्भ्यो दीर्घात् सुतिस्यपृक्तं हल् (६.१.६८)"""
        if not varna_list: return varna_list, None
        last = varna_list[-1]
        if last.char == 'स्':
            varna_list.pop()
            return varna_list, "६.१.६८ (सु-लोपः)"
        return varna_list, None

    @staticmethod
    def apply_ami_purvah_6_1_107(varna_list):
        """[SUTRA]: अमि पूर्वः (६.१.१०७)"""
        if len(varna_list) < 2: return varna_list, None
        v1 = varna_list[-2]
        v2 = varna_list[-1]
        if v1.char == 'अ' and v2.char == 'अ':
            varna_list.pop()
            return varna_list, "६.१.१०७ (अमि पूर्वः)"
        return varna_list, None

    @staticmethod
    def apply_upadha_dirgha_6_4_8(varna_list):
        """[SUTRA]: सर्वनामस्थाने चासम्बुद्धौ (६.४.८)"""
        if len(varna_list) < 2: return varna_list, None
        if varna_list[-1].char == 'न्':
            upadha = varna_list[-2]
            if upadha.char == 'अ':
                upadha.char = 'आ'
                return varna_list, "६.४.८ (उपधा दीर्घ)"
        return varna_list, None

    @staticmethod
    def apply_upadha_dirgha_6_4_11(varna_list):
        """[SUTRA]: अप्तृन्वृच्... (६.४.११)"""
        if len(varna_list) < 2: return varna_list, None
        upadha = varna_list[-2]
        if upadha.char == 'अ':
            upadha.char = 'आ'
            return varna_list, "६.४.११ (अ -> आ)"
        return varna_list, None

    @staticmethod
    def apply_ti_lopa_6_4_143(varna_list):
        """[SUTRA]: टेः (६.४.१४३)"""
        if len(varna_list) < 2: return varna_list, None
        limit = len(varna_list) - 1
        idx_to_remove = -1
        if varna_list[limit - 1].char == 'अ':
            idx_to_remove = limit - 1
        if idx_to_remove != -1:
            varna_list.pop(idx_to_remove)
            return varna_list, "६.४.१४३ (टि-लोपः)"
        return varna_list, None

    # =========================================================================
    # BOOK 7: Anga Transformations
    # =========================================================================

    @staticmethod
    def apply_ato_am_7_1_24(varna_list):
        """[SUTRA]: अतोऽम् (७.१.२४)"""
        if not varna_list: return varna_list, None
        last = varna_list[-1]
        if last.char == 'स्':
            last.char = 'म्'
            return varna_list, "७.१.२४ (सुँ -> अम्)"
        return varna_list, None

    @staticmethod
    def apply_add_7_1_25(varna_list):
        """[SUTRA]: अद्ड् डतरादिभ्यः पञ्चभ्यः (७.१.२५)"""
        if not varna_list: return varna_list, None
        last = varna_list[-1]
        if last.char in ['स्', 'म्']:
            last.char = 'त्'
            return varna_list, "७.१.२५ (अद्ड्-आदेशः)"
        return varna_list, None

    @staticmethod
    def apply_goto_nit_7_1_90(varna_list):
        """[SUTRA]: गोतो णित् (७.१.९०)"""
        return varna_list, "७.१.९० (णित्-वद्भाव)"

    @staticmethod
    def apply_anang_7_1_94(varna_list):
        """[SUTRA]: ऋदुशनस्पुरुदंसोऽनेहसां च (७.१.९४)"""
        if not varna_list: return varna_list, None
        last = varna_list[-1]
        if last.char == 'ऋ':
            last.char = 'अ'
            varna_list.append(Varna("न्"))
            return varna_list, "७.१.९४ (ऋ -> अनङ्)"
        return varna_list, None

    @staticmethod
    def apply_trijvadbhava_7_1_95(varna_list):
        """[SUTRA]: तृज्वत्क्रोष्टुः (७.१.९५)"""
        if len(varna_list) >= 2:
            if varna_list[-1].char == 'उ' and varna_list[-2].char == 'ट्':
                varna_list[-1].char = 'ऋ'
                return varna_list, "७.१.९५ (क्रोष्टु -> क्रोष्टृ)"
        return varna_list, None

    @staticmethod
    def apply_rayo_hali_7_2_85(varna_list):
        """[SUTRA]: रायो हलि (७.२.८५)"""
        if not varna_list: return varna_list, None
        last = varna_list[-1]
        if last.char == 'ऐ':
            last.char = 'आ'
            return varna_list, "७.२.८५ (ऐ -> आ)"
        return varna_list, None

    @staticmethod
    def apply_vṛddhi_7_2_115(varna_list):
        """[SUTRA]: अचो ञ्णिति (७.२.११५)"""
        if not varna_list: return varna_list, None
        last = varna_list[-1]
        mapping = {'ओ': 'औ', 'अ': 'आ', 'इ': 'ऐ', 'उ': 'औ'}
        if last.char in mapping:
            old = last.char
            last.char = mapping[old]
            return varna_list, f"७.२.११५ ({old}->{last.char})"
        return varna_list, None

    @staticmethod
    def apply_ata_upadhayah_7_2_116(anga_varnas, manual_range=None):
        """
        [SUTRA]: अत उपधायाः (७.२.११६)
        [LOGIC]: Short 'a' in penultimate position -> 'ā' if suffix is Ñit/Nit.
        [FIX]: limit-2 targets UPADHA (Penultimate), not Antya (Final).
        """
        if not anga_varnas: return anga_varnas, None

        limit = manual_range[1] if manual_range else len(anga_varnas)
        upadha_idx = limit - 2 # <--- [FIX]: -1 is Final, -2 is Upadha

        if upadha_idx < 0: return anga_varnas, None

        upadha_varna = anga_varnas[upadha_idx]

        if upadha_varna.char == 'अ':
            upadha_varna.char = 'आ'
            upadha_varna.sanjnas.add("वृद्धि")
            upadha_varna.trace.append("७.२.११६ अत उपधायाः")
            return anga_varnas, "७.२.११६ (अ -> आ)"
        return anga_varnas, None

    @staticmethod
    def apply_chajo_ku_7_3_52(anga_varnas, manual_range=None):
        """[SUTRA]: चजोः कु घिण्ण्यतोः (७.३.५२)"""
        if not anga_varnas: return anga_varnas, None
        limit = manual_range[1] if manual_range else len(anga_varnas)
        final_idx = limit - 1 # Correct for Final letter check
        if final_idx < 0: return anga_varnas, None
        final_varna = anga_varnas[final_idx]
        mapping = {'च्': 'क्', 'ज्': 'ग्'}
        if final_varna.char in mapping:
            old = final_varna.char
            final_varna.char = mapping[old]
            final_varna.trace.append("७.३.५२ चजोः कु...")
            return anga_varnas, f"७.३.५२ ({old} -> {final_varna.char})"
        return anga_varnas, None

    @staticmethod
    def apply_gher_niti_7_3_111(anga, nimitta=None):
        """[SUTRA]: घेर्ङिति (७.३.१११)"""
        if not is_ghi_1_4_7(anga): return anga, None
        last = anga[-1]
        guna_map = {'इ': 'ए', 'उ': 'ओ'}
        if last.char in guna_map:
            last.char = guna_map[last.char]
            return anga, "७.३.१११ (घेर्ङिति गुण)"
        return anga, None

    # =========================================================================
    # BOOK 8: Tripadi (Final Modifications)
    # =========================================================================

    @staticmethod
    def apply_nalopa_8_2_7(varna_list):
        """[SUTRA]: नलोपः प्रातिपदिकान्तस्य (८.२.७)"""
        if not varna_list: return varna_list, None
        last = varna_list[-1]
        if last.char == 'न्':
            varna_list.pop()
            return varna_list, "८.२.७ (न-लोपः)"
        return varna_list, None

    @staticmethod
    def apply_rutva_8_2_66(varna_list):
        """[SUTRA]: ससजुषो रुः (८.२.६६)"""
        if not varna_list: return varna_list, None
        last = varna_list[-1]
        if last.char == 'स्':
            last.char = 'र्'
            last.trace.append("८.२.६६ ससजुषो रुः")
            return varna_list, "८.२.६६ (स् -> रुँ -> र्)"
        return varna_list, None

    @staticmethod
    def apply_visarga_8_3_15(varna_list):
        """[SUTRA]: खरवसानयोर्विसर्जनीयः (८.३.१५)"""
        if not varna_list: return varna_list, None
        last = varna_list[-1]
        if last.char == 'र्':
            last.char = 'ः'
            last.trace.append("८.३.१५ विसर्गः")
            return varna_list, "८.३.१५ (र् -> ः)"
        return varna_list, None

    @staticmethod
    def apply_chartva_8_4_56(varna_list):
        """[SUTRA]: वाऽवसाने (८.४.५६)"""
        if not varna_list: return varna_list, None
        last = varna_list[-1]
        if last.char == 'द्':
            last.char = 'त्'
            return varna_list, "८.४.५६ (द् -> त्)"
        return varna_list, None


# =============================================================================
# EXPORTS (Module Level Aliases)
# =============================================================================

apply_hrasva_napumsaka_1_2_47 = VidhiEngine.apply_hrasva_napumsaka_1_2_47
apply_hal_nyab_6_1_68 = VidhiEngine.apply_hal_nyab_6_1_68
apply_ami_purvah_6_1_107 = VidhiEngine.apply_ami_purvah_6_1_107
apply_upadha_dirgha_6_4_8 = VidhiEngine.apply_upadha_dirgha_6_4_8
apply_upadha_dirgha_6_4_11 = VidhiEngine.apply_upadha_dirgha_6_4_11
apply_ti_lopa_6_4_143 = VidhiEngine.apply_ti_lopa_6_4_143
apply_ato_am_7_1_24 = VidhiEngine.apply_ato_am_7_1_24
apply_add_7_1_25 = VidhiEngine.apply_add_7_1_25
apply_goto_nit_7_1_90 = VidhiEngine.apply_goto_nit_7_1_90
apply_anang_7_1_94 = VidhiEngine.apply_anang_7_1_94
apply_trijvadbhava_7_1_95 = VidhiEngine.apply_trijvadbhava_7_1_95
apply_rayo_hali_7_2_85 = VidhiEngine.apply_rayo_hali_7_2_85
apply_vṛddhi_7_2_115 = VidhiEngine.apply_vṛddhi_7_2_115
apply_ata_upadhayah_7_2_116 = VidhiEngine.apply_ata_upadhayah_7_2_116
apply_chajo_ku_7_3_52 = VidhiEngine.apply_chajo_ku_7_3_52
apply_gher_niti_7_3_111 = VidhiEngine.apply_gher_niti_7_3_111
apply_nalopa_8_2_7 = VidhiEngine.apply_nalopa_8_2_7
apply_rutva_8_2_66 = VidhiEngine.apply_rutva_8_2_66
apply_visarga_8_3_15 = VidhiEngine.apply_visarga_8_3_15
apply_chartva_8_4_56 = VidhiEngine.apply_chartva_8_4_56