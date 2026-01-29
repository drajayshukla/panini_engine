"""
FILE: derive_nayi.py
TOPIC: नी + णिच् -> नायि (Step-by-Step Derivation)
"""

from core.phonology import ad, sanskrit_varna_samyoga
from logic.it_engine import ItEngine
from logic.vidhi_engine import VidhiEngine
from core.upadesha_registry import UpadeshaType


def derive_nayi():
    print("\n🔬 PANINIAN DERIVATION: Nī + Ṇic -> Nāyi\n")

    # --- STEP 1: IT-SANJNA (Cleaning) ---
    # Sutras: 1.3.3 (Halantyam), 1.3.7 (Chutu), 1.3.9 (Tasya Lopah)
    root_str = "नी"
    suffix_str = "णिच्"

    anga = ad(root_str)
    suffix_raw = ad(suffix_str)

    print(f"1. Input: {root_str} + {suffix_str}")

    # Apply Cleaning
    clean_suffix, _ = ItEngine.run_it_prakaran(suffix_raw, UpadeshaType.PRATYAYA)

    # [CRITICAL]: Manually tag the suffix as Ṇit because 1.3.7 removed 'Ñ/Ṇ'
    # In a full flow, ItEngine does this. We force it here for the test logic.
    if clean_suffix:
        clean_suffix[0].sanjnas.add("ṇit")

    print(f"   → {root_str} + {sanskrit_varna_samyoga(clean_suffix)} [इत्संज्ञालोपः]")

    # --- STEP 2: VRIDDHI (7.2.115) ---
    # Sutra: अचो ञ्णिति (7.2.115)
    anga, s_72115 = VidhiEngine.apply_vṛddhi_7_2_115(anga, clean_suffix)

    step2_form = sanskrit_varna_samyoga(anga)
    print(f"   → {step2_form} + {sanskrit_varna_samyoga(clean_suffix)} [{s_72115} इत्यनेन ईकारस्य वृद्धिः ऐकारः]")

    # --- STEP 3: AYADI SANDHI (6.1.78) ---
    # Sutra: एचोऽयवायावः (6.1.78)
    anga, s_6178 = VidhiEngine.apply_ayadi_6_1_78(anga, clean_suffix)

    step3_form = sanskrit_varna_samyoga(anga)
    print(f"   → {step3_form} + {sanskrit_varna_samyoga(clean_suffix)} [{s_6178} इति आयादेशः]")

    # --- STEP 4: SYNTHESIS (3.1.32) ---
    # Sutra: सनाद्यन्ता धातवः (3.1.32)
    final_varnas = anga + clean_suffix
    final_result = sanskrit_varna_samyoga(final_varnas)

    print(f"   → {final_result} [सनाद्यन्ता धातवः ३.१.३२ इति धातुसंज्ञा]")


if __name__ == "__main__":
    derive_nayi()