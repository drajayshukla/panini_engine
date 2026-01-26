def apply_halantyam(varna_list):
    """
    हलन्त्यम् (1.3.3): उपदेश के अंत में स्थित व्यंजन की इत् संज्ञा होती है।
    """
    if not varna_list: return varna_list, []

    it_letters = []
    # यदि अंतिम वर्ण हलन्त व्यंजन है
    if varna_list[-1].endswith('्'):
        it_letters.append(varna_list.pop())

    return varna_list, it_letters