# logic/anga_engine.py

from core.upadesha_registry import Upadesha


class AngaEngine:
    """
    सञ्ज्ञा-सञ्चालक: १.४.१३ यस्मात्प्रत्ययविधिस्तदादि प्रत्ययेऽङ्गम्।
    The Surgeon's Scalpel: Identifies the Aṅga (Stem) based on Paninian Sutras.

    This engine uses the 3.1.1 Pratyaya Adhikāra tag for automation but
    retains manual overrides for surgical precision (e.g., excluding Upasargas).
    """

    @staticmethod
    def yasmat_pratyaya_vidhi_1_4_13(full_varnas, manual_range=None):
        """
        Sutra: यस्मात्प्रत्ययविधिस्तदादि प्रत्ययेऽङ्गम् (१.४.१३)

        Logic:
        1. If 'manual_range' is provided, it uses those indices (Preserved logic).
        2. Otherwise, it scans for the FIRST Varna tagged with 'is_pratyaya' (3.1.1).
        3. Everything before that index is the Aṅga.
        """
        # --- 1. Manual Surgical Override ---
        if manual_range:
            start_idx, end_idx = manual_range
            return full_varnas[start_idx:end_idx]

        # --- 2. Automated Adhikāra Detection ---
        # Scans for the mandate boundary defined by Sutra 3.1.1
        for index, varna in enumerate(full_varnas):
            if getattr(varna, 'is_pratyaya', False):
                return full_varnas[:index]

        # --- 3. Fallback ---
        return full_varnas

    @staticmethod
    def identify_boundary_indices(full_varnas):
        """
        Helper for the UI slider. Returns the (start, end) index of the
        automatically detected Aṅga.
        """
        for index, varna in enumerate(full_varnas):
            if getattr(varna, 'is_pratyaya', False):
                return (0, index)
        return (0, len(full_varnas))

    @staticmethod
    def get_anga_antya(anga_varnas):
        """
        Extracts the final varna object of the Aṅga (Aṅga-Antya).
        Crucial for rules like 6.1.68 (Hal-Nyāb-Lopa).
        """
        if anga_varnas:
            # Returns the full Upadesha object to preserve its sutra_origin
            return anga_varnas[-1]
        return None