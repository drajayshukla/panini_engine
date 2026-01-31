"""
FILE: tests/test_shashti.py
TEST CASE: Rama (Shashti Vibhakti - Genitive)
Goal: Verify 6.1 (Ramasya), 6.2 (Ramayoh), 6.3 (Ramanam)
"""
import unittest
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

class TestRamaShashti(unittest.TestCase):
    
    def setUp(self):
        self.logger = PrakriyaLogger()

    def test_6_1_ramasya(self):
        """Test 6.1: Rāma + Ngas -> Rāmasya"""
        print("\n" + "="*60)
        print("🚀 TEST 6.1: Rāma + Ngas (Shashti Ekavachana)")
        res = SubantaProcessor.derive_pada("राम", 6, 1, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "रामस्य")

    def test_6_2_ramayoh(self):
        """Test 6.2: Rāma + Os -> Rāmayoḥ"""
        print("\n" + "="*60)
        print("🚀 TEST 6.2: Rāma + Os (Shashti Dvivachana)")
        res = SubantaProcessor.derive_pada("राम", 6, 2, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "रामयोः")

    def test_6_3_ramanam(self):
        """Test 6.3: Rāma + Am -> Rāmāṇām"""
        print("\n" + "="*60)
        print("🚀 TEST 6.3: Rāma + Am (Shashti Bahuvachana)")
        res = SubantaProcessor.derive_pada("राम", 6, 3, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "रामाणाम्")

if __name__ == '__main__':
    unittest.main()
