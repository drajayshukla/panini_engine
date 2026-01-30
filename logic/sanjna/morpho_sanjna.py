"""
FILE: logic/sanjna/morpho_sanjna.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Morphological Saṃjñās (Stem & Word Definitions)
REFERENCE: १.४.३ - १.४.१८
"""
from core.upadesha_registry import UpadeshaType
from core.pratyahara_engine import PratyaharaEngine

pe = PratyaharaEngine()

class MorphoSanjnas:
    """
    Handles technical designations for the Aṅga (stem) and Pada (word).
    These definitions act as 'Gatekeepers' for specific Vidhi rules.
    """

    @staticmethod
    def is_nadi_1_4_3(varna_list):
        """[SUTRA]: यू स्त्र्याख्यौ नदी (१.४.३)"""
        if not varna_list: return False
        # Ends in long ī or ū and is feminine (gender check to be added in future)
        return varna_list[-1].char in ['ई', 'ऊ']

    @staticmethod
    def is_ghi_1_4_7(varna_list):
        """[SUTRA]: शेषो घ्यसखि (१.४.७)"""
        if not varna_list: return False
        # Short i and u (excluding Nadi and 'Sakhi')
        return varna_list[-1].char in ['इ', 'उ']

    @staticmethod
    def is_hrasva_1_2_27(varna):
        """[SUTRA]: ऊकालोऽज्झ्रस्वदीर्घप्लुतः (१.२.२७)"""
        # Checks if a vowel is short
        return varna.char in ['अ', 'इ', 'उ', 'ऋ', 'ऌ']

    @staticmethod
    def is_laghu_1_4_10(varna_list, index):
        """
        [SUTRA]: ह्रस्वं लघु (१.४.१०)
        [LOGIC]: A short vowel is 'Laghu', UNLESS followed by a conjunct (Guru).
        """
        if index < 0 or index >= len(varna_list): return False
        varna = varna_list[index]

        if not varna.is_vowel: return False
        if varna.char not in ['अ', 'इ', 'उ', 'ऋ', 'ऌ']: return False

        # 1.4.11 Sanyoge Guru: Check if followed by a conjunct
        if index < len(varna_list) - 2:
            c1 = varna_list[index + 1]
            c2 = varna_list[index + 2]
            if c1.is_consonant and c2.is_consonant:
                return False  # It is Guru, not Laghu

        return True

    @staticmethod
    def check_pada_sanjna_1_4_14(varna_list, source_type):
        """[SUTRA]: सुप्तिङन्तं पदम् (१.४.१४)"""
        # A completed word with a declension/conjugation suffix is a Pada
        if source_type == UpadeshaType.VIBHAKTI:
            return True, "१.४.१४ (सुबन्तम्)"
        return False, ""

    @staticmethod
    def is_bha_1_4_18(varna_list, suffix_varna_list):
        """[SUTRA]: यचि भम् (१.४.१८)"""
        if not suffix_varna_list: return False
        first_char = suffix_varna_list[0].char
        # Stem is called 'Bha' before a vowel or 'y' starting suffix
        return first_char == 'य्' or pe.is_in(first_char, "अच्")

    @staticmethod
    def get_upadha_1_1_65(varna_list):
        """
        [SUTRA]: अलोऽन्त्यात् पूर्व उपधा (१.१.६५)
        [LOGIC]: The penultimate letter (Al) is called Upadhā.
        """
        if len(varna_list) < 2:
            return None, -1
        idx = len(varna_list) - 2
        return varna_list[idx], idx