"""
FILE: update_sambodhana_test.py
PURPOSE: Update Sambodhana test to verify 'He' prefix and print full history.
"""
import os
import shutil
import subprocess
import sys

# ==============================================================================
# अद्यतन टेस्ट फाइल (UPDATED TEST FILE)
# ==============================================================================
NEW_TEST_CODE = '''"""
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
        print("\\n" + "="*60)
        print("🚀 TEST 8.1: Rāma + Su (Sambodhana Ekavachana)")
        res = SubantaProcessor.derive_pada("राम", 8, 1, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "हे राम")

    def test_8_2_he_ramau(self):
        """Test 8.2: Rāma + Au -> हे रामौ"""
        print("\\n" + "="*60)
        print("🚀 TEST 8.2: Rāma + Au (Sambodhana Dvivachana)")
        res = SubantaProcessor.derive_pada("राम", 8, 2, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "हे रामौ")

    def test_8_3_he_ramah(self):
        """Test 8.3: Rāma + Jas -> हे रामाः"""
        print("\\n" + "="*60)
        print("🚀 TEST 8.3: Rāma + Jas (Sambodhana Bahuvachana)")
        res = SubantaProcessor.derive_pada("राम", 8, 3, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "हे रामाः")

if __name__ == '__main__':
    unittest.main()
'''

with open(os.path.join("tests", "test_sambodhana.py"), "w", encoding="utf-8") as f:
    f.write(NEW_TEST_CODE)

# कैश साफ़ करें (Clear Cache)
for root, dirs, files in os.walk("."):
    if "__pycache__" in dirs: shutil.rmtree(os.path.join(root, "__pycache__"))

print("🚀 टेस्ट फाइल अपडेटेड। रनिंग टेस्ट...")
subprocess.run([sys.executable, "tests/test_sambodhana.py"])