"""
FILE: logic/sanjna/it_prakaranam.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: It-Prakaraṇam (Technical Markers)
REFERENCE: १.३.२ - १.३.८
"""
from core.upadesha_registry import UpadeshaType

class ItSanjnas:
    """
    It-Prakaraṇam: Rules for identifying and tagging markers (Its).
    These markers are used to trigger specific grammatical operations
    but are elided by 1.3.9 (Tasya Lopaḥ).
    """

    @staticmethod
    def apply_1_3_2_ajanunasika(varna_list):
        """[SUTRA]: उपदेशेऽजनुनासिक इत् (१.३.२)"""
        indices = set()
        trace = []

        for i, v in enumerate(varna_list):
            # Check for explicit nasal symbols
            if v.char in ['ँ', 'ं']:
                indices.add(i)
                v.sanjnas.add("इत्")
                v.trace.append("१.३.२ (Nasal Symbol)")
                trace.append("१.३.२ (Nasal Symbol)")

                # If the symbol nasalizes the previous vowel
                if i > 0:
                    prev_v = varna_list[i - 1]
                    if prev_v.is_vowel:
                        indices.add(i - 1)
                        prev_v.sanjnas.add("इत्")
                        prev_v.trace.append("१.३.२ (Nasalized Vowel)")
                        trace.append("१.३.२ (Nasalized Vowel)")
                continue

            # Check for inherent property of the Varna object
            if v.is_vowel and getattr(v, 'is_anunasika', False):
                indices.add(i)
                v.sanjnas.add("इत्")
                v.trace.append("१.३.२ (Nasal Vowel)")
                trace.append("१.३.२ (Nasal Vowel)")

        return indices, trace

    @staticmethod
    def apply_1_3_3_halantyam(varna_list, blocked_indices=None):
        """[SUTRA]: हलन्त्यम् (१.३.३)"""
        if not varna_list: return set(), []
        last_idx = len(varna_list) - 1

        # Respect blocking by 1.3.4 (Na Vibhaktau)
        if blocked_indices and last_idx in blocked_indices:
            return set(), []

        last_varna = varna_list[last_idx]
        if last_varna.is_consonant:
            last_varna.sanjnas.add("इत्")
            return {last_idx}, ["१.३.३ हलन्त्यम्"]
        return set(), []

    @staticmethod
    def apply_1_3_4_na_vibhaktau(varna_list, source_type):
        """[SUTRA]: न विभक्तौ तुस्माः (१.३.४)"""
        blocked = set()
        if source_type != UpadeshaType.VIBHAKTI:
            return blocked

        if not varna_list: return blocked

        last_idx = len(varna_list) - 1
        char = varna_list[last_idx].char
        # tu-s-m (t-varga, s, m) are not its in a vibhakti
        restricted = ['त्', 'थ्', 'द्', 'ध्', 'न्', 'स्', 'म्']

        if char in restricted:
            blocked.add(last_idx)
        return blocked

    @staticmethod
    def apply_1_3_5_adir_nitudavah(varna_list):
        """[SUTRA]: आदिर्ञिटुडवः (१.३.५)"""
        if not varna_list: return set(), []
        indices = set()
        trace = []
        first = varna_list[0]

        # Check for initial clusters defined as Its
        if first.char in ['ञि', 'टु', 'डु', 'डुकृ']:
            indices.add(0)
            first.sanjnas.add("इत्")
            trace.append(f"१.३.५ आदिर्ञिटुडवः ({first.char})")
            return indices, trace

        # Check for split markers (e.g., Ñ-i)
        if len(varna_list) > 1:
            second = varna_list[1]
            if (first.char == 'ञ्' and second.char == 'इ') or \
               (first.char == 'ट्' and second.char == 'उ') or \
               (first.char == 'ड्' and second.char == 'उ'):
                indices.add(0)
                indices.add(1)
                first.sanjnas.add("इत्")
                second.sanjnas.add("इत्")
                trace.append("१.३.५ आदिर्ञिटुडवः (Split Marker)")

        return indices, trace

    @staticmethod
    def apply_1_3_6_shah(varna_list, source_type):
        """[SUTRA]: षः प्रत्ययस्य (१.३.६)"""
        if source_type not in [UpadeshaType.PRATYAYA, UpadeshaType.VIBHAKTI]:
            return set(), []
        if varna_list and varna_list[0].char == 'ष्':
            varna_list[0].sanjnas.add("इत्")
            return {0}, ["१.३.६ षः प्रत्ययस्य"]
        return set(), []

    @staticmethod
    def apply_1_3_7_chutu(varna_list, source_type):
        """[SUTRA]: चुटू (१.३.७)"""
        if source_type not in [UpadeshaType.PRATYAYA, UpadeshaType.VIBHAKTI]:
            return set(), []
        if not varna_list: return set(), []

        char = varna_list[0].char
        c_varga = ['च्', 'छ्', 'ज्', 'झ्', 'ञ्']
        t_varga = ['ट्', 'ठ्', 'ड्', 'ढ्', 'ण्']

        if char in c_varga or char in t_varga:
            varna_list[0].sanjnas.add("इत्")
            return {0}, ["१.३.७ चुटू"]
        return set(), []

    @staticmethod
    def apply_1_3_8_lashakva(varna_list, source_type, is_taddhita=False):
        """[SUTRA]: लशक्वतद्धिते (१.३.८)"""
        # Block for non-pratyayas and specifically for Taddhita suffixes
        if source_type in [UpadeshaType.DHATU, UpadeshaType.PRATIPADIKA, UpadeshaType.AGAMA]:
            return set(), []
        if is_taddhita or not varna_list:
            return set(), []

        char = varna_list[0].char
        # L, Sh, and Ku (k-varga) are Its
        targets = ['ल्', 'श्', 'क्', 'ख्', 'ग्', 'घ्', 'ङ्']

        if char in targets:
            varna_list[0].sanjnas.add("इत्")
            return {0}, ["१.३.८ लशक्वतद्धिते"]
        return set(), []