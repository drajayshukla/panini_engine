"""
FILE: tests/test_dhatu_factory.py
"""
import unittest
from logic.dhatu_processor import DhatuDiagnostic

class TestDhatuFactory(unittest.TestCase):

    def setUp(self):
        self.benchmarks = [
            # --- 1. Standard Shatva (Ṣ -> S) ---
            ("ष्वदँ", "स्वद्", []),       # 1.18 Aasvadane
            ("षहँ", "सह्", []),           # 4.23 Chakyarthe
            ("षिचँ", "सिच्", []),         # 6.170 Ksharane

            # --- 2. Hidden Ṣ (After 1.3.5 removal) ---
            ("ञिष्वपँ", "स्वप्", ["ञि-It"]), # 2.63 Shaye

            # --- 3. Ṣ + Retroflex Un-bending (Sṭutva Nivṛtti) ---
            ("ष्टगेँ", "स्तग्", []),      # 1.909 Samvarane
            ("ष्टिघँ", "स्तिघ्", []),     # 5.21 Aaskandane
            ("ष्ठा", "स्था", []),         # 1.1077 Gatinivrittau

            # --- 4. Ṣ + Nasal (Ṇ -> N) ---
            ("षणँ", "सन्", []),           # 1.535 Sambhaktau
            ("ष्णा", "स्ना", []),         # 2.47 Shauche
            ("ष्णिहँ", "स्निह्", []),     # 4.97 Preetau
            ("षणुँ", "सन्", []),          # 8.2 Dane

            # --- 5. Vartika Exceptions (No Change) ---
            ("ष्ठिवुँ", "ष्ठिव्", []),    # 1.641 Nirasane
            ("ष्वष्क्", "ष्वष्क्", []),   # 1.105 Gatau

            # --- 6. Previous Benchmarks ---
            ("डुकृञ्", "कृ", ["डु-It"]),
            ("णीञ्", "नी", ["ञ्-It"]),
            ("नदिँ", "नन्द्", ["इँ-It"])
        ]

    def test_dhatu_prakriya_benchmarks(self):
        print("\n   [ Running Dhātu Prakriyā Benchmarks ]")
        for upadesha, expected_root, required_tags in self.benchmarks:
            with self.subTest(root=upadesha):
                diag = DhatuDiagnostic(upadesha)
                actual_root = diag.get_final_root()

                # Check Root
                self.assertEqual(actual_root, expected_root, 
                    f"❌ {upadesha}: Got '{actual_root}', Expected '{expected_root}'")

                # Check Tags
                found_tags = [t for t in diag.it_tags]
                for req in required_tags:
                    req_core = req.split()[0]
                    self.assertTrue(any(req_core in t for t in found_tags),
                        f"❌ {upadesha}: Missing tag '{req_core}'")

                print(f"    ✅ {upadesha} -> {actual_root}")

if __name__ == "__main__":
    unittest.main()
