"""
FILE: logic/anga_engine.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Aṅga-Saṃjñā (Stem Identification)
REFERENCE: १.४.१३ यस्मात् प्रत्ययविधिस्तदादि प्रत्ययेऽङ्गम्
"""

from core.upadesha_registry import UpadeshaType


class AngaEngine:
    """
    अङ्ग-सञ्चालक: The Morphology Engine.
    The Surgeon's Scalpel: Identifies the Aṅga (Stem) based on Paninian Sutras.
    """

    @staticmethod
    def yasmat_pratyaya_vidhi_1_4_13(varna_list, manual_split_index=None):
        """
        [SUTRA]: यस्मात् प्रत्ययविधिस्तदादि प्रत्ययेऽङ्गम् (१.४.१३)
        [VRITTI]: यस्मात् शब्दात् यः प्रत्ययो विधीयते, तदादि शब्दस्वरूपं तस्मिन् प्रत्यये परे अङ्गसंज्ञं स्यात्।
        [LOGIC]:
          1. If 'manual_split_index' is provided, use it (Surgical Override).
          2. Otherwise, scan for the START of the Pratyaya (Suffix).
          3. Everything before that index is the Aṅga.
        """

        # 1. Manual Surgical Override
        if manual_split_index is not None:
            return varna_list[:manual_split_index]

        # 2. Automated Adhikāra Detection
        # Scan forward to find where the "Non-Pratyaya" ends and "Pratyaya" begins.
        split_index = -1

        for i, v in enumerate(varna_list):
            # Check 1: The official 3.1.1 Adhikara flag (Zone 4)
            is_legal_pratyaya = getattr(v, 'is_pratyaya', False)

            # Check 2: The Source Type injection (Controller) - Fallback
            is_type_pratyaya = False
            if hasattr(v, 'source_type'):
                is_type_pratyaya = v.source_type in [UpadeshaType.PRATYAYA, UpadeshaType.VIBHAKTI]

            # If this varna marks the start of a suffix...
            if is_legal_pratyaya or is_type_pratyaya:
                split_index = i
                break

        # 3. Surgical Extraction
        if split_index != -1:
            return varna_list[:split_index]

        # Fallback: If no suffix found, return whole list (or handle as error in strict mode)
        return varna_list

    @staticmethod
    def identify_boundary_indices(full_varnas):
        """
        [UI HELPER]: Returns (start, end) index of the automatically detected Aṅga.
        Used by the Streamlit 'Range Slider' to show the user what the engine sees.
        """
        for index, v in enumerate(full_varnas):
            # Check logic mirrors yasmat_pratyaya_vidhi
            is_legal = getattr(v, 'is_pratyaya', False)
            is_type = hasattr(v, 'source_type') and v.source_type in [UpadeshaType.PRATYAYA, UpadeshaType.VIBHAKTI]

            if is_legal or is_type:
                return (0, index)

        return (0, len(full_varnas))

    @staticmethod
    def get_anga_antya(anga_varnas):
        """
        [HELPER]: Extracts the final varna object of the Aṅga (Aṅga-Antya).
        Crucial for rules like 6.1.68 (Hal-Nyāb-Lopa).
        """
        if anga_varnas:
            # Returns the full Upadesha object to preserve its sutra_origin
            return anga_varnas[-1]
        return None