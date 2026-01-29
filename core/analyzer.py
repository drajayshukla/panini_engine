"""
FILE: core/analyzer.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Diagnostic Varṇodaya
REFERENCE: Brahmadutt Jigyasu, Prathamavritti Vol 1
"""

from logic import sanjna_rules

def analyze_sanjna(varna_list):
    """
    [PAS-5.0] अष्टाध्यायी-संज्ञा-विश्लेषणम्।
    Provides a comprehensive diagnostic report of all technical labels
    assigned to a varna sequence.
    """
    # Step 1: Execute all "Naming" rules to populate varna.sanjnas
    # This ensures we follow the sequence of the Ashtadhyayi
    varna_list = sanjna_rules.apply_1_1_1_vriddhi(varna_list)[0]
    varna_list = sanjna_rules.apply_1_1_2_guna(varna_list)[0]
    varna_list = sanjna_rules.apply_1_1_7_samyoga(varna_list)[0]
    varna_list = sanjna_rules.apply_1_1_8_anunasika(varna_list)[0]

    analysis_report = []

    for v in varna_list:
        # Step 2: Extract the "Clinical History" from each varna
        report_entry = {
            "varna": v.char,
            "tags": list(v.sanjnas), # Converts set to list for UI
            "sthana": getattr(v, 'sthana', 'अज्ञात'),
            "trace": v.trace, # Crucial for PAS-5 auditability
            "is_vowel": v.is_vowel
        }
        analysis_report.append(report_entry)

    return analysis_report