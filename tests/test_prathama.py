"""
FILE: tests/test_prathama.py
TEST CASE: Rama (Prathama Vibhakti)
"""
import unittest
import sys
import os

# Ensure imports work if run directly OR via master_runner
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor


class TestRamaPrathama(unittest.TestCase):

    def setUp(self):
        # This runs before EACH test function
        self.logger = PrakriyaLogger()

    def test_1_1_ramah(self):
        """Test 1.1: Rāma + Su -> Rāmaḥ"""
        # Run derivation
        res = SubantaProcessor.derive_pada("राम", 1, 1, self.logger)

        # Verify
        self.assertEqual(res, "रामः", f"Expected रामः but got {res}")

    def test_1_2_ramau(self):
        """Test 1.2: Rāma + Au -> Rāmau"""
        res = SubantaProcessor.derive_pada("राम", 1, 2, self.logger)
        self.assertEqual(res, "रामौ", f"Expected रामौ but got {res}")

    def test_1_3_ramah_plural(self):
        """Test 1.3: Rāma + Jas -> Rāmāḥ"""
        res = SubantaProcessor.derive_pada("राम", 1, 3, self.logger)
        self.assertEqual(res, "रामाः", f"Expected रामाः but got {res}")


if __name__ == '__main__':
    unittest.main()