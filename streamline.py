"""
REVISED logic/dhatu_processor.py
Focus: Correcting 1.3.5 (Adir-nyitudavah) and 1.3.3 (Halantyam)
"""


def run_diagnostic(self):
    # 1.3.5 (आदिर्ञिटुडवः) MUST run before other vowel checks
    self._apply_1_3_5_adir_nit_tu_du()

    # 1.3.2 (उपदेशेऽजनुनासिक इत्)
    self._apply_1_3_2_upadeshe_aj_it()

    # 1.3.3 (हलन्त्यम्)
    self._apply_1_3_3_halantyam()

    # Vartika: इँर इत्संज्ञा वाच्या
    self._apply_ir_it_vartika()

    # Phase 3 & 4 (Standardization & Augmentation)
    self._apply_6_1_64_shatva_vidhi()
    self._apply_6_1_65_natva_vidhi()


def _apply_1_3_5_adir_nit_tu_du(self):
    """
    1.3.5: आदिर्ञिटुडवः - Initial Ñi, Ṭu, Ḍu are It.
    Example: Ḍu-kṛ-ñ -> kṛ-ñ
    """
    if len(self.varnas) < 2: return

    # Get the first two varnas to check for combinations like 'ḍ' + 'u'
    v1 = self.varnas[0].char  # e.g., 'ड्'
    v2 = self.varnas[1].char  # e.g., 'उ'

    combined_prefix = v1.replace('्', '') + v2.replace('्', '')  # Normalizes to 'डु'

    target_prefixes = ['ञि', 'टु', 'डु']

    if combined_prefix in target_prefixes:
        self.it_tags.add(f"{combined_prefix}-It (1.3.5)")
        self.log("1.3.5", f"Removed initial {combined_prefix}")
        self.varnas = self.varnas[2:]  # Strip the first two varnas