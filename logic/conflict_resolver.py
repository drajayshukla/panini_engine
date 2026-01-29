# panini_engine/logic/conflict_resolver.py

from core.adhikara_manager import AdhikaraManager


class ConflictResolver:
    """
    विप्रतिषेध-सञ्चालक: (The Conflict Resolution Engine)
    Governs the priority of rules: Apavāda > Nitya > Antaraṅga > Para.
    """

    @staticmethod
    def resolve(sutra_a, sutra_b):
        """
        Main entry point to decide which rule wins in a collision.
        """
        # 1. Check for Apavāda (Exceptions) - Highest Priority
        # (Assuming sutra objects have a 'type' field from JSON)
        if sutra_a.get('type') == 'apavada' and sutra_b.get('type') == 'utsarga':
            return sutra_a, "अपवाद (Exception) उत्सर्ग को रोकता है।"
        if sutra_b.get('type') == 'apavada' and sutra_a.get('type') == 'utsarga':
            return sutra_b, "अपवाद (Exception) उत्सर्ग को रोकता है।"

        # 2. Fallback to Vipratiṣedha (1.4.2)
        return ConflictResolver.resolve_vipratishedha_1_4_2(sutra_a, sutra_b)

    @staticmethod
    def resolve_vipratishedha_1_4_2(sutra_a, sutra_b):
        """
        Sutra: विप्रतिषेधे परं कार्यम् (१.४.२)
        Logic: In a conflict of equal strength, the later rule prevails.
        """
        # Normalize sutra numbers using our foundation GPS
        num_a = sutra_a.get('sutra_num', '0.0.0')
        num_b = sutra_b.get('sutra_num', '0.0.0')

        addr_a = AdhikaraManager.parse_sutra(num_a)
        addr_b = AdhikaraManager.parse_sutra(num_b)

        if addr_b > addr_a:
            return sutra_b, "१.४.२ विप्रतिषेधे परं कार्यम्: पर-शास्त्र बलवान है।"
        elif addr_a > addr_b:
            return sutra_a, "१.४.२ विप्रतिषेधे परं कार्यम्: पर-शास्त्र बलवान है।"

        return sutra_a, "तुल्य-बल (Equal strength) - Defaulting to first."