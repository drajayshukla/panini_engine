"""
FILE: engine_main.py
PURPOSE: Core Logger utility with Varna-Viccheda capability.
"""

class PrakriyaLogger:
    def __init__(self):
        self.history = []

    def log(self, rule, operation, result, raw_state=None):
        """
        Logs a derivation step with atomic character breakdown.
        """
        viccheda = ""
        if raw_state:
            # List of Varna objects -> "र् + आ + म् + अ"
            chars = [v.char for v in raw_state]
            viccheda = " + ".join(chars)

        step_data = {
            "rule": rule,
            "operation": operation,
            "result": str(result),
            "viccheda": viccheda 
        }
        self.history.append(step_data)

    def print_history(self):
        """Console printing logic."""
        print("\n=== Prakriya Derivation (प्रक्रिया) ===")
        for step in self.history:
            print(f"→ {step['result']}   [{step['operation']}: {step['rule']}]")
            if step['viccheda']:
                print(f"   ↳ 🔍 विश्लेषण: {step['viccheda']}")
        print("=======================================")

    def get_history(self):
        return self.history
