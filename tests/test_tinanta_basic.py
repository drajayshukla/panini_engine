"""
FILE: tests/test_tinanta_basic.py
PURPOSE: Verify 7.3.101 Ato Dirgho Yani (Lengthening of A before Yañ-adi Sarvadhatuka)
"""
import unittest
from logic.subanta_processor import SubantaProcessor

class TestTinantaBasic(unittest.TestCase):

    def test_ato_dirgho_yani(self):
        print("\n   [ 🧪 Testing Ato Dirgho Yani (7.3.101) ]")

        # 1. Path + a (Shap) + mi (Mip) -> Pathami
        # Stem "patha" (ends in a), Suffix "mi" (starts with m - Yan)
        res = SubantaProcessor.derive_tinanta_weak("पठ", "मि")
        print(f"   patha + mi -> {res}")
        self.assertEqual(res, "पठामि", "Failed Patha + mi -> Pathami")

        # 2. Path + a + vah -> Pathavah
        res = SubantaProcessor.derive_tinanta_weak("पठ", "वः")
        print(f"   patha + vah -> {res}")
        self.assertEqual(res, "पठावः", "Failed Patha + vah -> Pathavah")

        # 3. Path + a + mah -> Pathamah
        res = SubantaProcessor.derive_tinanta_weak("पठ", "मः")
        print(f"   patha + mah -> {res}")
        self.assertEqual(res, "पठामः", "Failed Patha + mah -> Pathamah")

        # 4. Negative: Path + a + ti -> Pathati (t is not Yan)
        res = SubantaProcessor.derive_tinanta_weak("पठ", "ति")
        print(f"   patha + ti -> {res}")
        self.assertEqual(res, "पठति", "Should not lengthen for 'ti'")

        # 5. Negative: Path + a + anti -> Pathanti (Pararupa 6.1.97, not Dirgha)
        # Note: 'anti' starts with vowel, Sandhi takes over.
        # derive_tinanta_weak handles Sandhi too.
        res = SubantaProcessor.derive_tinanta_weak("पठ", "अन्ति")
        print(f"   patha + anti -> {res}")
        self.assertEqual(res, "पठन्ति", "Should apply Pararupa (Ato Gune)")

if __name__ == "__main__":
    unittest.main()
