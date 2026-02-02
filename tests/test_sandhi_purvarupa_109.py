"""
FILE: tests/test_sandhi_purvarupa_109.py
PURPOSE: Verify 6.1.109 Engah Padantadati (Purvarupa with Avagraha)
"""
import unittest
from logic.sandhi_processor import SandhiProcessor

class TestPurvarupa109(unittest.TestCase):

    def setUp(self):
        self.engine = SandhiProcessor()
        self.test_cases = [
            # 1. Padanta E + A -> E' (Avagraha)
            ("वने", "अस्मिन्", "वनेऽस्मिन्", "Vane + Asmin -> Vane'smin (Purvarupa)", ["Pada"]),
            ("हरे", "अत्र", "हरेऽत्र", "Hare + Atra -> Hare'tra", ["Pada"]),

            # 2. Padanta O + A -> O' (Avagraha)
            ("विष्णो", "अव", "विष्णोऽव", "Visno + Ava -> Visno'va", ["Pada"]),
            ("प्रभो", "अत्र", "प्रभोऽत्र", "Prabho + Atra -> Prabho'tra", ["Pada"]),

            # 3. Negative: Non-Padanta -> Ayadi (6.1.78)
            ("चे", "अन", "चयन", "Che + Ana -> Cayana (Ayadi)", []),

            # 4. Negative: Padanta + Long Aa -> Ayadi (Tapara 'At' blocks 'Aa')
            # Vane (e) + Aasit (aa) -> Vanay + Aasit -> Vanayaasit
            ("वने", "आसीत्", "वनयासीत्", "Vane + Aasit -> Vanayaasit (Ayadi)", ["Pada"]),

            # 5. Negative: Dual (Pragrhya) -> Prakritibhava
            ("पचेते", "अत्र", "पचेते अत्र", "Pacete + Atra -> Pacete Atra (Pragrhya blocks Purvarupa)", ["Pada", "Dual"])
        ]

    def test_purvarupa_109(self):
        print("\n   [ 🧪 Testing Purvarupa (6.1.109) ]")
        for t1, t2, expected, desc, tags in self.test_cases:
            with self.subTest(case=desc):
                actual = self.engine.join(t1, t2, context_tags=tags, return_as_str=True)

                status = "✅ PASS" if actual == expected else f"❌ FAIL (Got '{actual}')"
                print(f"   {status}: {t1} + {t2} -> {expected}")
                self.assertEqual(actual, expected, f"Failed: {desc}")

if __name__ == "__main__":
    unittest.main()
