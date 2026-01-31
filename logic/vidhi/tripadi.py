"""
FILE: logic/vidhi/tripadi.py
TIMESTAMP: 2026-01-31 03:00:00 (IST)
LOCATION: Lucknow, Uttar Pradesh, India
QUALITY: PAS-v2.0: 6.0 (Subanta) | PILLAR: Tripādī (Final Phonology)
DESCRIPTION: Implements the final three chapters of Ashtadhyayi (8.2-8.4).
             Includes Nalopa, Rutva, Visarga, Natva, and Chartva.
"""
from core.phonology import Varna

class Tripadi:
    """
    [VṚTTI]: त्रिपादी (८.२.१ - ८.४.६८)।
    The final three chapters of Aṣṭādhyāyī. These rules are 'Asiddha' (invisible)
    to the earlier Sapāda-saptādhyāyī (1.1.1 - 8.1.74) and to each other in serial order.
    """

    @staticmethod
    def apply_nalopa_8_2_7(varnas):
        """
        [8.2.7]: नलोपः प्रातिपदिकान्तस्य।
        Elision of final 'n' of a Pratipadika.
        Example: Rājan -> Rāja.
        """
        if varnas and varnas[-1].char == 'न्':
            # Remove the final 'n'
            return varnas[:-1], "8.2.7"
        return varnas, None

    @staticmethod
    def apply_rutva_8_2_66(varnas):
        """
        [8.2.66]: ससजुषो रुः।
        Padānta 's' (and 'ṣ' of sajus) becomes 'ru~'.
        Example: Rāmas -> Rāmaru~.
        """
        if not varnas: return varnas, None

        last = varnas[-1]
        # Check for final S or Sh
        if last.char in ['स्', 'ष्']:
            # Remove the 's'
            stem = varnas[:-1]
            # Add 'r', 'u', '~' (Ru~)
            stem.extend([Varna("र्"), Varna("उ"), Varna("ँ")])
            return stem, "8.2.66"

        return varnas, None

    @staticmethod
    def apply_visarga_8_3_15(varnas):
        """
        [8.3.15]: खरवसानयोर्विसर्जनीयः।
        'r' becomes 'ḥ' (Visarga) when at the end of a Pada (Avasana).
        Example: Rāmaru -> Rāmaḥ.
        """
        if not varnas: return varnas, None

        last = varnas[-1]
        # Check if last char is 'r' (Repha)
        if last.char == 'र्':
            # Remove 'r'
            stem = varnas[:-1]
            # Add Visarga 'h'
            stem.append(Varna("ः"))
            return stem, "8.3.15"

        return varnas, None

    @staticmethod
    def apply_natva_8_4_1(varnas):
        """
        [8.4.1]: रषाभ्यां नो णः समानपदे।
        Dental 'n' becomes Retroflex 'ṇ' if preceded by 'r' or 'ṣ' in the same word.
        Example: Tṛṣ + naj -> Tṛṣṇaj.
        """
        # Simplistic implementation: Check for trigger before target
        applied = False
        trigger_found = False

        # Scan for triggers (R, Sh, Rr)
        for v in varnas:
            if v.char in ['र्', 'ष्', 'ऋ', 'ॠ']:
                trigger_found = True
            elif v.char == 'न्' and trigger_found:
                v.char = 'ण्'
                applied = True

        # Note: In a real implementation, we need to check for blocking letters (8.4.2)
        return varnas, "8.4.1" if applied else None

    @staticmethod
    def apply_chartva_8_4_56(varnas):
        """
        [8.4.56]: वाऽवसाने।
        Final Jhala letters optionally become Char (unvoiced) in pause.
        Example: Tad -> Tat.
        """
        if not varnas: return varnas, None

        last = varnas[-1]
        # Mapping: Voiced -> Unvoiced (Jhal -> Char)
        # Simplified map for common cases
        char_map = {
            'द्': 'त्',
            'ड्': 'ट्',
            'ग्': 'क्',
            'ब्': 'प्',
            'ज्': 'च्'
        }

        if last.char in char_map:
            # Modify the existing Varna object in place
            last.char = char_map[last.char]
            return varnas, "8.4.56"

        return varnas, None