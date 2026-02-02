"""
FILE: engine_main.py - PAS-v23.2 (Restored print_history)
"""
from core.core_foundation import sanskrit_varna_samyoga

class PrakriyaLogger:
    def __init__(self):
        self.history = []

    def log(self, rule, name, desc, result, source="Panini"):
        """
        Logs a step in the derivation.
        """
        if isinstance(result, list):
            res_str = sanskrit_varna_samyoga(result)
        else:
            res_str = str(result)

        entry = {
            "rule": rule,       
            "name": name,       
            "desc": desc,       
            "result": res_str,  
            "source": source
        }
        self.history.append(entry)

    def get_history(self):
        return self.history

    def clear(self):
        self.history = []

    def print_history(self):
        """Prints the derivation history to the console (for tests)."""
        print("\n=== Prakriya Derivation (प्रक्रिया) ===")
        for step in self.history:
            print(f"→ {step['result']}")
            print(f"   [Rule: {step['rule']} {step['name']} | Op: {step['desc']} | Auth: {step['source']}]")
            # Analyze components if possible? No, result is string now.
        print("=======================================\n")
