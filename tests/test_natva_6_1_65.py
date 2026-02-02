"""
FILE: tests/test_natva_6_1_65.py
PURPOSE: Validation of 6.1.65 (Ṇo naḥ) - Initial Ṇ -> N
SOURCE: Siddhānta Kaumudī & Bhāṣya (Nad-ādi paryudāsa)
"""
import unittest
from logic.dhatu_processor import DhatuDiagnostic

class TestNatvaVidhi(unittest.TestCase):

    def setUp(self):
        # Format: (Upadesha, Expected_Root, Rule_Context)
        self.test_cases = [
            # ---------------------------------------------------------
            # 1. STANDARD EXAMPLES (From Prompt)
            # ---------------------------------------------------------
            ("णीञ्", "नी", "1.1049: Ṇīñ -> Nī (Prāpaṇe)"),
            ("णु", "नु", "2.30: Ṇu -> Nu (Stutau)"),
            ("णशँ", "नश्", "4.91: ṇaś -> Naś (Adarśane)"),
            ("णुदँ", "नुद्", "6.162: Ṇud -> Nud (Preraṇe)"),
            ("णभँ", "नभ्", "9.56: Ṇabh -> Nabh (Hiṃsāyām)"),

            # ---------------------------------------------------------
            # 2. BHASHYA EXCEPTIONS (Nad-ādi group - Naturally 'N')
            # These starts with 'N', so 6.1.65 effectively "does nothing" 
            # or they are input as 'N'.
            # ---------------------------------------------------------
            # Nad (Nadi~) -> Nand (Idit) -> Starts with N
            ("नदिँ", "नन्द्", "Nad-ādi: Nadi~ -> Nand (Starts with N)"),

            # Nath (Nāthṛ~) -> Nāth
            ("नाथृँ", "नाथ्", "Nad-ādi: Nāth -> Nāth (Starts with N)"),

            # Nrt (Nṛtī~) -> Nṛt
            ("नृतीँ", "नृत्", "Nad-ādi: Nṛt -> Nṛt (Starts with N)"),

            # ---------------------------------------------------------
            # 3. COMPLEX INTERACTION (Shatva + Natva)
            # ---------------------------------------------------------
            # Here 6.1.64 fires first (Ṣ->S), then 6.1.65 contextually reverts Ṇ->N
            ("षणँ", "सन्", "1.535: Ṣaṇ -> San (Shatva -> Natva/Stutva-Nivritti)")
        ]

    def test_natva_logic(self):
        print("\n   [ 🧪 Running 6.1.65 (Ṇo naḥ) Validation ]")
        for upadesha, expected, context in self.test_cases:
            with self.subTest(root=upadesha):
                diag = DhatuDiagnostic(upadesha)
                actual = diag.get_final_root()

                # Visual Feedback
                status = "✅ PASS" if actual == expected else f"❌ FAIL (Got '{actual}')"
                print(f"   {status}: {upadesha} -> {expected} | {context}")

                self.assertEqual(actual, expected, 
                    f"Failed {context}: Input {upadesha}, Got {actual}")

if __name__ == "__main__":
    unittest.main()
