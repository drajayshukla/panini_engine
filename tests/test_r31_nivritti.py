"""
FILE: tests/test_r31_nivritti.py
TEST CASE: Prove that Bhasya rules do NOT fire when Nivṛtti is active.
"""
import unittest
from core.adhikara_controller import AdhikaraController

class TestR31Nivritti(unittest.TestCase):
    def test_nivritti_logic(self):
        """
        Verify mathematical boundaries of Adhikaras.
        """
        print("\n" + "="*60)
        print("🚀 TEST R31: Nivṛtti (De-activation) Logic")
        
        # 1. Supi Ca (7.3.102) IS inside Angasya (6.4.1 - 7.4.97)
        self.assertTrue(AdhikaraController.is_rule_in_scope("7.3.102", "ANGASYA"), "7.3.102 must be inside ANGASYA")
        
        # 2. Supi Ca (7.3.102) IS NOT inside Bhasya (6.4.129 - 6.4.175)
        self.assertFalse(AdhikaraController.is_rule_in_scope("7.3.102", "BHASYA"), "7.3.102 must be OUTSIDE BHASYA")
        
        # 3. Contextual Nivṛtti
        # Case: Rama + Su (1.1). Not Bham.
        context = {"is_bham": False}
        is_nivrutta = AdhikaraController.check_nivritti(context, "BHASYA")
        self.assertTrue(is_nivrutta, "Bhasya must be Deactivated (Nivṛtti) for Rama + Su")

if __name__ == '__main__':
    unittest.main()
