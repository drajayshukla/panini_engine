
from logic.dhatu_processor import DhatuDiagnostic
class TinantaDiagnostic:
    def __init__(self, upadesha):
        self.history = []
        d = DhatuDiagnostic(upadesha)
        self.root = d.get_final_root()
        self.history.extend(d.history)
        self.final_form = self.root + "अति"
        self.history.append("3.4.78: Tiptasjhi... -> ti")
