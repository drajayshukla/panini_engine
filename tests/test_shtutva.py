"""
FILE: tests/test_shtutva.py
PURPOSE: Verify 8.4.41 Ṣṭunā Ṣṭuḥ and Exceptions (8.4.42, 8.4.43)
"""
import unittest
from logic.sandhi_processor import SandhiProcessor
from core.core_foundation import ad, sanskrit_varna_samyoga

class TestShtutva(unittest.TestCase):
    def run_shtutva(self, t1, t2):
        l, r = SandhiProcessor.apply_shtutva(ad(t1), ad(t2))
        return sanskrit_varna_samyoga(l + r)

    def test_s_to_sh_retro(self):
        # रामस् + षष्ठः -> रामष्षष्ठः (s -> ṣ)
        self.assertEqual(self.run_shtutva("रामस्", "षष्ठः"), "रामष्षष्ठः")

    def test_s_to_t_varga(self):
        # रामस् + टीकते -> रामष्टीकते (s -> ṣ)
        self.assertEqual(self.run_shtutva("रामस्", "टीकते"), "रामष्टीकते")

    def test_t_varga_to_retro(self):
        # तद् + टीका -> तट्टीका (d -> ḍ -> ṭ via Charvta - assuming input is 'tad')
        # Note: Our test isolates 8.4.41. 
        # If input is 'tat' (Charva already applied), then t -> ṭ
        self.assertEqual(self.run_shtutva("तत्", "टीका"), "तट्टीका")
        
        # कृष् + न -> कृष्ण (n -> ṇ)
        self.assertEqual(self.run_shtutva("कृष्", "न"), "कृष्ण")

    def test_to_shi_exception(self):
        # 8.4.43: T-varga + Ṣ -> Blocked
        # सन् + षष्ठः -> सन्षष्ठः (Not सण्षष्ठः)
        self.assertEqual(self.run_shtutva("सन्", "षष्ठः"), "सन्षष्ठः")

    def test_padantat_exception(self):
        # 8.4.42: Padanta Ṭ + S -> Blocked
        # षट् + सन्तः -> षट्सन्तः (Not षट्षण्तः)
        self.assertEqual(self.run_shtutva("षट्", "सन्तः"), "षट्सन्तः")

    def test_padantat_exception_vartika(self):
        # 8.4.42 Vartika: Allow for Navati
        # षट् + नवतिः -> षण्णवतिः (Allowed)
        # Note: Input 'ṣaḍ' becomes 'ṣaṇ' via Yaro-anunasike (8.4.45), 
        # but 8.4.41 triggers the retroflexion first on 'navati'.
        # Here we test 8.4.41 specifically: n -> ṇ allowed
        self.assertEqual(self.run_shtutva("षट्", "नवतिः"), "षट्णवतिः") 
        # (Note: full derivation involves multiple rules, this checks 8.4.41 trigger)

if __name__ == '__main__':
    unittest.main()
