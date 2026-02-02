"""
FILE: logic/sandhi_processor.py - PAS-v35.1 (Pluta Fix)
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga

class SandhiProcessor:
    AC = set("अआइईउऊऋॠऌएऐओऔ")

    PRADI = {
        "प्र", "परा", "अप", "सम्", "अनु", "अव", "निस्", "निर्", "दुस्", "दुर्", 
        "वि", "आङ्", "नि", "अधि", "अपि", "अति", "सु", "उत्", "अभि", "प्रति", "परि", "उप",
        "आ"
    }

    SHAKANDHVADI = {
        "शक": ["अन्धु"], "कर्क": ["अन्धु"], "कुल": ["अटा"], "सीमन्": ["अन्तः"],
        "मनस्": ["ईषा"], "हल": ["ईषा"], "लाङ्गल": ["ईषा"], "पतत्": ["अञ्जलिः"],
        "सार": ["अङ्ग"], "मृत": ["अण्ड"]
    }

    def __init__(self):
        self.yan_map = {'इ': 'य्', 'ई': 'य्', 'उ': 'व्', 'ऊ': 'व्', 'ऋ': 'र्', 'ॠ': 'र्', 'ऌ': 'ल्'}
        self.guna_map = {
            ('अ', 'इ'): 'ए', ('अ', 'ई'): 'ए', ('आ', 'इ'): 'ए', ('आ', 'ई'): 'ए',
            ('अ', 'उ'): 'ओ', ('अ', 'ऊ'): 'ओ', ('आ', 'उ'): 'ओ', ('आ', 'ऊ'): 'ओ',
            ('अ', 'ऋ'): 'अर्', ('अ', 'ॠ'): 'अर्', ('आ', 'ऋ'): 'अर्', ('आ', 'ॠ'): 'अर्',
            ('अ', 'ऌ'): 'अल्', ('अ', 'ॡ'): 'अल्', ('आ', 'ऌ'): 'अल्', ('आ', 'ॡ'): 'अल्'
        }
        self.vriddhi_map = {
            ('अ', 'ए'): 'ऐ', ('अ', 'ऐ'): 'ऐ', ('आ', 'ए'): 'ऐ', ('आ', 'ऐ'): 'ऐ',
            ('अ', 'ओ'): 'औ', ('अ', 'औ'): 'औ', ('आ', 'ओ'): 'औ', ('आ', 'औ'): 'औ'
        }
        self.ayadi_map = {'ए': 'अय्', 'ओ': 'अव्', 'ऐ': 'आय्', 'औ': 'आव्'}
        self.savarna_groups = [{'अ', 'आ'}, {'इ', 'ई'}, {'उ', 'ऊ'}, {'ऋ', 'ॠ', 'ऌ', 'ॡ'}]
        self.dirgha_map = {'अ': 'आ', 'आ': 'आ', 'इ': 'ई', 'ई': 'ई', 'उ': 'ऊ', 'ऊ': 'ऊ', 'ऋ': 'ॠ', 'ॠ': 'ॠ', 'ऌ': 'ॠ', 'ॡ': 'ॠ'}

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

        # Use RAW strings for checks to avoid normalization loss (e.g. Pluta '3')
        t1_raw = term1 if isinstance(term1, str) else sanskrit_varna_samyoga(term1)
        t2_raw = term2 if isinstance(term2, str) else sanskrit_varna_samyoga(term2)

        # Internal standardized strings
        t1_str = sanskrit_varna_samyoga(v1_list)
        t2_str = sanskrit_varna_samyoga(v2_list)

        def finish(res):
            if return_as_str: return sanskrit_varna_samyoga(res)
            return res

        # --- 1. SHAKANDHVADI ---
        for base, suffixes in SandhiProcessor.SHAKANDHVADI.items():
            if t1_str.startswith(base):
                for s in suffixes:
                    if t2_str.startswith(s):
                        if base in ["मनस्", "सीमन्", "पतत्"]: res = v1_list[:-2] + v2_list
                        else: res = v1_list[:-1] + v2_list
                        return finish(res)

        if v1_list and v2_list:
            last = v1_list[-1]
            first = v2_list[0]

            # --- 2. PRAKRITIBHAVA (6.1.125) - SUPREME BLOCKER ---
            # PLUTA Check on RAW string
            is_pluta = t1_raw.endswith("३") or t1_raw.endswith("3")
            if is_pluta and first.is_vowel:
                # If v1_list lost the 3, we must restore it for the output
                if not (t1_str.endswith("३") or t1_str.endswith("3")):
                    # Manually append 3 if missing
                    v1_list.append(Varna("३"))
                space = Varna(" ")
                return finish(v1_list + [space] + v2_list)

            # Pragrhya Check
            if first.is_vowel:
                is_dual_pragrhya = "Dual" in tags and last.char in ['ई', 'ऊ', 'ए']
                is_ami_amu = t1_str in ["अमी", "अमू"]
                is_ot_nipata = "Nipata" in tags and last.char == 'ओ'

                if is_dual_pragrhya or is_ami_amu or is_ot_nipata:
                    space = Varna(" ")
                    return finish(v1_list + [space] + v2_list)

            if last.is_vowel and first.is_vowel:
                lc, fc = last.char, first.char
                is_upasarga = t1_str in SandhiProcessor.PRADI or t1_str == "आ"

                # --- 6.1.107 AMI PURVAH ---
                is_am = "Am" in tags or t2_str == "अम्"
                is_ak = lc in ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ॠ', 'ऌ']
                if is_am and is_ak: return finish(v1_list + v2_list[1:])

                # --- EXCEPTIONS ---
                if "Augment-Aat" in tags and lc == 'आ':
                    if fc in ['इ', 'ई']: return finish(v1_list[:-1] + [Varna("ऐ")] + v2_list[1:])
                    elif fc in ['उ', 'ऊ']: return finish(v1_list[:-1] + [Varna("औ")] + v2_list[1:])
                    elif fc in ['ऋ', 'ॠ']: return finish(v1_list[:-1] + [Varna("आ"), Varna("र्")] + v2_list[1:])
                    elif fc in ['ए', 'ऐ']: return finish(v1_list[:-1] + [Varna("ऐ")] + v2_list[1:])
                    elif fc in ['ओ', 'औ']: return finish(v1_list[:-1] + [Varna("औ")] + v2_list[1:])

                if t1_str.endswith("अक्ष") and t2_str.startswith("ऊहिनी"):
                    return finish(v1_list[:-1] + [Varna("औ")] + v2_list[1:])
                if t1_str == "स्व" and t2_str.startswith("ईर"):
                    return finish(v1_list[:-1] + [Varna("ऐ")] + v2_list[1:])
                if t1_str == "प्र" and (t2_str.startswith("ऊह") or t2_str.startswith("ऊढ") or t2_str.startswith("एष") or t2_str.startswith("एष्य")):
                    if t2_str.startswith("ऊ"): return finish(v1_list[:-1] + [Varna("औ")] + v2_list[1:])
                    elif t2_str.startswith("ए"): return finish(v1_list[:-1] + [Varna("ऐ")] + v2_list[1:])

                if is_upasarga and fc == 'ऋ' and "Dhatu" in tags:
                     return finish(v1_list[:-1] + [Varna("आ"), Varna("र्")] + v2_list[1:])

                if ("Tritiya" in tags or (t1_str in ["प्र", "वत्सतर", "कम्बल", "वसन", "ऋण", "दश"] and t2_str.startswith("ऋण"))) and fc == 'ऋ':
                    return finish(v1_list[:-1] + [Varna("आ"), Varna("र्")] + v2_list[1:])

                if (lc in ['अ', 'आ']) and (t2_str.startswith("एति") or t2_str.startswith("एध") or t2_str.startswith("ऊठ्") or t2_str.startswith("ऊह")):
                    if fc == 'ए': return finish(v1_list[:-1] + [Varna("ऐ")] + v2_list[1:])
                    elif fc in ['उ', 'ऊ', 'ओ']: return finish(v1_list[:-1] + [Varna("औ")] + v2_list[1:])

                # --- 6.1.94 PARARUPA ---
                if is_upasarga and (lc in ['अ', 'आ']) and (fc in ['ए', 'ओ']):
                    return finish(v1_list[:-1] + v2_list)

                # --- STANDARD RULES ---
                if "Vibhakti-1-2" in tags and lc in ['अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ॠ']:
                     long = self.dirgha_map.get(lc, lc)
                     return finish(v1_list[:-1] + [Varna(long)] + v2_list[1:])

                if (lc == 'अ' and "Pada" not in tags) and (fc in ['अ', 'ए', 'ओ']):
                    return finish(v1_list[:-1] + v2_list)

                if "Dual" in tags and lc in ['ई', 'ऊ', 'ए']:
                    space = Varna(" ")
                    return finish(v1_list + [space] + v2_list)

                if "Pada" in tags and lc in ['ए', 'ओ'] and fc == 'अ':
                    return finish(v1_list + [Varna('ऽ')] + v2_list[1:])

                if lc in self.ayadi_map:
                    res_varnas = ad(self.ayadi_map[lc])
                    return finish(v1_list[:-1] + res_varnas + v2_list)

                if self._are_savarna(lc, fc):
                    long = self.dirgha_map.get(lc, lc)
                    return finish(v1_list[:-1] + [Varna(long)] + v2_list[1:])

                if (lc in ['अ', 'आ']) and (lc, fc) in self.vriddhi_map:
                    res_char = self.vriddhi_map[(lc, fc)]
                    return finish(v1_list[:-1] + [Varna(res_char)] + v2_list[1:])

                if (lc in ['अ', 'आ']) and (lc, fc) in self.guna_map:
                    res_varnas = ad(self.guna_map[(lc, fc)])
                    return finish(v1_list[:-1] + res_varnas + v2_list[1:])

                if lc in self.yan_map:
                    yan = self.yan_map[lc]
                    return finish(v1_list[:-1] + [Varna(yan)] + v2_list)

        return finish(result_list)

    @staticmethod
    def apply_ac_sandhi(term1, term2):
        engine = SandhiProcessor()
        res_list = engine.join(term1, term2, return_as_str=False)
        return res_list, "अच्-सन्धि"

    @staticmethod
    def run_tripadi(varnas, logger=None):
        if not varnas: return []
        v_list = SandhiProcessor._normalize_input(varnas)
        if not v_list: return []

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
                        if logger and hasattr(logger, 'append'): logger.append("८.४.१ णत्व")
            elif c_clean in raw_blockers:
                trigger = False

        in_ku_raw = set("इईउऊऋॠएऐओऔकखगघ")
        for i in range(1, len(v_list)):
            curr = v_list[i]
            prev = v_list[i-1]
            if curr.char == 'स्':
                if i == len(v_list) - 1: continue 
                prev_clean = prev.char.replace('्', '')
                if prev_clean in in_ku_raw or prev.char == 'र्':
                    curr.char = 'ष्'
                    if logger and hasattr(logger, 'append'): logger.append("८.३.५९ षत्व")

        last = v_list[-1]
        if last.char in ['स्', 'र्']:
            v_list[-1] = Varna('ः')
            if logger and hasattr(logger, 'append'): logger.append("८.३.१५ विसर्ग")

        return v_list

    def _are_savarna(self, c1, c2):
        for group in self.savarna_groups:
            if c1 in group and c2 in group: return True
        return False
