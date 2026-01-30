"""
FILE: tests/final_architecture_test.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Full-System Validation
DESCRIPTION: Verifies the integrity of all modular sub-systems.
"""

import pytest
from core.phonology import ad, sanskrit_varna_samyoga
from logic.vidhi import VidhiEngine
from logic.sanjna import SanjnaEngine
from logic.it_engine import ItEngine
from core.upadesha_registry import UpadeshaType


class TestFullSystemIntegrity:

    def test_sanjna_module_integrity(self):
        """Tests definitions_1_1.py and morpho_sanjna.py"""
        print("\n🔍 Checking Sanjna Module...")

        # Test 1.1.2 Guna Designation
        v_a = ad("अ")[0]
        assert SanjnaEngine.is_guna_1_1_2(v_a) is True

        # Test 1.4.10 Laghu Designation (Budh -> u is Laghu)
        anga_budh = ad("बुध्")
        assert SanjnaEngine.is_laghu_1_4_10(anga_budh, 1) is True

        # Test 1.1.27 Sarvanama Gana
        assert SanjnaEngine.is_sarvanama_1_1_27("सर्व") is True
        print("   ✅ Sanjna Engine: OK")

    def test_it_prakaran_module(self):
        """Tests it_prakaranam.py via ItEngine"""
        print("\n🔍 Checking It-Prakaranam...")

        # Test 1.3.3 (Halantyam) and 1.3.8 (Lashakva)
        # Input: 'ghañ' (घञ्) -> Result: 'a'
        suffix = ad("घञ्")
        clean, _ = ItEngine.run_it_prakaran(suffix, UpadeshaType.PRATYAYA)
        assert sanskrit_varna_samyoga(clean) == "अ"
        print("   ✅ It-Prakaranam: OK")

    def test_vriddhi_and_sandhi_pipeline(self):
        """Tests guna_vriddhi.py and sandhi_engine.py"""
        print("\n🔍 Checking Guna/Vriddhi + Sandhi Pipeline...")

        # Scenario: Nī + aka (ṇit) -> Nāyaka
        anga = ad("नी")
        suffix = ad("अक")
        suffix[0].sanjnas.add("ṇit")  # Force trigger for 7.2.115

        # 1. Vriddhi (7.2.115)
        anga, _ = VidhiEngine.apply_aco_niti_7_2_115(anga, suffix)
        assert sanskrit_varna_samyoga(anga) == "नै"

        # 2. Ayadi Sandhi (6.1.78)
        anga, _ = VidhiEngine.apply_ayadi_6_1_78(anga, suffix)
        assert sanskrit_varna_samyoga(anga) == "नाय्"
        print("   ✅ Vidhi Pipeline: OK")

    def test_tripadi_terminal_logic(self):
        """Tests tripadi.py"""
        print("\n🔍 Checking Tripadi (Final Phonology)...")

        # Scenario: suhṛd -> suhṛt (Chartva 8.4.56)
        word = ad("सुहृद्")
        final, rule = VidhiEngine.apply_chartva_8_4_56(word)
        assert sanskrit_varna_samyoga(final) == "सुहृत्"
        assert "८.४.५६" in rule
        print("   ✅ Tripadi: OK")


if __name__ == "__main__":
    pytest.main([__file__])