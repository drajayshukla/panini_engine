def apply_ata_upadhayah_7_2_116(varna_list, tags):
    """
    सूत्र: अत उपधायाः (7.2.116)
    तर्क: यदि उपधा (अन्तिम-वर्णात् पूर्वः) 'अ' अस्ति, तर्हि तस्य 'वृद्धि' (आ) भविष्यति।
    """
    if len(varna_list) < 2:
        return varna_list

    # उपधा वर्णस्य अन्वेषणम् (Second last character)
    upadha_index = -2 if varna_list[-1].endswith('्') else -2

    # यदि उपधा 'अ' अस्ति
    if varna_list[upadha_index] == 'अ':
        # १.१.१ सूत्रानुसारं 'अ' इत्यस्य स्थाने 'आ' (वृद्धि)
        varna_list[upadha_index] = 'आ'
        return varna_list, "७.२.११६ अत उपधायाः (वृद्धिः)"

    return varna_list, None