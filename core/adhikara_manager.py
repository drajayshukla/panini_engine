# core/adhikara_manager.py

class AdhikaraManager:
    """
    सञ्चालक: पाणिनीय-अधिकार-सूत्राणाम्।
    Strictly governs the scope of inheritance rules and spatial positioning.
    """

    # --- PRATYAYA ADHIKARA (3.1.1 - 5.4.160) ---
    PRATYAYA_START = (3, 1, 1)
    PARA_START     = (3, 1, 2)  # ३.१.२ परश्च
    PRATYAYA_END   = (5, 4, 160)

    # --- ANGASYA ADHIKARA (6.4.1 - 7.4.120) ---
    ANGASYA_START  = (6, 4, 1)
    ANGASYA_END    = (7, 4, 120)

    @staticmethod
    def parse_sutra(sutra_str):
        """
        Surgical Parsing: Converts '3.1.2' into (3, 1, 2).
        Pads malformed input to 3 levels for robust tuple comparison.
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
        """Sutra: ३.१.१ प्रत्ययः।"""
        target = cls.parse_sutra(sutra_number)
        return cls.PRATYAYA_START <= target <= cls.PRATYAYA_END

    @classmethod
    def is_para_adhikara(cls, sutra_number: str) -> bool:
        """Sutra: ३.१.२ परश्च।"""
        target = cls.parse_sutra(sutra_number)
        return cls.PARA_START <= target <= cls.PRATYAYA_END

    @classmethod
    def is_in_angasya_adhikara(cls, sutra_number: str) -> bool:
        """Sutra: ६.४.१ अङ्गस्य।"""
        target = cls.parse_sutra(sutra_number)
        return cls.ANGASYA_START <= target <= cls.ANGASYA_END