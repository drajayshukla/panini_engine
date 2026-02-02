"""
FILE: tests/test_sandhi_ato_gune.py
PURPOSE: Verify 6.1.97 Ato Gune (Apadanta A + Guna -> Pararupa)
"""
import unittest
from logic.sandhi_processor import SandhiProcessor

class TestAtoGune(unittest.TestCase):

    def setUp(self):
        self.engine = SandhiProcessor()
        self.test_cases = [
            # 1. A + A -> A (Blocks Savarna Dirgha Aa)
            # Path + a (Sap) + anti (Jhi)
            # Input: Patha + anti. Patha ends in 'a' (Apadanta).
            ("पठ", "अन्ति", "पठन्ति", "Patha + Anti -> Pathanti (Pararupa)", []),

            # 2. A + E -> E (Blocks Vriddhi Ai)
            # Labh + a (Sap) + e (It)
            # Input: Labha + e. Labha ends in 'a' (Apadanta).
            ("लभ", "ए", "लभे", "Labha + E -> Labhe (Pararupa)", []),

            # 3. Conflict: Rama + Jas -> Ramas
            # Rama (Ak) + As (Prathama).
            # Ato Gune applies? A + A -> A. Result Ramas.
            # BUT 6.1.102 applies? A + A -> Aa. Result Ramas.
            # 6.1.102 BLOCKS Ato Gune.
            # We simulate this by passing "Vibhakti-1-2" tag.
            ("राम", "अस्", "रामास्", "Rama + As (Vibhakti) -> Ramas (Purvasavarna Dirgha)", ["Vibhakti-1-2"]),

            # Control: Padanta A (Dandasya + Agram)
            # Dandasya ends in A (Pada).
            # Should do Savarna Dirgha.
            ("दण्डस्य", "अग्रम्", "दण्डस्याग्रम्", "Dandasya + Agram -> Dandasyagram (Savarna)", ["Pada"])
        ]

    def test_ato_gune_logic(self):
        print("\n   [ 🧪 Testing Ato Gune (6.1.97) ]")
        for t1, t2, expected, desc, tags in self.test_cases:
            with self.subTest(case=desc):
                actual = self.engine.join(t1, t2, context_tags=tags, return_as_str=True)

                status = "✅ PASS" if actual == expected else f"❌ FAIL (Got '{actual}')"
                print(f"   {status}: {t1} + {t2} -> {expected}")
                self.assertEqual(actual, expected, f"Failed: {desc}")

if __name__ == "__main__":
    unittest.main()
