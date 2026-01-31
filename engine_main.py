"""
FILE: engine_main.py
PURPOSE: Core Logger utility for the Paninian Engine.
"""
from core.core_foundation import sanskrit_varna_samyoga

class PrakriyaLogger:
    def __init__(self):
        self.history = []

    def log(self, rule, operation, result, raw_state=None):
        """
        Logs a single step in the derivation.
        rule: The Panini Sutra number (e.g., '6.1.78')
        operation: Description of the action (e.g., 'Ayadi Sandhi')
        result: The string state of the word after the operation
        raw_state: (Optional) The list of Varna objects
        """
        # Ensure result is a string for display
        res_str = str(result)

        step_data = {
            "rule": rule,
            "operation": operation,
            "result": res_str,
            "raw_state": raw_state
        }
        self.history.append(step_data)

    def print_history(self):
        """Prints the history to the console (Terminal Mode)."""
        print("\n=== Prakriya Derivation (प्रक्रिया) ===")
        for step in self.history:
            print(f"→ {step['result']}   [{step['operation']}: {step['rule']}]")
            if step['raw_state']:
                # Helper to visualize internal Varna breakdown
                analysis = sanskrit_varna_samyoga(step['raw_state'], debug=True)
                print(f"   ↳ 🔍 विश्लेषण: {analysis}")
        print("=======================================")

    def get_history(self):
        """
        Returns the list of derivation steps.
        Used by the Streamlit UI to render the 'Glassbox' view.
        """
        return self.history