"""
FILE: logic/anga_processor.py
PAS-v6.0 (Siddha) | PILLAR: Anga-Adhikara (6.4 - 7.4)
"""
from core.core_foundation import Varna, sanskrit_varna_samyoga

class AngaProcessor:
    @staticmethod
    def is_blocked_kniti(suffix, context=None):
        if not suffix: return False
        tags = getattr(suffix[0], 'sanjnas', set())
        if any(t in tags for t in ['kit', 'ngit', 'gnit']): return True
        return False

    @staticmethod
    def apply_guna_7_3_84(anga, suffix, context=None):
        if AngaProcessor.is_blocked_kniti(suffix): return anga, "Blocked by 1.1.5"
        if not anga: return anga, None
        last = anga[-1]
        guna_map = {'इ': 'ए', 'ई': 'ए', 'उ': 'ओ', 'ऊ': 'ओ', 'ऋ': 'अर्', 'ॠ': 'अर्', 'ऌ': 'अल्'}
        if last.char in guna_map:
            res = guna_map[last.char]
            if len(res) > 1 and res != 'ओ' and res != 'ए':
                anga.pop()
                for c in res:
                    v = Varna(c); v.trace.append("7.3.84")
                    anga.append(v)
            else:
                last.char = res; last.trace.append("7.3.84")
            return anga, "7.3.84"
        return anga, None

    @staticmethod
    def apply_puganta_laghupadhasya_7_3_86(anga, suffix):
        if AngaProcessor.is_blocked_kniti(suffix): return anga, "Blocked by 1.1.5"
        if len(anga) < 2: return anga, None
        upadha = anga[-2]
        guna_map = {'इ': 'ए', 'उ': 'ओ', 'ऋ': 'अर्', 'ऌ': 'अल्'}
        if upadha.char in guna_map:
            upadha.char = guna_map[upadha.char]; upadha.trace.append("7.3.86")
            return anga, "7.3.86"
        return anga, None

    @staticmethod
    def apply_mrjer_vriddhih_7_2_114(anga, suffix):
        if AngaProcessor.is_blocked_kniti(suffix): return anga, "Blocked"
        applied = False
        for v in anga:
            if v.char == 'ऋ':
                v.char = 'आ'; v.trace.append("7.2.114"); applied = True
        return anga, "7.2.114" if applied else None

    @staticmethod
    def apply_aco_niti_7_2_115(anga, suffix):
        if not suffix: return anga, None
        tags = getattr(suffix[0], 'sanjnas', set())
        if not ({'nit', 'ṇit'} & tags): return anga, None
        last = anga[-1]
        vriddhi_map = {'अ': 'आ', 'इ': 'ऐ', 'ई': 'ऐ', 'उ': 'औ', 'ऊ': 'औ', 'ऋ': 'आर्', 'ए': 'ऐ', 'ओ': 'औ'}
        if last.char in vriddhi_map:
            res = vriddhi_map[last.char]
            if len(res) > 1 and res != 'औ' and res != 'ऐ':
                anga.pop()
                for c in res:
                    v = Varna(c); v.trace.append("7.2.115")
                    anga.append(v)
            else:
                last.char = res; last.trace.append("7.2.115")
            return anga, "7.2.115"
        return anga, None