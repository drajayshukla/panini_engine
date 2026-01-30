"""
FILE: logic/vidhi/guna_vriddhi.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Guṇa-Vṛddhi-Prakaraṇam
REFERENCE: 7.2.115, 7.2.116, 7.2.117, 7.3.52, 7.3.82, 7.3.84, 7.3.86, 7.3.111
"""
from core.phonology import Varna, sanskrit_varna_samyoga
from core.paribhasha_manager import ParibhashaManager
from .engine_base import VidhiEngineBase

class GunaVriddhi(VidhiEngineBase):
    """
    Handles all Guṇa and Vṛddhi transformations, including Kutva and
    penultimate modifications required by Aṅga-Adhikāra.
    """

    @staticmethod
    def apply_aco_niti_7_2_115(anga_varnas, suffix_varnas):
        """[SUTRA]: अचो ञ्णिति (७.२.११५) - Final Ac becomes Vriddhi."""
        if not anga_varnas or not suffix_varnas: return anga_varnas, None
        suffix_tags = getattr(suffix_varnas[0], 'sanjnas', set())
        if not ({'ñit', 'ṇit', 'ñ', 'ṇ', 'nit_vadbhava'} & suffix_tags): return anga_varnas, None
        last_varna = anga_varnas[-1]
        if not last_varna.is_vowel: return anga_varnas, None
        vriddhi_map = {'अ': 'आ', 'इ': 'ऐ', 'ई': 'ऐ', 'ए': 'ऐ', 'ऐ': 'ऐ', 'उ': 'औ', 'ऊ': 'औ', 'ओ': 'औ', 'औ': 'औ', 'ऋ': ['आ', 'र्'], 'ॠ': ['आ', 'र्']}
        if last_varna.char in vriddhi_map:
            old_char = last_varna.char
            new_val = vriddhi_map[old_char]
            if isinstance(new_val, list):
                new_varnas = [Varna(c) for c in new_val]
                for v in new_varnas: v.sanjnas.add("वृद्धि"); v.trace.append("७.२.११५")
                anga_varnas.pop(); anga_varnas.extend(new_varnas)
                return anga_varnas, f"७.२.११५ ({old_char} -> {''.join(new_val)})"
            last_varna.char = new_val; last_varna.sanjnas.add("वृद्धि"); last_varna.trace.append("७.२.११५")
            return anga_varnas, f"७.२.११५ ({old_char} -> {new_val})"
        return anga_varnas, None

    @staticmethod
    def apply_ata_upadhayah_7_2_116(anga_varnas, manual_range=None):
        """[SUTRA]: अत उपधायाः (७.२.११६) - Penultimate short 'a' -> 'ā'."""
        if not anga_varnas: return anga_varnas, None
        limit = manual_range[1] if manual_range else len(anga_varnas)
        upadha_idx = limit - 2
        if upadha_idx < 0: return anga_varnas, None
        upadha_varna = anga_varnas[upadha_idx]
        if upadha_varna.char == 'अ':
            old = upadha_varna.char
            upadha_varna.char = 'आ'
            upadha_varna.sanjnas.add("वृद्धि"); upadha_varna.trace.append("७.२.११६")
            return anga_varnas, f"७.२.११६ ({old} -> आ)"
        return anga_varnas, None

    @staticmethod
    def apply_taddhiteshu_acam_ade_7_2_117(anga_varnas, suffix_varnas):
        """[SUTRA]: तद्धितेष्वचामादेः (७.२.११७) - First vowel becomes Vriddhi."""
        if not anga_varnas or not suffix_varnas: return anga_varnas, None
        suffix_tags = getattr(suffix_varnas[0], 'sanjnas', set())
        if not ({'ñit', 'ṇit', 'ñ', 'ṇ'} & suffix_tags): return anga_varnas, None
        target_idx = -1
        for i, v in enumerate(anga_varnas):
            if v.is_vowel: target_idx = i; break
        if target_idx == -1: return anga_varnas, None
        target_vowel = anga_varnas[target_idx]
        vriddhi_map = {'अ': 'आ', 'इ': 'ऐ', 'ई': 'ऐ', 'उ': 'औ', 'ऊ': 'औ', 'ऋ': ['आ', 'र्'], 'ॠ': ['आ', 'र्'], 'ए': 'ऐ', 'ओ': 'औ'}
        old_char = target_vowel.char
        if old_char in vriddhi_map:
            new_val = vriddhi_map[old_char]
            if isinstance(new_val, list):
                new_varnas = [Varna(c) for c in new_val]
                for v in new_varnas: v.sanjnas.add("वृद्धि"); v.trace.append("७.२.११७")
                anga_varnas[target_idx : target_idx + 1] = new_varnas
                return anga_varnas, f"७.२.११७ ({old_char} -> {''.join(new_val)})"
            target_vowel.char = new_val; target_vowel.sanjnas.add("वृद्धि"); target_vowel.trace.append("७.२.११७")
            return anga_varnas, f"७.२.११७ ({old_char} -> {new_val})"
        return anga_varnas, None

    @staticmethod
    def apply_chajo_ku_7_3_52(anga_varnas, manual_range=None):
        """[SUTRA]: चजोः कु घिण्ण्यतोः (७.३.५२) - Kutva substitution."""
        if not anga_varnas: return anga_varnas, None
        limit = manual_range[1] if manual_range else len(anga_varnas)
        idx = limit - 1
        varna = anga_varnas[idx]
        mapping = {'च्': 'क्', 'ज्': 'ग्'}
        if varna.char in mapping:
            old = varna.char
            varna.char = mapping[old]; varna.trace.append("७.३.५२")
            return anga_varnas, f"७.३.५२ ({old} -> {varna.char})"
        return anga_varnas, None

    @staticmethod
    def apply_mider_gunah_7_3_82(anga_varnas, suffix_varnas):
        """[SUTRA]: मिदेर्गुणः (७.३.८२) - Guna for root 'Mid'."""
        if sanskrit_varna_samyoga(anga_varnas) != "मिद्": return anga_varnas, None
        if "śit" not in suffix_varnas[0].sanjnas: return anga_varnas, None
        for v in anga_varnas:
            if ParibhashaManager.is_ika_1_1_3(v) and v.char == 'इ':
                v.char = 'ए'; v.trace.append("७.३.८२")
                return anga_varnas, "७.३.८२ (मिदेर्गुणः)"
        return anga_varnas, None

    @staticmethod
    def apply_sarvadhatukardhadhatukayoh_7_3_84(anga_varnas, suffix_varnas):
        """[SUTRA]: सार्वधातुकार्धधातुकयोः (७.३.८४) - Guna for final Ik."""
        from .meta_rules import MetaRules
        if MetaRules.is_kniti_1_1_5(suffix_varnas): return anga_varnas, None
        last = anga_varnas[-1]
        if not ParibhashaManager.is_ika_1_1_3(last): return anga_varnas, None
        guna_map = {'इ': 'ए', 'ई': 'ए', 'उ': 'ओ', 'ऊ': 'ओ', 'ऋ': ['अ', 'र्'], 'ॠ': ['अ', 'र्']}
        if last.char in guna_map:
            old = last.char
            new_val = guna_map[old]
            if isinstance(new_val, list):
                new_varnas = [Varna(c) for c in new_val]
                for v in new_varnas: v.trace.append("७.३.८४ + १.१.५१")
                anga_varnas.pop(); anga_varnas.extend(new_varnas)
                return anga_varnas, f"७.३.८४ ({old}->अर्)"
            last.char = new_val; last.trace.append("७.३.८४")
            return anga_varnas, f"७.३.८४ ({old}->{new_val})"
        return anga_varnas, None

    @staticmethod
    def apply_puganta_laghupadhasya_7_3_86(anga_varnas, suffix_varnas):
        """[SUTRA]: पुगन्तलघूपधस्य च (७.३.८६) - Guna for penultimate Laghu Ik."""
        upadha_varna, upadha_idx = ParibhashaManager.get_upadha_1_1_65(anga_varnas)
        if upadha_idx == -1: return anga_varnas, None
        from logic.sanjna import SanjnaEngine
        if SanjnaEngine.is_laghu_1_4_10(anga_varnas, upadha_idx):
            guna_map = {'इ': 'ए', 'उ': 'ओ', 'ऋ': 'अर्', 'ऌ': 'अल्'}
            if upadha_varna.char in guna_map:
                old = upadha_varna.char
                upadha_varna.char = guna_map[old]; upadha_varna.trace.append("७.३.८६")
                return anga_varnas, f"७.३.८६ ({old} -> {upadha_varna.char})"
        return anga_varnas, None

    @staticmethod
    def apply_gher_niti_7_3_111(anga_varnas, suffix_varnas=None):
        """[SUTRA]: घेर्ङिति (७.३.१११) - Guna for Ghi-stems before Nit."""
        if not anga_varnas: return anga_varnas, None
        last = anga_varnas[-1]
        guna_map = {'इ': 'ए', 'उ': 'ओ'}
        if last.char in guna_map:
            old = last.char
            last.char = guna_map[old]; last.trace.append("७.३.१११")
            return anga_varnas, f"७.३.१११ ({old} -> {last.char})"
        return anga_varnas, None