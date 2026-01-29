# panini_engine/logic/anuvritti_handler.py

from core.adhikara_manager import AdhikaraManager


class AnuvrittiHandler:
    """
    पाणिनीय अनुवृत्ति इंजन (The Hereditary Logic).
    उद्देश्य: पिछले सूत्रों से पदों (Keywords) को वर्तमान सूत्र में लाना।
    Zone 1: Core Sanjna & It-Prakarana Support.
    """

    @staticmethod
    def get_inherited_terms(current_sutra_num):
        """
        वर्तमान सूत्र संख्या के आधार पर अनुवृत्त पदों की पहचान करना।
        Uses Range-based logic to mirror the Shastric flow.
        """
        # Surgical Parse: '1.3.3' -> (1, 3, 3)
        target = AdhikaraManager.parse_sutra(current_sutra_num)
        terms = []

        # --- १. उपदेशे / इत् (It-Sanjna Flow: 1.3.2 - 1.3.10) ---
        # Note: 1.3.2 provides the base keywords for the entire marker section.
        if (1, 3, 2) <= target <= (1, 3, 10):
            # 1.3.9 is 'Tasya Lopah', it only needs 'It' (from 1.3.2)
            if target == (1, 3, 9):
                terms.append("इतः")
            else:
                terms.extend(["उपदेशे", "इत्"])

        # --- २. प्रत्ययस्य (Pratyaya Constraint: 1.3.6 - 1.3.8) ---
        # Specific markers found only in suffixes.
        if (1, 3, 6) <= target <= (1, 3, 8):
            terms.append("प्रत्ययस्य")

        # --- ३. अङ्गस्य (Aṅga Adhikāra: 6.4.1 - 7.4.120) ---
        # Critical for Zone 3 Vidhi operations.
        if (6, 4, 1) <= target <= (7, 4, 120):
            terms.append("अङ्गस्य")

        return terms

    @staticmethod
    def apply_anuvritti_context(sutra_obj):
        """
        सम्बद्ध पद: Contextualizes a Sutra object with its inherited terms.
        Used for UI display and Clinical Logic validation.
        """
        # Safety check for input format
        sutra_num = sutra_obj.get('sutra_num', sutra_obj.get('number', '0.0.0'))

        terms = AnuvrittiHandler.get_inherited_terms(sutra_num)

        if terms:
            sutra_obj['context_terms'] = terms
            # Builds the full "Clinical Meaning" (e.g., "उपदेशे इत् हलन्त्यम्")
            sutra_obj['full_meaning'] = f"{' '.join(terms)} {sutra_obj.get('name', '')}"
        else:
            sutra_obj['context_terms'] = []
            sutra_obj['full_meaning'] = sutra_obj.get('name', '')

        return sutra_obj