"""
FILE: logic/anga_engine.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Aṅga-Adhikāra (Stem Control)
REFERENCE: १.४.१३ यस्मात्प्रत्ययविधिस्तदादि प्रत्ययेऽङ्गम्
"""

from core.upadesha_registry import UpadeshaType

class AngaEngine:
    """
    अङ्ग-सञ्चालक: The Stem Controller.
    Defines the scope of 'Anga' for Chapter 6.4 and 7.
    """

    @staticmethod
    def identify_boundary_indices(varna_list):
        """
        Auto-detects the Anga boundary based on standard morphology.
        Returns: (start_index, end_index)
        """
        if not varna_list:
            return (0, 0)

        # 1. Scan for explicit Pratyaya markers (if available from Upadesha Registry)
        for index, v in enumerate(varna_list):
            is_legal = getattr(v, 'is_pratyaya', False)
            is_type = hasattr(v, 'source_type') and v.source_type in [UpadeshaType.PRATYAYA, UpadeshaType.VIBHAKTI]

            if is_legal or is_type:
                return (0, index)

        # 2. Fallback Heuristic for Demos (Assume suffix is the last element)
        # This handles cases like 'Rama' + 's' where 's' is the suffix.
        if len(varna_list) > 1:
            return (0, len(varna_list) - 1)

        return (0, len(varna_list))

    @staticmethod
    def yasmat_pratyaya_vidhi_1_4_13(varna_list, manual_split_index=None):
        """
        [SUTRA]: यस्मात् प्रत्ययविधिस्तदादि प्रत्ययेऽङ्गम् (१.४.१३)
        [LOGIC]: Isolates the Anga segment based on split index or range.
        """

        # 1. Manual Surgical Override (Robust handling for Int and Tuple)
        if manual_split_index is not None:
            # Case A: Tuple/List (Range) -> (start, end)
            if isinstance(manual_split_index, (tuple, list)) and len(manual_split_index) == 2:
                start, end = manual_split_index
                return varna_list[start:end]

            # Case B: Integer (Split Point) -> [:split_point]
            elif isinstance(manual_split_index, int):
                return varna_list[:manual_split_index]

        # 2. Automated Detection (Fallback)
        # Uses the identify logic to find where the stem likely ends.
        start, end = AngaEngine.identify_boundary_indices(varna_list)
        return varna_list[start:end]

    @staticmethod
    def get_anga_antya(anga_varnas):
        """
        [HELPER]: Extracts the final varna object of the Aṅga (Aṅga-Antya).
        Crucial for rules like 6.1.68 (Hal-Nyāb-Lopa).
        """
        if anga_varnas:
            return anga_varnas[-1]
        return None