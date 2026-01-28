from core.phonology import Varna


def apply_rutva_8_2_66(varna_list):
    """
    Step 4: ससजुषोः रुः (८.२.६६)
    Converts padanta 's' to 'ruँ'.
    The 'uँ' is an anunasika-vowel marker for the next It-Sanjna cycle.
    """
    if varna_list and varna_list[-1].char == 'स्':
        varna_list.pop()  # Remove 's'

        # Adding 'ruँ' (r + uँ)
        varna_list.append(Varna('र्'))
        varna_list.append(Varna('उँ', is_anunasika=True))  # Marker for 1.3.2

        return varna_list, "८.२.६६ (ससजुषोः रुः)"
    return varna_list, None


def apply_visarga_8_3_15(varna_list):
    """
    Step 6: खरवसानयोर्विसर्जनीयः (८.३.१५)
    In 'Avasana' (pause), converts padanta 'r' to Visarga (ः).
    """
    if varna_list and varna_list[-1].char == 'र्':
        varna_list.pop()  # Remove 'r'
        varna_list.append(Varna('ः'))  # Final form

        return varna_list, "८.३.१५ (खरवसानयोर्विसर्जनीयः)"
    return varna_list, None