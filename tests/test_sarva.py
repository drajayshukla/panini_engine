"""
FILE: tests/test_sarva.py
TEST CASE: Sarva (Pronoun) Declension
"""
import unittest
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

class TestSarva(unittest.TestCase):
    def setUp(self): self.logger = PrakriyaLogger()

    def test_1_3_sarve(self):
        """1.3: Sarve (Jas -> Shee)"""
        res = SubantaProcessor.derive_pada("सर्व", 1, 3, self.logger)
        self.assertEqual(res, "सर्वे")

    def test_4_1_sarvasmai(self):
        """4.1: Sarvasmai (Ne -> Smai)"""
        res = SubantaProcessor.derive_pada("सर्व", 4, 1, self.logger)
        self.assertEqual(res, "सर्वस्मै")

    def test_5_1_sarvasmat(self):
        """5.1: Sarvasmat (Ngasi -> Smat)"""
        res = SubantaProcessor.derive_pada("सर्व", 5, 1, self.logger)
        self.assertEqual(res, "सर्वस्मात्")

    def test_6_3_sarvesham(self):
        """6.3: Sarvesham (Aam -> Sut + Etva + Shatva)"""
        # Sarva + Aam -> Sarva + s + Aam -> Sarve + s + Aam -> Sarve + sh + Aam -> Sarveshaam
        res = SubantaProcessor.derive_pada("सर्व", 6, 3, self.logger)
        self.assertEqual(res, "सर्वेषाम्")

    def test_7_1_sarvasmin(self):
        """7.1: Sarvasmin (Ni -> Smin)"""
        res = SubantaProcessor.derive_pada("सर्व", 7, 1, self.logger)
        self.assertEqual(res, "सर्वस्मिन्")

    def test_2_3_sarvan(self):
        """2.3: Sarvan (Standard Rama-like Natva/Shaso-nah)"""
        res = SubantaProcessor.derive_pada("सर्व", 2, 3, self.logger)
        self.assertEqual(res, "सर्वान्")

if __name__ == '__main__':
    unittest.main()
