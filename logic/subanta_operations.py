# logic/subanta_operations.py
from core.phonology import Varna

# --- ६. अध्याय (Chapter 6) ---

def apply_hal_nyab_6_1_68(varna_list):
    """
    ६.१.६८ हल्ङ्याब्भ्यो...
    Strictly targets the 'स्' if preceded by 'आ' or 'ई'.
    """
    # Create a local copy to avoid reference issues
    v_list = list(varna_list)
    if len(v_list) >= 2 and v_list[-1].char == 'स्':
        # Check penultimate character
        if v_list[-2].char in ['आ', 'ई']:
            v_list.pop() # Remove 'स्'
            return v_list, "६.१.६८ (हल्ङ्याब्भ्यो... अपृक्त-लोप)"
    return varna_list, None

def apply_upadha_dirgha_6_4_11(varna_list):
    """
    ६.४.११ अप्तृन्तृच्स्वसृनप्तृनेष्टृत्वष्टृक्षत्तृहोतृपोतृप्रशास्तॄणाम्
    नियम: 'न्' से पहले स्थित उपधा 'अ' को दीर्घ 'आ' आदेश।
    """
    for i in range(len(varna_list) - 1, 0, -1):
        if varna_list[i].char == 'न्' and varna_list[i-1].char == 'अ':
            varna_list[i-1] = Varna('आ')
            return varna_list, "६.४.११ (अप्तृन्तृच्... उपधा दीर्घ)"
    return varna_list, None


# --- ७. अध्याय (Chapter 7) ---

def apply_anang_7_1_94(varna_list):
    """
    ७.१.९४ ऋदुशनस्पुरुदंसोऽनेहसां च
    नियम: ऋदन्त अङ्ग को 'अनङ्' (अ न् ङ्) आदेश। ङित् होने से अन्त्य ऋकार के स्थान पर।
    """
    for i in range(len(varna_list) - 1, -1, -1):
        if varna_list[i].char == 'ऋ':
            varna_list.pop(i)
            # १.१.५३ ङिच्च: अन्त्य के स्थान पर अ, न्, ङ्
            varna_list.insert(i, Varna('अ'))
            varna_list.insert(i+1, Varna('न्'))
            varna_list.insert(i+2, Varna('ङ्'))
            return varna_list, "७.१.९४ (ऋदुशनस्... अनङ्-आदेशः)"
    return varna_list, None


def apply_trijvadbhava_7_1_95(varna_list):
    """
    ७.१.९५ तृज्वत्क्रोष्टुः
    नियम: 'क्रोष्टु' शब्द के 'उ' को 'ऋ' (तृच् प्रत्यय के समान) आदेश।
    """
    for i in range(len(varna_list) - 1, -1, -1):
        if varna_list[i].char == 'उ':
            varna_list[i] = Varna('ऋ')
            return varna_list, "७.१.९५ (तृज्वत्क्रोष्टुः)"
    return varna_list, None


# --- ८. अध्याय (Chapter 8) ---

def apply_nalopa_8_2_7(varna_list):
    """
    ८.२.७ नलोपः प्रातिपदिकान्तस्य
    Target 'न्' only if it is the absolute final character.
    """
    v_list = list(varna_list)
    if v_list and v_list[-1].char == 'न्':
        v_list.pop() # Remove 'न्'
        return v_list, "८.२.७ (नलोपः प्रातिपदिकान्तस्य)"
    return varna_list, None

def apply_rutva_8_2_66(varna_list):
    """
    ८.२.६६ ससजुषोः रुः
    नियम: पदान्त 'स्' के स्थान पर 'रुँ' (र् उँ) आदेश।
    """
    if varna_list and varna_list[-1].char == 'स्':
        varna_list.pop()
        varna_list.append(Varna('र्'))
        varna_list.append(Varna('उँ'))
        return varna_list, "८.२.६६ (ससजुषोः रुः)"
    return varna_list, None


def apply_visarga_8_3_15(varna_list):
    """
    ८.३.१५ खरवसानयोर्विसर्जनीयः
    नियम: अवसान या खर परे होने पर पदान्त 'र्' को विसर्ग (ः) आदेश।
    """
    if varna_list and varna_list[-1].char == 'र्':
        varna_list.pop()
        varna_list.append(Varna('ः'))
        return varna_list, "८.३.१५ (खरवसानयोर्विसर्जनीयः)"
    return varna_list, None