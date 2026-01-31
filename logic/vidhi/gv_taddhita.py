"""
FILE: logic/vidhi/gv_taddhita.py
PAS-v2.0: 5.2 (Siddha) | PILLAR: Taddhita (Secondary Derivation)
TIMESTAMP: 2026-01-30 20:45:00
"""
from core.phonology import Varna, sanskrit_varna_samyoga
from .meta_rules import MetaRules

class GvTaddhita:
    """
    [VṚTTI]: तद्धित-प्रक्रिया।
    Operations specific to Taddhita suffixes (Patronymics, etc.).
    """

    @staticmethod
    def apply_vriddhi_7_2_117(anga, suffix, context=None):
        """
        [७.२.११७]: तद्धितेष्वचामादेः।
        The first vowel (Ādi-Ac) of the stem grows (Vṛddhi) if the Taddhita suffix
        has markers like Ñit or Ṇit.
        Example: Upagu + aṇ -> Aupagu.
        """
        if not anga: return anga, None

        # --- 1. PROHIBITION CHECK ---
        blocked, _ = MetaRules.is_blocked_1_1_4_5_6(anga, suffix, context)
        if blocked: return anga, None

        # --- 2. TRIGGER CHECK (Ñit / Ṇit) ---
        has_trigger = False
        if suffix:
            tags = getattr(suffix[0], 'sanjnas', set())
            if any(t in tags for t in ["ñit", "ṇit", "nit_vadbhava"]):
                has_trigger = True

        if not has_trigger: return anga, None

        # --- 3. FIND FIRST VOWEL (Adi Ac) ---
        for i, v in enumerate(anga):
            if v.is_vowel:
                # --- 4. APPLY VRIDDHI ---
                vriddhi_map = {
                    'अ': 'आ', 'इ': 'ऐ', 'ई': 'ऐ', 'ए': 'ऐ',
                    'उ': 'औ', 'ऊ': 'औ', 'ओ': 'औ',
                    'ऋ': ['आ', 'र्'], 'ॠ': ['आ', 'र्'] # Handling Raparatva 1.1.51
                }

                old_char = v.char
                if old_char in vriddhi_map:
                    new_val = vriddhi_map[old_char]

                    # Handle multi-varna substitution (e.g. Ṛ -> ĀR)
                    if isinstance(new_val, list):
                        new_varnas = [Varna(c) for c in new_val]
                        for nv in new_varnas:
                            nv.sanjnas.add("vriddhi")
                            nv.trace.append("७.२.११७")
                        # Replace in place
                        anga[i:i+1] = new_varnas
                    else:
                        # Standard Substitution
                        v.char = new_val
                        v.sanjnas.add("vriddhi")
                        v.trace.append("७.२.११७")

                    return anga, "७.२.११७"
                break # Only the first vowel changes

        return anga, None

    @staticmethod
    def apply_or_gunah_6_4_146(anga, suffix, context=None):
        """
        [६.४.१४६]: ओर्गुणः।
        The final 'u' (or 'ū') of a Bha-stem is replaced by Guṇa ('o')
        when a Taddhita suffix follows.
        Example: Aupagu + a -> Aupago + a.
        """
        if not anga: return anga, None

        last = anga[-1]
        # Check if it ends in u/ū
        if last.char in ['उ', 'ऊ']:
            # Apply Guṇa (o)
            last.char = 'ओ'
            last.trace.append("६.४.१४६")
            return anga, "६.४.१४६"

        return anga, None

    # --- Traditional Alias for VidhiEngine Bridge ---
    apply_taddhiteshu_acam_ade_7_2_117 = apply_vriddhi_7_2_117