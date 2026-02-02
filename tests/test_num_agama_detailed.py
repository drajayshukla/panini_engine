"""
FILE: tests/test_num_agama_detailed.py
PURPOSE: Verify 7.1.58 (Num Insertion) & Internal Sandhi (Parasavarna/Anusvara)
"""
import unittest
from logic.dhatu_processor import DhatuDiagnostic

class TestNumAgamaDetailed(unittest.TestCase):

    def setUp(self):
        # Format: (Upadesha, Expected, Explanation)
        self.test_cases = [
            # 1. K-Varga (n -> ṅ)
            ("अकिँ", "अङ्क्", "Aki~ -> Ank -> Aṅk (8.4.58)"),

            # 2. C-Varga (n -> ñ)
            ("भजिँ", "भञ्ज्", "Bhaji~ -> Bhanj -> Bhañj"),

            # 3. Ṭ-Varga (n -> ṇ)
            ("कुठिँ", "कुण्ठ्", "Kuṭhi~ -> Kunṭh -> Kuṇṭh"),

            # 4. T-Varga (n -> n)
            ("चितिँ", "चिन्त्", "Citi~ -> Cint -> Cint (No change)"),

            # 5. P-Varga (n -> m)
            ("जभिँ", "जम्भ्", "Jabhi~ -> Janbh -> Jambh"),

            # 6. Sibilant (n -> ṃ Anusvara)
            ("त्रसिँ", "त्रंस्", "Trasi~ -> Trans -> Traṃs (No Parasavarna before S)"),
            ("बृहिँ", "बृंह्", "Bṛhi~ -> Bṛnh -> Bṛṃh (No Parasavarna before H)"),

            # 7. Semivowel Exception (n remains n)
            # Corrected Input: "इविँ" (Must be nasalized to be Idit)
            ("इविँ", "इन्व्", "Ivi~ -> Inv -> Inv (v is not Jhal for Anusvara)"),

            # 8. Standard Check
            ("नदिँ", "नन्द्", "Nadi~ -> Nand")
        ]

    def test_num_sandhi_logic(self):
        print("\n   [ 🧪 Running Num-Āgama + Internal Sandhi Validation ]")
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
