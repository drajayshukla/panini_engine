"""
FILE: logic/tinanta_processor.py - Restored Feature
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga
from logic.dhatu_processor import DhatuDiagnostic

class TinantaDiagnostic:
    def __init__(self, upadesha, lakara="Lat", purusha=1, vacana=1):
        self.raw_root = upadesha
        self.history = []
        
        # Root Process
        d = DhatuDiagnostic(upadesha)
        self.root = d.get_final_root()
        self.pada_type = d.pada
        self.history.extend(d.history)
        
        # Conjugation (Basic Lat)
        self.suffix = "ति" # Default Tip
        self.history.append("3.4.78: Selected Tip (ti)")
        
        # Vikarana (Sap)
        self.root = self.root + "अ"
        self.history.append("3.1.68: Added Vikarana Sap (a)")
        
        self.final_form = self.root + self.suffix
