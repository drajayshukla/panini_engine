"""
FILE: logic/svara_rules.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Svara-Saṃjñā (Accentuation/Pitch)
REFERENCE: १.२.२९ to १.२.३१
"""

# --- MARKER REGISTRY ---
# Standard Vedic Unicode and common keyboard fallbacks
ANUDATTA_MARKS = {'॒', '_', '\u0331', '̱'}  # U+0952, Low Line, Comb Low Line
SVARITA_MARKS = {'॑', "'", '^', '\u030d', '̀'}  # U+0951, Apostrophe, Caret, Comb Vert


def apply_svara_sanjna(varna_obj, raw_string):
    """
    [LOGIC]: Parses input string markers to assign Pāṇinian Pitch.
    Executed inside Varna.__init__ to ensure DNA is complete at birth.
    """

    # 1. THE GATEKEEPER: १.२.२८ अचश्च
    # Pitch resides only in Vowels (Ac). Consonants carry the pitch of the vowel.
    if not varna_obj.is_vowel:
        varna_obj.svara = None
        varna_obj.svara_mark = None
        return varna_obj

    # 2. ANUDĀTTA CHECK (१.२.३० नीचैरनुदात्तः)
    # Low Pitch: Usually marked with a line below.
    if any(mark in raw_string for mark in ANUDATTA_MARKS):
        varna_obj.svara = "अनुदात्त"
        varna_obj.svara_mark = "॒"  # Standardize to Devanagari mark
        varna_obj.trace.append("१.२.३० नीचैरनुदात्तः")

    # 3. SVARITA CHECK (१.२.३१ समाहारः स्वरितः)
    # Mixed/Falling Pitch: Usually marked with a vertical line above.
    elif any(mark in raw_string for mark in SVARITA_MARKS):
        varna_obj.svara = "स्वरित"
        varna_obj.svara_mark = "॑"  # Standardize to Devanagari mark
        varna_obj.trace.append("१.२.३१ समाहारः स्वरितः")

    # 4. UDĀTTA DEFAULT (१.२.२९ उच्चैरुदात्तः)
    # High Pitch: In Pāṇinian notation, the Udātta is UNMARKED.
    # Logic: If it's a vowel and has no other mark, it is Udātta.
    else:
        varna_obj.svara = "उदात्त"
        varna_obj.svara_mark = None
        varna_obj.trace.append("१.२.२९ उच्चैरुदात्तः (Unmarked)")

    return varna_obj