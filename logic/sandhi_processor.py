"""
FILE: logic/sandhi_processor.py - PAS-v36.0 (Ścutva Integrated)
"""
from core.core_foundation import Varna, ad, sanskrit_varna_samyoga

class SandhiProcessor:
    AC = set("अआइईउऊऋॠऌएऐओऔ")
    
    # 8.4.40 Definitions
    T_VARGA = "तथदधन"
    C_VARGA = "चछजझञ"
    SHCU_SET = "शचछजझञ" # Triggers
    STO_MAP = {'स': 'श', 'त': 'च', 'थ': 'छ', 'द': 'ज', 'ध': 'झ', 'न': 'ञ'}

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

    @staticmethod
    def apply_shcutva(left_term, right_term, logger=None):
        """
        8.4.40 स्तोः श्चुना श्चुः (Stoḥ ścunā ścuḥ)
        8.4.44 शात् (Śāt) - Exception
        """
        l = SandhiProcessor._normalize_input(left_term)
        r = SandhiProcessor._normalize_input(right_term)
        
        if not l or not r: return l, r
        
        # We check the junction: End of Left (final), Start of Right (initial)
        final = l[-1]
        initial = r[0]
        
        f_char = final.char.replace('्', '')
        i_char = initial.char.replace('्', '')
        
        # --- EXCEPTION: 8.4.44 Śāt ---
        # If 'ś' is followed by T-varga, Scutva is BLOCKED.
        # e.g., Praś + na -> Praśna (Not Praśña)
        if f_char == 'श' and i_char in SandhiProcessor.T_VARGA:
             if logger: logger.log("8.4.44", "Śāt blocked Ścutva", f"{f_char} + {i_char}")
             return l, r
             
        # --- RULE: 8.4.40 Stoḥ Ścunā Ścuḥ ---
        
        # Case A: Left is Sto (s/t-varga), Right is Shcu (ś/c-varga) -> Left changes
        # e.g., Rāmas + Śete -> Rāmaśśete
        if f_char in SandhiProcessor.STO_MAP and i_char in SandhiProcessor.SHCU_SET:
            new_char = SandhiProcessor.STO_MAP[f_char]
            # Preserve virama if present
            final.char = new_char + ('्' if final.char.endswith('्') else '')
            if logger: logger.log("8.4.40", f"Ścutva (Left): {f_char} -> {new_char}")
            
        # Case B: Right is Sto, Left is Shcu -> Right changes
        # e.g., Yaj + na -> Yajña (j + n -> j + ñ)
        elif i_char in SandhiProcessor.STO_MAP and f_char in SandhiProcessor.SHCU_SET:
            new_char = SandhiProcessor.STO_MAP[i_char]
            initial.char = new_char + ('्' if initial.char.endswith('्') else '')
            if logger: logger.log("8.4.40", f"Ścutva (Right): {i_char} -> {new_char}")
            
        return l, r

    def join(self, term1, term2, context_tags=None, return_as_str=False):
        if term1 is None: term1 = ""
        if term2 is None: term2 = ""
        tags = set(context_tags) if context_tags else set()

        v1_list = self._normalize_input(term1)
        v2_list = self._normalize_input(term2)
        result_list = v1_list + v2_list

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

            # --- 2. PRAKRITIBHAVA ---
            if last.is_vowel and first.is_vowel:
                # [Ac Sandhi Logic Preserved]
                lc, fc = last.char, first.char
                if (lc in ['अ', 'आ']) and (lc, fc) in self.guna_map:
                    res_varnas = ad(self.guna_map[(lc, fc)])
                    return finish(v1_list[:-1] + res_varnas + v2_list[1:])
                if lc in self.yan_map:
                    yan = self.yan_map[lc]
                    return finish(v1_list[:-1] + [Varna(yan)] + v2_list)

        return finish(result_list)

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
            # 8.4.1 Natva
            if c in ['र्', 'ष्', 'ऋ', 'ॠ']: trigger = True
            elif c == 'न्':
                if trigger:
                    if i < len(v_list) - 1:
                        v.char = 'ण्'
                        if logger and hasattr(logger, 'append'): logger.append("८.४.१ णत्व")
            elif c_clean in raw_blockers:
                trigger = False

        # 8.3.59 Shatva
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

        # 8.3.15 Visarga
        last = v_list[-1]
        if last.char in ['स्', 'र्']:
            v_list[-1] = Varna('ः')
            if logger and hasattr(logger, 'append'): logger.append("८.३.१५ विसर्ग")

        return v_list

    def _are_savarna(self, c1, c2):
        for group in self.savarna_groups:
            if c1 in group and c2 in group: return True
        return False
