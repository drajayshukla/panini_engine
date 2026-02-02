"""
FILE: logic/dhatu_processor.py - PAS-v10.2 (Stabilized)
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga

class DhatuDiagnostic:
    def __init__(self, raw_upadesha):
        self.raw = raw_upadesha
        self.varnas = ad(raw_upadesha)

        # Snapshot for 1.3.3 context
        self.originally_halanta = False
        if self.varnas and self.varnas[-1].is_consonant:
            self.originally_halanta = True

        self.it_tags = set()
        self.history = []
        self.pada = "Unknown" # Default initialization

        self.process()
        self.pada = self.determine_pada()

    def log(self, rule, desc):
        self.history.append(f"{rule}: {desc}")

    def process(self):
        ir_it_processed = self._apply_ir_it_vartika()
        self._apply_1_3_5_adir_nit_tu_du()
        self._apply_1_3_2_upadeshe_aj_it()

        if self.originally_halanta and not ir_it_processed:
            self._apply_1_3_3_halantyam()

        self._apply_6_1_64_shatva_vidhi()
        self._apply_6_1_65_natva_vidhi()
        self._apply_7_1_58_num_agama()

    def determine_pada(self):
        raw_tags = [t.split('-')[0] for t in self.it_tags]
        # Check for specific tags
        if any(x in raw_tags for x in ['ङ', 'ङि', 'अँ']): 
             return "Ātmanepada (1.3.12)"
        if any(x in raw_tags for x in ['ञ', 'ञि']):
             return "Ubhayapada (1.3.72)"
        return "Parasmaipada (1.3.78)"

    def _apply_ir_it_vartika(self):
        if len(self.varnas) >= 2:
            last = self.varnas[-1]
            penult = self.varnas[-2]
            if last.char == 'र्' and any(x in penult.char for x in ['इ', 'ि', 'ई', 'ी']):
                self.it_tags.add("ir-It (Vartika)")
                self.varnas = self.varnas[:-2]
                self.log("Vartika", "Removed final 'ir' bundle")
                return True
        return False

    def _apply_1_3_5_adir_nit_tu_du(self):
        if len(self.varnas) >= 2:
            c1 = self.varnas[0].char.replace('्', '')
            c2 = self.varnas[1].char

            # Normalization Map for Tags
            marker = None
            if c1 == 'ञ' and any(v in c2 for v in ['इ', 'ि']): marker = "ञि"
            elif c1 == 'ट' and any(v in c2 for v in ['उ', 'ु']): marker = "टु"
            elif c1 == 'ड' and any(v in c2 for v in ['उ', 'ु']): marker = "डु"

            if marker:
                 self.it_tags.add(f"{marker}-It (1.3.5)")
                 self.varnas = self.varnas[2:]
                 self.log("1.3.5", f"Removed initial {marker}")

    def _apply_1_3_2_upadeshe_aj_it(self):
        to_remove = []
        for v in self.varnas:
            if v.is_anunasika:
                tag = "इँ-It" if any(x in v.char for x in 'इिईी') else "अँ-It"
                self.it_tags.add(f"{tag} (1.3.2)")
                to_remove.append(v)
                self.log("1.3.2", f"Removed nasal {v.char}")
        for v in to_remove:
            self.varnas.remove(v)

    def _apply_1_3_3_halantyam(self):
        if self.varnas and self.varnas[-1].is_consonant:
            last = self.varnas[-1].char
            self.it_tags.add(f"{last}-It (1.3.3)")
            self.varnas.pop()
            self.log("1.3.3", f"Removed final {last}")

    def _apply_7_1_58_num_agama(self):
        if "ir-It (Vartika)" in self.it_tags: return
        if any("इँ-It" in t for t in self.it_tags):
            v_indices = [i for i, v in enumerate(self.varnas) if v.is_vowel]
            if v_indices:
                idx = v_indices[-1] + 1
                self.varnas.insert(idx, Varna("न्"))
                self.log("7.1.58", "Added Num (n)")

    def _apply_6_1_64_shatva_vidhi(self):
        if not self.varnas: return
        text = sanskrit_varna_samyoga(self.varnas)
        if text.startswith('ष्') and not any(text.startswith(x) for x in ['ष्ठिव्', 'ष्वष्क्']):
            self.varnas[0].char = 'स्'
            self.log("6.1.64", "ṣ -> s")

    def _apply_6_1_65_natva_vidhi(self):
        if self.varnas and self.varnas[0].char.startswith('ण्'):
            self.varnas[0].char = 'न्'
            self.log("6.1.65", "ṇ -> n")

    def get_final_root(self):
        return sanskrit_varna_samyoga(self.varnas)
