"""
FILE: tests/test_dvitiya.py
TEST CASE: Rama (Dvitiya Vibhakti) - Student Friendly Validation
"""
import unittest
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor


class TestRamaDvitiya(unittest.TestCase):

    def setUp(self):
        self.logger = PrakriyaLogger()

    def test_2_1_ramam(self):
        """Test 2.1: Rāma + Am -> Rāmam"""
        print("\n" + "=" * 60)
        print("🚀 TEST 2.1: Rāma + Am (Dvitiya Ekavachana)")
        res = SubantaProcessor.derive_pada("राम", 2, 1, self.logger)
        self.logger.print_history()  # Show Student Friendly Output

        self.assertEqual(res, "रामम्")
        print("✅ Correct: रामम्")

    def test_2_2_ramau(self):
        """Test 2.2: Rāma + Aut -> Rāmau"""
        print("\n" + "=" * 60)
        print("🚀 TEST 2.2: Rāma + Aut (Dvitiya Dvivachana)")
        res = SubantaProcessor.derive_pada("राम", 2, 2, self.logger)
        self.logger.print_history()

        self.assertEqual(res, "रामौ")
        print("✅ Correct: रामौ")

    def test_2_3_raman(self):
        """Test 2.3: Rāma + Shas -> Rāmān"""
        print("\n" + "=" * 60)
        print("🚀 TEST 2.3: Rāma + Shas (Dvitiya Bahuvachana)")
        res = SubantaProcessor.derive_pada("राम", 2, 3, self.logger)
        self.logger.print_history()

        self.assertEqual(res, "रामान्")
        print("✅ Correct: रामान्")


if __name__ == '__main__':
    unittest.main()