"""
FILE: tests/test_chaturthi.py
TEST CASE: Rama (Chaturthi Vibhakti)
"""
import unittest
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

class TestRamaChaturthi(unittest.TestCase):
    
    def setUp(self):
        self.logger = PrakriyaLogger()

    def test_4_1_ramaya(self):
        res = SubantaProcessor.derive_pada("राम", 4, 1, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "रामाय")

    def test_4_2_ramabhyam(self):
        res = SubantaProcessor.derive_pada("राम", 4, 2, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "रामाभ्याम्")

    def test_4_3_ramebhyah(self):
        res = SubantaProcessor.derive_pada("राम", 4, 3, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "रामेभ्यः")

if __name__ == '__main__':
    unittest.main()
