"""
FILE: logic/sanjna/definitions_1_1.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Saṃjñā-Prakaraṇam
REFERENCE: १.१.१ - १.१.२७
"""
from core.pratyahara_engine import PratyaharaEngine

pe = PratyaharaEngine()

class FoundationSanjnas:
    """
    Foundational definitions for Vṛddhi, Guṇa, Saṃyoga, and Sarvanāma.
    These form the base of the Paninian logical hierarchy.
    """

    @staticmethod
    def apply_1_1_1_vriddhi(varna_list):
        """
        [SUTRA]: वृद्धिरादैच् (१.१.१)
        [DEFINITION]: Ā (आ) and Ai/Au (ऐच्) are designated as 'Vṛddhi'.
        """
        for v in varna_list:
            if v.char == 'आ' or pe.is_in(v.char, "ऐच्"):
                v.sanjnas.add("वृद्धि")
                v.trace.append("१.१.१ वृद्धिरादैच्")
        return varna_list

    @staticmethod
    def is_guna_1_1_2(varna_input):
        """
        [SUTRA]: अदेङ् गुणः (१.१.२)
        [DEFINITION]: Short 'a' (At) and 'e/o' (Eṅ) are designated as 'Guṇa'.
        """
        char = varna_input.char if hasattr(varna_input, 'char') else varna_input
        guna_set = {'अ', 'ए', 'ओ'}

        if char in guna_set:
            if hasattr(varna_input, 'sanjnas'):
                varna_input.sanjnas.add("guna")
                varna_input.trace.append("१.१.२ अदेङ् गुणः")
            return True
        return False

    @staticmethod
    def apply_1_1_7_samyoga(varna_list):
        """
        [SUTRA]: हलोऽनन्तराः संयोगः (१.१.७)
        [DEFINITION]: Consonants without intervening vowels are called 'Saṃyoga'.
        """
        if len(varna_list) < 2: return varna_list
        for i in range(len(varna_list) - 1):
            curr, nxt = varna_list[i], varna_list[i + 1]
            if pe.is_in(curr.char, "हल्") and pe.is_in(nxt.char, "हल्"):
                curr.sanjnas.add("संयोग")
                nxt.sanjnas.add("संयोग")
        return varna_list

    @staticmethod
    def is_sarvanama_1_1_27(word_str):
        """
        [SUTRA]: सर्वादीनि सर्वनामानि (१.१.२७)
        [LOGIC]: Checks if a word belongs to the Sarvādi-gaṇa (Pronouns).
        """
        sarvadi_gana = {
            "सर्व", "विश्व", "उभ", "उभय", "डतर", "डतम", "अन्य", "अन्यतर",
            "इतर", "त्वत्", "त्व", "नेम", "सम", "सिम", "पूर्व", "पर",
            "अवर", "दक्षिण", "उत्तर", "अपर", "अधर", "स्व", "अन्तर",
            "त्यद्", "तद्", "यद्", "एतद्", "इदम्", "अदस्", "एक", "द्वि",
            "युष्मद्", "अस्मद्", "भवतु", "किम्"
        }
        return word_str in sarvadi_gana