"""
FILE: logic/vidhi/sandhi_engine.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Saṃhitā-Prakaraṇam (Sandhi Engine)
REFERENCE: ६.१.७७ इको यणचि
"""
from core.phonology import Varna

class SandhiEngine:
    @staticmethod
    def apply_iko_yan_achi_6_1_77(anga_varnas, suffix_varnas=None):
        """[SUTRA]: इको यणचि (६.१.७७)"""
        if len(anga_varnas) < 2: return anga_varnas, None
        for i in range(len(anga_varnas) - 1):
            curr, nxt = anga_varnas[i], anga_varnas[i + 1]
            if curr.char in ['इ', 'ई'] and nxt.is_vowel:
                old = curr.char
                curr.char = 'य्'
                curr.trace.append("६.१.७७")
                return anga_varnas, f"६.१.७७ ({old} -> य्)"
        return anga_varnas, None

    @staticmethod
    def apply_ayadi_6_1_78(anga_varnas, suffix_varnas):
        """[SUTRA]: एचोऽयवायावः (६.१.७८)"""
        if not anga_varnas or not suffix_varnas: return anga_varnas, None
        last_varna = anga_varnas[-1]
        if not suffix_varnas[0].is_vowel: return anga_varnas, None
        mapping = {'ए': ['अ', 'य्'], 'ओ': ['अ', 'व्'], 'ऐ': ['आ', 'य्'], 'औ': ['आ', 'व्']}
        if last_varna.char in mapping:
            old_char = last_varna.char
            substitutes = mapping[old_char]
            anga_varnas.pop()
            for char in substitutes:
                v = Varna(char)
                v.trace.append("६.१.७८")
                anga_varnas.append(v)
            return anga_varnas, f"६.१.७८ ({old_char} -> {''.join(substitutes)})"
        return anga_varnas, None

    @staticmethod
    def apply_aka_savarne_dirgha_6_1_101(anga_varnas, suffix_varnas):
        """[SUTRA]: अकः सवर्णे दीर्घः (६.१.१०१)"""
        if not anga_varnas or not suffix_varnas: return anga_varnas, None
        last, first = anga_varnas[-1], suffix_varnas[0]
        sav_pairs = {'अ': ['अ', 'आ'], 'आ': ['अ', 'आ'], 'इ': ['इ', 'ई'], 'ई': ['इ', 'ई'], 'उ': ['उ', 'ऊ'], 'ऊ': ['उ', 'ऊ']}
        if last.char in sav_pairs and first.char in sav_pairs[last.char]:
            long_map = {'अ': 'आ', 'आ': 'आ', 'इ': 'ई', 'ई': 'ई', 'उ': 'ऊ', 'ऊ': 'ऊ'}
            res = long_map[last.char]
            last.char = res
            last.trace.append("६.१.१०१")
            suffix_varnas.pop(0)
            return anga_varnas, f"६.१.१०१ ({res})"
        return anga_varnas, None

    @staticmethod
    def apply_ami_purvah_6_1_107(varna_list):
        """[SUTRA]: अमि पूर्वः (६.१.१०७)"""
        if len(varna_list) < 2: return varna_list, None
        v1, v2 = varna_list[-2], varna_list[-1]
        if v1.char == 'अ' and v2.char == 'अ':
            varna_list.pop()
            return varna_list, "६.१.१०७ (अमि पूर्वः)"
        return varna_list, None