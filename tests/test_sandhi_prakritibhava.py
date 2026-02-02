"""
FILE: tests/test_sandhi_prakritibhava.py
PURPOSE: Verify 6.1.125 Plutapragrhya aci nityam (No Sandhi)
"""
import unittest
from logic.sandhi_processor import SandhiProcessor

class TestPrakritibhava(unittest.TestCase):

    def setUp(self):
        self.engine = SandhiProcessor()
        self.test_cases = [
            # 1. Pragrhya (Duals in I/U/E)
            ("हरी", "एतौ", "हरी एतौ", "Harī + Etau -> Hari Etau (Pragrhya)", ["Dual"]),
            ("विष्णू", "इमौ", "विष्णू इमौ", "Viṣṇū + Imau -> Visnu Imau", ["Dual"]),
            ("पचेते", "इमौ", "पचेते इमौ", "Pacete + Imau -> Pacete Imau", ["Dual"]),

            # 2. Pragrhya (Amī/Amū - 1.1.12)
            ("अमी", "ईषा", "अमी ईषा", "Amī + Īṣā -> Amī Īṣā (No Savarna)", []),
            ("अमू", "आसाते", "अमू आसाते", "Amū + Āsāte -> Amū Āsāte (No Yan)", []),

            # 3. Pragrhya (Ot - 1.1.15)
            ("अहो", "ईश", "अहो ईश", "Aho + Isha -> Aho Isha (No Ayadi)", ["Nipata"]),

            # 4. Pluta (Ends in 3)
            # Kṛṣṇa3 + Atra -> Kṛṣṇa3 Atra (No Savarna)
            ("कृष्ण३", "अत्र", "कृष्ण३ अत्र", "Krishna3 + Atra -> Krishna3 Atra", [])
        ]

    def test_prakritibhava_logic(self):
        print("\n   [ 🧪 Testing Prakritibhava (6.1.125) ]")
        for t1, t2, expected, desc, tags in self.test_cases:
            with self.subTest(case=desc):
                actual = self.engine.join(t1, t2, context_tags=tags, return_as_str=True)

                status = "✅ PASS" if actual == expected else f"❌ FAIL (Got '{actual}')"
                print(f"   {status}: {t1} + {t2} -> {expected}")
                self.assertEqual(actual, expected, f"Failed: {desc}")

if __name__ == "__main__":
    unittest.main()
