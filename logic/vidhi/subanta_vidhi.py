"""
FILE: logic/vidhi/subanta_vidhi.py
TIMESTAMP: 2026-01-31 03:50:00 (IST)
LOCATION: Lucknow, Uttar Pradesh, India
QUALITY: PAS-v2.0: 6.0 (Subanta) | PILLAR: Noun-Specific Rules
DESCRIPTION: Handles specific operations for noun declension (Chapters 7.1, 7.2, 7.3).
             Covers Neuter, Guna/Vriddhi, and irregular substitutions.
"""
from core.phonology import Varna, sanskrit_varna_samyoga


class SubantaVidhi:
    """
    [VṚTTI]: सुबन्त-प्रक्रिया।
    Specific operations for noun declension. This module handles stem and
    suffix transformations that occur before final Tripadi phonology.
    """

    @staticmethod
    def apply_ato_bhisa_ais_7_1_9(anga, suffix):
        """
        [7.1.9]: अतो भिस ऐस्।
        Requirement: Stem ends in short 'a' and suffix is 'bhis'.
        Action: Replace 'bhis' with 'ais'.
        """
        if not anga or not suffix: return anga, suffix, None

        if anga[-1].char == 'अ':
            suffix_str = sanskrit_varna_samyoga(suffix)
            if suffix_str == "भिस्":
                # Replace 'bhis' with 'ais'
                new_suffix = [Varna("ऐ"), Varna("स्")]
                for v in new_suffix:
                    v.sanjnas.add("adesha")
                    v.trace.append("7.1.9")
                return anga, new_suffix, "7.1.9"

        return anga, suffix, None

    @staticmethod
    def apply_ato_am_7_1_24(stem, suffix):
        """
        [7.1.24]: अतोऽम्।
        Requirement: Neuter stem ending in short 'a'.
        Action: Replace Su/Am pratyaya with 'Am'.
        """
        if stem and stem[-1].char == 'अ':
            new_suffix = [Varna("अ"), Varna("म्")]
            for v in new_suffix:
                v.sanjnas.add("adesha")
                v.trace.append("7.1.24")
            return stem, new_suffix, "7.1.24"

        return stem, suffix, None

    @staticmethod
    def apply_jasi_ca_7_3_109(stem, suffix):
        """
        [7.3.109]: जसि च।
        Requirement: Stem ending in short 'i' or 'u' followed by 'Jas'.
        Action: Apply Guna to the final vowel of the stem.
        """
        if not stem: return stem, None

        last_vowel = stem[-1].char
        if last_vowel == "इ":
            res = stem[:-1] + [Varna("ए")]
            return res, "7.3.109"
        elif last_vowel == "उ":
            res = stem[:-1] + [Varna("ओ")]
            return res, "7.3.109"

        return stem, None

    @staticmethod
    def apply_rto_ngi_sarvanamasthanayoh_7_3_110(stem, suffix):
        """
        [7.3.110]: ऋतो ङिसर्वनामस्थानयोः।
        Requirement: Stem ending in 'ṛ' followed by 'Ṅi' or Sarvanamasthana (Su, Au, Jas...).
        Action: Apply Guna to 'ṛ'. Note: 1.1.51 (Uran Raparah) makes it 'ar'.
        """
        if stem and stem[-1].char == "ऋ":
            # Guna of ṛ is 'a', but because it is 'ṛ', it becomes 'ar' (रपरत्वम्)
            res = stem[:-1] + [Varna("अ"), Varna("र्")]
            return res, "7.3.110"

        return stem, None

    @staticmethod
    def apply_aco_niti_7_2_115(stem, suffix):
        """
        [7.2.115]: अचो ञ्णिति।
        Requirement: Stem ending in any vowel followed by a Ñit or Ṇit suffix.
        Action: Apply Vriddhi to the final vowel.
        """
        if not stem or not suffix: return stem, None

        # Check for Ñit or Ṇit tags in the suffix
        is_n_nit = any(tag in ["ñit", "ṇit"] for v in suffix for tag in v.sanjnas)

        if is_n_nit:
            last_vowel = stem[-1].char
            vriddhi_map = {"इ": "ऐ", "ई": "ऐ", "उ": "औ", "ऊ": "औ", "ऋ": "आर्", "ओ": "औ"}

            if last_vowel in vriddhi_map:
                # Handle r-para internally for Ṛ
                if last_vowel == "ऋ":
                    res = stem[:-1] + [Varna("आ"), Varna("र्")]
                else:
                    res = stem[:-1] + [Varna(vriddhi_map[last_vowel])]
                return res, "7.2.115"

        return stem, None

    @staticmethod
    def apply_div_aut_7_1_84(stem, suffix):
        """
        [7.1.84]: दिव औत्।
        Requirement: Root 'Div' followed by 'Su'.
        Action: Replace final 'v' with 'au'. (1.1.52 Alo'ntyasya)
        """
        if stem and stem[-1].char == "व्":
            res = stem[:-1] + [Varna("औ")]
            return res, "7.1.84"
        return stem, None