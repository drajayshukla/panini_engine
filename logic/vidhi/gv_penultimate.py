"""
FILE: logic/vidhi/gv_penultimate.py
PAS-v2.0: 5.2 (Siddha) | PILLAR: Guṇa-Vṛddhi (Penultimate/Final)
TIMESTAMP: 2026-01-30 20:15:00
"""
from .kniti_nisedha import KnitiNisedha
from core.phonology import Varna, sanskrit_varna_samyoga


class GvPenultimate:
    """
    [VṚTTI]: अङ्गस्य उपधा-अचः विकाराः।
    The Core Engine for Penultimate and Final Vowel Transformations (Guṇa/Vṛddhi).
    """

    @staticmethod
    def _get_ctx_val(context, key, default=False):
        """
        Helper: Safely retrieves values from either a Dictionary or an Object.
        Prevents AttributeError when context formats vary across tests.
        """
        if context is None:
            return default
        if isinstance(context, dict):
            return context.get(key, default)
        return getattr(context, key, default)

    # =========================================================================
    # CHAPTER 7.2: Vṛddhi Operations
    # =========================================================================

    @staticmethod
    def apply_vṛddhi_7_2_114(anga, suffix, context=None):
        """[७.२.११४]: मृजेर्वृद्धिः। Mṛj -> Mārj."""
        context = context or {}

        # 1.1.4 Check (Na Dhatulopa...)
        if GvPenultimate._get_ctx_val(context, "dhatulopa_caused_by_suffix"):
            return anga, "Blocked by 1.1.4"

        # 1.1.5 Check (Kniti Ca)
        if KnitiNisedha.is_blocked(suffix, context):
            return anga, "Blocked by 1.1.5"

        # Apply logic (Mṛj -> Mārj)
        applied = False
        for v in anga:
            if v.char == 'ऋ':
                v.char = 'आ'
                v.trace.append("७.२.११४")
                applied = True

        return anga, "७.२.११४" if applied else None

    @staticmethod
    def apply_aco_niti_7_2_115(anga, suffix, context=None):
        """[७.२.११५]: अचो ञ्णिति। Final Vowel Vṛddhi."""
        if not anga: return anga, None

        last = anga[-1]
        vriddhi_map = {
            'अ': 'आ', 'इ': 'ऐ', 'ई': 'ऐ',
            'उ': 'औ', 'ऊ': 'औ', 'ऋ': 'आर्', 'ओ': 'औ'
        }

        if last.char in vriddhi_map:
            res = vriddhi_map[last.char]
            if len(res) > 1:
                anga.pop()
                for c in res:
                    v = Varna(c)
                    v.trace.append("७.२.११५")
                    anga.append(v)
            else:
                last.char = res
                last.trace.append("७.२.११५")
            return anga, "७.२.११५"

        return anga, None

    @staticmethod
    def apply_ata_upadhayah_7_2_116(anga, suffix=None, context=None, manual_range=None):
        """[७.२.११६]: अत उपधायाः। Penultimate 'a' -> 'ā'."""
        if len(anga) < 2: return anga, None

        upadha_idx = -2
        if anga[upadha_idx].char == 'अ':
            anga[upadha_idx].char = 'आ'
            anga[upadha_idx].trace.append("७.२.११६")
            return anga, "७.२.११६"

        return anga, None

    # =========================================================================
    # CHAPTER 7.3: Guṇa Operations
    # =========================================================================

    @staticmethod
    def apply_mider_gunah_7_3_82(anga, suffix, context=None):
        """[७.३.८२]: मिदेर्गुणः। Mid -> Med."""
        if sanskrit_varna_samyoga(anga) == "मिद्":
            anga[1].char = "ए"
            anga[1].trace.append("७.३.८२")
            return anga, "७.३.८२"
        return anga, None

    @staticmethod
    def apply_sarvadhatuka_ardhadhatuka_7_3_84(anga, suffix, context=None):
        """[७.३.८४]: सार्वधातुकार्धधातुकयोः (Alias)."""
        return GvPenultimate.apply_guna_7_3_84(anga, suffix, context)

    @staticmethod
    def apply_guna_7_3_84(anga, suffix, context=None):
        """[७.३.८४]: Core logic with 1.1.5 and 1.1.4 Checks."""
        context = context or {}

        # 1.1.4 Niṣedha
        is_ardha = GvPenultimate._get_ctx_val(context, "is_ardhadhatuka")
        has_lopa = GvPenultimate._get_ctx_val(context, "dhatulopa_caused_by_suffix")

        if is_ardha and has_lopa:
            return anga, None

        # 1.1.5 Niṣedha
        if KnitiNisedha.is_blocked(suffix, context):
            KnitiNisedha.apply_1_1_5_block(anga, "7.3.84")
            return anga, None

        # 1.1.3 Paribhasha
        if not anga or anga[-1].char not in ['इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ॠ', 'ऌ']:
            return anga, None

            # Apply Guṇa
        last_char = anga[-1].char
        guna_map = {
            'इ': 'ए', 'ई': 'ए',
            'उ': 'ओ', 'ऊ': 'ओ',
            'ऋ': 'अर्', 'ॠ': 'अर्',
            'ऌ': 'अल्'
        }

        if last_char in guna_map:
            res = guna_map[last_char]
            if len(res) > 1:
                anga.pop()
                for c in res:
                    v = Varna(c)
                    v.trace.append("७.३.८४")
                    anga.append(v)
            else:
                anga[-1].char = res
                anga[-1].trace.append("७.३.८४")

            return anga, "७.३.८४"

        return anga, None

    @staticmethod
    def apply_puganta_laghupadhasya_7_3_86(anga, suffix, context=None):
        """[७.३.८६]: पुगन्तलघूपधस्य च (Guṇa)."""
        context = context or {}

        # Check Blocking (1.1.5)
        if KnitiNisedha.is_blocked(suffix, context):
            KnitiNisedha.apply_1_1_5_block(anga, "7.3.86")
            return anga, None

        # Logic for Laghu Upadha
        if len(anga) >= 2:
            upadha = anga[-2]
            guna_map = {'इ': 'ए', 'उ': 'ओ', 'ऋ': 'अर्', 'ऌ': 'अल्'}

            if upadha.char in guna_map:
                res = guna_map[upadha.char]
                if len(res) > 1:
                    # Simple char replacement won't work for >1 char outputs like 'ar'
                    # Future robust implementation needed here
                    pass
                else:
                    upadha.char = res
                    upadha.trace.append("७.३.८६")
                return anga, "७.३.८६"

        return anga, None

    @staticmethod
    def apply_jasi_ca_7_3_109(anga, suffix):
        """[७.३.१०९]: जसि च। Final 'i'/'u' guṇa before Jas."""
        if not anga: return anga, None
        last = anga[-1]
        if last.char in ['इ', 'उ']:
            last.char = 'ए' if last.char == 'इ' else 'ओ'
            last.trace.append("७.३.१०९")
            return anga, "७.३.१०९"
        return anga, None

    @staticmethod
    def apply_rto_ngi_sarvanamasthanayoh_7_3_110(anga, suffix):
        """[७.३.११०]: ऋतो ङिसर्वनामस्थानयोः।"""
        if not anga: return anga, None
        if anga[-1].char == 'ऋ':
            anga.pop()
            anga.append(Varna('अ'))
            anga.append(Varna('र्'))
            # Tracing
            if len(anga) >= 2:
                anga[-2].trace.append("७.३.११०")
                anga[-1].trace.append("७.३.११०")
            return anga, "७.३.११०"
        return anga, None

    @staticmethod
    def apply_guna_7_3_111(anga, suffix=None):
        """[७.३.१११]: घेर्ङिति। Ghi-Guṇa."""
        if anga and anga[-1].char in ['इ', 'उ']:
            v = anga[-1]
            v.char = 'ए' if v.char == 'इ' else 'ओ'
            v.trace.append("७.३.१११")
            return anga, "७.३.१११"
        return anga, None

    # =========================================================================
    # CHAPTER 7.4: Abhyāsa & Other Guṇa
    # =========================================================================

    @staticmethod
    def apply_guna_7_4_82(anga):
        """[७.४.८२]: गुणो यङ्लुकोः। Abhyāsa Guṇa."""
        for v in anga:
            if "abhyasa" in v.sanjnas:
                if v.char == 'इ':
                    v.char = 'ए'
                elif v.char == 'उ':
                    v.char = 'ओ'
                elif v.char == 'ऋ':
                    v.char = 'अर्'

                # If a change occurred
                if v.char in ['ए', 'ओ', 'अर्']:
                    v.trace.append("७.४.८२")
                    return anga, "७.४.८२"
        return anga, None

    # --- Traditional Aliases for External Compatibility ---
    apply_mṛjer_vṛddhiḥ_7_2_114 = apply_vṛddhi_7_2_114
    apply_gher_niti_7_3_111 = apply_guna_7_3_111
    apply_guno_yanlukoh_7_4_82 = apply_guna_7_4_82