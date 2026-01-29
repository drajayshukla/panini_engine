"""
FILE: logic/pratyaya_types.py
PAS-v2.0: 5.0 (Siddha)
REFERENCE: ३.१.१ प्रत्ययः (Adhikara Sutra)
SOURCE: User Input (Sanskrit Commentary)
"""

class PratyayaCategory:
    """
    The 7-fold Classification of Pratyayas (3.1.1 onwards).
    Based on the range (Avadhi) defined in the Ashtadhyayi.
    """
    # 1. Sanadi (3.1.5 - 3.1.31)
    # गुप्तिज्किद्भ्यः सन् ... आयादय आर्धधातुके वा
    SANADI = "sanadi"

    # 2. Vikarana (3.1.33 - 3.1.86)
    # स्यतासी लृलुटोः ... लिङ्याशिष्यङ्
    VIKARANA = "vikarana"

    # 3. Ting (3.4.78)
    # तिप्तस्झिसिप्... (Verbal Endings)
    TING = "ting"

    # 4. Krt (3.1.91 - 3.4.117)
    # धातोः (Root Suffixes, excluding Ting)
    KRT = "krt"

    # 5. Sup (4.1.2)
    # स्वौजस्... (Nominal Case Endings)
    SUP = "sup"

    # 6. Stri (4.1.4 - 4.1.81)
    # अजाद्यतष्टाप् ... (Feminine Suffixes)
    STRI = "stri"

    # 7. Taddhita (4.1.76 onwards)
    # तद्धिताः (Secondary Derivatives)
    TADDHITA = "taddhita"