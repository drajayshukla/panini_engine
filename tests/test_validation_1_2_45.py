"""
FILE: tests/test_validation_1_2_45.py
TEST CASE: Verify 1.2.45 Rejection Logic
"""
import unittest
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

class TestPratipadikaValidation(unittest.TestCase):
    def setUp(self): self.logger = PrakriyaLogger()

    def test_valid_rama(self):
        """Test Valid Stem: Rama"""
        print("\n" + "="*60)
        print("🚀 TEST: Valid Stem (Rama)")
        res = SubantaProcessor.derive_pada("राम", 1, 1, self.logger)
        self.assertNotEqual(res, "Error: Dhatu")
        self.assertNotEqual(res, "Error: Pratyaya")
        self.assertEqual(res, "रामः")

    def test_invalid_dhatu(self):
        """Test Invalid Dhatu: Bhu"""
        print("\n" + "="*60)
        print("🚀 TEST: Invalid Dhatu (Bhu)")
        res = SubantaProcessor.derive_pada("भू", 1, 1, self.logger)
        print(f"Result: {res}")
        self.assertEqual(res, "Error: Dhatu")

    def test_invalid_pratyaya(self):
        """Test Invalid Pratyaya: Su"""
        print("\n" + "="*60)
        print("🚀 TEST: Invalid Pratyaya (Su)")
        res = SubantaProcessor.derive_pada("सु", 1, 1, self.logger)
        print(f"Result: {res}")
        self.assertEqual(res, "Error: Pratyaya")

if __name__ == '__main__':
    unittest.main()
