from core.core_foundation import Varna, ad, sanskrit_varna_samyoga
class DhatuDiagnostic:
    def __init__(self, raw_upadesha, is_subdhatu=False):
        self.raw = raw_upadesha
        self.varnas = ad(raw_upadesha)
        self.history = []
        self.it_tags = set()
        self.process()
        self.pada = "Parasmaipada (Default)"
    def log(self, rule, desc): self.history.append(f"{rule}: {desc}")
    def process(self):
        if self.varnas and self.varnas[-1].is_consonant:
            last = self.varnas[-1].char
            self.it_tags.add(f"{last}-It")
            self.varnas.pop()
            self.log("1.3.3", f"Halantyam: Removed final {last}")
        if self.varnas and self.varnas[0].char.startswith('ष्'):
            self.varnas[0].char = 'स्'
            self.log("6.1.64", "Initial ṣ -> s")
        if self.varnas and self.varnas[0].char.startswith('ण्'):
            self.varnas[0].char = 'न्'
            self.log("6.1.65", "Initial ṇ -> n")
    def get_final_root(self): return sanskrit_varna_samyoga(self.varnas)
