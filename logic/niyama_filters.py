"""
FILE: logic/niyama_filters.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Niyama & Nishedha (The Restrictive Logic)
REFERENCE: १.१.५, १.३.४, १.३.८
"""

from core.upadesha_registry import UpadeshaType


class NiyamaFilters:
    """
    नियम-फिल्टर: (Restrictive Logic Engine)
    Implements 'Siddhe sati yatra niyamah' & 'Nishedha'.
    Acts as the 'Gatekeeper' for Vidhi rules.
    """

    @staticmethod
    def is_it_sanjna_blocked_1_3_4(varna_obj, source_type):
        """
        [SUTRA]: न विभक्तौ तुस्माः (१.३.४)
        [LOGIC]: Blocking Antibody for 1.3.3 (Halantyam).
        In a 'Vibhakti' (Suffix), 't-varga', 's', and 'm' cannot be 'It'.
        """
        # 1. Scope Check: Must be Vibhakti
        if source_type != UpadeshaType.VIBHAKTI:
            return False, "Not a Vibhakti context"

        # 2. Phonetic Check
        # Tu (Dental Class) + s + m
        # We check simply against the char since we are in the surgical phase
        char = varna_obj.char
        restricted_chars = ['त्', 'थ्', 'द्', 'ध्', 'न्', 'स्', 'म्']

        if char in restricted_chars:
            return True, "१.३.४ न विभक्तौ तुस्माः: विभक्ति में 'तु-स्-म्' की इत्-संज्ञा वर्जित है।"

        return False, "Valid"

    @staticmethod
    def is_it_sanjna_blocked_1_3_8(varna_obj, source_type, is_taddhita):
        """
        [SUTRA]: लशक्वतद्धिते (१.३.८)
        [LOGIC]: Blocking Antibody for 1.3.3/General It-rules.
        'L', 'Sh', and 'Ku' (K-varga) are It markers, BUT NOT in Taddhitas.
        This function checks if the It-Sanjna should be BLOCKED (i.e. is it a Taddhita?)
        """
        # The Sutra says: [In Non-Taddhita], L-Sh-Ku are It.
        # Therefore, Niyama/Nishedha applies if it IS a Taddhita.

        if not is_taddhita:
            return False, "Not a Taddhita, restriction doesn't apply."

        char = varna_obj.char
        # L, Sh, K-Varga
        targets = ['ल्', 'श्', 'क्', 'ख्', 'ग्', 'घ्', 'ङ्']

        if char in targets:
            return True, "१.३.८ (Context): तद्धित प्रत्ययों में 'ल-श-कु' की इत्-संज्ञा वर्जित है।"

        return False, "Valid"

    @staticmethod
    def is_guna_vriddhi_blocked_1_1_5(nimitta_obj):
        """
        [SUTRA]: क्ङ्िति च (१.१.५)
        [LOGIC]: Major Nishedha for 7.3.84/7.2.115 etc.
        Guna and Vriddhi are PROHIBITED if the following suffix (Nimitta) 
        is marked as 'Kit' (k) or 'Ngit' (ng).
        """
        if not nimitta_obj:
            return False, "No trigger to block operation."

        # Access the 'Ghost Tags' (Sanjnas) preserved by the ItEngine/Atidesha
        # The Nimitta (Suffix) might have lost the 'k' char, but must have the 'kit' tag.

        # We allow checking against a Varna object or a rich Suffix object
        current_tags = getattr(nimitta_obj, 'sanjnas', set())

        # Check for the prohibitive markers
        if "क" in current_tags or "kit" in current_tags or "कित्" in current_tags:
            return True, "१.१.५ क्ङ्िति च: 'कित्' प्रत्यय परे होने से गुण/वृद्धि निषेध।"

        if "ङ" in current_tags or "ngit" in current_tags or "ङित्" in current_tags:
            return True, "१.१.५ क्ङ्िति च: 'ङित्' प्रत्यय परे होने से गुण/वृद्धि निषेध।"

        return False, "Valid"