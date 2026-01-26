def apply_ata_upadhayah_7_2_116(varna_list):
    """
    सूत्र: अत उपधायाः (7.2.116)
    विवरण: यदि अंग की उपधा (second last letter) 'अ' है,
    तो ञित् या णित् प्रत्यय परे होने पर उसे 'वृद्धि' (आ) आदेश होता है।
    """
    if len(varna_list) < 2:
        return varna_list, False

    # 1. उपधा (Upadha) की पहचान: अंतिम वर्ण से पूर्व वाला
    # ['प्', 'अ', 'ठ्'] -> उपधा है 'अ' (index -2)
    upadha_index = -2

    if varna_list[upadha_index] == 'अ':
        # 2. वृद्धि आदेश (Sutra 1.1.1 के आधार पर)
        # 'अ' का स्थान-सादृश्य (Stana) 'आ' के साथ है
        varna_list[upadha_index] = 'आ'
        return varna_list, True

    return varna_list, False