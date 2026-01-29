"""
FILE: logic/vidhi_engine.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Vidhi (Operational Rules)
REFERENCE: Chapters 1, 6, 7, 8
"""

from core.upadesha_registry import Upadesha
from logic.anga_adhikara_wrapper import angasya_rule
from core.atidesha_mapper import AtideshaMapper
from core.paribhasha_manager import ParibhashaManager
import logic.stem_classifier as classifier

# --- Expanded Sanjna Imports (Zone 1 Integration) ---
from logic.sanjna_rules import is_ghi_1_4_7, is_nadi_1_4_3

class VidhiEngine:
    """
    सञ्चालक: - Zone 3 (Operational Engine).
    The Workshop: Performs physical transformations (Adesha) on the Varna objects.
    Governed by Paribhasha targeting and Anga adhikara.
    """

    # =========================================================================
    # CHAPTER 1: Sañjñā-Dependent Vidhis (General)
    # =========================================================================

    @staticmethod
    def apply_hrasva_napumsaka_1_2_47(varna_list):
        """
        [SUTRA]: ह्रस्वो नपुंसके प्रातिपदिकस्य (१.२.४७)
        [LOGIC]: Shortens long vowels in Neuter gender stems.
        Example: 'Gomati' (Fem/Long) -> 'Gomati' (Neut/Short)
        """
        v_list = list(varna_list)
        if len(v_list) >= 2:
            sthani = v_list[-1]
            mapping = {
                'आ': 'अ', 'ा': 'अ',
                'ई': 'इ', 'ी': 'इ', 'ए': 'इ', 'ऐ': 'इ',
                'ऊ': 'उ', 'ू': 'उ', 'ओ': 'उ', 'औ': 'उ'
            }

            if sthani.char in mapping:
                new_char = mapping[sthani.char]
                adesha = Upadesha(new_char, "1.2.47")
                AtideshaMapper.apply_sthanivadbhava_1_1_56(adesha, sthani, is_al_vidhi=False)
                v_list[-1] = adesha
                return v_list, f"१.२.४७ (ह्रस्वादेशः: {sthani.char} -> {adesha.char})"

        return varna_list, None

    # =========================================================================
    # CHAPTER 6: Transformations & Elisions
    # =========================================================================

    @staticmethod
    def apply_hal_nyab_6_1_68(varna_list):
        """
        [SUTRA]: हल्ङ्याब्भ्यो दीर्घात् सुतिस्यपृक्तं हल् (६.१.६८)
        [LOGIC]: Deletes the single consonant 'su', 'ti', 'si' (Aprikta).
        """
        if not varna_list: return varna_list, None

        last_unit = varna_list[-1]
        if last_unit.char not in ['स्', 'त्', 'द्']:
            return varna_list, None

        if len(varna_list) < 2: return varna_list, None
        anchor = varna_list[-2]

        is_hal_prev = not anchor.is_vowel
        is_long_fem = anchor.char in ['आ', 'ई', 'ऊ', 'ॠ']

        if is_hal_prev or is_long_fem:
            new_list = varna_list[:-1]
            return new_list, "६.१.६८ (हल्-ङ्याब्-भ्यो लोपः)"

        return varna_list, None

    @staticmethod
    @angasya_rule("6.4.8")
    def apply_upadha_dirgha_6_4_8(anga, nimitta):
        """
        [SUTRA]: सर्वनामस्थाने चासम्बुद्धौ (६.४.८)
        [LOGIC]: Lengthens Upadha of 'n' ending stems in strong cases.
        """
        upadha_varna, idx = ParibhashaManager.get_upadha_1_1_65(anga)
        if not upadha_varna: return anga, None

        if anga[-1].char != 'न्':
            return anga, None

        if nimitta:
            classifier._transform_to_dirgha(upadha_varna, "६.४.८ सर्वनामस्थाने...")
            return anga, "६.४.८ (उपधा दीर्घ)"

        return anga, None

    # =========================================================================
    # CHAPTER 7: Anga Operations & Suffix Transformations
    # =========================================================================

    @staticmethod
    @angasya_rule("7.1.24")
    def ato_am_7_1_24(anga, nimitta):
        """
        [SUTRA]: अतोऽम् (७.१.२४)
        [LOGIC]: After a short 'a' stem, 'Su' and 'Am' become 'Am'.
        """
        if not anga or not nimitta: return anga, None

        if anga[-1].char != 'अ':
            return anga, None

        first_nim = nimitta[0]
        if first_nim.char not in ['स्', 'अ', 'म्']:
            return anga, None

        nimitta.clear()
        a_obj = Upadesha('अ', "7.1.24")
        m_obj = Upadesha('म्', "7.1.24")
        AtideshaMapper.apply_sthanivadbhava_1_1_56(a_obj, first_nim)
        nimitta.extend([a_obj, m_obj])

        return anga, "७.१.२४ (अतोऽम्)"

    @staticmethod
    @angasya_rule("7.1.94")
    def apply_anang_7_1_94(anga, nimitta):
        """
        [SUTRA]: ॠदुशनस्पुरुदंसोऽनेहसां च (७.१.९४) -> अनङ् सौ
        [LOGIC]: 'Ṛ' ending words get 'anan' replacement in Su.
        """
        if anga and anga[-1].char == 'ऋ':
            if nimitta and nimitta[0].char == 'स्':
                sthani = anga.pop()
                a_obj = Upadesha('अ', "7.1.94")
                n_obj = Upadesha('न्', "7.1.94")
                AtideshaMapper.apply_sthanivadbhava_1_1_56(a_obj, sthani)
                anga.extend([a_obj, n_obj])
                return anga, "७.१.९४ (अनङ्-आदेशः)"
        return anga, None

    @staticmethod
    @angasya_rule("7.2.115")
    def apply_vriddhi_7_2_115(anga, nimitta):
        """
        [SUTRA]: अचो ञ्णिति (७.२.११५)
        [LOGIC]: Final vowel of Anga undergoes Vriddhi if suffix is Ñit or Ṇit.
        """
        if not anga or not nimitta: return anga, None

        trigger = False
        suffix_tags = getattr(nimitta[0], 'sanjnas', set())
        if 'ñit' in suffix_tags or 'ṇit' in suffix_tags or 'ñ' in suffix_tags or 'ṇ' in suffix_tags:
            trigger = True

        if trigger:
            last_varna = anga[-1]
            if last_varna.is_vowel:
                vriddhi_map = {'अ': 'आ', 'इ': 'ऐ', 'उ': 'औ', 'ऋ': 'आर', 'ओ': 'औ', 'ए': 'ऐ'}
                if last_varna.char in vriddhi_map:
                    new_val = vriddhi_map[last_varna.char]
                    if len(new_val) > 1:
                        anga.pop()
                        for c in new_val:
                            anga.append(Upadesha(c, "7.2.115"))
                    else:
                        last_varna.char = new_val
                        last_varna.sanjnas.add("वृद्धि")
                    return anga, "७.२.११५ (अचो ञ्णिति वृद्धि)"
        return anga, None

    @staticmethod
    @angasya_rule("7.2.116")
    def apply_ata_upadhayah_7_2_116(anga, nimitta):
        """
        [SUTRA]: अत उपधायाः (७.२.११६)
        [LOGIC]: Penultimate short 'a' undergoes Vriddhi if suffix is Ñit/Ṇit.
        """
        upadha_varna, idx = ParibhashaManager.get_upadha_1_1_65(anga)
        if not upadha_varna: return anga, None

        if upadha_varna.char != 'अ':
            return anga, None

        trigger = False
        if nimitta:
            suffix_tags = getattr(nimitta[0], 'sanjnas', set())
            if 'ñit' in suffix_tags or 'ṇit' in suffix_tags:
                trigger = True

        if trigger:
            classifier._transform_to_dirgha(upadha_varna, "७.२.११६")
            return anga, "७.२.११६ (अत उपधायाः वृद्धि)"

        return anga, None

    @staticmethod
    @angasya_rule("7.3.111")
    def apply_gher_niti_7_3_111(anga, nimitta):
        """
        [SUTRA]: घेर्ङिति (७.३.१११)
        [LOGIC]: Ghi-sanjnaka stem gets Guna if suffix is Ñit (Nit).
        Example: Hari + Ñe -> Hari + e -> Haray + e -> Haraye
        """
        # 1. Check Ghi Sanjna using the imported rule
        # Note: We pass 'anga' (a list of Varnas) to the checker
        if not is_ghi_1_4_7(anga):
            return anga, None

        # 2. Check Suffix for 'Ñit' (Nit)
        # Note: Dative Sg (Ñe), Ablative Sg (Ñasi), etc. have 'Ñ'.
        trigger = False
        if nimitta:
            suffix_tags = getattr(nimitta[0], 'sanjnas', set())
            if 'ñit' in suffix_tags or 'ñ' in suffix_tags:
                trigger = True

        if trigger:
            last_varna = anga[-1]
            if last_varna.char in ['इ', 'उ']:
                guna_map = {'इ': 'ए', 'उ': 'ओ'}
                last_varna.char = guna_map[last_varna.char]
                last_varna.sanjnas.add("गुण")
                return anga, "७.३.१११ (घेर्ङिति गुण)"

        return anga, None

    # =========================================================================
    # CHAPTER 8: Tripādī (Final Phonetics)
    # =========================================================================

    @staticmethod
    def apply_rutva_8_2_66(varna_list):
        """
        [SUTRA]: ससजुषोः रुः (८.२.६६)
        [LOGIC]: Padanta 's' becomes 'ru'.
        """
        if varna_list and varna_list[-1].char == 'स्':
            sthani = varna_list.pop()
            r_obj = Upadesha('र्', "8.2.66")
            u_obj = Upadesha('उँ', "8.2.66")
            AtideshaMapper.apply_sthanivadbhava_1_1_56(r_obj, sthani)
            varna_list.extend([r_obj, u_obj])
            return varna_list, "८.२.६६ (रुत्वम्)"
        return varna_list, None

    @staticmethod
    def apply_upadeshe_ajanunasika_for_rutva(varna_list):
        """
        [HELPER]: Removes the 'u' from 'Ru' (1.3.2 + 1.3.9).
        """
        if len(varna_list) >= 2:
            last = varna_list[-1]
            prev = varna_list[-2]
            if last.char == 'उँ' and prev.char == 'र्':
                varna_list.pop()
                return varna_list, "१.३.९ (रुत्व-उकार-लोपः)"
        return varna_list, None

    @staticmethod
    def apply_visarga_8_3_15(varna_list):
        """
        [SUTRA]: खरवसानयोर्विसर्जनीयः (८.३.१५)
        [LOGIC]: Padanta 'r' becomes Visarga 'ḥ'.
        """
        if varna_list and varna_list[-1].char == 'र्':
            varna_list.pop()
            varna_list.append(Upadesha('ः', "8.3.15"))
            return varna_list, "८.३.१५ (विसर्गः)"
        return varna_list, None