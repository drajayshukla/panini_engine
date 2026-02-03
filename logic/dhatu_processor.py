"""
FILE: logic/dhatu_processor.py - Restored Feature
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga

class DhatuDiagnostic:
    def __init__(self, raw_upadesha, is_subdhatu=False):
        self.raw = raw_upadesha
        self.is_subdhatu = is_subdhatu
        self.varnas = ad(raw_upadesha)
        self.it_tags = set()
        self.history = []
        self.pada = "Unknown"
        self.process()
        self.pada = self.determine_pada()

    def log(self, rule, desc):
        self.history.append(f"{rule}: {desc}")

    def process(self):
        # 1.3.3 Halantyam
        if self.varnas and self.varnas[-1].is_consonant:
            last = self.varnas[-1].char
            self.it_tags.add(f"{last}-It")
            self.varnas.pop()
            self.log("1.3.3", f"Removed final {last}")
        
        # 6.1.64 Shatva
        if self.varnas and self.varnas[0].char.startswith('ष्'):
            self.varnas[0].char = 'स्'
            self.log("6.1.64", "Initial ṣ -> s")
            
        # 6.1.65 Natva
        if self.varnas and self.varnas[0].char.startswith('ण्'):
            self.varnas[0].char = 'न्'
            self.log("6.1.65", "Initial ṇ -> n")

    def determine_pada(self):
        return "Parasmaipada (Default)"

    def get_final_root(self):
        return sanskrit_varna_samyoga(self.varnas)
