"""
FILE: tests/test_hari_full.py
TEST CASE: Hari - Full Table (1.1 to 8.3)
"""
import unittest
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

class TestHariFull(unittest.TestCase):
    def setUp(self): self.logger = PrakriyaLogger()

    # --- चतुर्थी (Chaturthi) ---
    def test_4_1_haraye(self):
        """Test 4.1: Hari + Ne -> Haraye"""
        print("\n" + "="*60)
        print("🚀 TEST 4.1: Hari + Ne -> Haraye")
        res = SubantaProcessor.derive_pada("हरि", 4, 1, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "हरये")

    def test_4_3_haribhyah(self):
        """Test 4.3: Hari + Bhyas -> Haribhyaḥ"""
        res = SubantaProcessor.derive_pada("हरि", 4, 3, self.logger)
        self.assertEqual(res, "हरिभ्यः")

    # --- पञ्चमी (Panchami) ---
    def test_5_1_hareh(self):
        """Test 5.1: Hari + Ngasi -> Hareḥ"""
        print("\n" + "="*60)
        print("🚀 TEST 5.1: Hari + Ngasi -> Hareḥ")
        res = SubantaProcessor.derive_pada("हरि", 5, 1, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "हरेः")

    # --- षष्ठी (Shashti) ---
    def test_6_1_hareh(self):
        """Test 6.1: Hari + Ngas -> Hareḥ"""
        res = SubantaProcessor.derive_pada("हरि", 6, 1, self.logger)
        self.assertEqual(res, "हरेः")

    def test_6_3_harinam(self):
        """Test 6.3: Hari + Am -> Harīṇām"""
        print("\n" + "="*60)
        print("🚀 TEST 6.3: Hari + Am -> Harīṇām")
        res = SubantaProcessor.derive_pada("हरि", 6, 3, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "हरीणाम्")

    # --- सप्तमी (Saptami) ---
    def test_7_1_harau(self):
        """Test 7.1: Hari + Ni -> Harau"""
        print("\n" + "="*60)
        print("🚀 TEST 7.1: Hari + Ni -> Harau")
        res = SubantaProcessor.derive_pada("हरि", 7, 1, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "हरौ")
        
    def test_7_3_harishu(self):
        """Test 7.3: Hari + Sup -> Hariṣu"""
        res = SubantaProcessor.derive_pada("हरि", 7, 3, self.logger)
        self.assertEqual(res, "हरिषु")

if __name__ == '__main__':
    unittest.main()
