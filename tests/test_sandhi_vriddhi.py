"""
FILE: tests/test_sandhi_vriddhi.py
PURPOSE: Verify 6.1.88 Vriddhi Rechi (a/aa + e/o/ai/au -> ai/au)
"""
import unittest
from logic.sandhi_processor import SandhiProcessor

class TestVriddhiSandhi(unittest.TestCase):

    def setUp(self):
        self.engine = SandhiProcessor()
        self.test_cases = [
            # Note: "Pada" tag is added to prevent Ato Gune (6.1.97) from triggering
            # 6.1.97 applies to Apadanta A. External Sandhi is Padanta.

            # 1. A/Aa + E/Ai -> Ai
            ("कृष्ण", "एकत्वम्", "कृष्णैकत्वम्", "Krishna + ekatvam -> Krishnaikatvam", ["Pada"]),
            ("ललिता", "एकत्वम्", "ललितैकत्वम्", "Lalita + ekatvam -> Lalitaikatvam", ["Pada"]),
            ("देव", "ऐश्वर्यम्", "देवैश्वर्यम्", "Deva + aishvaryam -> Devaishvaryam", ["Pada"]),
            ("ललिता", "ऐश्वर्यम्", "ललितैश्वर्यम्", "Lalita + aishvaryam -> Lalitaishvaryam", ["Pada"]),

            # 2. A/Aa + O/Au -> Au
            ("जल", "ओघः", "जलौघः", "Jala + oghah -> Jalaughah", ["Pada"]),
            ("गङ्गा", "ओघः", "गङ्गौघः", "Ganga + oghah -> Gangaughah", ["Pada"]),
            ("कृष्ण", "औचित्यम्", "कृष्णौचित्यम्", "Krishna + auchityam -> Krishnauchityam", ["Pada"]),
            ("गङ्गा", "औचित्यम्", "गङ्गौचित्यम्", "Ganga + auchityam -> Gangauchityam", ["Pada"])
        ]

    def test_vriddhi_logic(self):
        print("\n   [ 🧪 Testing Vriddhi Rechi (6.1.88) ]")
        for t1, t2, expected, desc, tags in self.test_cases:
            with self.subTest(case=desc):
                actual = self.engine.join(t1, t2, context_tags=tags, return_as_str=True)

                status = "✅ PASS" if actual == expected else f"❌ FAIL (Got '{actual}')"
                print(f"   {status}: {t1} + {t2} -> {expected}")
                self.assertEqual(actual, expected, f"Failed: {desc}")

if __name__ == "__main__":
    unittest.main()
