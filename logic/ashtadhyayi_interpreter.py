"""
FILE: logic/ashtadhyayi_interpreter.py
PURPOSE: The "Interpreter" (Orchestrator)
"""
from logic.rules_registry import define_rules

class AshtadhyayiInterpreter:
    def __init__(self):
        self.rules = define_rules()

    def run_derivation(self, state):
        """
        Naive implementation: Linear scan.
        Real Pāṇinian Engine requires Paratva/Nityatva conflict resolution.
        """
        max_steps = 20
        steps = 0

        while steps < max_steps:
            rule_applied = False

            for rule in self.rules:
                context = rule.condition(state)
                if context:
                    desc = rule.transformation(state, context)
                    state.step(rule.id, rule.name, desc, state.render())
                    rule_applied = True
                    break # Restart scan after modification (Siddha principle)

            if not rule_applied:
                break
            steps += 1

        return state
