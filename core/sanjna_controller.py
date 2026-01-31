"""
FILE: core/sanjna_controller.py
PAS-v6.0 (Siddha) | PILLAR: Definitions & Cleaning (R3, R4)
"""
from .core_foundation import Varna, PratyaharaEngine, UpadeshaType

pe = PratyaharaEngine()

class SanjnaController:
    TAG_FACTORY = {
        'ञि': 'ñit', 'टु': 'ṭit', 'डु': 'dit',
        'क्': 'kit', 'ङ्': 'ngit', 'च्': 'cit', 'ञ्': 'ñit',
        'ण्': 'ṇit', 'प्': 'pit', 'म्': 'mit', 'श्': 'śit', 'ष्': 'ṣit'
    }
    LASHAKVA = ['ल्', 'श्', 'क्', 'ख्', 'ग्', 'घ्', 'ङ्']
    CHU_VARGA = ['च्', 'छ्', 'ज्', 'झ्', 'ञ्']
    TU_VARGA  = ['ट्', 'ठ्', 'ड्', 'ढ्', 'ण्']

    @staticmethod
    def run_it_prakaran(varna_list, source_type, is_taddhita=False):
        if not varna_list: return [], []
        it_indices = set()
        trace = []

        # 1.3.2 Upadeshe Aj Anunasika
        for i, v in enumerate(varna_list):
            if v.char == 'ँ':
                it_indices.add(i)
                if i > 0 and varna_list[i - 1].is_vowel:
                    varna_list[i - 1].sanjnas.add("it")
                    it_indices.add(i - 1)
                    trace.append("1.3.2")

        first = varna_list[0].char
        if source_type == UpadeshaType.DHATU:
            if first in ['ञि', 'टु', 'डु'] or (len(varna_list) > 1 and first == 'ञ्' and varna_list[1].char == 'इ'):
                it_indices.add(0)
                if first == 'ञ्': it_indices.add(1)
                trace.append("1.3.5")

        # [CRITICAL FIX]: Vibhakti is also checked here
        elif source_type in [UpadeshaType.PRATYAYA, UpadeshaType.VIBHAKTI]:
            if first in SanjnaController.CHU_VARGA or first in SanjnaController.TU_VARGA:
                it_indices.add(0)
                trace.append("1.3.7 (Chuṭū)")
            elif not is_taddhita and first in SanjnaController.LASHAKVA:
                it_indices.add(0)
                trace.append("1.3.8 (Lashakva)")

        # 1.3.3 Halantyam
        last_idx = len(varna_list) - 1
        if last_idx >= 0 and last_idx not in it_indices:
            last_char = varna_list[last_idx].char
            is_vibhakti_blocked = (source_type == UpadeshaType.VIBHAKTI and last_char in ['त्', 'थ्', 'द्', 'ध्', 'न्', 'स्', 'म्'])
            if varna_list[last_idx].is_consonant and not is_vibhakti_blocked:
                it_indices.add(last_idx)
                trace.append("1.3.3")

        inherited_tags = set()
        for idx in it_indices:
            char_clean = varna_list[idx].char.replace('्', '')
            if char_clean in SanjnaController.TAG_FACTORY:
                inherited_tags.add(SanjnaController.TAG_FACTORY[char_clean])

        cleaned = [v for i, v in enumerate(varna_list) if i not in it_indices]
        if cleaned and inherited_tags:
            cleaned[0].sanjnas.update(inherited_tags)
        return cleaned, trace

    @staticmethod
    def is_vriddhi_1_1_1(char): return char == 'आ' or pe.is_in(char, "ऐच्")
    @staticmethod
    def is_guna_1_1_2(char): return char == 'अ' or pe.is_in(char, "एङ्")
    @staticmethod
    def is_samyoga_1_1_7(varna_list):
        if len(varna_list) < 2: return False
        for i in range(len(varna_list) - 1):
            if varna_list[i].is_consonant and varna_list[i + 1].is_consonant: return True
        return False
    @staticmethod
    def is_laghu_1_4_10(varna_list, index):
        if index >= len(varna_list): return False
        v = varna_list[index]
        if not v.is_vowel: return False
        is_short = v.char in ['अ', 'इ', 'उ', 'ऋ', 'ऌ']
        if not is_short: return False
        if index < len(varna_list) - 2:
            if varna_list[index + 1].is_consonant and varna_list[index + 2].is_consonant: return False
        return True
    @staticmethod
    def is_nadi_1_4_3(stem_varnas):
        if not stem_varnas: return False
        return stem_varnas[-1].char in ['ई', 'ऊ']
    @staticmethod
    def is_ghi_1_4_7(stem_varnas):
        if not stem_varnas: return False
        return stem_varnas[-1].char in ['इ', 'उ']