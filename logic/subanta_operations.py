from core.phonology import Varna


def apply_rutva_8_2_66(varna_list):
    """
    सूत्र: ससजुषोः रुः (८.२.६६)
    विवरण: पदान्त 'स्' के स्थान पर 'रुँ' आदेश होता है।
    प्रक्रिया: 'स्' को हटाकर 'र्' और इत्-संज्ञक 'उँ' जोड़ा जाता है।
    """
    # पदान्त 'स्' की जाँच
    if varna_list and varna_list[-1].char == 'स्':
        varna_list.pop()  # 'स्' का निष्कासन

        # 'रुँ' का निर्माण (र् + उँ)
        # 'उँ' अनुनासिक है, जो अगले इत्-संज्ञा चक्र (१.३.२) में लोप हो जाएगा
        varna_list.append(Varna('र्'))
        varna_list.append(Varna('उँ'))

        return varna_list, "८.२.६६ (ससजुषोः रुः)"

    return varna_list, None


def apply_visarga_8_3_15(varna_list):
    """
    सूत्र: खरवसानयोर्विसर्जनीयः (८.३.१५)
    विवरण: अवसान (वर्णों का अभाव) होने पर पदान्त 'र्' के स्थान पर 'विसर्ग' (ः) होता है।
    """
    # पदान्त 'र्' की जाँच (इत्-लोप के पश्चात शेष रहा 'र्')
    if varna_list and varna_list[-1].char == 'र्':
        varna_list.pop()  # 'र्' का निष्कासन

        # विसर्ग (ः) आदेश
        varna_list.append(Varna('ः'))

        return varna_list, "८.३.१५ (खरवसानयोर्विसर्जनीयः)"

    return varna_list, None