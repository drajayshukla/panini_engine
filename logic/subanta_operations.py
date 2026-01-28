from core.phonology import Varna


# logic/subanta_operations.py

def apply_rutva_8_2_66(varna_list):
    """
    ससजुषोः रुः (८.२.६६)
    Converts padanta 's' to 'ruँ'.
    """
    if varna_list and varna_list[-1].char == 'स्':
        varna_list.pop()  # Remove 's'

        # We append 'र्' and 'उँ' as separate Varna objects.
        # The ItSanjnaEngine will detect 'उँ' as anunasika automatically
        # based on your phonology logic.
        from core.phonology import Varna
        varna_list.append(Varna('र्'))
        varna_list.append(Varna('उँ'))

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


def apply_hal_nyab_6_1_68(varna_list):
    """
    Sutra: हल्ङ्याब्भ्यो दीर्घात् सुतिस्यपृक्तं हल् (६.१.६८)
    Description: Deletes the single-letter 's' (Apṛkta) after
    a long Ni (ई) or Ap (आ) ending word.
    """
    # Check if word ends with 'स्'
    if varna_list and varna_list[-1].char == 'स्':
        # Logic: Is the preceding varna a long 'ई' or 'आ'?
        if len(varna_list) >= 2:
            prev_varna = varna_list[-2].char
            if prev_varna in ['ई', 'आ']:
                varna_list.pop()  # Surgical deletion of 'स्'
                return varna_list, "६.१.६८ (हल्ङ्याब्भ्यो दीर्घात् सुतिस्यपृक्तं हल्)"

    return varna_list, None