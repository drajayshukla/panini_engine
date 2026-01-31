"""
FILE: tests/test_hari_phase2.py
TEST CASE: Hari - Dvitiya & Tritiya
"""
import unittest
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

class TestHariPhase2(unittest.TestCase):
    def setUp(self): self.logger = PrakriyaLogger()

    def test_2_1_harim(self):
        """Test 2.1: Hari + Am -> Harim (Ami Purvah)"""
        print("\n" + "="*60)
        print("🚀 TEST 2.1: Hari + Am -> Harim")
        res = SubantaProcessor.derive_pada("हरि", 2, 1, self.logger)
        self.assertEqual(res, "हरिम्")

    def test_2_2_hari(self):
        """Test 2.2: Hari + Out -> Harī (Purva Savarna)"""
        print("\n" + "="*60)
        print("🚀 TEST 2.2: Hari + Out -> Harī")
        res = SubantaProcessor.derive_pada("हरि", 2, 2, self.logger)
        self.assertEqual(res, "हरी")

    def test_2_3_harin(self):
        """Test 2.3: Hari + Shas -> Harīn (Shaso Nah)"""
        print("\n" + "="*60)
        print("🚀 TEST 2.3: Hari + Shas -> Harīn")
        res = SubantaProcessor.derive_pada("हरि", 2, 3, self.logger)
        self.assertEqual(res, "हरीन्")
        
    def test_3_1_harina(self):
        """Test 3.1: Hari + Ta -> Hariṇā (Natva)"""
        print("\n" + "="*60)
        print("🚀 TEST 3.1: Hari + Ta -> Hariṇā")
        res = SubantaProcessor.derive_pada("हरि", 3, 1, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "हरिणा")
        
    def test_3_2_haribhyam(self):
        """Test 3.2: Hari + Bhyam -> Haribhyām"""
        res = SubantaProcessor.derive_pada("हरि", 3, 2, self.logger)
        self.assertEqual(res, "हरिभ्याम्")
        
    def test_3_3_haribhih(self):
        """Test 3.3: Hari + Bhis -> Haribhiḥ"""
        res = SubantaProcessor.derive_pada("हरि", 3, 3, self.logger)
        self.assertEqual(res, "हरिभिः")

if __name__ == '__main__':
    unittest.main()
