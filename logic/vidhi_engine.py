# logic/vidhi_engine.py

from core.upadesha_registry import Upadesha
from logic.anga_adhikara_wrapper import angasya_rule
from core.atidesha_mapper import AtideshaMapper
from core.paribhasha_manager import ParibhashaManager

class VidhiEngine:
    """
    सञ्चालक: - Zone 3 (Operational Engine).
    Unified workshop for all Vidhi Sutras, governed by Paribhasha targeting.
    """

    # --- CHAPTER 1: Sañjñā & General Vidhis ---

    @staticmethod
    def apply_hrasva_napumsaka_1_2_47(varna_list):
        """१.२.४७ ह्रस्वो नपुंसके प्रातिपदिकस्य (Shortening Neuter Stems)"""
        v_list = list(varna_list)
        if len(v_list) >= 2 and v_list[-1].char == 'स्':
            sthani = v_list[-2]
            mapping = {'आ': 'अ', 'ई': 'इ', 'ऊ': 'उ', 'ए': 'इ', 'ओ': 'उ'}

            if sthani.char in mapping:
                adesha = Upadesha(mapping[sthani.char], "1.2.47")
                # Genetic inheritance via 1.1.56
                v_list[-2] = AtideshaMapper.apply_sthanivadbhava_1_1_56(adesha, sthani, "1.2.47")
                return v_list, f"१.२.४७ (ह्रस्वादेशः: {sthani.char} -> {adesha.char})"
        return varna_list, None

    # --- CHAPTER 6: Transformations & Elisions ---

    @staticmethod
    def apply_hal_nyab_6_1_68(varna_list):
        """६.१.६८ हल्ङ्याब्भ्यो... (Removal of Apṛkta 'स्')"""
        v_list = list(varna_list)
        if v_list and v_list[-1].char == 'स्':
            last_chars = "".join([v.char for v in v_list[-4:]])
            # Triggered by words ending in long vowels (ā, ī, ū)
            if any(v in last_chars for v in ['आ', 'ई', 'ऊ']):
                v_list.pop()
                return v_list, "६.१.६८ (लोपः)"
        return varna_list, None

    @staticmethod
    @angasya_rule("6.4.8")
    def apply_upadha_dirgha_6_4_8(anga, nimitta):
        """६.४.८ सर्वनामस्थाने चासम्बुद्धौ (Upadhā Lengthening)"""
        # Surgical targeting using 1.1.65
        upadha_idx = ParibhashaManager.get_upadha_index_1_1_65(anga)
        if upadha_idx is None: return anga, None

        v_list = list(anga)
        # Condition: N-anta stems where penultimate is 'a'
        if v_list[-1].char == 'न्' and v_list[upadha_idx].char == 'अ':
            sthani = v_list[upadha_idx]
            adesha = Upadesha('आ', "6.4.8")
            v_list[upadha_idx] = AtideshaMapper.apply_sthanivadbhava_1_1_56(adesha, sthani, "6.4.8")
            return v_list, "६.४.८ (उपधा दीर्घ)"
        return anga, None

    # --- CHAPTER 7: Suffix Replacements & Anga Operations ---

    @staticmethod
    @angasya_rule("7.1.24")
    def ato_am_7_1_24(anga, nimitta):
        """७.१.२४ अतोऽम्"""
        if not nimitta: return anga, None

        sthani = nimitta[0]
        # Replaces 'su' with 'am'
        adesha_char = Upadesha('अ', "7.1.24")
        adesha_final = AtideshaMapper.apply_sthanivadbhava_1_1_56(adesha_char, sthani, "7.1.24")

        # FIX: We return the new nimitta segment as well
        new_nimitta = [adesha_final, Upadesha('म्', "7.1.24")]
        return (anga, new_nimitta), "७.१.२४ (अतोऽम्)"

    @staticmethod
    @angasya_rule("7.1.94")
    def apply_anang_7_1_94(anga, nimitta):
        """७.१.९४ अनङ्-आदेशः (Final 'ऋ' replacement)"""
        v_list = list(anga)
        for i in range(len(v_list) - 1, -1, -1):
            if v_list[i].char == 'ऋ':
                sthani = v_list.pop(i)
                adesha = AtideshaMapper.apply_sthanivadbhava_1_1_56(Upadesha('अ', "7.1.94"), sthani, "7.1.94")
                v_list.insert(i, adesha)
                v_list.insert(i + 1, Upadesha('न्', "7.1.94"))
                return v_list, "७.१.९४ (अनङ्-आदेशः)"
        return anga, None

    @staticmethod
    @angasya_rule("7.2.115")
    def apply_vriddhi_7_2_115(anga, nimitta):
        """७.२.११५ अचो ञ्णिति (Final Vowel Vṛddhi)"""
        v_list = list(anga)
        for i in range(len(v_list)):
            if v_list[i].char == 'ओ':
                sthani = v_list[i]
                adesha = AtideshaMapper.apply_sthanivadbhava_1_1_56(Upadesha('औ', "7.2.115"), sthani, "7.2.115")
                v_list[i] = adesha
                return v_list, "७.२.११५ (वृद्धिः)"
        return anga, None

    @staticmethod
    @angasya_rule("7.2.116")
    def apply_ata_upadhayah_7_2_116(anga, nimitta):
        """७.२.११६ अत उपधायाः (Penultimate 'a' Vṛddhi)"""
        # Dynamic Upadhā Identification (1.1.65)
        upadha_idx = ParibhashaManager.get_upadha_index_1_1_65(anga)
        if upadha_idx is None: return anga, None

        v_list = list(anga)
        target_varna = v_list[upadha_idx]

        # Suffix must be Ñit or Ṇit
        is_nit_or_nit = False
        if nimitta:
            is_nit_or_nit = any(tag in nimitta[0].sanjnas for tag in ["ñit", "ṇit"])

        if is_nit_or_nit and target_varna.char == 'अ':
            adesha = Upadesha('आ', "7.2.116")
            v_list[upadha_idx] = AtideshaMapper.apply_sthanivadbhava_1_1_56(adesha, target_varna, "7.2.116")
            return v_list, "७.२.११६ (वृद्धिः)"
        return anga, None

    # --- CHAPTER 8: Tripādī (Final Phonetics) ---

    @staticmethod
    def apply_rutva_8_2_66(varna_list):
        """८.२.६६ ससजुषोः रुः"""
        v_list = list(varna_list)
        if v_list and v_list[-1].char == 'स्':
            sthani = v_list.pop()
            adesha_r = AtideshaMapper.apply_sthanivadbhava_1_1_56(Upadesha('र्', "8.2.66"), sthani, "8.2.66")
            v_list.extend([adesha_r, Upadesha('उँ', "8.2.66")])
            return v_list, "८.२.६६ (रुत्वम्)"
        return varna_list, None

    @staticmethod
    def apply_visarga_8_3_15(varna_list):
        """८.३.१५ खरवसानयोर्विसर्जनीयः"""
        v_list = list(varna_list)
        # Final 'r' becomes Visarga at the end of a word (Avasāna)
        if v_list and v_list[-1].char == 'र्':
            v_list.pop()
            v_list.append(Upadesha('ः', "8.3.15"))
            return v_list, "८.३.१५ (विसर्गः)"
        return varna_list, None