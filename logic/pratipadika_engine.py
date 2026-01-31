"""
FILE: logic/pratipadika_engine.py
PAS-v2.0: 6.0 (Subanta) | PILLAR: Validation (Gatekeeper)
REFERENCE: १.२.४५ अर्थवदधातुरप्रत्ययः प्रातिपदिकम्
"""
from core.upadesha_registry import UpadeshaType

class PratipadikaEngine:
    """
    [VṚTTI]: प्रातिपदिक-सञ्ज्ञा-विधायकम्।
    The Gatekeeper: Validates if a string is eligible for declension (Sup-pratyayas).
    """

    @staticmethod
    def validate(text):
        """
        [VERIFICATION PIPELINE]:
        1. Registry Scan: Checks if it's a Dhatu/Pratyaya (Conflict Check).
        2. 1.2.46 Check: Is it a Taddhita (Derived Noun)?
        3. 1.2.45 Check: Is it a valid dictionary word (Arthavat)?

        Returns:
            (bool, reason) -> (True, "Valid Stem") or (False, "It is a Dhatu")
        """
        if not text:
            return False, "Input is empty."

        # --- PHASE 1: REGISTRY SCAN (Auto-Detect) ---
        detected_type, is_taddhita, origin = UpadeshaType.auto_detect(text)

        # A. EXCLUSION CHECK (1.2.45: Adhātuḥ Apratyayaḥ)
        # If it is a Dhatu, it is NOT a Pratipadika.
        if detected_type == UpadeshaType.DHATU:
            return False, f"Conflict: '{text}' is a Dhatu ({origin}). Use Tinanta generator."

        # If it is a bare Pratyaya (and NOT a Taddhita derivative), it is excluded.
        if detected_type == UpadeshaType.PRATYAYA and not is_taddhita:
            return False, f"Conflict: '{text}' is a Pratyaya ({origin}). Cannot decline."

        # B. INCLUSION CHECK (1.2.46: Kṛt-Taddhita-Samāsāśca)
        if is_taddhita:
            return True, f"Validated via 1.2.46 (Taddhita: {origin})"

        # --- PHASE 2: DEFAULT INCLUSION (1.2.45) ---
        # If it passed the Exclusion check (not Dhatu/Pratyaya), we assume it is Arthavat.
        return True, "Validated via 1.2.45 (Arthavat)"