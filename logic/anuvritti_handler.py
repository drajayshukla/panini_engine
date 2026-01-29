"""
FILE: logic/anuvritti_handler.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Anuvṛtti (Hereditary Context)
REFERENCE: Ashtadhyayi.com & Jigyasu Prathamavritti
"""

from core.adhikara_manager import AdhikaraManager


class AnuvrittiHandler:
    """
    पाणिनीय अनुवृत्ति इंजन (The Hereditary Logic).
    Mechanizes the flow of keywords from previous Sutras to the current one.
    """

    @staticmethod
    def get_inherited_terms(current_sutra_num):
        """
        [LOGIC]: Determines which keywords apply to the current sūtra based on its location.
        Uses the 'AdhikaraManager' as the single source of truth for boundaries.
        """
        target = AdhikaraManager.parse_sutra(current_sutra_num)
        terms = []

        # --- 1. THE IT-PRAKARANA FLOW (1.3.2 - 1.3.9) ---
        # Context: "Upadeshe" (from 1.3.2) and "It" (from 1.3.2)
        # Note: 1.3.9 (Tasya Lopah) needs 'It' to know what to delete.
        start_it = (1, 3, 2)
        end_it = (1, 3, 9)

        if start_it <= target <= end_it:
            if target == (1, 3, 2):
                # The source itself doesn't inherit, it declares.
                pass
            else:
                terms.append("उपदेशे")
                terms.append("इत्")

        # --- 2. PRATYAYA CONSTRAINT (1.3.6 - 1.3.8) ---
        # Context: "Pratyayasya" (Of the suffix) - specifically for Adi-It rules.
        if (1, 3, 6) <= target <= (1, 3, 8):
            terms.append("प्रत्ययस्य (आदिः)")

        # --- 3. PRATYAYA ADHIKARA (3.1.1 - 5.4.160) ---
        # Context: "Pratyayah", "Parashcha"
        # Using AdhikaraManager constants to maintain S.S.O.T.
        if AdhikaraManager.is_in_pratyaya_adhikara(current_sutra_num):
            terms.extend(["प्रत्ययः", "परश्च"])

        # --- 4. ANGASYA ADHIKARA (6.4.1 - 7.4.120) ---
        # Context: "Angasya" (Of the Stem)
        if AdhikaraManager.is_in_angasya_adhikara(current_sutra_num):
            terms.append("अङ्गस्य")

        # --- 5. BHASYA ADHIKARA (1.4.18 - 6.4.175 approx) ---
        # (Simplified for PAS-5: Only checking standard range if needed later)
        # if (1,4,18) <= target <= (6,4,175): terms.append("भस्य")

        return terms

    @staticmethod
    def apply_anuvritti_context(sutra_obj):
        """
        [UI HELPER]: Injects context into a Sutra object for display.
        Example: Transforms "Halantyam" -> "Upadeshe It Halantyam"
        """
        # 1. Safe Extraction of Sutra Number
        sutra_num = sutra_obj.get('sutra_num', sutra_obj.get('number', '0.0.0'))

        # 2. Retrieve Hereditary Terms
        terms = AnuvrittiHandler.get_inherited_terms(sutra_num)

        # 3. Construct Clinical Meaning
        # We prepend the inherited terms to the native name/meaning
        native_name = sutra_obj.get('name', '')

        if terms:
            sutra_obj['context_terms'] = terms
            # E.g. [उपदेशे, इत्] + [हलन्त्यम्]
            sutra_obj['full_meaning'] = f"[{' '.join(terms)}] {native_name}"
        else:
            sutra_obj['context_terms'] = []
            sutra_obj['full_meaning'] = native_name

        return sutra_obj