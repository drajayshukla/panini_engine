"""
FILE: logic/vidhi/sarvanama_vidhi.py
TIMESTAMP: 2026-01-30 22:45:00 (IST)
LOCATION: Lucknow, Uttar Pradesh, India
QUALITY: PAS-v2.0: 6.0 (Subanta) | PILLAR: Pronoun Logic (Sarvanama)
"""
from core.phonology import Varna, ad


class SarvanamaVidhi:
    """
    Handles specific operations for Sarvanama (Pronouns).
    Rules: 7.1.14, 7.1.15, 7.1.16, 7.1.17, 7.1.52.
    """

    @staticmethod
    def is_sarvanama(stem_str):
        """
        [1.1.27] Sarvadini Sarvanamani.
        Checks if the stem is in the Sarvadi Gana.
        """
        sarvadi_gana = [
            "सर्व", "विश्व", "उभ", "उभय", "डतर", "डतम", "अन्य", "अन्यतर", "इतर",
            "त्वत्", "त्व", "नेम", "सम", "सिम",
            "पूर्व", "पर", "अवर", "दक्षिण", "उत्तर", "अपर", "अधर", "स्व", "अन्तर",
            "त्यद्", "तद्", "यद्", "एतद्", "इदम्", "अदस्", "एक", "द्वि", "युष्मद्", "अस्मद्",
            "भवतु", "किम्"
        ]
        return stem_str in sarvadi_gana

    @staticmethod
    def apply_jasah_shi_7_1_17(stem, suffix):
        """
        [7.1.17] Jasah Shi.
        For 'a' ending Sarvanama, Jas (1.3) becomes Shi (ī).
        Example: Sarva + Jas -> Sarva + Shi -> Sarve.
        """
        # Condition: Suffix is Jas (as) and Stem ends in 'a'
        if not suffix: return stem, suffix, None

        # Jas is cleaned to 'as' by ItEngine, but we identify it by context
        # (This method must be called BEFORE general sandhi merges stem+suffix)

        # Simple check: suffix starts with 'अ' and ends with 'स्' (approx)
        # Better: The caller (Engine) knows it's Case 1, Plural.

        # We replace the entire suffix with 'ई' (Shi)
        new_suffix = [Varna("ई")]
        return stem, new_suffix, "7.1.17"

    @staticmethod
    def apply_sarvanamnah_smai_7_1_14(stem, suffix):
        """
        [7.1.14] Sarvanamnah Smai.
        For 'a' ending Sarvanama, Ne (4.1) becomes Smai.
        Example: Sarva + e -> Sarvasmai.
        """
        # We replace suffix with Smai (s, m, ai)
        new_suffix = ad("स्मै")
        return stem, new_suffix, "7.1.14"

    @staticmethod
    def apply_nasinyoh_smatsminau_7_1_15(stem, suffix, is_nasi=True):
        """
        [7.1.15] Nasinyoh Smatsminau.
        Nasi (5.1) -> Smat.
        Ni (7.1) -> Smin.
        """
        if is_nasi:
            new_suffix = ad("स्मात्")
            return stem, new_suffix, "7.1.15"
        else:
            new_suffix = ad("स्मिन्")
            return stem, new_suffix, "7.1.15"

    @staticmethod
    def apply_ami_sarvanamnah_sut_7_1_52(stem, suffix):
        """
        [7.1.52] Ami Sarvanamnah Sut.
        Insert 's' (sut) before Am (6.3).
        Example: Sarva + am -> Sarva + s + am -> Sarvesham.
        """
        # Inject 's' at the start of suffix
        suffix.insert(0, Varna("स्"))
        return stem, suffix, "7.1.52"