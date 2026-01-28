# logic/stem_classifier.py
from core.phonology import Varna

def mark_dirgha_stems(varna_list):
    """
    Specifically tags long vowels created during derivation
    to trigger Lopa rules correctly.
    """
    if len(varna_list) >= 2:
        # If we find the 'आ' created by 6.4.11
        for v in varna_list:
            if v.char in ['आ', 'ई']:
                v.is_dirgha_stem = True # Adding a custom attribute
    return varna_list