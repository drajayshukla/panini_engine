"""
FILE: tests/test_rama_fem.py
TEST CASE: Ramā (Ākārānta Strīliṅga) - All Vibhaktis
"""
import unittest
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

class TestRamaFem(unittest.TestCase):
    def setUp(self): self.logger = PrakriyaLogger()

    def test_1_1_rama(self):
        res = SubantaProcessor.derive_pada("रमा", 1, 1, self.logger)
        self.assertEqual(res, "रमा")

    def test_1_2_rame(self):
        res = SubantaProcessor.derive_pada("रमा", 1, 2, self.logger)
        self.assertEqual(res, "रमे")

    def test_1_3_ramah(self):
        res = SubantaProcessor.derive_pada("रमा", 1, 3, self.logger)
        self.assertEqual(res, "रमाः")

    def test_2_1_ramam(self):
        res = SubantaProcessor.derive_pada("रमा", 2, 1, self.logger)
        self.assertEqual(res, "रमाम्")

    def test_3_1_ramaya(self):
        res = SubantaProcessor.derive_pada("रमा", 3, 1, self.logger)
        self.assertEqual(res, "रमया")

    def test_4_1_ramayai(self):
        res = SubantaProcessor.derive_pada("रमा", 4, 1, self.logger)
        self.assertEqual(res, "रमायै")

    def test_6_1_ramayah(self):
        """Test 6.1: Ramāyāḥ (Verify Yat Agama fusion)"""
        print("\n" + "="*60)
        print("🚀 TEST 6.1: Ramā + Ngas -> Ramāyāḥ")
        res = SubantaProcessor.derive_pada("रमा", 6, 1, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "रमायाः")

    def test_7_1_ramayam(self):
        """Test 7.1: Ramāyām (Verify Yat Agama fusion)"""
        print("\n" + "="*60)
        print("🚀 TEST 7.1: Ramā + Ni -> Ramāyām")
        res = SubantaProcessor.derive_pada("रमा", 7, 1, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "रमायाम्")

    def test_8_1_he_rame(self):
        res = SubantaProcessor.derive_pada("रमा", 8, 1, self.logger)
        self.assertEqual(res, "हे रमे")

if __name__ == '__main__':
    unittest.main()
