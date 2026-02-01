"""
FILE: tests/test_sambodhana_ghi.py
TEST CASE: Sambodhana for Hari and Guru (8.1)
"""
import unittest
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

class TestSambodhanaGhi(unittest.TestCase):
    def setUp(self): self.logger = PrakriyaLogger()

    def test_8_1_hari(self):
        """Hari + Su (Vocative) -> He Hare"""
        print("\n" + "="*60)
        print("🚀 TEST 8.1: Hari -> He Hare")
        res = SubantaProcessor.derive_pada("हरि", 8, 1, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "हे हरे")

    def test_8_1_guru(self):
        """Guru + Su (Vocative) -> He Guro"""
        print("\n" + "="*60)
        print("🚀 TEST 8.1: Guru -> He Guro")
        res = SubantaProcessor.derive_pada("गुरु", 8, 1, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "हे गुरो")
        
    def test_8_1_rama(self):
        """Rama + Su (Vocative) -> He Rama (Regression Check)"""
        print("\n" + "="*60)
        print("🚀 TEST 8.1: Rama -> He Rama")
        res = SubantaProcessor.derive_pada("राम", 8, 1, self.logger)
        self.assertEqual(res, "हे राम")

if __name__ == '__main__':
    unittest.main()
