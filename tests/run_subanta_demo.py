import sys
import os

# 1. PATH SETUP
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.phonology import ad, sanskrit_varna_samyoga
from core.prakriya_logger import PrakriyaLogger
from core.upadesha_registry import UpadeshaType
from logic.it_engine import ItEngine
from logic.vidhi.vidhi_engine import VidhiEngine


def run_final_audit():
    print(f"\n{'=' * 60}\n{'TEST: Mati + Jas (1.3 Plural) - 7.3.109':^60}\n{'=' * 60}")

    logger = PrakriyaLogger()
    anga = ad("मति")
    suffix_raw = ad("जस्")

    # 1. IT-LOPA: Physically remove 'j' to get 'as'
    # ItEngine.run_it_prakaran must return the list WITHOUT 'j'
    clean_suf, _ = ItEngine.run_it_prakaran(suffix_raw, UpadeshaType.VIBHAKTI)

    # LOG: Use clean_suf here so 'j' disappears from the student's view
    logger.add_step(anga + clean_suf, "1.3.7", "जकारस्य इत्संज्ञा, लोपः च। (Jas -> As)")

    # 2. GUNA: Mati + as -> Mate + as
    # Ensure VidhiEngine receives the cleaned suffix 'as'
    res_anga, rule_guna = VidhiEngine.apply_jasi_ca_7_3_109(anga, clean_suf)
    logger.add_step(res_anga + clean_suf, rule_guna)

    # 3. AYADI SANDHI: Mate + as -> Matay + as
    # Now that 'j' is gone, the engine sees 'e' + 'a' (vowel) and will trigger 6.1.78
    res_anga, rule_ayadi = VidhiEngine.apply_ayadi_6_1_78(res_anga, clean_suf)
    logger.add_step(res_anga + clean_suf, rule_ayadi)

    # 4. TRIPADI: Final Synthesis
    full = res_anga + clean_suf

    # Rutva (s -> r)
    full, _ = VidhiEngine.apply_rutva_8_2_66(full)

    # IMPORTANT: Re-run cleaning or remove 'u' from 'ru' to leave 'r'
    full, _ = ItEngine.run_it_prakaran(full, UpadeshaType.VIBHAKTI)

    # Visarga (r -> h)
    full, _ = VidhiEngine.apply_visarga_8_3_15(full)
    logger.add_step(full, "8.3.15", "अवसाने विसर्गः।")

    logger.render_educational()

    # 5. VALIDATION
    final_str = sanskrit_varna_samyoga(full)
    print(f"✅ FINAL RESULT: {final_str}")
    assert final_str == "मतयः", f"Expected मतयः, got {final_str}"

if __name__ == "__main__":
    # You must explicitly call the function here!
    run_final_audit()