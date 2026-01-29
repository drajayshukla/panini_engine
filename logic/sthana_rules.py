"""
FILE: logic/sthana_rules.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Śikṣā (Phonetics)
REFERENCE: पाणिनीय शिक्षा (स्थान-प्रकरण)
"""

# The Master Map (Single Source of Truth)
STHANA_MAP = {
    "कण्ठ": ['अ', 'आ', 'क', 'ख', 'ग', 'घ', 'ङ', 'ह', 'ः'],
    "तालु": ['इ', 'ई', 'च', 'छ', 'ज', 'झ', 'ञ', 'य', 'श'],
    "मूर्धा": ['ऋ', 'ॠ', 'ट', 'ठ', 'ड', 'ढ', 'ण', 'र', 'ष'],
    "दन्त": ['ऌ', 'त', 'थ', 'द', 'ध', 'न', 'ल', 'स'],
    "ओष्ठ": ['उ', 'ऊ', 'प', 'फ', 'ब', 'भ', 'म'],
    "नासिका": ['ङ', 'ञ', 'ण', 'न', 'म', 'ं', 'ँ'],  # Added 'ँ' (Chandrabindu)
    "कण्ठतालु": ['ए', 'ऐ'],
    "कण्ठोष्ठ": ['ओ', 'औ'],
    "दन्तोष्ठ": ['व']
}


def apply_sthana_to_varna(varna_obj):
    """
    [LOGIC]: Maps the 'Biological Address' to the Varna object.
    Updates varna_obj.sthana as a LIST (essential for 1.1.9 Savarna logic).
    """
    if not hasattr(varna_obj, 'char') or not varna_obj.char:
        varna_obj.sthana = []
        return varna_obj

    # Normalize char (Handle 'क्' -> 'क')
    # We strip Halant or Matras to find the root articulation point
    base_char = varna_obj.char[0]

    found_sthanas = []

    # 1. Standard Mapping
    for sthana, chars in STHANA_MAP.items():
        if base_char in chars:
            found_sthanas.append(sthana)

    # 2. Ayogavaha Handling (Special Rules)
    # Jihvamuliya / Upadhmaniya could be added here if needed.

    # 3. Anunasika (Nasal) Override for Chandra-bindu
    if varna_obj.is_anunasika and "नासिका" not in found_sthanas:
        found_sthanas.append("नासिका")

    # Update the object with a List (PAS-5 Standard)
    # 'Kanth' + 'Nasika' for 'Ng' is maintained as ['कण्ठ', 'नासिका']
    varna_obj.sthana = found_sthanas

    # Optional: Human-readable string for UI display (trace)
    if found_sthanas:
        varna_obj.trace.append(f"स्थान: {'+'.join(found_sthanas)}")

    return varna_obj