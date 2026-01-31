"""
FILE: core/prakriya_logger.py
TIMESTAMP: 2026-01-31 02:45:00 (IST)
PILLAR: Derivation History + Student UI
DESCRIPTION:
    1. Captures derivation steps with phonetic breakdown (Vichchheda).
    2. Supports both string and dict-based Sutra definitions for advanced notes.
    3. Provides dual rendering: 'render()' for logs and 'render_educational()' for students.
"""
from core.phonology import sanskrit_varna_samyoga
from core.sutra_manager import SutraManager

class PrakriyaLogger:
    def __init__(self):
        self.steps = []

    def add_step(self, varnas, rule, description=""):
        """
        Records a step. If SutraManager returns a dict, it stores it as metadata.
        """
        if isinstance(varnas, list):
            form = sanskrit_varna_samyoga(varnas)
            breakdown = "+".join([v.char for v in varnas])
        else:
            form = str(varnas)
            breakdown = form

        # Fetch from Manager if description is empty
        if not description:
            try:
                # This may now return a string OR a dict with {'text':..., 'note':...}
                description = SutraManager.get(rule)
            except Exception:
                description = ""

        entry = {
            "step": len(self.steps) + 1,
            "form": form,
            "vikchhed": breakdown,
            "rule": rule,
            "description": description
        }
        self.steps.append(entry)

    def render(self):
        """Standard developer-focused trace."""
        if not self.steps:
            print("No steps recorded.")
            return
        print(f"\nViewing: {self.steps[-1]['form']}")
        for step in self.steps:
            # Handle case where description might be a dict
            desc = step['description']
            if isinstance(desc, dict):
                desc = desc.get('text', '')
            print(f"→ {step['form']:<10} ({step['vikchhed']}) [{desc} {step['rule']}]")

    def render_educational(self):
        """
        Pedagogical output with ANSI colors for terminal clarity.
        Displays Sutra, Vritti, and Logic Notes separately.
        """
        print(f"\n{'='*80}")
        print(f"{'SANSKRIT DERIVATION (SIDDHI) LAB':^80}")
        print(f"{'='*80}\n")

        for i, step in enumerate(self.steps):
            rule_data = step['description']

            # Extract rich metadata if available
            if isinstance(rule_data, dict):
                sutra_text = rule_data.get('text', step['rule'])
                note = rule_data.get('note', '')
                vritti = rule_data.get('vritti', '')
            else:
                sutra_text = rule_data
                note = ""
                vritti = ""

            print(f"STEP {i+1}: \033[1m{step['form']}\033[0m")
            print(f"  Phonetic : {step['vikchhed']}")
            print(f"  Sutra    : \033[1;32m{step['rule']} ({sutra_text})\033[0m")

            if vritti:
                print(f"  Vritti   : {vritti}")
            if note:
                print(f"  Logic    : \033[34m{note}\033[0m")

            print("-" * 60)

        print(f"\033[1;32m✅ FINAL FORM: {self.steps[-1]['form']}\033[0m\n")

    @property
    def history(self):
        """Alias for steps to maintain test compatibility."""
        return self.steps