"""
FILE: logic/sandhi_processor.py - PAS-v23.0 (Hindi Localization)
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga

class SandhiProcessor:
    AC = set("अआइईउऊऋॠऌएऐओऔ")
    HAL = set("कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह")

    def __init__(self):
        self.yan_map = {'इ': 'य्', 'ई': 'य्', 'उ': 'व्', 'ऊ': 'व्', 'ऋ': 'र्', 'ॠ': 'र्', 'ऌ': 'ल्'}
        self.guna_map = {
            ('अ', 'इ'): 'ए', ('अ', 'ई'): 'ए', ('आ', 'इ'): 'ए', ('आ', 'ई'): 'ए',
            ('अ', 'उ'): 'ओ', ('अ', 'ऊ'): 'ओ', ('आ', 'उ'): 'ओ', ('आ', 'ऊ'): 'ओ',
            ('अ', 'ऋ'): 'अर्', ('अ', 'ॠ'): 'अर्', ('आ', 'ऋ'): 'अर्', ('आ', 'ॠ'): 'अर्'
        }
        self.vriddhi_map = {
            ('अ', 'ए'): 'ऐ', ('अ', 'ऐ'): 'ऐ', ('आ', 'ए'): 'ऐ', ('आ', 'ऐ'): 'ऐ',
            ('अ', 'ओ'): 'औ', ('अ', 'औ'): 'औ', ('आ', 'ओ'): 'औ', ('आ', 'औ'): 'औ'
        }
        self.ayadi_map = {'ए': 'अय्', 'ओ': 'अव्', 'ऐ': 'आय्', 'औ': 'आव्'}
        self.savarna_groups = [{'अ', 'आ'}, {'इ', 'ई'}, {'उ', 'ऊ'}, {'ऋ', 'ॠ'}]
        self.dirgha_map = {'अ': 'आ', 'आ': 'आ', 'इ': 'ई', 'ई': 'ई', 'उ': 'ऊ', 'ऊ': 'ऊ', 'ऋ': 'ॠ', 'ॠ': 'ॠ'}

    @staticmethod
    def _normalize_input(term):
        if isinstance(term, str): return ad(term)
        elif isinstance(term, list):
            if term and isinstance(term[0], str): return [Varna(c) for c in term]
            return term 
        return []

    def join(self, term1, term2, context_tags=None, return_as_str=False):
        if term1 is None: term1 = ""
        if term2 is None: term2 = ""
        tags = set(context_tags) if context_tags else set()

        v1_list = self._normalize_input(term1)
        v2_list = self._normalize_input(term2)
        result_list = v1_list + v2_list

        if v1_list and v2_list:
            last = v1_list[-1]
            first = v2_list[0]

            if last.is_vowel and first.is_vowel:
                lc, fc = last.char, first.char
                if "Dual" in tags and lc in ['ई', 'ऊ', 'ए']: pass # Pragrhya
                elif lc in self.ayadi_map:
                    res_varnas = ad(self.ayadi_map[lc])
                    result_list = v1_list[:-1] + res_varnas + v2_list
                elif self._are_savarna(lc, fc):
                    long = self.dirgha_map.get(lc, lc)
                    result_list = v1_list[:-1] + [Varna(long)] + v2_list[1:]
                elif (lc in ['अ', 'आ']) and (lc, fc) in self.vriddhi_map:
                    res_char = self.vriddhi_map[(lc, fc)]
                    result_list = v1_list[:-1] + [Varna(res_char)] + v2_list[1:]
                elif (lc in ['अ', 'आ']) and (lc, fc) in self.guna_map:
                    res_varnas = ad(self.guna_map[(lc, fc)])
                    result_list = v1_list[:-1] + res_varnas + v2_list[1:]
                elif lc in self.yan_map:
                    yan = self.yan_map[lc]
                    result_list = v1_list[:-1] + [Varna(yan)] + v2_list

        if return_as_str: return sanskrit_varna_samyoga(result_list)
        return result_list

    @staticmethod
    def apply_ac_sandhi(term1, term2):
        engine = SandhiProcessor()
        res_list = engine.join(term1, term2, return_as_str=False)
        return res_list, "अच्-सन्धि (यण्/गुण/वृद्धि/अयादि)"

    @staticmethod
    def run_tripadi(varnas, logger=None):
        if not varnas: return []
        v_list = SandhiProcessor._normalize_input(varnas)
        if not v_list: return []

        # 1. Natva
        trigger = False
        raw_blockers = set("चछजझञटठडढणतथदधनलशस") 
        for i, v in enumerate(v_list):
            c = v.char
            c_clean = c.replace('्', '')
            if c in ['र्', 'ष्', 'ऋ', 'ॠ']: trigger = True
            elif c == 'न्':
                if trigger:
                    if i < len(v_list) - 1:
                        v.char = 'ण्'
                        if logger and hasattr(logger, 'append'): logger.append("८.४.१ रषाभ्यां नो णः समानपदे (णत्व)")
            elif c_clean in raw_blockers:
                trigger = False

        # 2. Satva
        in_ku_raw = set("इईउऊऋॠएऐओऔकखगघ")
        for i in range(1, len(v_list)):
            curr = v_list[i]
            prev = v_list[i-1]
            if curr.char == 'स्':
                if i == len(v_list) - 1: continue 
                prev_clean = prev.char.replace('्', '')
                if prev_clean in in_ku_raw or prev.char == 'र्':
                    curr.char = 'ष्'
                    if logger and hasattr(logger, 'append'): logger.append("८.३.५९ आदेशप्रत्यययोः (षत्व)")

        # 3. Visarga
        last = v_list[-1]
        if last.char in ['स्', 'र्']:
            v_list[-1] = Varna('ः')
            if logger and hasattr(logger, 'append'): logger.append("८.३.१५ खरवसानयोर्विसर्जनीयः (विसर्ग)")

        return v_list

    def _are_savarna(self, c1, c2):
        for group in self.savarna_groups:
            if c1 in group and c2 in group: return True
        return False
