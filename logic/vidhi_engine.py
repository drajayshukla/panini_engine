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
            # Look at the stem ending (assuming interaction with a suffix usually implies checking stem)
            # Identifying the ending vowel.
            # Simplified logic: Check the last character of the stem portion.
            # (In a full engine, we'd use Anga split, but this is a general Vidhi).

            # Logic: If the word ends in Long Vowel and is Neuter.
            # We assume 'varna_list' passed here is the Stem (Pratipadika).
            sthani = v_list[-1]

            # Strict Mapping for 1.1.48 (Antaratama)
            mapping = {
                'आ': 'अ', 'ा': 'अ',
                'ई': 'इ', 'ी': 'इ', 'ए': 'इ', 'ऐ': 'इ',
                'ऊ': 'उ', 'ू': 'उ', 'ओ': 'उ', 'औ': 'उ'
            }

            if sthani.char in mapping:
                # Create the replacement
                new_char = mapping[sthani.char]
                adesha = Upadesha(new_char, "1.2.47")

                # Apply 1.1.56 (Inheritance)
                # Not Al-vidhi because it replaces the whole phoneme based on morphology
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
        [LOGIC]: Deletes the single consonant 'su', 'ti', 'si' (Aprikta)
                 if they follow a consonant (Hal) OR long feminine markers (Ni/Ap).
        """
        if not varna_list: return varna_list, None

        # 1. Identify Aprikta (Single Letter Suffix)
        last_unit = varna_list[-1]

        # Must be S, T, or D (remnants of Su, Ti, Si)
        # And must be single consonant (checked by the flow usually, but we check char)
        if last_unit.char not in ['स्', 'त्', 'द्']:
            return varna_list, None

        # 2. Check Preceding Condition (The Anchor)
        if len(varna_list) < 2: return varna_list, None
        anchor = varna_list[-2]

        # Condition A: After Hal (Consonant)
        is_hal_prev = not anchor.is_vowel

        # Condition B: After Long Ni/Ap (ī, ū, ā) - simplified check on char
        is_long_fem = anchor.char in ['आ', 'ई', 'ऊ', 'ॠ']

        if is_hal_prev or is_long_fem:
            # EXECUTE LOPA
            # We treat Lopa as removing the element from the list
            new_list = varna_list[:-1]
            return new_list, "६.१.६८ (हल्-ङ्याब्-भ्यो लोपः)"

        return varna_list, None

    @staticmethod
    @angasya_rule("6.4.8")
    def apply_upadha_dirgha_6_4_8(anga, nimitta):
        """
        [SUTRA]: सर्वनामस्थाने चासम्बुद्धौ (६.४.८)
        [CONTEXT]: 6.4.7 'Nopadhayah' (Stems ending in 'n')
        [LOGIC]: Lengthens Upadha (Penultimate) of 'n' ending stems in strong cases (Sarvanamasthana).
        Example: rājan + au -> rājānau
        """
        # 1. Identify Upadha
        upadha_varna, idx = ParibhashaManager.get_upadha_1_1_65(anga)
        if not upadha_varna: return anga, None

        # 2. Strict Anga Check: Must end in 'n' (Anuvritti from 6.4.7)
        if anga[-1].char != 'न्':
            return anga, None

        # 3. Nimitta Check: Must be Sarvanamasthana
        # We rely on 'sanjnas' or 'source_type' logic, or basic char checks for the demo
        is_sarvanamasthana = False
        if nimitta:
            # Check known strong suffixes (Su, Au, Jas, Am, Out)
            # Simplistic check: Au, As, Am
            first_nim = nimitta[0].char
            if first_nim in ['औ', 'अ', 'स']:  # Very heuristic for demo; implies Au, Jas/Am, etc.
                is_sarvanamasthana = True

        # In a real app, the Controller injects 'is_sarvanamasthana' flag into metadata.
        # We assume True if nimitta is present for this specific function trigger context.
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
        Example: Rāma + Su -> Rāmam
        """
        if not anga or not nimitta: return anga, None

        # Condition 1: Anga ends in short 'a'
        if anga[-1].char != 'अ':
            return anga, None

        # Condition 2: Nimitta is 'Su' or 'Am'
        # 'Su' usually appears as 's' after It-Lopa
        first_nim = nimitta[0]
        if first_nim.char not in ['स्', 'अ', 'म्']:
            return anga, None

        # OPERATION: Replace Nimitta with 'Am'
        # Since 'nimitta' is a list passed by reference from the wrapper,
        # we can clear it and add the new content.
        nimitta.clear()

        # Create 'Am'
        a_obj = Upadesha('अ', "7.1.24")
        m_obj = Upadesha('म्', "7.1.24")
        AtideshaMapper.apply_sthanivadbhava_1_1_56(a_obj, first_nim)  # Inherit

        nimitta.extend([a_obj, m_obj])

        # 6.1.107 Ami Purvah (Sandhi) usually handles the 'a' + 'a' -> 'a'.
        # But 7.1.24 specifically dictates the replacement first.

        return anga, "७.१.२४ (अतोऽम्)"

    @staticmethod
    @angasya_rule("7.1.94")
    def apply_anang_7_1_94(anga, nimitta):
        """
        [SUTRA]: ॠदुशनस्पुरुदंसोऽनेहसां च (७.१.९४) -> अनङ् सौ
        [LOGIC]: 'Ṛ' ending words get 'anan' replacement in Su (Nom. Sg.).
        Example: Pitṛ + Su -> Pitan + Su
        """
        # Check if Anga ends in 'ṛ'
        if anga and anga[-1].char == 'ऋ':
            # Check if Nimitta is 'Su' (Nom. Sg.)
            # Su appears as 's' after it-lopa
            if nimitta and nimitta[0].char == 'स्':
                # Remove final 'ṛ'
                sthani = anga.pop()

                # Insert 'an' (un-adi) -> 'a' + 'n'
                # Note: 'ng' is It-marker, so we just add 'a' and 'n'

                a_obj = Upadesha('अ', "7.1.94")
                n_obj = Upadesha('न्', "7.1.94")

                # Inherit from sthani
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

        # Check Nimitta for Ñit/Ṇit tags
        # (Assuming ItEngine has populated sanjnas or 'kit/ngit' logic)
        trigger = False
        suffix_tags = getattr(nimitta[0], 'sanjnas', set())
        if 'ñit' in suffix_tags or 'ṇit' in suffix_tags or 'ñ' in suffix_tags or 'ṇ' in suffix_tags:
            trigger = True

        if trigger:
            last_varna = anga[-1]
            if last_varna.is_vowel:
                # Apply Vriddhi
                # Simple Mapping for demo
                vriddhi_map = {'अ': 'आ', 'इ': 'ऐ', 'उ': 'औ', 'ऋ': 'आर', 'ओ': 'औ', 'ए': 'ऐ'}

                if last_varna.char in vriddhi_map:
                    new_val = vriddhi_map[last_varna.char]

                    # Handle 'ar' / 'aar' split if needed
                    if len(new_val) > 1:  # e.g. 'aar'
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
        # 1. Identify Upadha
        upadha_varna, idx = ParibhashaManager.get_upadha_1_1_65(anga)
        if not upadha_varna: return anga, None

        # 2. Check Constraint: Must be short 'a'
        if upadha_varna.char != 'अ':
            return anga, None

        # 3. Check Nimitta for Ñit/Ṇit
        trigger = False
        if nimitta:
            suffix_tags = getattr(nimitta[0], 'sanjnas', set())
            if 'ñit' in suffix_tags or 'ṇit' in suffix_tags:
                trigger = True

        if trigger:
            # Transform 'a' -> 'ā'
            classifier._transform_to_dirgha(upadha_varna, "७.२.११६")
            return anga, "७.२.११६ (अत उपधायाः वृद्धि)"

        return anga, None

    # =========================================================================
    # CHAPTER 8: Tripādī (Final Phonetics)
    # =========================================================================

    @staticmethod
    def apply_rutva_8_2_66(varna_list):
        """
        [SUTRA]: ससजुषोः रुः (८.२.६६)
        [LOGIC]: Padanta 's' and 'sajush' become 'ru'.
        """
        if varna_list and varna_list[-1].char == 'स्':
            sthani = varna_list.pop()

            # Replacement is 'ru' (r + u_it)
            # In strict grammar, 'u' is nasalized and IT.
            # We add 'r' and 'u' separately to allow U-lopa later if needed,
            # or just 'r' if we skip the u-it step for simplified derivation.
            # Let's add strict Ru: 'r' + 'u~'

            r_obj = Upadesha('र्', "8.2.66")
            u_obj = Upadesha('उँ', "8.2.66")  # Nasal U is It

            # Inherit properties
            AtideshaMapper.apply_sthanivadbhava_1_1_56(r_obj, sthani)

            varna_list.extend([r_obj, u_obj])
            return varna_list, "८.२.६६ (रुत्वम्)"

        return varna_list, None

    @staticmethod
    def apply_upadeshe_ajanunasika_for_rutva(varna_list):
        """
        [HELPER]: Removes the 'u' from 'Ru' (1.3.2 + 1.3.9) usually happens immediately.
        """
        if len(varna_list) >= 2:
            last = varna_list[-1]
            prev = varna_list[-2]
            if last.char == 'उँ' and prev.char == 'र्':
                varna_list.pop()  # Remove u
                return varna_list, "१.३.९ (रुत्व-उकार-लोपः)"
        return varna_list, None

    @staticmethod
    def apply_visarga_8_3_15(varna_list):
        """
        [SUTRA]: खरवसानयोर्विसर्जनीयः (८.३.१५)
        [LOGIC]: Padanta 'r' becomes Visarga 'ḥ' at end of word (Avasana) or before Khar.
        """
        if varna_list and varna_list[-1].char == 'र्':
            # Check Avasana (End of list implies end of word in this engine)
            varna_list.pop()
            varna_list.append(Upadesha('ः', "8.3.15"))
            return varna_list, "८.३.१५ (विसर्गः)"
        return varna_list, None