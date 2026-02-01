"""
FILE: tests/test_guru.py
TEST CASE: Guru (Ukārānta Puṃliṅga) - Uses Generalized Ghi Logic
"""
import unittest
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor

class TestGuru(unittest.TestCase):
    def setUp(self): self.logger = PrakriyaLogger()

    def test_1_1_guruh(self):
        """1.1 Guru + Su -> Guruḥ"""
        print("\n" + "="*60)
        print("🚀 TEST 1.1: Guru + Su -> Guruḥ")
        res = SubantaProcessor.derive_pada("गुरु", 1, 1, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "गुरुः")

    def test_1_2_guru(self):
        """1.2 Guru + Au -> Gurū (Purva Savarna)"""
        print("\n" + "="*60)
        print("🚀 TEST 1.2: Guru + Au -> Gurū")
        res = SubantaProcessor.derive_pada("गुरु", 1, 2, self.logger)
        self.assertEqual(res, "गुरू")

    def test_1_3_guravah(self):
        """1.3 Guru + Jas -> Guravaḥ (Guna + Ayadi)"""
        print("\n" + "="*60)
        print("🚀 TEST 1.3: Guru + Jas -> Guravaḥ")
        res = SubantaProcessor.derive_pada("गुरु", 1, 3, self.logger)
        self.logger.print_history()
        self.assertEqual(res, "गुरवः")

    def test_3_1_guruna(self):
        """3.1 Guru + Ta -> Guruṇā (Ango Na + Natva)"""
        res = SubantaProcessor.derive_pada("गुरु", 3, 1, self.logger)
        self.assertEqual(res, "गुरुणा")

    def test_4_1_gurave(self):
        """4.1 Guru + Ne -> Gurave (Guna + Ayadi)"""
        res = SubantaProcessor.derive_pada("गुरु", 4, 1, self.logger)
        self.assertEqual(res, "गुरवे")

    def test_6_1_guroh(self):
        """6.1 Guru + Ngas -> Guroḥ (Guna + Purvarupa)"""
        res = SubantaProcessor.derive_pada("गुरु", 6, 1, self.logger)
        self.assertEqual(res, "गुरोः")

    def test_7_1_gurau(self):
        """7.1 Guru + Ni -> Gurau (Aut)"""
        res = SubantaProcessor.derive_pada("गुरु", 7, 1, self.logger)
        self.assertEqual(res, "गुरौ")

if __name__ == '__main__':
    unittest.main()
