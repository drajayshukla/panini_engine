# logic/sthana_rules.py

def apply_sthana_rules(varna_obj):
    char = varna_obj.char.replace('्', '')  # हलन्त हटाकर चेक करें

    # अकुहविसर्जनीयानां कण्ठः
    if char in ['अ', 'आ', 'क', 'ख', 'ग', 'घ', 'ङ', 'ह', 'ः']:
        varna_obj.sthana = "कण्ठ"
    # इचुयशानां तालु
    elif char in ['इ', 'ई', 'च', 'छ', 'ज', 'झ', 'ञ', 'य', 'श']:
        varna_obj.sthana = "तालु"
    # ... अन्य सूत्र
    return varna_obj