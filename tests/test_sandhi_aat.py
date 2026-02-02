"""
FILE: tests/test_sandhi_aat.py
PURPOSE: Verify 6.1.90 Aatasca (Vriddhi for Aat Augment)
"""
import unittest
from logic.sandhi_processor import SandhiProcessor

class TestAatSandhi(unittest.TestCase):

    def setUp(self):
        self.engine = SandhiProcessor()
        self.test_cases = [
            # 1. Past Tense Augment (Luṅ/Laṅ)
            # Ā + Īkṣata -> Aikṣata (Vriddhi Ai, not Guna E)
            ("आ", "ईक्षत", "ऐक्षत", "Aat + Ikshata -> Aikshata", ["Augment-Aat"]),

            # Ā + Ubjīt -> Aubjīt (Vriddhi Au, not Guna O)
            ("आ", "उब्जीत्", "औब्जीत्", "Aat + Ubjit -> Aubjit", ["Augment-Aat"]),

            # 2. Loṭ Uttama Purusha (Āḍuttamasya Picca 3.4.92)
            # Cakṣ + Āṭ + i -> Cakṣ + Ā + i -> Cakṣ + Ai (Vriddhi)
            # We test the junction: Ā + i -> Ai
            ("आ", "इ", "ऐ", "Aat + i -> Ai", ["Augment-Aat"]),
            # Context: Caksh + Ai -> Cakshai

            # 3. Nadi Words (Āṇnadyāḥ 7.3.112)
            # Nadī + Ṅe -> Nadī + Āṭ + e -> Nadī + Ā + e
            # First Sandhi: Ā + e -> Ai (Vriddhi 6.1.90 / 6.1.88 both give Ai)
            ("आ", "ए", "ऐ", "Aat + e -> Ai", ["Augment-Aat"]),
            # Then: Nadī + Ai -> Nadyai (Yan).

            # Control Test: No Aat tag -> Standard Rules apply
            # A + I -> E (Guna)
            ("आ", "ईक्षत", "एक्षत", "Aa + Ikshata (No Tag) -> Ekshata (Guna)", [])
        ]

    def test_aat_logic(self):
        print("\n   [ 🧪 Testing Aatasca (6.1.90) ]")
        for t1, t2, expected, desc, tags in self.test_cases:
            with self.subTest(case=desc):
                actual = self.engine.join(t1, t2, context_tags=tags, return_as_str=True)

                status = "✅ PASS" if actual == expected else f"❌ FAIL (Got '{actual}')"
                print(f"   {status}: {t1} + {t2} -> {expected}")
                self.assertEqual(actual, expected, f"Failed: {desc}")

if __name__ == "__main__":
    unittest.main()
