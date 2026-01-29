#logic/niyama_filters.py
# logic/niyama_filters.py

from core.adhikara_manager import AdhikaraManager


class NiyamaFilters:
    """
    नियम-फिल्टर: (Restrictive Logic Engine)
    Rule: 'Siddhe sati yatra niyamah' (When a rule is already applicable,
    a Niyama restricts its scope).
    """

    @staticmethod
    def apply_vibhakti_niyama_1_3_4(varna_obj, source_type):
        """
        Sutra: न विभक्तौ तुस्माः (१.३.४)
        Logic: In a 'Vibhakti' (Suffix), 't-varga', 's', and 'm' are NOT It.
        This is a restrictive filter on 1.3.3 (Halantyam).
        """
        if source_type != "Vibhakti":
            return True, "Not a Vibhakti context"

        char = varna_obj.char
        # T-Varga (त्, थ्, द्, ध्, न्), स्, म्
        restricted_chars = ['त्', 'थ्', 'द्', 'ध्', 'न्', 'स्', 'म्']

        if any(char.startswith(r) for r in restricted_chars):
            return False, "१.३.४ न विभक्तौ तुस्माः: विभक्ति में 'तु-स्-म्' की इत्-संज्ञा वर्जित है।"

        return True, "Valid"

    @staticmethod
    def apply_taddhita_niyama_1_3_7(varna_obj, is_taddhita):
        """
        Sutra: चुटू (१.३.७) - Restrictive aspect via 1.3.8 context.
        Note: Rules like 1.3.8 (Lashakvat) apply only to non-taddhita suffixes.
        """
        if is_taddhita and varna_obj.char in ['ल्', 'श्', 'क्', 'ख्', 'ग्', 'घ्', 'ङ्']:
            return False, "१.३.८ लशक्वतद्धिते: तद्धित प्रत्ययों में ल-श-कु की इत्-संज्ञा वर्जित है।"

        return True, "Valid"

    @staticmethod
    def apply_guna_vriddhi_niyama_1_1_5(varna_obj, nimitta_obj):
        """
        Sutra: क्ङ्िति च (१.१.५)
        Logic: Guna and Vriddhi are prohibited if the trigger (Nimitta) is 'Kit' or 'Njit'.
        """
        if not nimitta_obj:
            return True, "No trigger"

        # Check for technical markers (K or Nj) on the following suffix
        is_prohibited = any(tag in nimitta_obj.sanjnas for tag in ["kit", "ñit"])

        if is_prohibited:
            return False, "१.१.५ क्ङ्िति च: 'क्' या 'ङ्' इत् वाले प्रत्यय के परे होने पर गुण-वृद्धि निषेध।"

        return True, "Valid"
