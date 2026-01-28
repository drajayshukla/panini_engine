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

class ItSanjnaEngine:
    """
    पाणिनीय इत्-संज्ञा मास्टर इंजन (एकीकृत कौमुदी-प्रकरण मॉडल)
    Orders: 1.3.2 -> 1.3.4 (Shield) -> 1.3.3 (Halantyam) -> 1.3.5-8 (Adi-It) -> 1.3.9 (Lopa)
    """

    @staticmethod
    def run_it_sanjna_prakaran(varna_list, original_input, source_type, is_taddhita=False):
        """
        Orchestrates the 1.3.2 - 1.3.8 sequence with surgical precision.
        """
        if not varna_list or not isinstance(source_type, UpadeshaType):
            return varna_list, []

        it_indices = set()
        sutra_tags = []

        # १. उपदेशेऽजनुनासिक इत् (१.३.२)
        idx2, tags2 = apply_upadeshe_ajanunasika_1_3_2(varna_list)
        it_indices.update(idx2)
        sutra_tags.extend(tags2)

        # २. सुरक्षा कवच: न विभक्तौ तुस्माः (१.३.४) - FIX: Passing source_type
        # This prevents 1.3.3 from deleting 's', 'm', or 'tu-varga' in Vibhaktis.
        blocked_indices = apply_na_vibhaktau_1_3_4(varna_list, source_type)

        # ३. हलन्त्यम् (१.३.३) - Respects the blocked indices from 1.3.4
        idx3, tags3 = apply_halantyam_1_3_3(varna_list, blocked_indices)
        it_indices.update(idx3)
        sutra_tags.extend(tags3)

        # ४. आदि-इत् संज्ञा (Identifying initial markers)
        if source_type == UpadeshaType.DHATU:
            idx5, tags5 = apply_adir_nitudavah_1_3_5(varna_list)
            it_indices.update(idx5)
            sutra_tags.extend(tags5)

        elif source_type in [UpadeshaType.PRATYAYA, UpadeshaType.VIBHAKTI]:
            # 1.3.6: षः प्रत्ययस्य
            idx6, tags6 = apply_shah_pratyayasya_1_3_6(varna_list, source_type)
            it_indices.update(idx6)
            sutra_tags.extend(tags6)

            # 1.3.7: चुटू
            idx7, tags7 = apply_chuttu_1_3_7(varna_list, source_type)
            it_indices.update(idx7)
            sutra_tags.extend(tags7)

            # 1.3.8: लशक्वतद्धिते (Respects is_taddhita flag)
            idx8, tags8 = apply_lashakvataddhite_1_3_8(varna_list, source_type, is_taddhita)
            it_indices.update(idx8)
            sutra_tags.extend(tags8)

        # ५. तस्य लोपः (१.३.९) - Final surgical removal
        remaining_varnas = [
            v for idx, v in enumerate(varna_list)
            if idx not in it_indices
        ]

        # Ensure unique tags for the UI
        return remaining_varnas, list(set(sutra_tags))