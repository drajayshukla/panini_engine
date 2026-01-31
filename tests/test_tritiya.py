"""
FILE: tests/test_tritiya.py
TEST CASE: Rama (Tritiya Vibhakti)
"""
import unittest
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor


class TestRamaTritiya(unittest.TestCase):

    def setUp(self):
        self.logger = PrakriyaLogger()

    def test_3_1_ramena(self):
        """Test 3.1: Rāma + Tā -> Rāmeṇa"""
        print("\n" + "=" * 60)
        print("🚀 TEST 3.1: Rāma + Tā (Tritiya Ekavachana)")
        res = SubantaProcessor.derive_pada("राम", 3, 1, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "रामेण")

    def test_3_2_ramabhyam(self):
        """Test 3.2: Rāma + Bhyām -> Rāmābhyām"""
        print("\n" + "=" * 60)
        print("🚀 TEST 3.2: Rāma + Bhyām (Tritiya Dvivachana)")
        res = SubantaProcessor.derive_pada("राम", 3, 2, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "रामाभ्याम्")

    def test_3_3_ramaih(self):
        """Test 3.3: Rāma + Bhis -> Rāmaiḥ"""
        print("\n" + "=" * 60)
        print("🚀 TEST 3.3: Rāma + Bhis (Tritiya Bahuvachana)")
        res = SubantaProcessor.derive_pada("राम", 3, 3, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "रामैः")


if __name__ == '__main__':
    unittest.main()