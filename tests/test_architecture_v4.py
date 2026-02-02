"""
FILE: tests/test_architecture_v4.py
PURPOSE: Verify the Phase 4 Architecture (Prakriya + Rules + Interpreter)
"""
import unittest
from core.prakriya_stack import PrakriyaState
from logic.ashtadhyayi_interpreter import AshtadhyayiInterpreter

class TestArchitectureV4(unittest.TestCase):
    def test_yan_sandhi_flow(self):
        print("\n   [ 🧪 Testing V22 Architecture: Rule Engine Flow ]")

        # 1. Initialize State (Dadhim + Atra)
        # Note: We manually input 'Dadhi' (Ik ending) and 'Atra' (Ac beginning)
        state = PrakriyaState()
        state.add_term("दधि", tags={"Anga"})
        state.add_term("अत्र", tags={"Pada"})

        print(f"   Input State: {state.render()}")

        # 2. Run Interpreter
        engine = AshtadhyayiInterpreter()
        engine.run_derivation(state)

        # 3. Verify
        result = state.render()
        print(f"   Final State: {result}")
        print("   History Trace:")
        for step in state.history:
            print(f"     -> {step['rule']} {step['name']}: {step['desc']}")

        self.assertEqual(result, "दध्यत्र")

    def test_visarga_flow(self):
        # Test Hari + s -> Harih
        state = PrakriyaState()
        state.add_term("हरि", tags={"Anga"})
        state.add_term("स्", tags={"Pratyaya"}) # Padanta S

        engine = AshtadhyayiInterpreter()
        engine.run_derivation(state)

        self.assertEqual(state.render(), "हरिः")

if __name__ == "__main__":
    unittest.main()
