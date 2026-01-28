# logic/subanta_operations.py
from core.phonology import Varna

# --- ६. अध्याय (Chapter 6) ---

'''def apply_hal_nyab_6_1_68(varna_list):
    """
    ६.१.६८ (हल्ङ्याब्भ्यो...): Removal of 'स्'
    Logic: If word ends in 'स्' and the stem has a long vowel (आ/ई)
    created by upadha-dirgha, drop 'स्'.
    """
    v_list = list(varna_list)
    if v_list and v_list[-1].char == 'स्':
        # Check if 'आ' exists in the last few positions (Aggressive search)
        last_chars = [v.char for v in v_list[-4:]]
        if 'आ' in last_chars or 'ई' in last_chars:
            v_list.pop() # Surgical removal of 'स्'
            return v_list, "६.१.६८ (हल्ङ्याब्भ्यो... अपृक्त-लोप)"
    return varna_list, None'''


'''def apply_hal_nyab_6_1_68(varna_list):
    """
    ६.१.६८ (हल्ङ्याब्भ्यो...): Removal of 'स्'
    Aggressive search version to accommodate intermediate consonants like 'n'.
    """
    v_list = list(varna_list)
    if v_list and v_list[-1].char == 'स्':
        # Create a string of the last 4 characters for easy searching
        last_chars_str = "".join([v.char for v in v_list[-4:]])

        # Check for Paninian triggers: Dirgha (Long) vowels
        if 'आ' in last_chars_str or 'ई' in last_chars_str or 'ऊ' in last_chars_str:
            v_list.pop()  # Surgical removal of 'स्'
            return v_list, "६.१.६८ (हल्ङ्याब्भ्यो... अपृक्त-लोप)"

    return varna_list, None'''
# logic/subanta_operations.py
def apply_ami_purvah_6_1_107(varna_list):
    """
    ६.१.१०७ अमि पूर्वः
    Logic: Merge stem-final 'a' and suffix 'a' into a single 'a'.
    Example: ज्ञान + अम् -> ज्ञानम्
    """
    v_list = list(varna_list)
    # Check for two consecutive 'अ's followed by 'म्'
    for i in range(len(v_list) - 2):
        if v_list[i].char == 'अ' and v_list[i+1].char == 'अ' and v_list[i+2].char == 'म्':
            v_list.pop(i+1) # Remove the second 'अ'
            return v_list, "६.१.१०७ (अमि पूर्वः - पूर्वरूपम्)"
    return varna_list, None
def apply_hal_nyab_6_1_68(varna_list):
    """
    ६.१.६८ (हल्ङ्याब्भ्यो...): Removal of 'स्'
    Aggressive search version to handle intermediate 'n' and
    various long vowel triggers (ā, ī, ū).
    """
    v_list = list(varna_list)
    if v_list and v_list[-1].char == 'स्':
        # Examine the end of the word for the trigger vowel
        last_chars_str = "".join([v.char for v in v_list[-4:]])
        if any(v in last_chars_str for v in ['आ', 'ई', 'ऊ']):
            v_list.pop()
            return v_list, "६.१.६८ (हल्ङ्याब्भ्यो... अपृक्त-लोप)"
    return varna_list, None
def apply_upadha_dirgha_6_4_8(varna_list):
    """
    ६.४.८ सर्वनामस्थाने चासम्बुद्धौ
    Logic: Penultimate 'a' -> 'ā' for N-anta stems (like Jāmātṛ/Pitṛ).
    """
    v_list = list(varna_list)
    for i in range(len(v_list) - 1, 0, -1):
        if v_list[i].char == 'न्' and v_list[i-1].char == 'अ':
            v_list[i-1] = Varna('आ')
            return v_list, "६.४.८ (सर्वनामस्थाने चासम्बुद्धौ - उपधा दीर्घ)"
    return varna_list, None

def apply_upadha_dirgha_6_4_11(varna_list):
    """
    ६.४.११ अङ्गस्य उपधा दीर्घ:
    Logic: Penultimate lengthening for Kroṣṭu pipeline.
    """
    v_list = list(varna_list)
    for i in range(len(v_list) - 1, 0, -1):
        if v_list[i].char == 'न्' and v_list[i-1].char == 'अ':
            v_list[i-1] = Varna('आ')
            return v_list, "६.४.११ (अप्तृन्तृच्... उपधा दीर्घ)"
    return varna_list, None


def apply_ti_lopa_6_4_143(varna_list):
    """
    ६.४.१४३ टेः
    Correct Logic: Only the final 'अ' of the stem (अन्य) is removed.
    The 'य्' is preserved.
    """
    v_list = list(varna_list)

    # In the list: ['अ', 'न्', 'य्', 'अ', 'अ', 'द्']
    # Indices:       0    1    2    3    4    5
    # We need to remove index 3 (the stem's final vowel)

    if len(v_list) >= 6:
        # Assuming the suffix 'ad' starts at index -2
        # The stem's Ti is at index -3 relative to the end of the list
        v_list.pop(-3)
        return v_list, "६.४.१४३ (टेः - टि-लोपः)"
    return varna_list, None

# --- ७. अध्याय (Chapter 7) ---

def apply_ato_am_7_1_24(varna_list):
    """
    ७.१.२४ अतोऽम्
    Logic: For neuter stems ending in 'a', replace 'su' (s) with 'am'.
    """
    v_list = list(varna_list)
    # Find where the suffix starts (after 'न' in 'ज्ञान')
    if v_list and v_list[-1].char == 'स्':
        v_list.pop() # Remove 'स्'
        v_list.append(Varna('अ'))
        v_list.append(Varna('म्'))
        return v_list, "७.१.२४ (अतोऽम् - सुँ -> अम् आदेशः)"
    return varna_list, None

def apply_add_7_1_25(varna_list):
    """
    ७.१.२५ अद्ड् डतरादिभ्यः पञ्चभ्यः
    Logic: Replace 'su' (s) with 'adḍ' for specific pronouns.
    """
    v_list = list(varna_list)
    if v_list and v_list[-1].char == 'स्':
        v_list.pop() # Remove 'स्'
        # Add 'अ', 'द्', 'ड्'
        v_list.extend([Varna('अ'), Varna('द्'), Varna('ड्')])
        return v_list, "७.१.२५ (अद्ड्-आदेशः)"
    return varna_list, None

def apply_goto_nit_7_1_90(varna_list):
    """
    ७.१.९० गोतो णित्
    Logic: Mark the current suffix/process as 'Nit' for Go-shabda.
    (In our code, this serves as a trigger for 7.2.115).
    """
    # This is a conceptual rule, returns the list as is with a label.
    return varna_list, "७.१.९० (गोतो णित् - णिद्वद्भावः)"
def apply_anang_7_1_94(varna_list):
    """
    ७.१.९४ ऋदुशनस्... (अनङ्-आदेशः)
    Replacement of final 'ṛ' with 'an-aṅ'.
    """
    for i in range(len(varna_list) - 1, -1, -1):
        if varna_list[i].char == 'ऋ':
            varna_list.pop(i)
            # ङिच्च (1.1.53) logic
            varna_list.insert(i, Varna('अ'))
            varna_list.insert(i+1, Varna('न्'))
            varna_list.insert(i+2, Varna('ङ्'))
            return varna_list, "७.१.९४ (ऋदुशनस्... अनङ्-आदेशः)"
    return varna_list, None

def apply_trijvadbhava_7_1_95(varna_list):
    """
    ७.१.९५ तृज्वत्क्रोष्टुः
    Converts 'u' to 'ṛ' in Kroṣṭu.
    """
    for i in range(len(varna_list) - 1, -1, -1):
        if varna_list[i].char == 'उ':
            varna_list[i] = Varna('ऋ')
            return varna_list, "७.१.९५ (तृज्वत्क्रोष्टुः)"
    return varna_list, None
# logic/subanta_operations.py

def apply_rayo_hali_7_2_85(varna_list):
    """
    ७.२.८५ रायो हलि
    Logic: Replace 'ऐ' with 'आ' when followed by a Hal-ādi suffix.
    """
    v_list = list(varna_list)
    for i in range(len(v_list)):
        if v_list[i].char == 'ऐ':
            v_list[i] = Varna('आ')
            return v_list, "७.२.८५ (रायो हलि - आकारादेशः)"
    return varna_list, None
def apply_vṛddhi_7_2_115(varna_list):
    """
    ७.२.११५ अचो ञ्णिति
    Logic: Replace final 'ओ' with Vṛddhi 'औ' before a Nit suffix.
    """
    v_list = list(varna_list)
    for i in range(len(v_list)):
        if v_list[i].char == 'ओ':
            v_list[i] = Varna('औ')
            return v_list, "७.२.११५ (अचो ञ्णिति - वृद्धिः)"
    return varna_list, None
# --- ८. अध्याय (Chapter 8) ---

def apply_nalopa_8_2_7(varna_list):
    """
    ८.२.७ (नलोपः...): Removal of 'न्' at pada-anta.
    """
    v_list = list(varna_list)
    if v_list and v_list[-1].char == 'न्':
        v_list.pop()
        return v_list, "८.२.७ (नलोपः प्रातिपदिकान्तस्य)"
    return varna_list, None

def apply_rutva_8_2_66(varna_list):
    """८.२.६६ ससजुषोः रुः"""
    if varna_list and varna_list[-1].char == 'स्':
        varna_list.pop()
        varna_list.append(Varna('र्'))
        varna_list.append(Varna('उँ'))
        return varna_list, "८.२.६६ (ससजुषोः रुः)"
    return varna_list, None

def apply_visarga_8_3_15(varna_list):
    """८.३.१५ खरवसानयोर्विसर्जनीयः"""
    if varna_list and varna_list[-1].char == 'र्':
        varna_list.pop()
        varna_list.append(Varna('ः'))
        return varna_list, "८.३.१५ (खरवसानयोर्विसर्जनीयः)"
    return varna_list, None

def apply_chartva_8_4_56(varna_list):
    """
    ८.४.५६ वाऽवसाने
    Logic: Optional replacement of 'd' with 't' at the end of a word.
    """
    v_list = list(varna_list)
    if v_list and v_list[-1].char == 'द्':
        v_list[-1] = Varna('त्')
        return v_list, "८.४.५६ (चर्त्वम् - वैकल्पिके)"
    return varna_list, None
