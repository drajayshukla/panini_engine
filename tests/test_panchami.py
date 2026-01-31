"""
FILE: tests/test_panchami.py
TEST CASE: Rama (Panchami Vibhakti - Ablative)
"""
import unittest
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

class TestRamaPanchami(unittest.TestCase):
    
    def setUp(self):
        self.logger = PrakriyaLogger()

    def test_5_1_ramat(self):
        """Test 5.1: Rāma + Ngasi -> Rāmāt"""
        print("\n" + "="*60)
        print("🚀 TEST 5.1: Rāma + Ngasi (Panchami Ekavachana)")
        res = SubantaProcessor.derive_pada("राम", 5, 1, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "रामात्")

    def test_5_2_ramabhyam(self):
        """Test 5.2: Rāma + Bhyām -> Rāmābhyām"""
        print("\n" + "="*60)
        print("🚀 TEST 5.2: Rāma + Bhyām (Panchami Dvivachana)")
        res = SubantaProcessor.derive_pada("राम", 5, 2, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "रामाभ्याम्")

    def test_5_3_ramebhyah(self):
        """Test 5.3: Rāma + Bhyas -> Rāmebhyaḥ"""
        print("\n" + "="*60)
        print("🚀 TEST 5.3: Rāma + Bhyas (Panchami Bahuvachana)")
        res = SubantaProcessor.derive_pada("राम", 5, 3, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "रामेभ्यः")

if __name__ == '__main__':
    unittest.main()
