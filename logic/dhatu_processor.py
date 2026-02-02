"""
FILE: logic/dhatu_processor.py - PAS-v8.1
TASK 2: Validation of Dhātu Upadeśa → Dhātu-in-Action
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga
from core.dhatu_repo import DhatuRepository

class DhatuDiagnostic:
    def __init__(self, raw_upadesha):
        self.raw = raw_upadesha
        # Convert raw text to Varna Objects for processing
        self.varnas = ad(raw_upadesha)
        self.it_tags = set()
        self.history = []

        # Start Diagnostic Flow
        self.run_diagnostic()

    def log(self, rule, desc):
        self.history.append(f"{rule}: {desc}")

    def run_diagnostic(self):
        # PHASE 2: It-Kārya Factory
        self._apply_1_3_2_upadeshe_aj_it()
        self._apply_1_3_3_halantyam()
        self._apply_1_3_5_adir_nit_tu_du()
        self._apply_ir_it_vartika()

        # PHASE 3: Standardization
        self._apply_6_1_64_shatva_vidhi()
        self._apply_6_1_65_natva_vidhi()

    def _apply_1_3_2_upadeshe_aj_it(self):
        """1.3.2: उपदेशेऽजनुनासिक इत् - Nasalized vowels are It."""
        for v in list(self.varnas):
            if v.is_anunasika:
                self.it_tags.add("Anunāsika-It (1.3.2)")
                self.log("1.3.2", f"Removed nasalized vowel {v.char}")
                self.varnas.remove(v)

    def _apply_1_3_3_halantyam(self):
        """1.3.3: हलन्त्यम् - Final consonant is It."""
        if self.varnas and self.varnas[-1].is_consonant:
            # Note: 1.3.4 (Na Vibhaktau Tusmah) only applies to Vibhakti, not Dhatu
            last_char = self.varnas[-1].char
            self.it_tags.add(f"{last_char}-It (1.3.3)")
            self.log("1.3.3", f"Removed final consonant {last_char}")
            self.varnas.pop()

    def _apply_1_3_5_adir_nit_tu_du(self):
        """1.3.5: आदिर्ञिटुडवः - Initial ñi, ṭu, ḍu are It."""
        if len(self.varnas) >= 2:
            prefix = self.varnas[0].char + self.varnas[1].char.replace('्', '')
            if prefix in ['ञि', 'टु', 'डु']:
                self.it_tags.add(f"{prefix}-It (1.3.5)")
                self.log("1.3.5", f"Removed initial {prefix}")
                self.varnas = self.varnas[2:]

    def _apply_ir_it_vartika(self):
        """Vartika: इँर इत्संज्ञा वाच्या - ir is It at the end."""
        text = sanskrit_varna_samyoga(self.varnas)
        if text.endswith('इर्'):
            self.it_tags.add("ir-It (Vartika)")
            self.log("Vartika", "Removed final ir")
            self.varnas = self.varnas[:-2]

    def _apply_6_1_64_shatva_vidhi(self):
        """6.1.64: धात्वादेः षः सः - Initial ṣ -> s."""
        if self.varnas and self.varnas[0].char.startswith('ष्'):
            # Exception: sthivu, svashka (R8: Baliyah)
            current_text = sanskrit_varna_samyoga(self.varnas)
            if current_text not in ['ष्ठिवु', 'ष्वष्क']:
                self.varnas[0].char = 'स्'
                self.log("6.1.64", "Changed initial ṣ to s")

    def _apply_6_1_65_natva_vidhi(self):
        """6.1.65: णो नः - Initial ṇ -> n."""
        if self.varnas and self.varnas[0].char.startswith('ण्'):
            self.varnas[0].char = 'न्'
            self.log("6.1.65", "Changed initial ṇ to n")

    def get_final_root(self):
        return sanskrit_varna_samyoga(self.varnas)