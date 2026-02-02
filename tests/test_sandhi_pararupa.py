"""
FILE: tests/test_sandhi_pararupa.py
PURPOSE: Verify 6.1.94 Engi Pararupam and Vartikas (Shakandhu etc.)
"""
import unittest
from logic.sandhi_processor import SandhiProcessor

class TestPararupaSandhi(unittest.TestCase):

    def setUp(self):
        self.engine = SandhiProcessor()
        self.test_cases = [
            # 1. 6.1.94 Engi Pararupam (Upasarga + Eng-adi Dhatu)
            ("प्र", "एजते", "प्रेजते", "Pra + Ejate -> Prejate (Pararupa)", []),
            ("परा", "एजते", "परेजते", "Para + Ejate -> Parejate (Pararupa)", []),
            ("प्र", "ओषति", "प्रोषति", "Pra + Oshati -> Proshati (Pararupa)", []),

            # Counter-Examples: Non-Upasarga (Tava is a Pada)
            # Tava + Eva -> Tavaiva (Vriddhi 6.1.88)
            # Must tag as "Pada" to avoid Ato Gune (6.1.97)
            ("तव", "एव", "तवैव", "Tava + Eva -> Tavaiva (Vriddhi)", ["Pada"]),

            # Counter-Examples: Etyedhatyuthsu (6.1.89) Exception to Pararupa
            ("उप", "एति", "उपैति", "Upa + Eti -> Upaiti (Vriddhi 6.1.89)", []),

            # 2. Vartika: Shakandhvadi (Ti-Lopa + Pararupa)
            ("शक", "अन्धुः", "शकन्धुः", "Shaka + Andhuh -> Shakandhuh", []),
            ("कर्क", "अन्धुः", "कर्कन्धुः", "Karka + Andhuh -> Karkandhuh", []),
            ("कुल", "अटा", "कुलटा", "Kula + Ata -> Kulata", []),
            ("सीमन्", "अन्तः", "सीमन्तः", "Siman + Antah -> Simantah (Ti 'an' lost)", []),
            ("मनस्", "ईषा", "मनीषा", "Manas + Isha -> Manisha (Ti 'as' lost)", []),
            ("हल", "ईषा", "हलीषा", "Hala + Isha -> Halisha", []),
            ("पतत्", "अञ्जलिः", "पतञ्जलिः", "Patat + Anjalih -> Patanjalih (Ti 'at' lost)", []),
            ("सार", "अङ्गः", "सारङ्गः", "Sara + Angah -> Sarangah", [])
        ]

    def test_pararupa_logic(self):
        print("\n   [ 🧪 Testing Pararupa Sandhi (6.1.94) ]")
        for t1, t2, expected, desc, tags in self.test_cases:
            with self.subTest(case=desc):
                actual = self.engine.join(t1, t2, context_tags=tags, return_as_str=True)

                status = "✅ PASS" if actual == expected else f"❌ FAIL (Got '{actual}')"
                print(f"   {status}: {t1} + {t2} -> {expected}")
                self.assertEqual(actual, expected, f"Failed: {desc}")

if __name__ == "__main__":
    unittest.main()
