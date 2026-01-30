"""
FILE: logic/vidhi/tripadi.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Tripādī (Final Phonology)
REFERENCE: ८.२.७, ८.२.६६, ८.३.१५, ८.४.५६
"""
from .engine_base import VidhiEngineBase

class Tripadi(VidhiEngineBase):
    """
    Final Phonological transformations.
    These rules are 'Asiddha' (invisible) to the previous 7 books.
    Once we enter Tripadi, rules apply sequentially.
    """

    @staticmethod
    def apply_nalopa_8_2_7(varna_list):
        """[SUTRA]: नलोपः प्रातिपदिकान्तस्य (८.२.७)"""
        if varna_list and varna_list[-1].char == 'न्':
            old = varna_list[-1].char
            varna_list.pop()
            return varna_list, f"८.२.७ ({old}-लोपः)"
        return varna_list, None

    @staticmethod
    def apply_rutva_8_2_66(varna_list):
        """[SUTRA]: ससजुषो रुः (८.२.६६)"""
        if not varna_list: return varna_list, None
        last = varna_list[-1]
        if last.char == 'स्':
            old = last.char
            last.char = 'र्'
            last.trace.append("८.२.६६")
            return varna_list, f"८.२.६६ ({old} -> र्)"
        return varna_list, None

    @staticmethod
    def apply_visarga_8_3_15(varna_list):
        """[SUTRA]: खरवसानयोर्विसर्जनीयः (८.३.१५)"""
        if not varna_list: return varna_list, None
        last = varna_list[-1]
        if last.char == 'र्':
            old = last.char
            last.char = 'ः'
            last.trace.append("८.३.१५")
            return varna_list, f"८.३.१५ ({old} -> ः)"
        return varna_list, None

    @staticmethod
    def apply_chartva_8_4_56(varna_list):
        """
        [SUTRA]: वाऽवसाने (८.४.५६)
        [LOGIC]: Optionally (Vā), in Pause (Avasāna),
        Jhal becomes Car (De-voicing).
        Example: d -> t.
        """
        if not varna_list: return varna_list, None
        last = varna_list[-1]

        # Mapping for common terminal de-voicing (Jhal -> Car)
        mapping = {
            'ग्': 'क्',
            'ज्': 'क्',
            'ड्': 'ट्',
            'द्': 'त्',
            'ब्': 'प्'
        }

        if last.char in mapping:
            old = last.char
            last.char = mapping[old]
            last.trace.append("८.४.५६")
            return varna_list, f"८.४.५६ ({old} -> {last.char})"
        return varna_list, None