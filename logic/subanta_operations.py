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

from core.phonology import Varna

def apply_trijvadbhava_7_1_95(varna_list):
    """
    Sutra: तृज्वत्क्रोष्टुः (७.१.९५)
    Description: Converts 'u' to 'ṛ' in the word 'kroṣṭu' before certain suffixes.
    """
    # Kroṣṭu -> Kroṣṭṛ
    word = "".join([v.char for v in varna_list])
    if "क्रोष्टु" in word:
        # Replacing the final 'u' (उ) with 'ṛ' (ऋ)
        if varna_list[-2].char == 'उ': # Assuming word+s structure
            varna_list[-2] = Varna('ऋ')
            return varna_list, "७.१.९५ (तृज्वत्क्रोष्टुः)"
    return varna_list, None

def apply_anang_7_1_94(varna_list):
    """
    Sutra: ऋदुशनस्पुरुदंसोऽनेहसां च (७.१.९४)
    Description: Applies 'anaṅ' (अनङ्) substitution to the end of ṛ-ending words.
    """
    # kroṣṭṛ + s -> kroṣṭ-anang + s
    if varna_list and varna_list[-2].char == 'ऋ':
        varna_list.pop(-2) # Remove 'ṛ'
        # Insert 'anang' components
        varna_list.insert(-1, Varna('अ'))
        varna_list.insert(-1, Varna('न्'))
        varna_list.insert(-1, Varna('ङ्'))
        return varna_list, "७.१.९४ (ऋदुशनस्पुरुदंसोऽनेहसां च)"
    return varna_list, None

def apply_upadha_dirgha_6_4_11(varna_list):
    """
    Sutra: अप्तृन्तृच्स्वसृ... (६.४.११)
    Description: Lengthens the penultimate vowel (Upadha) of 'n' ending bases.
    """
    # kroṣṭan + s -> kroṣṭān + s
    for i in range(len(varna_list)-1, -1, -1):
        if varna_list[i].char == 'अ':
            varna_list[i] = Varna('आ')
            return varna_list, "६.४.११ (अप्तृन्तृच्... दीर्घः)"
    return varna_list, None

def apply_nalopa_8_2_7(varna_list):
    """
    Sutra: नलोपः प्रातिपदिकान्तस्य (८.२.७)
    Description: Deletes the final 'n' of a Pada that is also a Pratipadika.
    """
    if varna_list and varna_list[-1].char == 'न्':
        varna_list.pop()
        return varna_list, "८.२.७ (नलोपः प्रातिपदिकान्तस्य)"
    return varna_list, None
