"""
FILE: tests/test_hari.py
TEST CASE: Hari (1.1, 1.2, 1.3)
"""
import unittest
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

class TestHariPrathama(unittest.TestCase):
    def setUp(self): self.logger = PrakriyaLogger()

    def test_1_1_harih(self):
        """Test 1.1: Hari + Su -> Hariḥ"""
        print("\n" + "="*60)
        print("🚀 TEST 1.1: Hari + Su (Visarga)")
        res = SubantaProcessor.derive_pada("हरि", 1, 1, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "हरिः")

    def test_1_2_hari(self):
        """Test 1.2: Hari + Au -> Harī (R8: Balīyaḥ)"""
        print("\n" + "="*60)
        print("🚀 TEST 1.2: Hari + Au -> Harī")
        res = SubantaProcessor.derive_pada("हरि", 1, 2, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "हरी")

    def test_1_3_harayah(self):
        """Test 1.3: Hari + Jas -> Harayaḥ (Guna/Ayadi)"""
        print("\n" + "="*60)
        print("🚀 TEST 1.3: Hari + Jas -> Harayaḥ")
        res = SubantaProcessor.derive_pada("हरि", 1, 3, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "हरयः")

if __name__ == '__main__':
    unittest.main()
