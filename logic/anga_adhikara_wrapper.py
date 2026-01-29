"""
FILE: logic/anga_adhikara_wrapper.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Adhikāra (Jurisdictional Scope)
REFERENCE: ६.४.१ अङ्गस्य
"""

from core.adhikara_manager import AdhikaraManager
from logic.anga_engine import AngaEngine


def angasya_rule(sutra_number):
    """
    [DECORATOR]: Enforces the ६.४.१ अङ्गस्य अधिकार.
    Automatically slices the input into Aṅga (Stem) and Nimitta (Suffix).
    """

    def decorator(func):
        def wrapper(full_varna_list, manual_range=None, *args, **kwargs):
            # 1. Scope Check: Is the rule strictly within 6.4.1 - 7.4.120?
            if not AdhikaraManager.is_in_angasya_adhikara(sutra_number):
                # If outside Angasya, pass as a single block (General Vidhi)
                return func(full_varna_list, *args, **kwargs)

            # 2. Surgical Splitting (1.4.13)
            # Uses the logic/anga_engine.py to identify the Stem/Suffix boundary
            anga = AngaEngine.yasmat_pratyaya_vidhi_1_4_13(full_varna_list, manual_range)

            # The remainder is the Nimitta (Suffix)
            nimitta = full_varna_list[len(anga):]

            # 3. Execution on Aṅga only
            # The rule function receives the Stem and Suffix separately.
            # Note: If the rule modifies the suffix (e.g. 7.1.24), it must modify 'nimitta' in-place.
            new_anga, sutra_meta = func(anga, nimitta, *args, **kwargs)

            # 4. Reconstruction
            # Join the modified Stem with the (possibly modified) Suffix
            return new_anga + nimitta, sutra_meta

        return wrapper

    return decorator