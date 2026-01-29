"""
FILE: logic/conflict_resolver.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Paribhāṣā (Conflict Resolution)
HIERARCHY: Asiddha > Apavāda > Nitya > Antaraṅga > Para
"""

from core.adhikara_manager import AdhikaraManager

class ConflictResolver:
    """
    विप्रतिषेध-सञ्चालक: (The Conflict Resolution Engine)
    Decides the winner when two rules vie for the same target.
    """

    @staticmethod
    def resolve(sutra_a, sutra_b):
        """
        [JUDGMENT]: Main entry point to decide which rule wins.
        Input: Two Sutra dictionary objects (must contain 'sutra_num' and optionally 'type').
        """

        # 0. Prep: Parse Geolocation
        num_a = sutra_a.get('sutra_num', '0.0.0')
        num_b = sutra_b.get('sutra_num', '0.0.0')

        addr_a = AdhikaraManager.parse_sutra(num_a)
        addr_b = AdhikaraManager.parse_sutra(num_b)

        # ---------------------------------------------------------
        # 1. TRIPĀDĪ CHECK (८.२.१ पूर्वत्रासिद्धम्) - The Dimensional Barrier
        # ---------------------------------------------------------
        # Logic: If one is Sapta-adhyāyī and other is Tripādī, the Tripādī rule is 'Asiddha'.
        # Therefore, the Sapta-adhyāyī rule ALWAYS wins (or executes first).

        is_a_tripadi = AdhikaraManager.is_tripadi(num_a)
        is_b_tripadi = AdhikaraManager.is_tripadi(num_b)

        if not is_a_tripadi and is_b_tripadi:
            return sutra_a, "८.२.१ पूर्वत्रासिद्धम् (Tripādī is invisible to Sapta-adhyāyī)."

        if is_a_tripadi and not is_b_tripadi:
            return sutra_b, "८.२.१ पूर्वत्रासिद्धम् (Tripādī is invisible to Sapta-adhyāyī)."

        # Note: If BOTH are Tripādī, the 'Purva' (Earlier) is stronger because
        # the later is Asiddha to the former.
        if is_a_tripadi and is_b_tripadi:
            if addr_a < addr_b:
                return sutra_a, "८.२.१ (Tripādī Internal): पूर्व (Earlier) rule wins."
            else:
                return sutra_b, "८.२.१ (Tripādī Internal): पूर्व (Earlier) rule wins."

        # ---------------------------------------------------------
        # 2. APAVĀDA CHECK (Exception vs General)
        # ---------------------------------------------------------
        # Usually flagged in the rule logic itself via metadata.
        type_a = sutra_a.get('type', 'utsarga')
        type_b = sutra_b.get('type', 'utsarga')

        if type_a == 'apavada' and type_b != 'apavada':
            return sutra_a, "अपवादो नित्य-बाधकः (Exception blocks General)."
        if type_b == 'apavada' and type_a != 'apavada':
            return sutra_b, "अपवादो नित्य-बाधकः (Exception blocks General)."

        # ---------------------------------------------------------
        # 3. PARA CHECK (१.४.२ विप्रतिषेधे परं कार्यम्)
        # ---------------------------------------------------------
        # Logic: If both are equal strength (Sapta-adhyāyī), later wins.
        if addr_b > addr_a:
            return sutra_b, "१.४.२ विप्रतिषेधे परं कार्यम्: पर (Later) rule wins."
        elif addr_a > addr_b:
            return sutra_a, "१.४.२ विप्रतिषेधे परं कार्यम्: पर (Later) rule wins."

        # Default (Same rule or unknown)
        return sutra_a, "Equal strength/Identity."