"""
FILE: tests/test_saptami.py
"""
import unittest
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

class TestRamaSaptami(unittest.TestCase):
    def setUp(self): self.logger = PrakriyaLogger()

    def test_7_1_rame(self):
        res = SubantaProcessor.derive_pada("राम", 7, 1, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "रामे")

    def test_7_2_ramayoh(self):
        res = SubantaProcessor.derive_pada("राम", 7, 2, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "रामयोः")

    def test_7_3_ramesu(self):
        res = SubantaProcessor.derive_pada("राम", 7, 3, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "रामेषु")

if __name__ == '__main__': unittest.main()
