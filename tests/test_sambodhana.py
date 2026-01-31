"""
FILE: tests/test_sambodhana.py
TEST CASE: Rama (Sambodhana - Vocative with 'Hey')
"""
import unittest
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

class TestRamaSambodhana(unittest.TestCase):
    def setUp(self): self.logger = PrakriyaLogger()

    def test_8_1_he_rama(self):
        """Test 8.1: Rāma + Su -> हे राम"""
        print("\n" + "="*60)
        print("🚀 TEST 8.1: Rāma + Su (Sambodhana Ekavachana)")
        res = SubantaProcessor.derive_pada("राम", 8, 1, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "हे राम")

    def test_8_2_he_ramau(self):
        """Test 8.2: Rāma + Au -> हे रामौ"""
        print("\n" + "="*60)
        print("🚀 TEST 8.2: Rāma + Au (Sambodhana Dvivachana)")
        res = SubantaProcessor.derive_pada("राम", 8, 2, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "हे रामौ")

    def test_8_3_he_ramah(self):
        """Test 8.3: Rāma + Jas -> हे रामाः"""
        print("\n" + "="*60)
        print("🚀 TEST 8.3: Rāma + Jas (Sambodhana Bahuvachana)")
        res = SubantaProcessor.derive_pada("राम", 8, 3, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "हे रामाः")

if __name__ == '__main__':
    unittest.main()
