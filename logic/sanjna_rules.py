def check_vriddhi_1_1_1(varna):
    """वृद्धिरादैच्: आ, ऐ, औ की वृद्धि संज्ञा होती है।"""
    vriddhi_letters = ['आ', 'ऐ', 'औ']
    return "वृद्धि" if varna in vriddhi_letters else None

def check_guna_1_1_2(varna):
    """अदेङ्गुणः: अ, ए, ओ की गुण संज्ञा होती है।"""
    guna_letters = ['अ', 'ए', 'ओ']
    return "गुण" if varna in guna_letters else None