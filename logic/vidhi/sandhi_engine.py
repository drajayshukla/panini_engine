"""
FILE: logic/vidhi/sandhi_engine.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Padānta-Saṃskāra (Word-End Transformation)
"""
from core.phonology import Varna
import copy
class SandhiEngine:
    @staticmethod
    def apply_iko_yan_achi_6_1_77(anga_varnas, suffix_varnas=None):
        """[SUTRA]: इको यणचि (६.१.७७)"""
        if len(anga_varnas) < 2: return anga_varnas, None
        for i in range(len(anga_varnas) - 1):
            curr, nxt = anga_varnas[i], anga_varnas[i + 1]
            if curr.char in ['इ', 'ई'] and nxt.is_vowel:
                old = curr.char
                curr.char = 'य्'
                curr.trace.append("६.१.७७")
                return anga_varnas, f"६.१.७७ ({old} -> य्)"
        return anga_varnas, None

    @staticmethod
    def apply_ayadi_6_1_78(stem, suffix):
        """
        [6.1.78]: एचोऽयवायावः।
        Requirement: Stem ends in an 'Ec' (e, ai, o, au) and suffix starts with any vowel.
        Action: Replace the final vowel with its respective Ayādi substitute.

        Mapping:
            ए (e)  -> अय् (ay)
            ऐ (ai) -> आय् (āy)
            ओ (o)  -> अव् (av)
            औ (au) -> आव् (āv)
        """
        # 1. Basic Safety Checks
        if not stem or not suffix:
            return stem, None

        # 2. Nimitta Check: Rule only applies if followed by a vowel (Aci)
        if not suffix[0].is_vowel:
            return stem, None

        # 3. Sthānī (Substitution) Logic
        last_varna = stem[-1]
        mapping = {
            'ए': ['अ', 'य्'],
            'ओ': ['अ', 'व्'],
            'ऐ': ['आ', 'य्'],
            'औ': ['आ', 'व्']
        }

        if last_varna.char in mapping:
            old_char = last_varna.char
            substitutes = mapping[old_char]

            # Create new Varna objects for the substitutes
            new_varnas = []
            for char in substitutes:
                v = Varna(char)
                v.trace.append("6.1.78")
                # Inherit relevant sanjnas if necessary
                new_varnas.append(v)

            # Reconstruct stem: All but last + new substitutes
            res_stem = stem[:-1] + new_varnas

            # Return detailed rule string for the PrakriyaLogger
            rule_desc = f"6.1.78 (एचोऽयवायावः: {old_char} -> {''.join(substitutes)})"
            return res_stem, rule_desc

        return stem, None

    @staticmethod
    def apply_vriddhi_rechi_6_1_88(anga, suffix):
        """
        [6.1.88] Vṛddhir eci.
        a/ā + e/o/ai/au -> ai/au
        """
        if not anga or not suffix: return anga, None

        last = anga[-1]
        first = suffix[0]

        # Condition: Stem ends in 'a' or 'ā'
        if last.char not in ['अ', 'आ']: return anga, None

        # Scenario 1: a + ai -> ai (Rāma + ais -> Rāmais)
        if first.char == 'ऐ':
            last.char = 'ऐ'
            suffix.pop(0)
            return anga, "6.1.88"

        # Scenario 2: a + au -> au (Rāma + au -> Rāmau)
        if first.char == 'औ':
            last.char = 'औ'  # Update Stem
            suffix.pop(0)  # Remove first char of suffix
            return anga, "6.1.88"

        return anga, None

    @staticmethod
    def apply_aka_savarne_dirgha_6_1_101(anga, suffix):
        """
        [6.1.101] Akah Savarne Dirgha.
        (a, i, u, r, l) + Savarna (same vowel) -> Long Vowel.
        Example: Rāma + a -> Rāmā; Kavi + i -> Kavī.
        """
        if not anga or not suffix: return anga, None

        last = anga[-1]
        first = suffix[0]

        # 1. Define Savarna Pairs (Matches)
        savarna_map = {
            'अ': ['अ', 'आ'], 'आ': ['अ', 'आ'],
            'इ': ['इ', 'ई'], 'ई': ['इ', 'ई'],
            'उ': ['उ', 'ऊ'], 'ऊ': ['उ', 'ऊ'],
            'ऋ': ['ऋ', 'ॠ'], 'ॠ': ['ऋ', 'ॠ']
        }

        # 2. Define Resulting Long Vowel (Adesha)
        long_map = {
            'अ': 'आ', 'आ': 'आ',
            'इ': 'ई', 'ई': 'ई',
            'उ': 'ऊ', 'ऊ': 'ऊ',
            'ऋ': 'ॠ', 'ॠ': 'ॠ'
        }

        # 3. Check Condition: Last letter is Ak, First letter is Savarna
        if last.char in savarna_map and first.char in savarna_map[last.char]:
            # Apply Change
            last.char = long_map[last.char]
            suffix.pop(0)  # Remove the second vowel (Eka-adesha merges both into first)

            # Return Clean Code for Logger Lookup
            return anga, "6.1.101"

        return anga, None

    @staticmethod
    def apply_ami_purvah_6_1_107(stem_or_list, suffix=None):
        """
        [6.1.107]: अमि पूर्वः।
        Requirement: A short 'a' followed by the 'a' of the 'Am' suffix.
        Action: Both vowels are replaced by the 'Purva' (the first vowel).

        Supports two input modes:
        1. Dual Argument: (stem, suffix) -> Used by Strategy Engines (e.g., s_1_1.py)
        2. Single Argument: (combined_list) -> Used for general list processing.
        """
        # --- MODE 1: SEPARATE STEM AND SUFFIX ---
        if suffix is not None:
            stem = stem_or_list
            if not stem or not suffix:
                return (stem + suffix), None

            # Check: Stem ends in 'a' AND Suffix starts with 'a' (from 'am')
            if stem[-1].char == 'अ' and suffix[0].char == 'अ':
                # Result: Stem remains intact, suffix starts from index 1 (skipping its 'a')
                result = stem + suffix[1:]
                return result, "6.1.107 (अमि पूर्वः)"

            return (stem + suffix), None

        # --- MODE 2: COMBINED LIST (Backwards Compatibility) ---
        else:
            varna_list = stem_or_list
            if len(varna_list) < 2:
                return varna_list, None

            # Analyze the internal junction (last two Varna objects)
            v1, v2 = varna_list[-2], varna_list[-1]

            # Condition: Both are short 'a'
            if v1.char == 'अ' and v2.char == 'अ':
                # Remove the second 'a' (the Para-rūpa) to leave only the Purva-rūpa
                varna_list.pop()
                return varna_list, "6.1.107 (अमि पूर्वः)"

            return varna_list, None
    @staticmethod
    def apply_uvang_6_4_77(anga, suffix):
        """[६.४.७७]: अचि श्नुधातुभ्रूवाम्... (उवङ्-आदेशः)।"""
        if not anga or not suffix or not suffix[0].is_vowel: return anga, None

        # Sthāna: Identify final non-abhyāsa vowel
        t_idx = -1
        for i in range(len(anga) - 1, -1, -1):
            if "abhyasa" not in anga[i].sanjnas and anga[i].is_vowel:
                t_idx = i;
                break

        if t_idx != -1 and anga[t_idx].char in ['उ', 'ऊ']:
            old = anga[t_idx].char
            u_v, v_v = Varna('उ'), Varna('व्')
            for v in [u_v, v_v]: v.trace.append("६.४.७७")
            anga[t_idx: t_idx + 1] = [u_v, v_v]
            return anga, f"६.४.७७ ({old}->उवङ्)"
        return anga, None

    @staticmethod
    def apply_jshatvam_8_2_39(anga):
        """
        [8.2.39]: झलां जशोऽन्ते। (Jaśatvam)
        At the padānta, 'ṣ' undergoes a complex change to 'ḍ'
        (via 8.2.36 and 8.4.41).
        """
        if not anga: return anga, None
        last = anga[-1]

        # Mapping for final transformations
        jash_map = {'ष्': 'ड्', 'क्': 'ग्', 'च्': 'ज्', 'त्': 'द्', 'प्': 'ब्'}

        if last.char in jash_map:
            last.char = jash_map[last.char]
            last.trace.append("8.2.39")
            return anga, "8.2.39"
        return anga, None

    @staticmethod
    def apply_chartvam_8_4_56(anga):
        """
        [8.4.56]: वाऽवसाने। (Chartvam)
        Optional unvoicing at the pause (avasāna).
        """
        if not anga: return anga, None
        last = anga[-1]

        char_map = {'ड्': 'ट्', 'ग्': 'क्', 'ज्': 'च्', 'द्': 'त्', 'ब्': 'प्'}

        if last.char in char_map:
            # Creating the optional 'Vā' form
            alt_anga = copy.deepcopy(anga)
            alt_anga[-1].char = char_map[last.char]
            alt_anga[-1].trace.append("8.4.56")
            return alt_anga, "8.4.56"
        return anga, None

