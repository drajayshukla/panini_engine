"""
FILE: tests/test_dhatu_json.py
TEST CASE: Verify that Dhatu JSON is loaded and used for validation.
"""
import unittest
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

class TestDhatuJson(unittest.TestCase):
    def setUp(self): self.logger = PrakriyaLogger()

    def test_json_rejection_bhu(self):
        """Test: 'Bhu' should be rejected via JSON lookup"""
        print("\n" + "="*60)
        print("🚀 TEST: JSON Rejection (Bhu)")
        res = SubantaProcessor.derive_pada("भू", 1, 1, self.logger)
        print(f"Result: {res}")
        self.assertEqual(res, "Error: Dhatu")
        
    def test_json_rejection_edh(self):
        """Test: 'Edh' (from JSON) should be rejected"""
        res = SubantaProcessor.derive_pada("एध्", 1, 1, self.logger)
        self.assertEqual(res, "Error: Dhatu")

    def test_valid_word_hari(self):
        """Test: 'Hari' should be valid"""
        res = SubantaProcessor.derive_pada("हरि", 1, 1, self.logger)
        self.assertEqual(res, "हरिः")

if __name__ == '__main__':
    unittest.main()
