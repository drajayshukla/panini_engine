# logic/anga_adhikara_wrapper.py

from core.adhikara_manager import AdhikaraManager
from logic.anga_engine import AngaEngine


def angasya_rule(sutra_number):
    """
    Decorator to enforce the ६.४.१ अङ्गस्य अधिकार।
    Automatically slices the input into Aṅga and Nimitta.
    """

    def decorator(func):
        def wrapper(full_varna_list, manual_range=None, *args, **kwargs):
            # 1. Scope Check
            if not AdhikaraManager.is_in_angasya_adhikara(sutra_number):
                # If outside Angasya, pass as a single block
                return func(full_varna_list, *args, **kwargs)

            # 2. Surgical Splitting (1.4.13)
            # Uses the logic/anga_engine.py we just finalized
            anga = AngaEngine.yasmat_pratyaya_vidhi_1_4_13(full_varna_list, manual_range)
            nimitta = full_varna_list[len(anga):]

            # 3. Execution on Aṅga only
            # Your function only has to worry about the Stem
            new_anga, sutra_meta = func(anga, nimitta, *args, **kwargs)

            # 4. Reconstruction
            return new_anga + nimitta, sutra_meta

        return wrapper

    return decorator