"""
FILE: core/paribhasha_manager.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Paribhāṣā (Meta-Rules)
PURPOSE: Manages interpretive rules that decide HOW and WHERE Vidhi rules apply.
"""

from core.phonology import Varna


def get_sutra_link(sutra_num):
    """Helper to generate links to Ashtadhyayi.com for reference."""
    return f"https://ashtadhyayi.com/sutraani/{sutra_num.replace('.', '/')}"


class ParibhashaManager:
    """
    परिभाषा-सञ्चालक: (The Interpretive Engine)
    Zone 2: Global guidelines for rule application, targeting, and interpretation.
    """

    # =========================================================================
    # SECTION 1.1: Interpretive Definitions (Sthana-Nirdesha)
    # =========================================================================

    @staticmethod
    def is_ika_1_1_3(varna_input):
        """
        [SUTRA]: इकः गुणवृद्धी (१.१.३)
        [MEANING]: Guna and Vriddhi prescribed without a specific sthanin
                   apply ONLY to 'Ik' letters (i, u, ṛ, ḷ).
        """
        char = varna_input.char if hasattr(varna_input, 'char') else varna_input

        # Pratyahara 'Ik' includes short and long vowels
        ik_set = {
            'इ', 'ई',  # i, ī
            'उ', 'ऊ',  # u, ū
            'ऋ', 'ॠ',  # ṛ, ṝ
            'ऌ', 'ॡ'  # ḷ, ḹ
        }

        return char in ik_set

    @staticmethod
    def resolve_shashthi_1_1_49(target_index=None):
        """
        [SUTRA]: षष्ठी स्थानेयोगा (१.१.४९)
        [LOGIC]: Genitive Case (Shashthi) -> Operation is a Substitution (Sthana).
        Note: This is usually implicit in the Vidhi engine, but good to define.
        """
        return "SUBSTITUTION"

    # =========================================================================
    # SECTION 1.1: Structural Definitions (Anga Analysis)
    # =========================================================================

    @staticmethod
    def get_ti_1_1_64(varna_list):
        """
        [SUTRA]: अचोऽन्त्यादि टि (१.१.६४)
        [VRITTI]: अचामन्त्यादि यत् तट्टिसंज्ञं स्यात्।
        [LOGIC]: Starting from the last vowel (Ac) to the end is called 'Ti'.
        """
        if not varna_list:
            return [], -1

        # PAS-5 Optimization: Use the biological 'is_vowel' flag from Phonology
        last_vowel_idx = -1
        for i in range(len(varna_list) - 1, -1, -1):
            if varna_list[i].is_vowel:
                last_vowel_idx = i
                break

        if last_vowel_idx == -1:
            return [], -1  # No vowel found (e.g., purely consonantal fragment)

        # Returns the 'Ti' portion (slice) and its starting index
        return varna_list[last_vowel_idx:], last_vowel_idx

    @staticmethod
    def get_upadha_1_1_65(varna_list):
        """
        [SUTRA]: अलोऽन्त्यात् पूर्व उपधा (१.१.६५)
        [VRITTI]: अन्त्यादलो यः पूर्वो वर्णः स उपधासंज्ञः स्यात्।
        [LOGIC]: Returns (VarnaObj, Index) of the penultimate character.
        """
        if len(varna_list) < 2:
            # A single letter cannot have a 'preceding' element.
            return None, -1

        idx = len(varna_list) - 2
        return varna_list[idx], idx

    # =========================================================================
    # SECTION 1.1: Contextual Resolution (Saptami/Panchami)
    # =========================================================================

    @staticmethod
    def resolve_tasmin_1_1_66(trigger_index):
        """
        [SUTRA]: तस्मिन्निति निर्दिष्टे पूर्वस्य (१.१.६६)
        [LOGIC]: Locative Case (Saptami) -> Operation applies to Preceding Element.
        Input: Index of the cause (Nimitta).
        Output: Index of the target (Karya-bhagi).
        """
        return trigger_index - 1

    @staticmethod
    def resolve_tasmad_1_1_67(trigger_index):
        """
        [SUTRA]: तस्मादित्युत्तरस्य (१.१.६७)
        [LOGIC]: Ablative Case (Panchami) -> Operation applies to Following Element.
        Input: Index of the cause (Nimitta).
        Output: Index of the target (Karya-bhagi).
        """
        return trigger_index + 1