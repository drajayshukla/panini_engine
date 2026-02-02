"""
FILE: tests/test_sandhi_ayadi.py
PURPOSE: Verify Ayadi Sandhi (6.1.78) and its Exceptions (6.1.109, 6.1.125)
"""
import unittest
from logic.sandhi_processor import SandhiProcessor

class TestAyadiSandhi(unittest.TestCase):

    def setUp(self):
        self.engine = SandhiProcessor()
        self.test_cases = [
            # --- 1. Standard Ayadi (6.1.78) ---
            # e + a -> ay
            ("ने", "अनम्", "नयनम्", "Ne + anam -> Nayanam", []),
            # o + a -> av
            ("भो", "अनम्", "भवनम्", "Bho + anam -> Bhavanam", []),
            # ai + a -> ay (long)
            ("नै", "अकः", "नायकः", "Nai + akah -> Nayakah", []),
            # au + a -> av (long)
            ("पौ", "अकः", "पावकः", "Pau + akah -> Pavakah", []),

            # --- 2. Purvarupa Exception (6.1.109) ---
            # Condition: Padanta e/o + short a -> 'a' is absorbed (Avagraha optional)
            ("वने", "अस्मिन्", "वनेऽस्मिन्", "Vane (Pada) + asmin -> Vane'smin", ["Pada"]),
            ("प्रभो", "अत्र", "प्रभोऽत्र", "Prabho (Pada) + atra -> Prabho'tra", ["Pada"]),

            # Counter-Example: Internal Sandhi (No 'Pada' tag)
            # Here Ayadi MUST apply, not Purvarupa
            ("गुरो", "अस्", "गुरवस्", "Guro (Anga) + as -> Guravas", ["Anga"]),

            # --- 3. Pragrhya Exception (6.1.125) ---
            # Dual ending in e/o/i/u blocks everything
            ("पचेते", "इमे", "पचेते इमे", "Pacete (Dual) + ime -> No Sandhi", ["Dual"]),
            ("कवी", "एतौ", "कवी एतौ", "Kavi (Dual) + etau -> No Sandhi", ["Dual"])
        ]

    def test_ayadi_logic(self):
        print("\n   [ 🧪 Testing Ayadi Sandhi (6.1.78) & Exceptions ]")
        for t1, t2, expected, desc, tags in self.test_cases:
            with self.subTest(case=desc):
                actual = self.engine.join(t1, t2, context_tags=tags, return_as_str=True)

                # Check for success
                # Note: v24.0 implementation adds 'ऽ' for Purvarupa.
                # If engine doesn't output ' ', handled below.

                # Normalization for Pragrhya check (if space is missing in raw join)
                if "Dual" in tags and " " not in actual:
                    # Our engine currently joins list physically. 
                    # If logic says 'pass', it concats.
                    # We accept "Paceteime" if logic is correct internally, 
                    # but prefer "Pacete ime" for readability.
                    pass 

                status = "✅ PASS" if actual == expected else f"❌ FAIL (Got '{actual}')"
                print(f"   {status}: {t1} + {t2} -> {expected}")
                self.assertEqual(actual, expected, f"Failed: {desc}")

if __name__ == "__main__":
    unittest.main()
