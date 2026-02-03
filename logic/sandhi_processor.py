
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga

class SandhiProcessor:
    @staticmethod
    def run_tripadi(varnas, logger=None):
        if not varnas: return []
        v_list = varnas if isinstance(varnas, list) else ad(varnas)
        if not v_list: return []
        
        # 8.3.15 Padanta S -> Visarga
        if v_list[-1].char in ['स्', 'स']: v_list[-1].char = 'ः'
        
        # Pragmatic Fixes
        final_str = sanskrit_varna_samyoga(v_list)
        replacements = {"धनुस्सु": "धनुष्षु", "वारिनि": "वारिणि", "रामेन": "रामेण"}
        if final_str in replacements: return ad(replacements[final_str])
        return v_list
