"""
FILE: tests/test_sandhi_ami_purvah.py
PURPOSE: Verify 6.1.107 Ami Purvah (Ak + Am -> Purvarupa)
"""
import unittest
from logic.sandhi_processor import SandhiProcessor

class TestAmiPurvah(unittest.TestCase):

    def setUp(self):
        self.engine = SandhiProcessor()
        self.test_cases = [
            # 1. A + Am -> Am
            ("राम", "अम्", "रामम्", "Rama + Am -> Ramam (Purvarupa)", ["Am"]),
            ("फल", "अम्", "फलम्", "Phala + Am -> Phalam", ["Am"]),

            # 2. I + Am -> Im
            ("हरि", "अम्", "हरिम्", "Hari + Am -> Harim (Not Harim/Yana)", ["Am"]),
            ("मति", "अम्", "मतिम्", "Mati + Am -> Matim", ["Am"]),

            # 3. U + Am -> Um
            ("भानु", "अम्", "भानुम्", "Bhanu + Am -> Bhanum", ["Am"]),
            ("धेनु", "अम्", "धेनुम्", "Dhenu + Am -> Dhenum", ["Am"]),

            # 4. Conflict with 6.1.102 (Prathamayoh Purvasavarnah)
            # 6.1.102 says Ak + Am -> Long Ak.
            # 6.1.107 says Purvarupa.
            # 6.1.107 is Apavada.
            # Tested by passing "Am" tag.
            ("राम", "अम्", "रामम्", "Rama + Am (Blocks 102)", ["Am", "Vibhakti-1-2"]),

            # 5. Non-Am (e.g. Jas/Aut) -> Savarna Dirgha or Yana
            # Just to ensure logic doesn't bleed.
            ("हरि", "औ", "हरी", "Hari + Au -> Hari (Purvasavarna blocked by 6.1.102 exception logic elsewhere, here 6.1.102)", ["Vibhakti-1-2"]),
            # Note: Hari + Au -> HarI (Dirgha) via 6.1.102? No, 6.1.102 applies.
            # Wait, Hari + Au -> HarI is standard declension.
            # If not tagged Am, it falls through to 102.
        ]

    def test_ami_logic(self):
        print("\n   [ 🧪 Testing Ami Purvah (6.1.107) ]")
        for t1, t2, expected, desc, tags in self.test_cases:
            with self.subTest(case=desc):
                actual = self.engine.join(t1, t2, context_tags=tags, return_as_str=True)

                status = "✅ PASS" if actual == expected else f"❌ FAIL (Got '{actual}')"
                print(f"   {status}: {t1} + {t2} -> {expected}")
                self.assertEqual(actual, expected, f"Failed: {desc}")

if __name__ == "__main__":
    unittest.main()
