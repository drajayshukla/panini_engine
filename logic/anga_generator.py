"""
FILE: logic/anga_generator.py - PAS-v8.3
TASK 3: Action Root + Vikarana -> Functional Anga
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga
from logic.anga_processor import AngaProcessor

class AngaGenerator:
    @staticmethod
    def create_bhvadi_anga(dhatu_varnas, logger=None):
        """Root + Sap -> Anga with Guna."""
        # 3.1.68: Sap Vikarana (a)
        sap = ad("अ")
        
        # 7.3.84: Apply Guna to Root before Sap
        updated_root, rule = AngaProcessor.apply_guna_7_3_84(list(dhatu_varnas), sap)
        
        if logger and rule:
            logger.log(rule, "Guna Transformation", sanskrit_varna_samyoga(updated_root), updated_root)

        # 6.1.78: Ayadi Logic (e.g., bho + a -> bhav + a)
        # Simplified for streamline
        final_anga_text = sanskrit_varna_samyoga(updated_root + sap)
        final_anga_text = final_anga_text.replace("ओअ", "अव").replace("एअ", "अय")
        
        return ad(final_anga_text)
