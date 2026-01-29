# core/sanjna_engine.py

from core.pratyahara_engine import PratyaharaEngine

# Initialize the Zone 1 Decoder to power our definitions
pe = PratyaharaEngine()

class SanjnaEngine:
    """
    अथ संज्ञा-प्रकरणम्: The Definition Engine.
    Zone 1: Assigns technical identities (DNA) using Pratyahara ranges.
    """

    @staticmethod
    def is_vriddhi_1_1_1(char: str) -> bool:
        """
        Sutra: वृद्धिरादैच् (१.१.१)
        Logic: 'ā' and the range 'aic' (ऐ, औ).
        """
        # ā (आ) + aic (ऐ, औ)
        return char == 'आ' or pe.is_in(char, "ऐच्")

    @staticmethod
    def is_guna_1_1_2(char: str) -> bool:
        """
        Sutra: अदेङ्गुणः (१.१.२)
        Logic: 'a' (short) and the range 'eṅ' (ए, ओ).
        """
        # a (अ) + eṅ (ए, ओ)
        return char == 'अ' or pe.is_in(char, "एङ्")

    @staticmethod
    def is_hal(char: str) -> bool:
        """
        Logic: True Consonant check using the Shiva Sutra range 'हल्'.
        """
        return pe.is_in(char, "हल्")

    @staticmethod
    def is_ac(char: str) -> bool:
        """
        Logic: True Vowel check using the Shiva Sutra range 'अच्'.
        """
        return pe.is_in(char, "अच्")

    @staticmethod
    def is_samyoga_1_1_7(varna_list: list) -> bool:
        """
        Sutra: हलोऽनन्तराः संयोगः (१.१.७)
        Logic: Conjunction of consonants (Hal) without intervening vowels (Ac).
        """
        if len(varna_list) < 2:
            return False
        # Uses the dynamic is_hal check
        return all(SanjnaEngine.is_hal(v.char if hasattr(v, 'char') else v) for v in varna_list)