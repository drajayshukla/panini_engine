# core/paribhasha_manager.py
from core.pratyahara_engine import PratyaharaEngine

# Initialize the Zone 1 engine to power Zone 2 logic
pe = PratyaharaEngine()

class ParibhashaManager:
    """
    परिभाषा-सञ्चालक: (The Interpretive Engine)
    Zone 2: Global guidelines for rule application, targeting, and interpretation.
    """

    @staticmethod
    def get_upadha_index_1_1_65(varna_list):
        """
        Sutra: अलोऽन्त्यात् पूर्व उपधा (१.१.६५)
        Logic: The 'Al' (phoneme) immediately preceding the final one is Upadha.
        Returns the index of the penultimate element.
        """
        if len(varna_list) < 2:
            return 0 if len(varna_list) == 1 else None
        return -2

    @staticmethod
    def get_ti_indices_1_1_64(varna_list):
        """
        Sutra: अचोऽन्त्यादि टि (१.१.६४)
        Logic: Starting from the last vowel (Ac) to the end is called 'Ti'.
        Uses the PratyaharaEngine to dynamically identify vowels.
        """
        if not varna_list:
            return []

        # Find the index of the last vowel using the 'ac' (अच्) range
        last_vowel_idx = -1
        for i in range(len(varna_list) - 1, -1, -1):
            if pe.is_in(varna_list[i].char, "अच्"):
                last_vowel_idx = i
                break

        if last_vowel_idx == -1:
            return []  # No 'Ti' if no vowel exists

        return list(range(last_vowel_idx, len(varna_list)))

    @staticmethod
    def apply_tasmin_1_1_66(target_index):
        """
        Sutra: तस्मिन्निति निर्दिष्टे पूर्वस्य (१.१.६६)
        Logic: If a condition is in Locative (Saptami), the operation
        happens to the element IMMEDIATELY PRECEDING the trigger.
        """
        return target_index - 1

    @staticmethod
    def apply_tasmad_1_1_67(target_index):
        """
        Sutra: तस्मादित्युत्तरस्य (१.१.६७)
        Logic: If a condition is in Ablative (Panchami), the operation
        happens to the element IMMEDIATELY FOLLOWING the trigger.
        """
        return target_index + 1