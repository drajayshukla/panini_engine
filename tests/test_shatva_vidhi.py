"""
FILE: tests/test_shatva_vidhi.py
PURPOSE: Validation of 6.1.64 Vartika: Subdhātu-Ṣṭhivu-Ṣvaṣkatīnām Satvapratiṣedhaḥ
"""
import unittest
from logic.dhatu_processor import DhatuDiagnostic

class TestShatvaVidhi(unittest.TestCase):

    def setUp(self):
        self.test_cases = [
            # 1. Ṣṭhivu (Standard Vartika Exception)
            # ष्ठिवुँ -> ष्ठिव् (No Shatva, No Stutva-Nivritti)
            ("ष्ठिवुँ", "ष्ठिव्", "1.641: Ṣṭhivu -> Ṣṭhiv (Protected)", False),

            # 2. Ṣvaṣk (Standard Vartika Exception)
            # ष्वष्क् -> ष्वष्क् (No Shatva)
            ("ष्वष्क्", "ष्वष्क्", "1.105: Ṣvaṣk -> Ṣvaṣk (Protected)", False),

            # 3. Subdhātu (Nāmadhātu) - Ṣaṇmukhāya
            # Must set is_subdhatu=True. 
            # Ṣaṇmukhāya -> Ṣaṇmukhāya (Initial Ṣ does NOT become S)
            ("षण्मुखाय", "षण्मुखाय", "Vartika: Subdhātu Protection", True),

            # 4. Standard Case (Control Group)
            # Ṣah -> Sah (Should change)
            ("षहँ", "सह्", "4.23: Ṣah -> Sah (Normal)", False)
        ]

    def test_vartika_exceptions(self):
        print("\n   [ 🧪 Running Vartika Validation (6.1.64 Exceptions) ]")
        for upadesha, expected, context, is_sub in self.test_cases:
            with self.subTest(root=upadesha):
                # Pass the Subdhātu flag
                diag = DhatuDiagnostic(upadesha, is_subdhatu=is_sub)
                actual = diag.get_final_root()

                if actual != expected:
                    print(f"   ❌ FAIL: {upadesha} -> Got '{actual}', Expected '{expected}'")
                else:
                    print(f"   ✅ PASS: {upadesha} -> {actual} ({context})")

                self.assertEqual(actual, expected, 
                    f"Failed {context}: Input {upadesha}, Got {actual}")

if __name__ == "__main__":
    unittest.main()
