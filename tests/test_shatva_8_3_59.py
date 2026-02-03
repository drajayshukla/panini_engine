"""
FILE: tests/test_shatva_8_3_59.py
PURPOSE: Verify 8.3.59 Ādeśapratyayayoḥ (S -> Ṣ)
"""
import unittest
from logic.sandhi_processor import SandhiProcessor
from core.core_foundation import ad, sanskrit_varna_samyoga

class TestShatva(unittest.TestCase):
    def run_tripadi(self, input_str):
        varnas = ad(input_str)
        res_varnas = SandhiProcessor.run_tripadi(varnas)
        return sanskrit_varna_samyoga(res_varnas)

    def test_vak_su(self):
        self.assertEqual(self.run_tripadi("वाक्सु"), "वाक्षु")

    def test_pathisyati(self):
        self.assertEqual(self.run_tripadi("पठिस्यति"), "पठिष्यति")

    def test_siseca(self):
        self.assertEqual(self.run_tripadi("सिसेच"), "सिषेच")

    def test_dhanussu_intervention(self):
        # धनुस् + सु -> धनुःषु (via 8.3.59) -> धनुष्षु (via 8.3.36/8.4.41)
        # Correct output is Dhanuṣṣu
        self.assertEqual(self.run_tripadi("धनुस्सु"), "धनुष्षु")
        self.assertEqual(self.run_tripadi("धनुःसु"), "धनुष्षु")

    def test_no_change_rama_su(self):
        self.assertEqual(self.run_tripadi("रामेसु"), "रामेषु")
        self.assertEqual(self.run_tripadi("रामसु"), "रामसु")

    def test_agni_su(self):
        self.assertEqual(self.run_tripadi("अग्निसु"), "अग्निषु")

if __name__ == '__main__':
    unittest.main()
