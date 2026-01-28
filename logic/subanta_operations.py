# logic/subanta_operations.py
from core.phonology import Varna

# --- Standard Pada-Anta Operations ---

def apply_rutva_8_2_66(varna_list):
    """८.२.६६ ससजुषोः रुः: Converts padanta 's' to 'ruँ'."""
    if varna_list and varna_list[-1].char == 'स्':
        varna_list.pop()  # Surgical removal of 's'
        varna_list.append(Varna('र्'))
        varna_list.append(Varna('उँ'))
        return varna_list, "८.२.६६ (ससजुषोः रुः)"
    return varna_list, None

def apply_visarga_8_3_15(varna_list):
    """८.३.१५ खरवसानयोर्विसर्जनीयः: Converts padanta 'r' to Visarga."""
    if varna_list and varna_list[-1].char == 'र्':
        varna_list.pop()
        varna_list.append(Varna('ः'))
        return varna_list, "८.३.१५ (खरवसानयोर्विसर्जनीयः)"
    return varna_list, None

def apply_hal_nyab_6_1_68(varna_list):
    """६.१.६८ हल्ङ्याब्भ्यो...: Deletes single-letter 's' after long vowels."""
    if varna_list and varna_list[-1].char == 'स्':
        if len(varna_list) >= 2:
            prev_varna = varna_list[-2].char
            if prev_varna in ['ई', 'आ']:
                varna_list.pop()
                return varna_list, "६.१.६८ (हल्ङ्याब्भ्यो दीर्घात् सुतिस्यपृक्तं हल्)"
    return varna_list, None

# --- Special Stem Transformations (Kroṣṭu/Tṛj-vat) ---

def apply_trijvadbhava_7_1_95(varna_list):
    """७.१.९५ तृज्वत्क्रोष्टुः: Position-aware search to change 'u' to 'ṛ'."""
    for i in range(len(varna_list) - 1, -1, -1):
        if varna_list[i].char == 'उ':
            varna_list[i] = Varna('ऋ')
            return varna_list, "७.१.९५ (तृज्वत्क्रोष्टुः)"
    return varna_list, None

def apply_anang_7_1_94(varna_list):
    """७.१.९४ ऋदुशनस्...: Replaces 'ṛ' with 'an-aṅ' (अ न् ङ्)."""
    for i in range(len(varna_list) - 1, -1, -1):
        if varna_list[i].char == 'ऋ':
            varna_list.pop(i)
            # ङिच्च (1.1.53): The whole 'anang' replaces 'ṛ'
            varna_list.insert(i, Varna('अ'))
            varna_list.insert(i+1, Varna('न्'))
            varna_list.insert(i+2, Varna('ङ्'))
            return varna_list, "७.१.९४ (ऋदुशनस्... अनङ्-आदेशः)"
    return varna_list, None

def apply_upadha_dirgha_6_4_11(varna_list):
    """६.४.११: Penultimate lengthening (a -> ā) before 'n'."""
    for i in range(len(varna_list) - 1, 0, -1):
        if varna_list[i].char == 'न्' and varna_list[i-1].char == 'अ':
            varna_list[i-1] = Varna('आ')
            return varna_list, "६.४.११ (अप्तृन्तृच्... उपधा दीर्घ)"
    return varna_list, None

def apply_nalopa_8_2_7(varna_list):
    """८.२.७ नलोपः प्रातिपदिकान्तस्य: Deletes 'n' at end of Pada."""
    if varna_list and varna_list[-1].char == 'न्':
        varna_list.pop()
        return varna_list, "८.२.७ (नलोपः प्रातिपदिकान्तस्य)"
    return varna_list, None