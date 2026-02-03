
class PrakriyaLogger:
    def __init__(self): self.history = []
    def log(self, rule, name, desc, result):
        self.history.append({"rule": rule, "name": name, "desc": desc, "result": result})
    def get_history(self): return self.history
