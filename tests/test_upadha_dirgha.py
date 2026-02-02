"""
FILE: tests/test_upadha_dirgha.py
PURPOSE: Verify 8.2.78 (Upadhāyāṁ ca) - Lengthening before r/v + Hal
"""
import unittest
from logic.dhatu_processor import DhatuDiagnostic

class TestUpadhaDirgha(unittest.TestCase):

    def setUp(self):
        self.test_cases = [
            # 1. R-Upadha (u -> ū)
            ("कुर्दँ", "कूर्द्", "Kurda~ -> Kurd -> Kūrd (u-r-d)"),
            ("खुर्दँ", "खूर्द्", "Khurda~ -> Khurd -> Khūrd"),
            ("गुर्दँ", "गूर्द्", "Gurda~ -> Gurd -> Gūrd"),

            # 2. Ū-Upadha (Already Long -> No Change)
            ("ऊर्दँ", "ऊर्द्", "Ūrda~ -> Ūrd (Already long)"),

            # 3. Negative Cases (No Lengthening)
            # 'a' is not Ik
            ("पर्दँ", "पर्द्", "Parda~ -> Pard (a is not Ik)"),

            # Not r/v (Num cases)
            ("नदिँ", "नन्द्", "Nadi~ -> Nand (n is not r/v)"),

            # No final Hal? (Not relevant for Dhatu Patha roots usually, but good check)
            # Actually, standard Dhatus end in vowel (Upadesha) or Hal (after IT removal).

            # 4. Complex: Ṣūd (Ṣūda~)
            # Ṣūda~ -> Ṣūd -> Sūd (Shatva) -> Sūd (Already long)
            ("षूदँ", "सूद्", "Ṣūda~ -> Sūd (Shatva applied, no lengthening needed)")
        ]

    def test_upadha_logic(self):
        print("\n   [ 🧪 Running 8.2.78 Upadhā Dīrgha Validation ]")
        for upadesha, expected, context in self.test_cases:
            with self.subTest(root=upadesha):
                diag = DhatuDiagnostic(upadesha)
                actual = diag.get_final_root()

                status = "✅ PASS" if actual == expected else f"❌ FAIL (Got '{actual}')"
                print(f"   {status}: {upadesha} -> {expected} | {context}")

                self.assertEqual(actual, expected, 
                    f"Failed {context}: Input {upadesha}, Got {actual}")

if __name__ == "__main__":
    unittest.main()
