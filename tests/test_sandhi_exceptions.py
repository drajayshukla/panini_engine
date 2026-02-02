"""
FILE: tests/test_sandhi_exceptions.py
PURPOSE: Verify 6.1.89 and Vartikas (Upaiti, Akshauhini, Sukharta, etc.)
"""
import unittest
from logic.sandhi_processor import SandhiProcessor

class TestSandhiExceptions(unittest.TestCase):

    def setUp(self):
        self.engine = SandhiProcessor()
        self.test_cases = [
            # 1. Etyedhatyuthsu (6.1.89)
            ("उप", "एति", "उपैति", "Upa + Eti -> Upaiti", []),
            ("उप", "एधते", "उपैधते", "Upa + Edhate -> Upaidhate", []),

            # Visvavah + Ta -> (Samprasarana) -> Visva + Uha
            # Testing the Sandhi part: A + U -> Au (Vriddhi)
            # Input adjusted to reflect the state BEFORE Sandhi
            ("विश्व", "ऊह", "विश्वौह", "Visva + Uha -> Visvauha", []),

            # 2. Akshauhini (Vartika)
            ("अक्ष", "ऊहिनी", "अक्षौहिणी", "Aksha + Uhini -> Akshauhini", []),

            # 3. Svad Irerinoh (Vartika)
            ("स्व", "ईरः", "स्वैरः", "Sva + Ira -> Svaira", []),
            ("स्व", "ईरिणी", "स्वैरिणी", "Sva + Irini -> Svairini", []),

            # 4. Prad Uhodhodha... (Vartika)
            ("प्र", "ऊहः", "प्रौहः", "Pra + Uha -> Prauha", []),
            ("प्र", "ऊढः", "प्रौढः", "Pra + Udha -> Praudha", []),
            ("प्र", "एषः", "प्रैषः", "Pra + Esha -> Praisha", []),

            # 5. Rte ca tritiyasamase (Vartika)
            ("सुख", "ऋतः", "सुखार्तः", "Sukha + Rita -> Sukharta (Tritiya)", ["Tritiya"]),
            ("परम", "ऋतः", "परमर्तः", "Parama + Rita -> Paramarta (Guna)", []),

            # 6. Pra-vatsatara... (Vartika)
            ("प्र", "ऋणम्", "प्रार्णम्", "Pra + Rnam -> Prarnam", []),
            ("वत्सतर", "ऋणम्", "वत्सतरार्णम्", "Vatsatara + Rnam -> Vatsatararnam", []),
            ("दश", "ऋणः", "दशार्णः", "Dasha + Rnah -> Dasharnah", [])
        ]

    def test_exception_logic(self):
        print("\n   [ 🧪 Testing Sandhi Exceptions (6.1.89+) ]")
        for t1, t2, expected, desc, tags in self.test_cases:
            with self.subTest(case=desc):
                joined_list = self.engine.join(t1, t2, context_tags=tags, return_as_str=False)
                final_list = self.engine.run_tripadi(joined_list)

                from core.core_foundation import sanskrit_varna_samyoga
                actual = sanskrit_varna_samyoga(final_list)

                status = "✅ PASS" if actual == expected else f"❌ FAIL (Got '{actual}')"
                print(f"   {status}: {t1} + {t2} -> {expected}")
                self.assertEqual(actual, expected, f"Failed: {desc}")

if __name__ == "__main__":
    unittest.main()
