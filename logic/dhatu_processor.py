"""
FILE: logic/dhatu_processor.py - PAS-v9.2
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga

class DhatuDiagnostic:
    def __init__(self, raw_upadesha):
        self.raw = raw_upadesha
        self.varnas = ad(raw_upadesha)
        self.it_tags = set()
        self.history = []
        self.process()

    def log(self, rule, desc):
        self.history.append(f"{rule}: {desc}")

    def process(self):
        # 1. Vartika: ir-it (Aggressive Check)
        # Check raw string ending because tokenization might split modifiers
        if self.raw.endswith("इर्") or self.raw.endswith("इँर्"):
            self.it_tags.add("ir-It (Vartika)")
            # Remove the last Varna (r) and the one before it (i~)
            # We assume ad() tokenized correctly as [... 'i~', 'r']
            if len(self.varnas) >= 2:
                self.varnas = self.varnas[:-2]
                self.log("Vartika", "Removed final 'ir'")

        # 2. 1.3.5: Initial ñi, tu, du
        if len(self.varnas) >= 2:
            c1 = self.varnas[0].char.replace('्', '')
            c2 = self.varnas[1].char
            if c1 in ['ञ', 'ट', 'ड'] and any(v in c2 for v in ['इ', 'उ', 'ि', 'ु']):
                 marker = c1 + c2
                 self.it_tags.add(f"{marker}-It (1.3.5)")
                 self.varnas = self.varnas[2:]
                 self.log("1.3.5", f"Removed initial {marker}")

        # 3. 1.3.3: Final Consonant
        if self.varnas and self.varnas[-1].is_consonant:
            last = self.varnas[-1].char
            self.it_tags.add(f"{last}-It (1.3.3)")
            self.varnas.pop()
            self.log("1.3.3", f"Removed final {last}")

        # 4. 1.3.2: Nasal Vowels
        to_remove = []
        for v in self.varnas:
            if v.is_anunasika:
                # If we have ir-It tag, ensure we don't double count if something remains
                # But typically ir-It removal handles it.
                tag = "इँ-It" if any(x in v.char for x in 'इिईी') else "अँ-It"
                self.it_tags.add(f"{tag} (1.3.2)")
                to_remove.append(v)
                self.log("1.3.2", f"Removed nasal {v.char}")

        for v in to_remove:
            self.varnas.remove(v)

        # 5. Phonology
        text = sanskrit_varna_samyoga(self.varnas)
        if text.startswith('ष्') and not any(text.startswith(x) for x in ['ष्ठिव्', 'ष्वष्क्']):
            self.varnas[0].char = 'स्'
        if self.varnas and self.varnas[0].char.startswith('ण्'):
            self.varnas[0].char = 'न्'

        # 6. 7.1.58: Num-agama
        # CRITICAL: Do NOT fire if 'ir-It' is present (it overrides Idit)
        if any("इँ-It" in t for t in self.it_tags) and "ir-It (Vartika)" not in self.it_tags:
            v_indices = [i for i, v in enumerate(self.varnas) if v.is_vowel]
            if v_indices:
                idx = v_indices[-1] + 1
                self.varnas.insert(idx, Varna("न्"))
                self.log("7.1.58", "Added Num (n)")

    def get_final_root(self):
        return sanskrit_varna_samyoga(self.varnas)
