"""
FILE: engine_main.py
"""
class PrakriyaLogger:
    def __init__(self):
        self.history = []

    def log(self, rule, name, desc, result, viccheda=""):
        self.history.append({
            "rule": rule,
            "name": name,
            "desc": desc,
            "result": result,
            "viccheda": viccheda,
            "source": "Pāṇini"
        })

    def get_history(self):
        return self.history
