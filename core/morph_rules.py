# panini_engine/core/morph_rules.py

def apply_ata_upadhayah_7_2_116(varna_list, is_nit_prakaran=False):
    """
    सूत्र: अत उपधायाः (७.२.११६)
    विवरण: ञित् या णित् प्रत्यय परे होने पर अङ्ग की 'उपधा' (अ) को वृद्धि (आ) होती है।
    उदाहरण: पठ् + ण्वुल् -> पाठ् + अक = पाठक।
    """
    # १. उपधा की परिभाषा (१.१.६५): अन्त्य वर्ण से पूर्व वाला अलू।
    if len(varna_list) < 2:
        return varna_list, False

    # २. केवल तभी लागू करें जब ञित्/णित् प्रत्यय का संदर्भ हो
    if not is_nit_prakaran:
        return varna_list, False

    # ३. उपधा की पहचान (Index -2)
    upadha_index = -2
    upadha_varna = varna_list[upadha_index]

    # ४. Object-Safe Check: क्या उपधा 'अ' (ह्रस्व) है?
    if upadha_varna.char == 'अ' and upadha_varna.matra == 1:
        # ५. वृद्धि आदेश (स्थान-सादृश्य के आधार पर अ -> आ)
        # हम नया Varna ऑब्जेक्ट बनाएंगे ताकि पुराने एट्रिब्यूट्स (जैसे स्थान) अपडेट हो सकें
        from core.phonology import Varna
        varna_list[upadha_index] = Varna('आ')

        return varna_list, True

    return varna_list, False