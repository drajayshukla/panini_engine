"""
FILE: core/sanjna_engine.py
PAS-v2.0: 6.0 (Siddha)
ROLE: The Sanjñā Orchestrator & Query Interface
DESCRIPTION:
    A unified facade combining phonemic class queries (Vriddhi, Guna, Hal, Ac)
    with the v6.0 It-marker identification logic.
    Maintains compatibility with the logic bridge to prevent AttributeErrors.
"""
"""
FILE: core/sanjna_engine.py
PAS-v2.0: 6.0 (Siddha)
ROLE: The Saṃjñā Orchestrator & Query Interface
DESCRIPTION:
    Unified facade that provides:
      - Fast phonemic classification queries (hal/ac/vriddhi/guna/samyoga)
      - IT-marker identification & removal logic (1.3.x series)
      - In-place saṃjñā labeling on Varna objects
      - Morphological classification stubs (1.4.x) for future expansion
    Maintains compatibility bridge to logic/sanjna/it_prakaranam.py
"""

from typing import List, Set, Tuple, Optional, Union

from core.pratyahara_engine import PratyaharaEngine
from core.phonology import Varna
from core.upadesha_registry import UpadeshaType
from logic.sanjna.it_prakaranam import ItSanjnas


# Global instance for fast pratyāhāra lookups
pe = PratyaharaEngine()


class SanjnaEngine:
    """
    अथ संज्ञा-प्रकरणम् — The Definition Engine

    Three main responsibilities:
    1. Quick boolean queries for sandhi & phonology
    2. IT-saṃjñā identification, tagging and lopah (1.3 section)
    3. Basic morphological saṃjñās & labeling (1.1 + 1.4 stubs)
    """

    # ────────────────────────────────────────────────
    # ROLE 1: Fast Phonemic Classification Queries
    # ────────────────────────────────────────────────

    @staticmethod
    def is_vriddhi_1_1_1(char: str) -> bool:
        """वृद्धिरादैच् १.१.१"""
        return char == 'आ' or pe.is_in(char, "ऐच्")

    @staticmethod
    def is_guna_1_1_2(char: str) -> bool:
        """अदेङ् गुणः १.१.२"""
        return char == 'अ' or pe.is_in(char, "एङ्")

    @staticmethod
    def is_hal(char: str) -> bool:
        """हल्"""
        return pe.is_in(char, "हल्")

    @staticmethod
    def is_ac(char: str) -> bool:
        """अच्"""
        return pe.is_in(char, "अच्")

    @staticmethod
    def is_samyoga_1_1_7(varnas: List[Union[str, Varna]]) -> bool:
        """हलोऽनन्तराः संयोगः १.१.७"""
        if len(varnas) < 2:
            return False
        chars = [v.char if isinstance(v, Varna) else v for v in varnas]
        return all(SanjnaEngine.is_hal(c) for c in chars)

    # ────────────────────────────────────────────────
    # ROLE 2: IT-Prakaraṇam — Identification & Removal
    # ────────────────────────────────────────────────

    @staticmethod
    def identify_and_tag_its(
        varna_list: List[Varna],
        source_type: str,
        is_taddhita: bool = False
    ) -> Tuple[List[Varna], Set[str]]:
        """Master entry point — delegates to ItSanjnas"""
        return ItSanjnas.identify_and_tag_its(varna_list, source_type, is_taddhita)

    @staticmethod
    def apply_1_3_2_ajanunasika(varna_list: List[Varna]) -> Tuple[List[Varna], Set[str]]:
        """उपदेशेऽजनुनासिक इत् १.३.२"""
        return ItSanjnas.apply_1_3_2_ajanunasika(varna_list)

    @staticmethod
    def apply_1_3_3_halantyam(
        varna_list: List[Varna],
        source_type: str,
        blocked: Optional[Set[str]] = None
    ) -> Tuple[List[Varna], Set[str]]:
        """हलन्त्यम् १.३.३"""
        return ItSanjnas.apply_1_3_3_halantyam(varna_list, source_type, blocked)

    @staticmethod
    def apply_1_3_4_na_vibhaktau(
        varna_list: List[Varna],
        source_type: str
    ) -> Tuple[List[Varna], Set[str]]:
        """
        न विभक्तौ तुस्माः १.३.४
        Usually handled inside 1.3.3 when source_type indicates vibhakti.
        Kept for explicit calls / bridge compatibility.
        """
        if hasattr(ItSanjnas, 'apply_1_3_4_na_vibhaktau'):
            return ItSanjnas.apply_1_3_4_na_vibhaktau(varna_list, source_type)
        # Minimal fallback
        return varna_list, {"1.3.4 (handled implicitly or blocked)"}

    @staticmethod
    def apply_1_3_5_adir_nitudavah(varna_list: List[Varna]) -> Tuple[List[Varna], Set[str]]:
        """आदिर्निटुडवः १.३.५"""
        return ItSanjnas.apply_1_3_5_adir_nitudavah(varna_list)

    @staticmethod
    def apply_1_3_6_shah(
        varna_list: List[Varna],
        source_type: str
    ) -> Tuple[List[Varna], Set[str]]:
        """षः प्रत्ययस्य १.३.६"""
        try:
            return ItSanjnas.apply_1_3_6_shah(varna_list, source_type)
        except AttributeError:
            if source_type == UpadeshaType.PRATYAYA and varna_list and varna_list[0].char == 'ष्':
                varna_list[0].sanjnas.add("it")
                return varna_list, {0}, {"1.3.6 ṣaḥ (fallback)"}
            return varna_list, set(), set()

    @staticmethod
    def apply_1_3_7_chutu(
        varna_list: List[Varna],
        source_type: Optional[str] = None
    ) -> Tuple[List[Varna], Set[str]]:
        """चुटू १.३.७"""
        return ItSanjnas.apply_1_3_7_chutu(varna_list, source_type)

    @staticmethod
    def apply_1_3_8_lashakva(
        varna_list: List[Varna],
        source_type: str,
        is_taddhita: bool = False
    ) -> Tuple[List[Varna], Set[str]]:
        """लशक्वतद्धिते १.३.८"""
        return ItSanjnas.apply_1_3_8_lashakva(varna_list, source_type, is_taddhita)

    @staticmethod
    def run_tasya_lopah_1_3_9(
        varna_list: List[Varna],
        it_indices: Set[int]
    ) -> Tuple[List[Varna], Set[str]]:
        """तस्य लोपः १.३.९ — physical removal + DNA inheritance"""
        return ItSanjnas.run_tasya_lopah_1_3_9(varna_list, it_indices)

    # ────────────────────────────────────────────────
    # ROLE 3: Basic Morphological Labeling & Stubs
    # ────────────────────────────────────────────────

    @staticmethod
    def label_vriddhi_and_guna(varna_list: List[Varna]) -> List[Varna]:
        """Labels vriddhi & guna saṃjñās in-place"""
        for v in varna_list:
            char = v.char
            if SanjnaEngine.is_vriddhi_1_1_1(char):
                v.sanjnas.add("vriddhi")
            if SanjnaEngine.is_guna_1_1_2(char):
                v.sanjnas.add("guna")
        return varna_list

    @staticmethod
    def label_samyoga(varna_list: List[Varna]) -> List[Varna]:
        """Labels संयोग saṃjñā when applicable"""
        if SanjnaEngine.is_samyoga_1_1_7(varna_list):
            for v in varna_list:
                v.sanjnas.add("samyoga")
        return varna_list

    @staticmethod
    def run_basic_sanjna_labeling(varna_list: List[Varna]) -> List[Varna]:
        """Convenience: vriddhi + guna + samyoga labeling"""
        SanjnaEngine.label_vriddhi_and_guna(varna_list)
        SanjnaEngine.label_samyoga(varna_list)
        return varna_list

    # 1.4 stubs — to be filled later
    @staticmethod
    def is_nadi_1_4_3(v: Varna) -> bool: return False
    @staticmethod
    def is_ghi_1_4_7(v: Varna) -> bool: return False
    @staticmethod
    def is_laghu_1_4_10(v: Varna) -> bool: return False
    @staticmethod
    def is_bha_1_4_18(v: Varna) -> bool: return False

    @staticmethod
    def check_pada_sanjna_1_4_14(v: Varna) -> Tuple[Varna, str]:
        return v, "1.4.14 (stub)"