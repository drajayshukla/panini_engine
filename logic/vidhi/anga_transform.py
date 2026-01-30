"""
FILE: logic/vidhi/anga_transform.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Aṅga-Adhikāra (Stem Control)
REFERENCE: ७.१.८४ दिव औत्
"""
from core.phonology import Varna, sanskrit_varna_samyoga
from .engine_base import VidhiEngineBase

class AngaTransform(VidhiEngineBase):
    @staticmethod
    def apply_div_aut_7_1_84(anga_varnas, suffix_varnas):
        """[SUTRA]: दिव औत् (७.१.८४)"""
        if sanskrit_varna_samyoga(anga_varnas) != "दिव्":
            return anga_varnas, None

        # Check if suffix is 'Su' (Nominative Sg)
        suffix_str = "".join([s.char for s in suffix_varnas])
        if suffix_str not in ['स्', 'सुँ']:
            return anga_varnas, None

        old_char = anga_varnas[-1].char
        # Substitution: v -> au
        anga_varnas[-1] = Varna("औ")
        anga_varnas[-1].trace.append("७.१.८४")
        return anga_varnas, f"७.१.८४ ({old_char} -> औ)"

    @staticmethod
    def apply_goto_nit_7_1_90(suffix_varnas):
        """[SUTRA]: गोतो णित् (७.१.९०)"""
        if suffix_varnas:
            suffix_varnas[0].sanjnas.add("nit_vadbhava")
            return "७.१.९० (णिद्वद्भाव)"
        return None

    @staticmethod
    def apply_hal_nyab_6_1_68(varna_list):
        """[SUTRA]: हल्ङ्याब्भ्यो दीर्घात्... (६.१.६८)"""
        if not varna_list: return varna_list, None
        # Simplification: Su-lopa after certain endings
        if varna_list[-1].char == 'स्':
            varna_list.pop()
            return varna_list, "६.१.६८ (सु-लोपः)"
        return varna_list, None

    @staticmethod
    def apply_ti_lopa_6_4_143(varna_list):
        """[SUTRA]: टेः (६.४.१४३)"""
        if len(varna_list) < 2: return varna_list, None
        # Simple T-Lopa: removes the final syllable segment
        varna_list.pop()
        return varna_list, "६.४.१४३ (टि-लोपः)"