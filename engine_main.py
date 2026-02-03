"""
FILE: engine_main.py
PURPOSE: Shared Logger for tracking Paninian derivations.
"""
class PrakriyaLogger:
    def __init__(self):
        self.history = []

    def log(self, rule, name, desc, result):
        """
        Logs a single step in the derivation.
        rule: Sūtra Number (e.g., "1.3.3")
        name: Sūtra Name (e.g., "Halantyam")
        desc: Description of the operation
        result: The form after the operation
        """
        self.history.append({
            "rule": rule,
            "name": name,
            "desc": desc,
            "result": result,
            "source": "Pāṇini"
        })

    def get_history(self):
        return self.history
