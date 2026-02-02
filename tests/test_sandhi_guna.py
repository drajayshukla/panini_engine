"""
FILE: tests/test_sandhi_guna.py
PURPOSE: Verify 6.1.87 Ad Gunah (a/aa + i/u/r/l -> e/o/ar/al)
"""
import unittest
from logic.sandhi_processor import SandhiProcessor

class TestGunaSandhi(unittest.TestCase):

    def setUp(self):
        self.engine = SandhiProcessor()
        self.test_cases = [
            # 1. A + I -> E
            ("देव", "इन्द्रः", "देवेन्द्रः", "Deva + Indrah -> Devendrah"),
            ("महा", "इन्द्र", "महेन्द्र", "Maha + Indra -> Mahendra"), # Note: Dropping Visarga from input if assumed Padanta in suffix
            ("देव", "ईशः", "देवेशः", "Deva + Ishah -> Deveshah"),
            ("महा", "ईशः", "महेशः", "Maha + Ishah -> Maheshah"),

            # 2. A + U -> O
            ("सूर्य", "उदयः", "सूर्योदयः", "Surya + Udayah -> Suryodayah"),
            ("गङ्गा", "उदकम्", "गङ्गोदकम्", "Ganga + Udakam -> Gangodakam"),
            ("पाद", "ऊनम्", "पादोनम्", "Pada + Unam -> Padonam"),
            ("एका", "ऊनम्", "एकोनम्", "Eka + Unam -> Ekonam"),

            # 3. A + R -> Ar (Uran Raparah)
            ("देव", "ऋषिः", "देवर्षिः", "Deva + Rishih -> Devarshih"),
            ("महा", "ऋषिः", "महर्षिः", "Maha + Rishih -> Maharshih"),
            ("प्रथम", "ॠकारः", "प्रथमर्कारः", "Prathama + Rkarah -> Prathamarkarah"),
            ("बालिका", "ॠकारः", "बालिकर्कारः", "Balika + Rkarah -> Balikarkarah"),

            # 4. A + L -> Al (Lapara)
            ("कृष्ण", "ऌकारः", "कृष्णल्कारः", "Krishna + Lkarah -> Krishnalkarah"),
            ("महा", "ऌकारः", "महल्कारः", "Maha + Lkarah -> Mahalkarah")
        ]

    def test_guna_logic(self):
        print("\n   [ 🧪 Testing Ad Gunah (6.1.87) ]")
        for t1, t2, expected, desc in self.test_cases:
            with self.subTest(case=desc):
                actual = self.engine.join(t1, t2, return_as_str=True)

                status = "✅ PASS" if actual == expected else f"❌ FAIL (Got '{actual}')"
                print(f"   {status}: {t1} + {t2} -> {expected}")
                self.assertEqual(actual, expected, f"Failed: {desc}")

if __name__ == "__main__":
    unittest.main()
