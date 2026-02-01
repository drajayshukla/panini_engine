"""
FILE: engine_main.py
PURPOSE: Handles derivation logging with Rich Metadata from SutraRepo.
"""
from core.sutra_repo import SutraRepository

class PrakriyaLogger:
    def __init__(self):
        self.history = []

    def log(self, rule_num, operation, result, varnas, source="Panini"):
        """
        Logs a derivation step.
        Enriches 'rule_num' with Sanskrit Name if found in Repo.
        """
        sutra_data = SutraRepository.get(rule_num)
        
        display_rule = rule_num
        display_op = operation
        vartika_html = ""

        if sutra_data:
            # Append Sanskrit Name
            sanskrit_name = sutra_data.get('name', '')
            if sanskrit_name:
                display_rule = f"{rule_num} {sanskrit_name}"
            
            # Append Vartikas if any
            vartikas = sutra_data.get('vartikas', [])
            if vartikas:
                v_list = "<br>".join([f"🔸 <i>{v}</i>" for v in vartikas])
                vartika_html = f"<div style='font-size:0.8rem; color:#d35400; margin-top:4px;'>{v_list}</div>"

        # Prepare Varna Viccheda String
        viccheda = ""
        if varnas:
            # varnas is list of Varna objects or just string check
            try:
                viccheda = " + ".join([v.char for v in varnas])
            except:
                viccheda = str(varnas)

        step_record = {
            "rule": display_rule,
            "operation": display_op,
            "result": result,
            "viccheda": viccheda,
            "source": source,
            "vartika_html": vartika_html
        }
        self.history.append(step_record)

    def get_history(self):
        return self.history

    def print_history(self):
        """
        Prints the derivation history to the console (for tests/debugging).
        """
        print("\n=== Prakriya Derivation (प्रक्रिया) ===")
        for step in self.history:
            print(f"→ {step['result']}")
            # Remove HTML tags for console clean view if needed, or just print
            print(f"   [Rule: {step['rule']} | Op: {step['operation']} | Auth: {step['source']}]")
            if step['viccheda']:
                print(f"   ↳ 🔍 विश्लेषण: {step['viccheda']}")
        print("=======================================\n")
