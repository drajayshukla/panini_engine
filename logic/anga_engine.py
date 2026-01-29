# logic/anga_engine.py

from core.phonology import Varna


class AngaEngine:
    """
    Handles the identification of the Aṅga (Stem) based on Paninian Sutras.
    """

    @staticmethod
    def yasmat_pratyaya_vidhi_1_4_13(full_varnas, pratyaya_len, manual_range=None):
        """
        Sutra: यस्मात्प्रत्ययविधिस्तदादि प्रत्ययेऽङ्गम् (१.४.१३)

        Translation: That [sequence of letters] which begins with the element
        (root/stem) to which a suffix is mandated is called 'Aṅga' with
        respect to that suffix.

        Logic:
        1. Identifies the portion of the word that acts as the 'Aṅga'.
        2. If 'manual_range' is provided (start, end), it allows surgical
           exclusion of Upasargas (prefixes) like 'sam' in 'sam-a-pathat'.
        """
        if manual_range:
            start_idx, end_idx = manual_range
            # Precision surgical slice based on Paninian mandate
            return full_varnas[start_idx:end_idx]

        # Default: The entire sequence before the suffix is the Aṅga
        # This is used for standard Prātipadikas like 'Rāma' or 'Ramā'
        if len(full_varnas) > pratyaya_len:
            return full_varnas[:-pratyaya_len]

        return full_varnas

    @staticmethod
    def get_anga_antya(anga_varnas):
        """
        Extracts the final varna of the Aṅga (Aṅga-Antya).
        Crucial for rules like 6.1.68 (Hal-Nyāb-Lopa).
        """
        if anga_varnas:
            return anga_varnas[-1].char
        return None