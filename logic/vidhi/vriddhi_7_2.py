"""
FILE: logic/vidhi/vriddhi_7_2.py
PAS-v2.0: 5.2 (Siddha) | PILLAR: Vṛddhi Operations
"""
from .kniti_nisedha import KnitiNisedha
from core.phonology import Varna


class Vriddhi72:

    @staticmethod
    def apply_mṛjer_vṛddhiḥ_7_2_114(anga, suffix, context=None):
        """[७.२.११४]: मृजेर्वृद्धिः।"""
        # Context extraction helper (inline for brevity or shared util)
        is_lopa = context.get("dhatulopa_caused_by_suffix") if isinstance(context, dict) else getattr(context,
                                                                                                      "dhatulopa_caused_by_suffix",
                                                                                                      False) if context else False

        if is_lopa: return anga, "Blocked by 1.1.4"
        if KnitiNisedha.is_blocked(suffix, context): return anga, "Blocked by 1.1.5"

        for v in anga:
            if v.char == 'ऋ':
                v.char = 'आ'
                v.trace.append("७.२.११४")
                return anga, "७.२.११४"
        return anga, None

    @staticmethod
    def apply_aco_niti_7_2_115(anga, suffix, context=None):
        """[७.२.११५]: अचो ञ्णिति।"""
        if not anga: return anga, None
        last = anga[-1]

        # 1.1.3 Paribhasha implies Ik only, but 7.2.115 explicitly says 'Ac'.
        # However, for 'Gauh', 'o' -> 'au'.
        vriddhi_map = {
            'अ': 'आ', 'इ': 'ऐ', 'ई': 'ऐ',
            'उ': 'औ', 'ऊ': 'औ', 'ऋ': 'आर्', 'ओ': 'औ'
        }

        if last.char in vriddhi_map:
            res = vriddhi_map[last.char]
            if len(res) > 1:
                anga.pop()
                for c in res:
                    anga.append(Varna(c))
            else:
                last.char = res
            last.trace.append("७.२.११५")
            return anga, "७.२.११५"
        return anga, None

    @staticmethod
    def apply_ata_upadhayah_7_2_116(anga, suffix=None, context=None, manual_range=None):
        """[७.२.११६]: अत उपधायाः।"""
        if len(anga) < 2: return anga, None

        upadha_idx = -2
        if anga[upadha_idx].char == 'अ':
            anga[upadha_idx].char = 'आ'
            anga[upadha_idx].trace.append("७.२.११६")
            return anga, "७.२.११६"
        return anga, None