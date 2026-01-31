"""
FILE: logic/sanjna/it_prakaranam.py
PAS-v2.0: 6.0 (Siddha) | PILLAR: Extensive Tagging & Inheritance
TIMESTAMP: 2026-01-31 04:15:00
DESCRIPTION:
    Full implementation of the It-Prakaranam (Chapter 1.3).
    Handles identification (Sanjna), Inheritance (Metadata Transfer),
    and Removal (Lopa).
"""
from core.upadesha_registry import UpadeshaType
from core.phonology import Varna

class ItSanjnas:
    """
    [VṚTTI]: उपदेशेऽजनुनासिक इत् (१.३.२) - तस्य लोपः (१.३.९)।
    Master Engine for Marker Identification and Removal.
    """

    # --- EXTENSIVE TAG REGISTRY ---
    TAG_FACTORY = {
        'अँ': 'adit', 'आँ': 'ādit', 'इँ': 'idit', 'ईँ': 'īdit',
        'उँ': 'udit', 'ऊँ': 'ūdit', 'ऋँ': 'ṛdit', 'ॠँ': 'ṝdit',
        'ञि': 'ñit', 'टु': 'ṭit', 'डु': 'dit',
        'क्': 'kit', 'ङ्': 'ngit', 'च्': 'cit', 'ञ्': 'ñit',
        'ण्': 'ṇit', 'प्': 'pit', 'म्': 'mit', 'श्': 'śit', 'ष्': 'ṣit'
    }

    CHU_VARGA = ['च्', 'छ्', 'ज्', 'झ्', 'ञ्']
    TU_VARGA  = ['ट्', 'ठ्', 'ड्', 'ढ्', 'ण्']
    LASHAKVA  = ['ल्', 'श्', 'क्', 'ख्', 'ग्', 'घ्', 'ङ्']
    TVAS_MAH  = ['त्', 'थ्', 'द्', 'ध्', 'न्', 'स्', 'म्']

    @staticmethod
    def identify_and_tag_its(varna_list, source_type, is_taddhita=False):
        """
        Runs the identification suite (1.3.2 - 1.3.8).
        Returns a set of indices marked for removal and a trace log.
        """
        if not varna_list: return set(), []
        it_indices, trace = set(), []

        # 1.3.2: Ajanunasika (Vowels with markers)
        idx, log = ItSanjnas.apply_1_3_2_ajanunasika(varna_list)
        it_indices.update(idx); trace.extend(log)

        # Initial Markers (1.3.5 - 1.3.8)
        if source_type == UpadeshaType.DHATU:
            idx, log = ItSanjnas.apply_1_3_5_adir_nitudavah(varna_list)
            it_indices.update(idx); trace.extend(log)

        elif source_type == UpadeshaType.PRATYAYA:
            # 1.3.7: Chutu (Initial Palatals/Cerebrals)
            idx, log = ItSanjnas.apply_1_3_7_chutu(varna_list)
            it_indices.update(idx); trace.extend(log)
            # 1.3.8: Lashakva (Initial l, sh, ku in non-Taddhita)
            idx, log = ItSanjnas.apply_1_3_8_lashakva(varna_list, is_taddhita)
            it_indices.update(idx); trace.extend(log)

        # 1.3.3: Halantyam (Final Consonants)
        idx, log = ItSanjnas.apply_1_3_3_halantyam(varna_list, source_type, it_indices)
        it_indices.update(idx); trace.extend(log)

        return it_indices, trace

    @staticmethod
    def run_tasya_lopah_1_3_9(varna_list, it_indices):
        """
        [१.३.९]: तस्य लोपः।
        Performs the physical removal and transfers markers to the survivors.
        """
        if not it_indices: return varna_list

        # 1. Metadata Harvest: Capture tags from the dying Varnas
        inherited_tags = set()
        for idx in it_indices:
            # Find tags like 'kit', 'nit', 'ṇit'
            tags = {s for s in varna_list[idx].sanjnas if s.endswith('it')}
            inherited_tags.update(tags)

        # 2. LOPA: Filter the list to remove 'it' characters
        cleaned = [v for i, v in enumerate(varna_list) if i not in it_indices]

        # 3. INHERITANCE: Assign the harvested tags to the surviving segment
        if cleaned and inherited_tags:
            # The first character of the remaining segment 'remembers' the markers
            cleaned[0].sanjnas.update(inherited_tags)
            cleaned[0].trace.append(f"1.3.9 Inheritance: {sorted(list(inherited_tags))}")

        return cleaned

    # --- INDIVIDUAL SŪTRA LOGIC ---

    @staticmethod
    def apply_1_3_2_ajanunasika(varna_list):
        """Processes vowels with nasal markers (e.g., in 'bhaj~')."""
        it_idx = set()
        # Find the chandrabindu modifier
        for i, v in enumerate(varna_list):
            if v.char == 'ँ':
                it_idx.add(i)
                if i > 0 and varna_list[i-1].is_vowel:
                    varna_list[i-1].sanjnas.add("it")
                    it_idx.add(i-1)
                return it_idx, ["1.3.2 (Ajanunasika)"]
        return set(), []

    @staticmethod
    def apply_1_3_3_halantyam(varna_list, source_type, blocked):
        """Final consonant markers (e.g., in 'Jas', 'Ṇvul')."""
        last_idx = len(varna_list) - 1
        if last_idx < 0 or last_idx in blocked: return set(), []

        # 1.3.4 Prohibition: No 't, s, m' markers at the end of a Vibhakti
        if source_type == UpadeshaType.VIBHAKTI and varna_list[last_idx].char in ItSanjnas.TVAS_MAH:
            return set(), ["1.3.4 (Vibhakti Block)"]

        if varna_list[last_idx].is_consonant:
            varna_list[last_idx].sanjnas.add("it")
            return {last_idx}, ["1.3.3 (Halantyam)"]
        return set(), []

    @staticmethod
    def apply_1_3_5_adir_nitudavah(varna_list):
        """Initial markers ñi, tu, du in Dhātus."""
        if not varna_list: return set(), []

        # Check for initial clusters like 'ñi'
        first_char = varna_list[0].char
        if first_char in ['ञि', 'टु', 'डु']:
            varna_list[0].sanjnas.add("it")
            return {0}, [f"1.3.5 ({first_char})"]

        # Split check (ñ + i)
        if len(varna_list) > 1:
            if varna_list[0].char == 'ञ्' and varna_list[1].char == 'इ':
                return {0, 1}, ["1.3.5 (ñi)"]
        return set(), []

    @staticmethod
    def apply_1_3_7_chutu(varna_list):
        """Initial markers in suffixes like 'Jas' (j)."""
        if not varna_list: return set(), []
        if varna_list[0].char in ItSanjnas.CHU_VARGA or varna_list[0].char in ItSanjnas.TU_VARGA:
            varna_list[0].sanjnas.add("it")
            return {0}, ["1.3.7 (Chuṭū)"]
        return set(), []

    @staticmethod
    def apply_1_3_8_lashakva(varna_list, is_taddhita):
        """Initial l, sh, ku in suffixes (e.g., 'Ṇvul')."""
        if is_taddhita or not varna_list: return set(), []
        if varna_list[0].char in ItSanjnas.LASHAKVA:
            varna_list[0].sanjnas.add("it")
            return {0}, ["1.3.8 (Lashakva)"]
        return set(), []