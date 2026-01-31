"""
FILE: core/adhikara_manager.py
TIMESTAMP: 2026-01-30 20:50:00 (IST)
LOCATION: Lucknow, Uttar Pradesh, India
QUALITY: PAS-v2.0: 6.0 (Subanta) | PILLAR: Adhikāra (Spatial Jurisdiction)
REFERENCE: Brahmadutt Jigyasu, Prathamavritti Vol 1 & Ashtadhyayi.com
"""

class AdhikaraManager:
    """
    सञ्चालक: पाणिनीय-अधिकार-सूत्राणाम्।
    Governs the 'Adhikāra' (Jurisdiction) and 'Asiddhatva' (Invisibility) logic.
    """

    # --- PRATYAYA ADHIKARA (3.1.1 - 5.4.160) ---
    PRATYAYA_START = (3, 1, 1) # ३.१.१ प्रत्ययः
    PARA_START     = (3, 1, 2) # ३.१.२ परश्च
    PRATYAYA_END   = (5, 4, 160)

    # --- ANGASYA ADHIKARA (6.4.1 - 7.4.120) ---
    ANGASYA_START  = (6, 4, 1) # ६.४.१ अङ्गस्य
    ANGASYA_END    = (7, 4, 120)

    # --- TRIPĀDĪ BOUNDARY (8.2.1) ---
    # The 'Invisible' zone of the Ashtadhyayi
    TRIPADI_START  = (8, 2, 1) # ८.२.१ पूर्वत्रासिद्धम्

    @staticmethod
    def parse_sutra(sutra_str):
        """
        [PAS-5.0] Surgical Parsing: Converts '3.1.2' into (3, 1, 2).
        Essential for mathematical 'Para' vs 'Purva' logic.
        """
        try:
            parts = [int(x) for x in str(sutra_str).split('.')]
            while len(parts) < 3:
                parts.append(0)
            return tuple(parts[:3])
        except (ValueError, AttributeError):
            return (0, 0, 0)

    @classmethod
    def is_in_pratyaya_adhikara(cls, sutra_number: str) -> bool:
        """Sutra: ३.१.१ प्रत्ययः। (Rules governing suffixes)"""
        target = cls.parse_sutra(sutra_number)
        return cls.PRATYAYA_START <= target <= cls.PRATYAYA_END

    @classmethod
    def is_in_angasya_adhikara(cls, sutra_number: str) -> bool:
        """Sutra: ६.४.१ अङ्गस्य। (Rules governing stem modifications)"""
        target = cls.parse_sutra(sutra_number)
        return cls.ANGASYA_START <= target <= cls.ANGASYA_END

    @classmethod
    def is_tripadi(cls, sutra_number: str) -> bool:
        """
        Sutra: ८.२.१ पूर्वत्रासिद्धम्।
        Logic: Rules in the Tripādī are 'Asiddha' (invisible) to the Sapāda-saptādhyāyī.
        """
        target = cls.parse_sutra(sutra_number)
        return target >= cls.TRIPADI_START