"""
FILE: core/atidesha_mapper.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Atideśa (Property Inheritance)
REFERENCE: १.१.५६ स्थानिवदादेशोऽनल्विधौ
"""


class AtideshaMapper:
    """
    अतिदेश-सञ्चालक: (The Extension Engine)
    Governs how an Ādeśa (substitute) inherits the 'Soul' of its Sthānī (original).
    """

    @staticmethod
    def apply_sthanivadbhava_1_1_56(adesha_obj, sthani_obj, is_al_vidhi=False):
        """
        [SUTRA]: स्थानिवदादेशोऽनल्विधौ (१.१.५६)
        [VRITTI]: आदेशः स्थानिवत् स्यात् न तु अल्-विधौ।
        Logic: Substitute behaves like the original EXCEPT for phonetic rules.
        """
        # 1. Check for 'Al-vidhi' (Phonetic operations check)
        # If the rule targets specific phonemes (Al), inheritance is forbidden.
        if is_al_vidhi:
            adesha_obj.trace.append("१.१.५६: Inheritance blocked (Al-vidhi restriction).")
            return adesha_obj

        # 2. Inherit Functional Identity (Non-Al-vidhi)
        # These are properties like 'It', 'Pratyaya', 'Pada', etc.
        if hasattr(sthani_obj, 'sanjnas'):
            inherited_tags = sthani_obj.sanjnas.copy()
            adesha_obj.sanjnas.update(inherited_tags)

        # 3. Inherit Metadata (Pillar: Adhikara)
        adesha_obj.is_pratyaya = getattr(sthani_obj, 'is_pratyaya', False)

        # Trace for PAS-5 Audit
        adesha_obj.trace.append(f"१.१.५६: {adesha_obj.char} behaves as {sthani_obj.char}")

        return adesha_obj

    @staticmethod
    def apply_7_1_90_nitvadbhava(suffix_obj):
        """
        [SUTRA]: गोतो णित् (७.१.९०)
        [VRITTI]: ओकारान्तात् गो-शब्दात् परस्य अंगावयवस्य सर्वनामस्थानस्य णित्वं स्यात्।
        Logic: Suffix behaves like it has a 'Nit' marker (triggers Vriddhi).
        """
        suffix_obj.sanjnas.add("णित्-वत्")  # Mark as 'behaved-like-Nit'
        suffix_obj.trace.append("७.१.९० गोतो णित् (णित्-वद्भाव)")
        return suffix_obj