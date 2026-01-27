# logic/kala_rules.py
# logic/kala_rules.py

def apply_ukalo_aj_1_2_27(varna_obj):
    """
    नियम २: ऌ-कारस्य दीर्घाभावात् (ऌ का दीर्घ नहीं होता)
    नियम ३: एचां ह्रस्वाभावात् (एच/ए, ओ, ऐ, औ का ह्रस्व नहीं होता)
    """
    if not varna_obj.is_vowel:
        varna_obj.kala_sanjna = "व्यञ्जन"
        return varna_obj

    # संज्ञा आवंटन
    if varna_obj.matra == 1:
        varna_obj.kala_sanjna = "ह्रस्व"
    elif varna_obj.matra == 2:
        varna_obj.kala_sanjna = "दीर्घ"
    elif varna_obj.matra == 3:
        varna_obj.kala_sanjna = "प्लुत"

    return varna_obj