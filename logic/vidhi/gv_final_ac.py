"""
FILE: logic/vidhi/gv_final_ac.py
PAS-v2.0: 5.0 (Siddha) | RATIO: ~28% Doc | LIMIT: < 200 Lines
TIMESTAMP: 2026-01-30 10:15:00
"""
from core.phonology import Varna
from core.paribhasha_manager import ParibhashaManager
from .meta_rules import MetaRules

class GvFinalAc:
    """[VṚTTI]: अङ्गान्त्य-अचः स्थाने गुणाः वृद्धयश्च।"""

    @staticmethod
    def apply_sarvadhatukardhadhatukayoh_7_3_84(anga, suffix, context=None):
        """[७.३.८४]: इगन्त-अङ्गस्य गुणः सार्वधातुकार्धधातुकयोः। (निषेधः: १.१.४)"""
        blocked, _ = MetaRules.is_blocked_1_1_4_5_6(anga, suffix, context)
        if blocked or not anga: return anga, None

        last = anga[-1]
        if not ParibhashaManager.is_ika_1_1_3(last): return anga, None

        g_map = {'इ':'ए', 'ई':'ए', 'उ':'ओ', 'ऊ':'ओ', 'ऋ':['अ','र्'], 'ॠ':['अ','र्']}
        if last.char in g_map:
            old = last.char; val = g_map[old]
            if isinstance(val, list):
                new_v = [Varna(c) for c in val]
                for v in new_v: v.trace.append("७.३.८४")
                anga.pop(); anga.extend(new_v)
                return anga, f"७.३.८४ ({old}->अर्)"
            last.char = val; last.trace.append("७.३.८४")
            return anga, f"७.३.८४ ({old}->{val})"
        return anga, None

    @staticmethod
    def apply_vṛddhi_7_2_115(anga, suffix, context=None):
        """
        [७.२.११५]: अचो ञ्णिति।
        Substitute Vṛddhi for the final vowel of an anga before Ñit or Ṇit suffixes.
        """
        # --- 1.1.4 / 1.1.5 / 1.1.6 Niṣedha Check ---
        blocked, _ = MetaRules.is_blocked_1_1_4_5_6(anga, suffix, context)
        if blocked or not anga or not suffix:
            return anga, None

        # --- Sanjñā Verification (Ñit/Ṇit) ---
        tags = getattr(suffix[0], 'sanjnas', set())
        if not ({'ñit', 'ṇit', 'nit_vadbhava'} & tags):
            return anga, None

        last = anga[-1]
        if not last.is_vowel:
            return anga, None

        # --- Transformation Map (Including Raparatva 1.1.51) ---
        v_map = {
            'अ': 'आ', 'इ': 'ऐ', 'ई': 'ऐ', 'उ': 'औ', 'ऊ': 'औ',
            'ए': 'ऐ', 'ओ': 'औ', 'ऋ': ['आ', 'र्'], 'ऌ': ['आ', 'ल्']
        }

        if last.char in v_map:
            old_char = last.char
            val = v_map[old_char]

            if isinstance(val, list):
                # Handle cases like ऋ -> आर् (Raparatva)
                new_varna_list = [Varna(c) for c in val]
                for v in new_varna_list:
                    v.sanjnas.add("वृद्धि")
                    v.trace.append("7.2.115")

                anga.pop()
                anga.extend(new_varna_list)
                return anga, "7.2.115"

            # Standard vowel substitution
            last.char = val
            last.sanjnas.add("वृद्धि")
            last.trace.append("7.2.115")
            return anga, "7.2.115"

        return anga, None

    # Alias for traditional nomenclature support
    apply_aco_niti_7_2_115 = apply_vṛddhi_7_2_115

    @staticmethod
    def apply_gher_niti_7_3_111(anga, suffix):
        """[७.३.१११]: घेः गुणः ङिति प्रत्यये। (निषेधः: १.१.५)"""
        if MetaRules.is_kniti_1_1_5(suffix) or not anga: return anga, None
        last = anga[-1]
        g_map = {'इ': 'ए', 'उ': 'ओ'}
        if last.char in g_map:
            old = last.char; last.char = g_map[old]
            last.trace.append("७.३.१११")
            return anga, f"७.३.१११ ({old}->{last.char})"
        return anga, None
