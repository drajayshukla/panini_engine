#core/atidesha_mapper.py
# core/atidesha_mapper.py

class AtideshaMapper:
    """
    अतिदेश-सञ्चालक: (The Extension Engine)
    Zone 5: Handles property inheritance where one entity behaves like another.
    """

    @staticmethod
    def apply_sthanivadbhava_1_1_56(adesha_obj, sthani_obj, rule_id):
        """
        Sutra: स्थानिवदादेशोऽनल्विधौ (१.१.५६)
        Logic: An 'Adesha' (substitute) behaves like the 'Sthani' (original)
        it replaced, except in rules specifically targeting phonemes (al-vidhi).
        """
        # Inherit non-phonetic Sanjnas (like 'it', 'pratyaya', etc.)
        if hasattr(sthani_obj, 'sanjnas'):
            adesha_obj.sanjnas.update(sthani_obj.sanjnas)

        # Inherit Adhikara metadata
        adesha_obj.is_pratyaya = getattr(sthani_obj, 'is_pratyaya', False)
        adesha_obj.is_para = getattr(sthani_obj, 'is_para', False)

        # Add a trace for the debugger
        if not hasattr(adesha_obj, 'trace'):
            adesha_obj.trace = []
        adesha_obj.trace.append(f"Inherited properties from {sthani_obj.char} via 1.1.56 (Ref: {rule_id})")

        return adesha_obj

    @staticmethod
    def is_nit_vat_7_1_90(varna_obj):
        """
        Sutra: गोतो णित् (७.१.९०)
        Logic: The suffix following 'Go' behaves as if it has a 'Nit' marker.
        This is a 'Nit-vad-bhava' (behaving like Nit).
        """
        if hasattr(varna_obj, 'sanjnas'):
            varna_obj.sanjnas.add("nit_equivalent")
        return varna_obj