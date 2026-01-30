"""
FILE: logic/vidhi/meta_rules.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Paribhāṣā & Saṃjñā Extensions
REFERENCE: १.१.५ क्ङिति च
"""
from core.phonology import Varna

class MetaRules:
    @staticmethod
    def is_kniti_1_1_5(suffix_varnas):
        """[SUTRA]: क्ङिति च (१.१.५)"""
        if not suffix_varnas: return False
        first = suffix_varnas[0]
        return bool({'kit', 'gnit', 'ngit'} & first.sanjnas)

    @staticmethod
    def apply_hrasva_napumsaka_1_2_47(varna_list):
        """[SUTRA]: ह्रस्वो नपुंसके प्रातिपदिकस्य (१.२.४७)"""
        if not varna_list: return varna_list, None
        last = varna_list[-1]
        mapping = {'आ': 'अ', 'ई': 'इ', 'ऊ': 'उ'}
        if last.char in mapping:
            old = last.char
            last.char = mapping[old]
            return varna_list, f"१.२.४७ ({old}->{last.char})"
        return varna_list, None