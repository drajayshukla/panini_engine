"""
FILE: tests/test_sandhi_yan.py
PURPOSE: Verify 6.1.77 (Yan), 6.1.101 (Savarna), 6.1.125 (Pragrhya)
"""
import unittest
from logic.sandhi_processor import SandhiProcessor

class TestYanSandhi(unittest.TestCase):

    def setUp(self):
        self.engine = SandhiProcessor()
        self.test_cases = [
            ("दधि", "अत्र", "दध्यत्र", "Dadhi + atra -> Dadhyatra"),
            ("नदी", "ऊर्ध्वम्", "नद्यूर्ध्वम्", "Nadī + ūrdhvam -> Nadyūrdhvam"),
            ("मधु", "इति", "मध्विति", "Madhu + iti -> Madhviti"),
            ("वधू", "आदेशः", "वध्वादेशः", "Vadhū + ādeśaḥ -> Vadhvādeśaḥ"),
            ("पितृ", "इच्छा", "पित्रिच्छा", "Pitṛ + icchā -> Pitricchā"),
            ("ॠ", "अस्य", "रस्य", "Ṝ + asya -> Rasya"),
            ("ऌ", "आकृतिः", "लाकृतिः", "Ḷ + ākṛtiḥ -> Lākṛtiḥ"),
            ("नदी", "इयम्", "नदीयम्", "Nadī + iyam -> Nadīyam (Savarna Block)"),
            ("गुरु", "उपदेशः", "गुरूपदेशः", "Guru + upadeśaḥ -> Gurūpadeśaḥ"),

            # Pragrhya returns separated string (Prakrti-Bhava)
            # The Engine v24.2 inserts a Space.
            ("धेनू", "इमे", "धेनू इमे", "Dhenū (Dual) + ime -> No Sandhi (Space)"), 
            ("हरी", "एतौ", "हरी एतौ", "Harī (Dual) + etau -> No Sandhi (Space)"),
            ("पचेते", "इमौ", "पचेते इमौ", "Pacete (Dual Verb) + imau -> No Sandhi (Space)")
        ]

    def test_sandhi_logic(self):
        print("\n   [ 🧪 Running Sandhi Validation (Yan, Savarna, Pragṛhya) ]")
        for t1, t2, expected, desc in self.test_cases:
            with self.subTest(case=desc):
                context = []
                if t1 in ["धेनू", "हरी", "पचेते"]:
                    context.append("Dual")

                actual = self.engine.join(t1, t2, context_tags=context, return_as_str=True)

                status = "✅ PASS" if actual == expected else f"❌ FAIL (Got '{actual}')"
                print(f"   {status}: {t1} + {t2} -> {expected}")
                self.assertEqual(actual, expected, f"Failed: {desc}")

if __name__ == "__main__":
    unittest.main()
