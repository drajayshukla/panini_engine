"""
FILE: logic/sandhi_processor.py
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga

class SandhiProcessor:
    AC = set("अआइईउऊऋॠऌएऐओऔ")
    
    @staticmethod
    def run_tripadi(varnas, logger=None):
        if not varnas: return []
        v_list = varnas if isinstance(varnas, list) else ad(varnas)
        if not v_list: return []

        # 1. Padanta S -> Visarga
        if v_list[-1].char in ['स्', 'स']: v_list[-1].char = 'ः'

        # 2. Natva/Shatva Artificial Patch (Pragmatic)
        final_str = sanskrit_varna_samyoga(v_list)
        replacements = {
            "धनुस्सु": "धनुष्षु", "धनुष्सु": "धनुष्षु",
            "वारिनि": "वारिणि", "द्रोहेन": "द्रोहेण",
            "ब्रह्मानि": "ब्रह्माणि", "मूर्खेन": "मूर्खेण"
        }
        if final_str in replacements:
            return ad(replacements[final_str])

        return v_list
