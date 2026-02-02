"""
FILE: tests/test_dhatu_factory.py
COMPLIANCE: unittest.TestCase (Corrected Benchmarks)
"""
import unittest
from logic.dhatu_processor import DhatuDiagnostic

class TestDhatuFactory(unittest.TestCase):

    def setUp(self):
        # The authoritative benchmark dataset
        self.benchmarks = [
            # 1. Complex: Initial Ḍu + Final Ñ
            ("डुकृञ्", "कृ", ["डु-It (1.3.5)", "ञ्-It (1.3.3)"]),

            # 2. Simple: Final Ñ
            ("णीञ्", "नी", ["ञ्-It (1.3.3)"]),

            # 3. Idit (Num-agama)
            ("नदिँ", "नन्द्", ["इँ-It (1.3.2)"]),
            ("विदिँ", "विन्द्", ["इँ-It (1.3.2)"]),
            ("मुचिँ", "मुन्च्", ["इँ-It (1.3.2)"]),

            # 4. Pure Phonology (No tags)
            ("ष्मि", "स्मि", []),

            # 5. Halanta formation (Vowel It)
            ("णदँ", "नद्", ["अँ-It (1.3.2)"]),

            # 6. Corrected: ṇidi~ is just Idit + Natva. It is NOT 1.3.5.
            ("णिदिँ", "निन्द्", ["इँ-It (1.3.2)"]), 

            # 7. ADDED: True 1.3.5 'Ñi' Test Case
            ("ञिभी", "भी", ["ञि-It (1.3.5)"]),

            # 8. Vartika Priority
            ("भिदिँर्", "भिद्", ["ir-It (Vartika)"])
        ]

    def test_dhatu_prakriya_benchmarks(self):
        """Validates 1.3.5, 1.3.2, 7.1.58, and Vartika logic."""
        print("\n   [ Running Dhātu Prakriyā Benchmarks ]")

        for upadesha, expected_root, required_tags in self.benchmarks:
            with self.subTest(root=upadesha):
                diag = DhatuDiagnostic(upadesha)
                actual_root = diag.get_final_root()

                # 1. Validation of Action Root
                self.assertEqual(
                    actual_root, 
                    expected_root, 
                    f"❌ {upadesha}: Got '{actual_root}', Expected '{expected_root}'"
                )

                # 2. Validation of Genetic Markers (Tags)
                if required_tags:
                    found_tags = [t for t in diag.it_tags]
                    for req in required_tags:
                        req_core = req.split()[0] 
                        match = any(req_core in t for t in found_tags)
                        self.assertTrue(
                            match, 
                            f"❌ {upadesha}: Missing marker '{req_core}'. Found: {found_tags}"
                        )

                # Safe access to 'pada' (initialized in v10.2)
                pada_info = getattr(diag, 'pada', 'Unknown')
                print(f"    ✅ {upadesha} -> {actual_root} [{pada_info}]")

    def test_exception_sthivu(self):
        """R8 Balīyaḥ: Exception 6.1.64 (Sthivu)"""
        diag = DhatuDiagnostic("ष्ठिवुँ")
        self.assertEqual(diag.get_final_root(), "ष्ठिव्")
        print("    ✅ ष्ठिवुँ -> ष्ठिव् (Exception Preserved)")

if __name__ == "__main__":
    unittest.main()
