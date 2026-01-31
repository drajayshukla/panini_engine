"""
FILE: logic/vidhi/meta_rules.py
PAS-v2.0: 5.2 (Siddha) | PILLAR: Atideśa & Niṣedha (Extension & Prohibition)
TIMESTAMP: 2026-01-30 19:30:00
"""
from core.phonology import Varna, sanskrit_varna_samyoga


class MetaRules:
    """
    [VṚTTI]: अतिदेश-प्रतिषेध-सूत्राणि।
    Manages Meta-Rules:
    1. Atideśa (Extension): Treating X like Y (e.g., Go -> Nit-like).
    2. Niṣedha (Prohibition): Blocking operations (e.g., 1.1.4, 1.1.6).
    """

    # =========================================================================
    # SECTION 1: ATIDEŚA (Extension Rules)
    # =========================================================================

    @staticmethod
    def apply_goto_nit_7_1_90(suffix_varnas):
        """
        [७.१.९०]: गोतो णित्।
        The Sarvanāmasthāna suffixes (Su, Au, Jas, Am, Aut) are treated as
        having the 'Nit' (ṇit) marker when following the stem 'Go'.
        Effect: Triggers 7.2.115 (Aco ñṇiti) -> Vṛddhi (o -> au).
        """
        if suffix_varnas:
            suffix_varnas[0].sanjnas.add("ṇit")
            suffix_varnas[0].trace.append("७.१.९०")
            return "७.१.९०"
        return None

    @staticmethod
    def apply_sarvadhatukam_apit_1_2_4(suffix_varnas):
        """
        [१.२.४]: सार्वधातुकमपित्।
        A Sārvadhātuka suffix that is NOT Pit is treated as Nit (Ngit).
        Effect: Blocks Guṇa/Vṛddhi via 1.1.5 (Kṅiti ca).
        """
        if not suffix_varnas: return None

        has_pit = any("pit" in v.sanjnas for v in suffix_varnas)
        if not has_pit:
            suffix_varnas[0].sanjnas.add("ngit")
            suffix_varnas[0].trace.append("१.२.४")
            return "१.२.४"
        return None

    @staticmethod
    def apply_hrasva_napumsaka_1_2_47(varna_list):
        """[१.२.४७]: ह्रस्वो नपुंसके प्रातिपदिकस्य। Shortening in Neuters."""
        if not varna_list: return varna_list, None
        last = varna_list[-1]
        mapping = {'आ': 'अ', 'ई': 'इ', 'ऊ': 'उ', 'ॠ': 'ऋ'}
        if last.char in mapping:
            last.char = mapping[last.char]
            last.trace.append("१.२.४७")
            return varna_list, "१.२.४७"
        return varna_list, None

    # =========================================================================
    # SECTION 2: NIṢEDHA (Prohibition Logic)
    # =========================================================================

    @staticmethod
    def is_blocked_1_1_4_5_6(anga_varnas, suffix_varnas, context=None):
        """
        [१.१.४ - १.१.६]: गुणादीनां प्रतिषेधः।
        Checks for blocking conditions based on context and suffix tags.
        Legacy bridge for tests calling this specific function signature.
        """
        # --- १.१.५ क्ङिति च ---
        if MetaRules.is_kniti_1_1_5(suffix_varnas):
            return True, "१.१.५ (क्ङिति च)"

        # --- १.१.४ न धातुलोप आर्धधातुके ---
        if context and suffix_varnas:
            # Robust dictionary safe access
            is_ardha = context.get('is_ardhadhatuka', False) if isinstance(context, dict) else getattr(context,
                                                                                                       'is_ardhadhatuka',
                                                                                                       False)
            has_lopa = context.get('dhatulopa_caused_by_suffix', False) if isinstance(context, dict) else getattr(
                context, 'dhatulopa_caused_by_suffix', False)

            if is_ardha and has_lopa:
                return True, "१.१.४ (न धातुलोपः)"

        # --- १.१.६ दीधीवेवीटाम् ---
        stem = sanskrit_varna_samyoga(anga_varnas)
        if stem in ["दीधी", "वेवी"]:
            return True, "१.१.६ (दीधीवेवीटाम्)"

        # इट्-आगम-निषेधः
        if suffix_varnas and suffix_varnas[0].char == "इ":
            is_it = context.get('is_it_agama', False) if isinstance(context, dict) else getattr(context, 'is_it_agama',
                                                                                                False)
            if is_it:
                return True, "१.१.६ (दीधीवेवीटाम् - इट्)"

        return False, None

    @staticmethod
    def is_kniti_1_1_5(suffix_varnas):
        """
        [१.१.५]: क्ङिति च। (Internal Helper)
        Checks if suffix has Kit, Ngit, Git, or Gnit markers.
        """
        if not suffix_varnas: return False
        tags = getattr(suffix_varnas[0], 'sanjnas', set())
        # Comprehensive blocking tags
        return bool({'kit', 'ṅit', 'git', 'gnit', 'ngit'} & tags)