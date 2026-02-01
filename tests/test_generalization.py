"""
FILE: test_generalization.py
PURPOSE: The Ultimate Test. Prove that the engine can derive ANY word (Krishna, Kavi, Bhanu)
without writing new code, simply by using the existing pillars.
"""
import unittest
from engine_main import PrakriyaLogger
from logic.subanta_processor import SubantaProcessor


class TestGeneralization(unittest.TestCase):
    def setUp(self): self.logger = PrakriyaLogger()

    # --- TYPE 1: RAMA-WAT (Like Rama) ---
    def test_krishna_like_rama(self):
        """Test: Kṛṣṇa (Krishna) should behave exactly like Rāma"""
        print("\n" + "=" * 60)
        print("🚀 GENERALIZATION 1: Kṛṣṇa (Like Rāma)")

        # 1.1: Krishna + Su -> Krishnaḥ
        res = SubantaProcessor.derive_pada("कृष्ण", 1, 1, self.logger)
        print(f"  Result: {res}")
        self.assertEqual(res, "कृष्णः")

        # 3.1: Krishna + Ta -> Krishnena (Natva check!)
        res = SubantaProcessor.derive_pada("कृष्ण", 3, 1, self.logger)
        print(f"  Result: {res}")
        self.assertEqual(res, "कृष्णेन")  # R6 (Ta->Ina) + R20 (Sandhi)

    # --- TYPE 2: HARI-WAT (Like Hari) ---
    def test_kavi_like_hari(self):
        """Test: Kavi (Poet) should behave exactly like Hari"""
        print("\n" + "=" * 60)
        print("🚀 GENERALIZATION 2: Kavi (Like Hari)")

        # 1.3: Kavi + Jas -> Kavayaḥ (Guna + Ayadi)
        res = SubantaProcessor.derive_pada("कवि", 1, 3, self.logger)
        print(f"  Result: {res}")
        self.assertEqual(res, "कवयः")

        # 4.1: Kavi + Ne -> Kavaye
        res = SubantaProcessor.derive_pada("कवि", 4, 1, self.logger)
        print(f"  Result: {res}")
        self.assertEqual(res, "कवये")

    # --- TYPE 3: GURU-WAT (Like Guru) ---
    def test_bhanu_like_guru(self):
        """Test: Bhānu (Sun) should behave exactly like Guru"""
        print("\n" + "=" * 60)
        print("🚀 GENERALIZATION 3: Bhānu (Like Guru)")

        # 1.3: Bhanu + Jas -> Bhanavaḥ
        res = SubantaProcessor.derive_pada("भानु", 1, 3, self.logger)
        print(f"  Result: {res}")
        self.assertEqual(res, "भानवः")

        # 6.1: Bhanu + Ngas -> Bhanoh
        res = SubantaProcessor.derive_pada("भानु", 6, 1, self.logger)
        print(f"  Result: {res}")
        self.assertEqual(res, "भानोः")

        # 7.1: Bhanu + Ni -> Bhanau
        res = SubantaProcessor.derive_pada("भानु", 7, 1, self.logger)
        print(f"  Result: {res}")
        self.assertEqual(res, "भानौ")

    def test_vayu_natva(self):
        """Test: Vāyu (Wind) - Special check for Natva absence"""
        # Vayu + Ta -> Vayuna (Not Vayuna, because no R/Sh)
        # Wait, Vayu has no 'Ra' or 'Sha'. So it should be 'Vayunā'.
        # Guru -> Guruṇā (because of r). Vayu -> Vayunā.
        print("\n" + "=" * 60)
        print("🚀 GENERALIZATION 4: Vāyu (Natva Check)")
        res = SubantaProcessor.derive_pada("वायु", 3, 1, self.logger)
        print(f"  Result: {res}")
        self.assertEqual(res, "वायुना")  # Correct: No Natva


if __name__ == '__main__':
    unittest.main()