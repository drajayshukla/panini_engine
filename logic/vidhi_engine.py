# logic/vidhi_engine.py

from core.upadesha_registry import Upadesha
from logic.anga_adhikara_wrapper import angasya_rule

class VidhiEngine:
    """
    विधि-सञ्चालक: (The Operational Engine)
    Zone 3: Performs actual transformations (Sūtra 1.1.x, 6.1.x, etc.)
    """

    # --- CHAPTER 1: Sañjñā & General Rules ---

    @staticmethod
    def apply_hrasva_napumsaka_1_2_47(varna_list):
        """१.२.४७ ह्रस्वो नपुंसके प्रातिपदिकस्य"""
        v_list = list(varna_list)
        if len(v_list) >= 2 and v_list[-1].char == 'स्':
            target_vowel = v_list[-2].char
            mapping = {'आ': 'अ', 'ई': 'इ', 'ऊ': 'उ', 'ए': 'इ', 'ओ': 'उ'}
            if target_vowel in mapping:
                v_list[-2] = Upadesha(mapping[target_vowel], "1.2.47")
                return v_list, f"१.२.४७ (ह्रस्वादेशः: {target_vowel} -> {mapping[target_vowel]})"
        return varna_list, None

    # --- CHAPTER 6: Transformations & Elisions ---

    @staticmethod
    def apply_hal_nyab_6_1_68(varna_list):
        """६.१.६८ (हल्ङ्याब्भ्यो...): Removal of 'स्'"""
        v_list = list(varna_list)
        if v_list and v_list[-1].char == 'स्':
            last_chars_str = "".join([v.char for v in v_list[-4:]])
            if any(v in last_chars_str for v in ['आ', 'ई', 'ऊ']):
                v_list.pop()
                return v_list, "६.१.६८ (हल्ङ्याब्भ्यो... अपृक्त-लोप)"
        return varna_list, None

    @staticmethod
    def apply_ami_purvah_6_1_107(varna_list):
        """६.१.१०७ अमि पूर्वः"""
        v_list = list(varna_list)
        for i in range(len(v_list) - 2):
            if v_list[i].char == 'अ' and v_list[i+1].char == 'अ' and v_list[i+2].char == 'म्':
                v_list.pop(i+1)
                return v_list, "६.१.१०७ (अमि पूर्वः - पूर्वरूपम्)"
        return varna_list, None

    # --- ANGA ADHIKARA (Decorated Rules 6.4.1 - 7.4.120) ---

    @staticmethod
    @angasya_rule("6.4.8")
    def apply_upadha_dirgha_6_4_8(anga, nimitta):
        """६.४.८ सर्वनामस्थाने चासम्बुद्धौ"""
        v_list = list(anga)
        for i in range(len(v_list) - 1, 0, -1):
            if v_list[i].char == 'न्' and v_list[i-1].char == 'अ':
                v_list[i-1] = Upadesha('आ', "6.4.8")
                return v_list, "६.४.८ (उपधा दीर्घ)"
        return anga, None

    @staticmethod
    @angasya_rule("6.4.143")
    def apply_ti_lopa_6_4_143(anga, nimitta):
        """६.४.१४३ टेः (Ti-Lopa)"""
        v_list = list(anga)
        if v_list and v_list[-1].char == 'अ':
            v_list.pop()
            return v_list, "६.४.१४३ (टेः - टि-लोपः)"
        return anga, None

    @staticmethod
    @angasya_rule("7.1.24")
    def ato_am_7_1_24(anga, nimitta):
        """७.१.२४ अतोऽम्"""
        # Note: In a strict engine, this rule replaces the NIMITTA (suffix)
        # We modify the nimitta segment and return
        new_nimitta = [Upadesha('अ', "7.1.24"), Upadesha('म्', "7.1.24")]
        return anga, "७.१.२४ (अतोऽम्)"

    @staticmethod
    @angasya_rule("7.1.94")
    def apply_anang_7_1_94(anga, nimitta):
        """७.१.९४ ऋदुशनस्... (अनङ्-आदेशः)"""
        v_list = list(anga)
        for i in range(len(v_list) - 1, -1, -1):
            if v_list[i].char == 'ऋ':
                v_list.pop(i)
                v_list.insert(i, Upadesha('अ', "7.1.94"))
                v_list.insert(i+1, Upadesha('न्', "7.1.94"))
                return v_list, "७.१.९४ (अनङ्-आदेशः)"
        return anga, None

    @staticmethod
    @angasya_rule("7.2.115")
    def apply_vriddhi_7_2_115(anga, nimitta):
        """७.२.११५ अचो ञ्णिति (Vṛddhi)"""
        v_list = list(anga)
        for i in range(len(v_list)):
            if v_list[i].char == 'ओ':
                v_list[i] = Upadesha('औ', "7.2.115")
                return v_list, "७.२.११५ (वृद्धिः)"
        return anga, None

    # --- CHAPTER 8: Phonetic Polishing (Tripādī) ---

    @staticmethod
    def apply_nalopa_8_2_7(varna_list):
        """८.२.७ नलोपः प्रातिपदिकान्तस्य"""
        v_list = list(varna_list)
        if v_list and v_list[-1].char == 'न्':
            v_list.pop()
            return v_list, "८.२.७ (नलोपः)"
        return varna_list, None

    @staticmethod
    def apply_rutva_8_2_66(varna_list):
        """८.२.६६ ससजुषोः रुः"""
        v_list = list(varna_list)
        if v_list and v_list[-1].char == 'स्':
            v_list.pop()
            v_list.extend([Upadesha('र्', "8.2.66"), Upadesha('उँ', "8.2.66")])
            return v_list, "८.२.६६ (रुत्वम्)"
        return varna_list, None

    @staticmethod
    def apply_visarga_8_3_15(varna_list):
        """८.३.१५ खरवसानयोर्विसर्जनीयः"""
        v_list = list(varna_list)
        if v_list and v_list[-1].char == 'र्':
            v_list.pop()
            v_list.append(Upadesha('ः', "8.3.15"))
            return v_list, "८.३.१५ (विसर्गः)"
        return varna_list, None