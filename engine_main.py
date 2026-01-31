"""
FILE: engine_main.py
PAS-v6.0 (Siddha) | PILLAR: Orchestrator
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logic.subanta_processor import SubantaProcessor
from core.core_foundation import sanskrit_varna_samyoga

class PrakriyaLogger:
    """
    R17: Lakṣya-Lakṣaṇa (Validation Logging).
    Now includes 'Molecular View' (Varna Vichheda) for students.
    """
    def __init__(self):
        self.steps = []

    def log(self, rule, stage, result, varna_view=None):
        # 1. Main Entry
        entry = f"→ {result}  [{stage}: {rule}]"
        self.steps.append(entry)

        # 2. Student Microscope (Varna Vichheda)
        # If raw Varnas are provided, show them: e.g. [र्, आ, म, अ] + [अ, म्]
        if varna_view:
            chem_str = " + ".join([str(v) for v in varna_view])
            self.steps.append(f"   ↳ 🔍 विश्लेषण: {chem_str}")

    def print_history(self):
        print("\n=== Prakriya Derivation (प्रक्रिया) ===")
        for step in self.steps:
            print(step)
        print("=======================================\n")

def derive(word, vibhakti=1, vacana=1):
    logger = PrakriyaLogger()
    print(f"🎯 Input: {word} (Case {vibhakti}, Num {vacana})")
    result = SubantaProcessor.derive_pada(word, vibhakti, vacana, logger)
    logger.print_history()
    print(f"✅ Final Siddha Rupa: {result}")
    return result

if __name__ == "__main__":
    derive("राम")