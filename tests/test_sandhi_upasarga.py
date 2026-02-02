"""
FILE: tests/test_sandhi_upasarga.py
PURPOSE: Verify 6.1.91 Upasargad Rti Dhatau (Vriddhi vs Guna)
"""
import unittest
from logic.sandhi_processor import SandhiProcessor

class TestUpasargaSandhi(unittest.TestCase):

    def setUp(self):
        self.engine = SandhiProcessor()
        self.test_cases = [
            # 1. Upasarga + R-adi Dhatu -> Vriddhi (Aar)
            ("प्र", "ऋच्छति", "प्रार्च्छति", "Pra + Rcchati -> Prarcchati (Vriddhi)", ["Dhatu"]),
            ("परा", "ऋणाति", "परार्णाति", "Para + Rnati -> Pararnati (Vriddhi)", ["Dhatu"]),
            ("उप", "ऋच्छति", "उपार्च्छति", "Upa + Rcchati -> Uparcchati (Vriddhi)", ["Dhatu"]),
            ("आ", "ऋतीयते", "आर्तीयते", "Aa + Rtiyate -> Aartiyate (Vriddhi)", ["Dhatu"]),
            ("अप", "ऋध्नोति", "अपार्ध्नोति", "Apa + Rdhnoti -> Apardhnoti (Vriddhi)", ["Dhatu"]),
            ("अव", "ऋणोति", "अवार्णोति", "Ava + Rnoti -> Avarnoti (Vriddhi)", ["Dhatu"]),

            # 2. Non-Upasarga + R-adi Dhatu -> Guna (Ar)
            # Mala is not in Pradi Gana
            ("माला", "ऋच्छति", "मालर्च्छति", "Mala + Rcchati -> Malarcchati (Guna)", ["Dhatu"]),

            # 3. Upasarga + Non-R-adi Dhatu -> Guna
            # Iyarti (Root R, but form starts with I)
            ("प्र", "इयर्ति", "प्रेयर्ति", "Pra + Iyarti -> Preyarti (Guna A+I=E)", ["Dhatu"]),

            # 4. Upasarga + Non-Dhatu (Adjective/Noun) -> Guna
            # Pra + Rcchaka (if not Dhatu context) -> Prarcchaka
            # We simulate this by NOT passing "Dhatu" tag
            ("प्र", "ऋच्छकः", "प्रर्च्छकः", "Pra + Rcchakah (Noun) -> Prarcchakah (Guna)", [])
        ]

    def test_upasarga_logic(self):
        print("\n   [ 🧪 Testing Upasargad Rti Dhatau (6.1.91) ]")
        for t1, t2, expected, desc, tags in self.test_cases:
            with self.subTest(case=desc):
                actual = self.engine.join(t1, t2, context_tags=tags, return_as_str=True)

                status = "✅ PASS" if actual == expected else f"❌ FAIL (Got '{actual}')"
                print(f"   {status}: {t1} + {t2} -> {expected}")
                self.assertEqual(actual, expected, f"Failed: {desc}")

if __name__ == "__main__":
    unittest.main()
