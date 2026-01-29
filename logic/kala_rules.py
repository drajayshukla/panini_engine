"""
FILE: logic/kala_rules.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Kāla-Saṃjñā (Temporal Definitions)
REFERENCE: १.२.२७ to १.२.२८
"""

# --- Static Data: Intrinsic Duration Mapping ---
HRASVA_SET = {'अ', 'इ', 'उ', 'ऋ', 'ऌ'}
DIRGHA_SET = {
    'आ', 'ई', 'ऊ', 'ॠ',
    'ए', 'ऐ', 'ो', 'औ',  # Diphthongs are inherently long
    'े', 'ै', 'ो', 'ौ',  # Matra forms
    'ा', 'ी', 'ू', 'ॄ'  # Matra forms
}


def apply_1_2_28_acashca(varna_obj, action_name="Kala-Sanjna"):
    """
    [SUTRA]: अचश्च (१.२.२८)
    [LOGIC]: The definitions Hrasva, Dirgha, and Pluta apply ONLY to Ac (Vowels).
    Returns: (Boolean Is_Valid, String Message)
    """
    if not varna_obj.is_vowel:
        msg = f"१.२.२८ अचश्च: '{varna_obj.char}' is a Consonant. {action_name} blocked."
        # We assume the caller might want to log this blockage in the trace
        return False, msg
    return True, "Valid"


def apply_1_2_27_ukalo(varna_obj):
    """
    [SUTRA]: ऊकालोऽज्झ्रस्वदीर्घप्लुतः (१.२.२७)
    [VRITTI]: वां-काल इव कालो यस्य सोऽच् क्रमात् ह्रस्वदीर्घप्लुतसंज्ञः स्यात्।
    [LOGIC]: Assigns 'Hrasva' (1), 'Dirgha' (2), or 'Pluta' (3) labels.
    """
    # 1. The Gatekeeper (1.2.28)
    is_valid, msg = apply_1_2_28_acashca(varna_obj, "१.२.२७ ऊकालो...")
    if not is_valid:
        # If it's a consonant, we define duration as 0.5 (Ardha-matra) per tradition
        varna_obj.matra = 0.5
        varna_obj.trace.append(msg)
        return varna_obj

    # 2. Determine Duration (Physiological Assessment)
    char = varna_obj.char

    # Check for Pluta mark (Explicit 3)
    if '३' in char:
        varna_obj.matra = 3
        varna_obj.sanjnas.add("प्लुत")
        varna_obj.kala_sanjna = "प्लुत"
        varna_obj.trace.append("१.२.२७: Pluta assigned (3 Matras)")

    # Check for Long (Dirgha)
    elif char in DIRGHA_SET or any(x in char for x in DIRGHA_SET):
        varna_obj.matra = 2
        varna_obj.sanjnas.add("दीर्घ")
        varna_obj.kala_sanjna = "दीर्घ"
        varna_obj.trace.append("१.२.२७: Dirgha assigned (2 Matras)")

    # Default to Short (Hrasva)
    else:
        varna_obj.matra = 1
        varna_obj.sanjnas.add("ह्रस्व")
        varna_obj.kala_sanjna = "ह्रस्व"
        varna_obj.trace.append("१.२.२७: Hrasva assigned (1 Matra)")

    return varna_obj


def get_savarna_variants_18_bheda(varna_obj):
    """
    Generates the 18 varieties (Bhedas) for a vowel.
    Used for 1.1.69 (Savarna-grahana) expansion.
    """
    if not varna_obj.is_vowel:
        return []

    # Identify the base sound (removing Pluta/Nasal markers for classification)
    raw_char = varna_obj.char[0]

    # --- Dimensions ---
    kalas = ["ह्रस्व", "दीर्घ", "प्लुत"]
    svaras = ["उदात्त", "अनुदात्त", "स्वरित"]
    nasals = ["अनुनासिक", "निरनुनासिक"]

    # --- Constraints ---
    # 1. ऌकारस्य दीर्घाभावात् (Lri has no Dirgha) -> 12 Bhedas
    if raw_char in ['ऌ', 'ॢ', 'ॡ']:
        kalas = ["ह्रस्व", "प्लुत"]

    # 2. एचां ह्रस्वाभावात् (Diphthongs have no Hrasva) -> 12 Bhedas
    elif raw_char in ['ए', 'ऐ', 'ओ', 'औ', 'े', 'ै', 'ो', 'ौ']:
        kalas = ["दीर्घ", "प्लुत"]

    # --- Matrix Generation ---
    matrix = []
    for k in kalas:
        for s in svaras:
            for n in nasals:
                matrix.append(f"{raw_char} ({k}-{s}-{n})")

    return matrix