"""
FILE: engine_main.py
PURPOSE: Core Logger with A1 Authority Citations and Varna-Viccheda.
"""

class PrakriyaLogger:
    def __init__(self):
        self.history = []

    def log(self, rule, operation, result, raw_state=None, source="Maharshi Pāṇini"):
        """
        Logs a derivation step with Authority Citation (A1).
        source: 'Maharshi Pāṇini', 'Vārttikakāra Kātyāyana', 'Patañjali', etc.
        """
        viccheda = ""
        if raw_state:
            chars = [v.char for v in raw_state]
            viccheda = " + ".join(chars)

        step_data = {
            "rule": rule,
            "operation": operation,
            "result": str(result),
            "viccheda": viccheda,
            "source": source
        }
        self.history.append(step_data)

    def print_history(self):
        print("\n=== Prakriya Derivation (प्रक्रिया) ===")
        for step in self.history:
            print(f"→ {step['result']}")
            print(f"   [Rule: {step['rule']} | Op: {step['operation']} | Auth: {step['source']}]")
            if step['viccheda']:
                print(f"   ↳ 🔍 विश्लेषण: {step['viccheda']}")
        print("=======================================")

    def get_history(self):
        return self.history
