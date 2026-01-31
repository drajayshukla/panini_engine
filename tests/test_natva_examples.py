"""
FILE: tests/test_natva_examples.py
"""
import unittest
from core.core_foundation import Varna
from logic.sandhi_processor import SandhiProcessor
from core.core_foundation import ad, sanskrit_varna_samyoga

class TestNatvaStrict(unittest.TestCase):
    
    def check_natva(self, input_str, expected):
        # Helper to simulate 8.4.2 on a raw varna list
        varnas = ad(input_str)
        res_varnas = SandhiProcessor.run_tripadi(varnas)
        res_str = sanskrit_varna_samyoga(res_varnas)
        print(f"Input: {input_str} -> Output: {res_str} | Expected: {expected}")
        self.assertEqual(res_str, expected)

    def test_ex1_varini(self):
        # Vari + ni -> Varini (Vowel intervention)
        self.check_natva("वारिनि", "वारिणि") # Mocking the state before Natva
        
    def test_ex2_drohena(self):
        # Droha + ena -> Drohena (H + Vowel intervention)
        self.check_natva("द्रोहेन", "द्रोहेण")
        
    def test_ex3_brahmani(self):
        # Brahma + ani -> Brahmani (H + M + Vowel)
        self.check_natva("ब्रह्मानि", "ब्रह्माणि")
        
    def test_ex5_murkhena(self):
        # Murkha + ena -> Murkhena (Ku + Vowel)
        self.check_natva("मूर्खेन", "मूर्खेण")

if __name__ == '__main__':
    unittest.main()
