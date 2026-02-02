"""
FILE: logic/dhatu_processor.py - PAS-v15.0 (Upadhā Dīrgha 8.2.78)
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga

class DhatuDiagnostic:
    def __init__(self, raw_upadesha, is_subdhatu=False):
        self.raw = raw_upadesha
        self.is_subdhatu = is_subdhatu
        self.varnas = ad(raw_upadesha)

        self.originally_halanta = False
        if self.varnas and self.varnas[-1].is_consonant:
            self.originally_halanta = True

        self.it_tags = set()
        self.history = []
        self.pada = "Unknown"

        self.process()
        self.pada = self.determine_pada()

    def log(self, rule, desc):
        self.history.append(f"{rule}: {desc}")

    def process(self):
        # 1. Clean Upadesha
        ir_it_processed = self._apply_ir_it_vartika()
        self._apply_1_3_5_adir_nit_tu_du()
        self._apply_1_3_2_upadeshe_aj_it()

        text = sanskrit_varna_samyoga(self.varnas)
        is_vartika_exception = any(text.startswith(x) for x in ["ष्वष्क्", "ष्ठिव्"])

        if self.originally_halanta and not ir_it_processed and not is_vartika_exception:
            self._apply_1_3_3_halantyam()

        # 2. Root Phonology
        self._apply_6_1_64_shatva_vidhi()
        self._apply_6_1_65_natva_vidhi()

        # 3. Augmentation
        self._apply_7_1_58_num_agama()
        self._apply_internal_sandhi()

        # 4. Anga/Stem Operations (Tripadi 8.2.78)
        self._apply_8_2_78_upadhayam_ca()

    def _apply_8_2_78_upadhayam_ca(self):
        """
        8.2.78 Upadhāyāṁ ca:
        If Upadhā (penultimate) is 'r' or 'v', followed by a Hal (final consonant),
        then the preceding Ik vowel becomes Dīrgha.
        Structure: [Ik] + [r/v] + [Hal] -> [Dīrgha] + [r/v] + [Hal]
        """
        if len(self.varnas) < 3: return

        # Indices
        last = self.varnas[-1]
        upadha = self.varnas[-2]
        pre_upadha = self.varnas[-3]

        # Condition 1: Final is Hal (Consonant)
        if not last.is_consonant: return

        # Condition 2: Upadhā is Repha ('r') or Vakara ('v')
        if upadha.char not in ['र्', 'व्']: return

        # Condition 3: Pre-Upadhā is Ik (i, u, ṛ, ḷ) - Short
        ik_map = {'इ': 'ई', 'उ': 'ऊ', 'ऋ': 'ॠ', 'ऌ': 'ॡ'}
        # Handle matras too (basic normalization assumed in ad(), but checking char base)

        current_vowel = pre_upadha.char
        if current_vowel in ik_map:
            # Apply Lengthening
            long_vowel = ik_map[current_vowel]
            pre_upadha.char = long_vowel
            self.log("8.2.78", f"Upadhā Dīrgha: {current_vowel} -> {long_vowel} (before {upadha.char}{last.char})")

    # --- Standard Helpers (Unchanged) ---
    def determine_pada(self):
        raw_tags = [t.split('-')[0] for t in self.it_tags]
        if any(x in raw_tags for x in ['ङ', 'ङि', 'अँ']): return "Ātmanepada (1.3.12)"
        if any(x in raw_tags for x in ['ञ', 'ञि']): return "Ubhayapada (1.3.72)"
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
                tag = "Aj-It" 
                if any(x in v.char for x in ['इ', 'ि']): tag = "इँ-It"
                elif any(x in v.char for x in ['ई', 'ी']): tag = "ईँ-It"
                elif any(x in v.char for x in ['उ', 'ु']): tag = "उँ-It"
                else: tag = "अँ-It"
                self.it_tags.add(f"{tag} (1.3.2)")
                to_remove.append(v)
                self.log("1.3.2", f"Removed nasal {v.char}")
        for v in to_remove: self.varnas.remove(v)

    def _apply_1_3_3_halantyam(self):
        if self.varnas and self.varnas[-1].is_consonant:
            last = self.varnas[-1].char
            self.it_tags.add(f"{last}-It (1.3.3)")
            self.varnas.pop()
            self.log("1.3.3", f"Removed final {last}")

    def _apply_6_1_64_shatva_vidhi(self):
        if not self.varnas: return
        text = sanskrit_varna_samyoga(self.varnas)
        if self.is_subdhatu: return
        exceptions = ["ष्ठिव्", "ष्वष्क्", "ष्ठिवु"]
        if any(text.startswith(ex) for ex in exceptions): return
        if self.varnas[0].char.startswith('ष्'):
            self.varnas[0].char = self.varnas[0].char.replace('ष्', 'स्')
            self.log("6.1.64", "Changed initial ṣ -> s")
            for i in range(1, min(len(self.varnas), 3)):
                char = self.varnas[i].char
                if 'ट' in char: self.varnas[i].char = char.replace('ट', 'त')
                elif 'ठ' in char: self.varnas[i].char = char.replace('ठ', 'थ')
                elif 'ण' in char: self.varnas[i].char = char.replace('ण', 'न')

    def _apply_6_1_65_natva_vidhi(self):
        if self.varnas and self.varnas[0].char.startswith('ण्'):
            self.varnas[0].char = self.varnas[0].char.replace('ण्', 'न्')
            self.log("6.1.65", "Changed initial ṇ -> n")

    def _apply_7_1_58_num_agama(self):
        if "ir-It (Vartika)" in self.it_tags: return
        if any("इँ-It" in t for t in self.it_tags):
            v_indices = [i for i, v in enumerate(self.varnas) if v.is_vowel]
            if v_indices:
                idx = v_indices[-1] + 1
                self.varnas.insert(idx, Varna("न्"))
                self.log("7.1.58", "Added Num (n)")

    def _apply_internal_sandhi(self):
        for i in range(len(self.varnas) - 1):
            curr = self.varnas[i].char
            if curr != 'न्': continue
            nxt = self.varnas[i+1].char
            if any(k in nxt for k in ['क', 'ख', 'ग', 'घ']): self.varnas[i].char = 'ङ्'
            elif any(c in nxt for c in ['च', 'छ', 'ज', 'झ']): self.varnas[i].char = 'ञ्'
            elif any(t in nxt for t in ['ट', 'ठ', 'ड', 'ढ']): self.varnas[i].char = 'ण्'
            elif any(p in nxt for p in ['प', 'फ', 'ब', 'भ']): self.varnas[i].char = 'म्'
            elif any(s in nxt for s in ['श', 'ष', 'स', 'ह']): self.varnas[i].char = 'ं'

    def get_final_root(self):
        return sanskrit_varna_samyoga(self.varnas)
