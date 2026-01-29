# logic/it_engine.py

from core.upadesha_registry import UpadeshaType
from logic.sanjna_rules import (
    apply_upadeshe_ajanunasika_1_3_2,
    apply_na_vibhaktau_1_3_4,
    apply_halantyam_1_3_3,
    apply_adir_nitudavah_1_3_5,
    apply_shah_pratyayasya_1_3_6,
    apply_chuttu_1_3_7,
    apply_lashakvataddhite_1_3_8
)


class ItEngine:
    """
    पाणिनीय इत्-संज्ञा मास्टर इंजन (इत्-प्रकरणम्)
    Surgical Scrub: Identifies markers and performs Tasya Lopah (1.3.9).
    """

    @staticmethod
    def run_it_prakaran(varna_list, source_type, is_taddhita=False):
        """
        Orchestrates the 1.3.2 -> 1.3.8 sequence and executes 1.3.9.
        """
        if not varna_list or not isinstance(source_type, UpadeshaType):
            return varna_list, []

        it_indices = set()
        sutra_tags = []

        # 1. Nasal Vowels (1.3.2)
        idx2, tags2 = apply_upadeshe_ajanunasika_1_3_2(varna_list)
        it_indices.update(idx2)
        sutra_tags.extend(tags2)

        # 2. Shield: Na Vibhaktau (1.3.4)
        blocked_indices = apply_na_vibhaktau_1_3_4(varna_list, source_type)

        # 3. Final Consonants: Halantyam (1.3.3)
        idx3, tags3 = apply_halantyam_1_3_3(varna_list, blocked_indices)
        it_indices.update(idx3)
        sutra_tags.extend(tags3)

        # 4. Initial Markers (Adi-It)
        if source_type == UpadeshaType.DHATU:
            idx5, tags5 = apply_adir_nitudavah_1_3_5(varna_list)
            it_indices.update(idx5)
            sutra_tags.extend(tags5)
        elif source_type in [UpadeshaType.PRATYAYA, UpadeshaType.VIBHAKTI]:
            # 1.3.6 (Sha), 1.3.7 (Chu-Tu), 1.3.8 (L-Sh-Ku)
            for func in [apply_shah_pratyayasya_1_3_6, apply_chuttu_1_3_7]:
                idx, tags = func(varna_list, source_type)
                it_indices.update(idx)
                sutra_tags.extend(tags)

            idx8, tags8 = apply_lashakvataddhite_1_3_8(varna_list, source_type, is_taddhita)
            it_indices.update(idx8)
            sutra_tags.extend(tags8)

        # --- ५. तस्य लोपः (१.३.९) ---
        # The execution of the deletion mandate
        remaining_varnas = [
            v for idx, v in enumerate(varna_list) if idx not in it_indices
        ]

        return remaining_varnas, list(set(sutra_tags))