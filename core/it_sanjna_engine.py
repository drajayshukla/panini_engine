from core.upadesha_registry import UpadeshaType
from logic.sanjna_rules import (
    apply_upadeshe_ajanunasika_1_3_2,
    apply_halantyam_1_3_3,
    apply_adir_nitudavah_1_3_5,
    apply_shah_pratyayasya_1_3_6,
    apply_chuttu_1_3_7,
    apply_lashakvataddhite_1_3_8
)
from utils.data_loader import get_all_vibhakti

class ItSanjnaEngine:
    """
    पाणिनीय इत्-संज्ञा मास्टर इंजन (Tasya Lopah Model)
    सिद्धांत: पहले संज्ञा (Tagging), फिर लोप (Deletion - 1.3.9)।
    """

    @staticmethod
    def run_it_sanjna_prakaran(varna_list, original_input, source_type, is_taddhita=False):
        if not isinstance(source_type, UpadeshaType) or not varna_list:
            return varna_list, []

        all_it_tags = []
        it_indices = set() # इत् वर्णों की अनुक्रमणिकाएँ (Indices)

        # --- १. तैयारी (Context Setup) ---
        vibhakti_list = get_all_vibhakti()
        is_vibhakti = original_input in vibhakti_list

        # --- २. संज्ञा प्रकरण (Identification Stage: 1.3.2 to 1.3.8) ---
        # नियम: कोई वर्ण हटाया नहीं जाएगा, केवल 'Index' मार्क की जाएगी।

        # सूत्र १.३.५: आदिर्ञिटुडवः (केवल धातु)
        if source_type == UpadeshaType.DHATU:
            indices, tags = apply_adir_nitudavah_1_3_5(varna_list)
            it_indices.update(indices)
            all_it_tags.extend(tags)

        # सूत्र १.३.६, १.३.७, १.३.८ (केवल प्रत्यय)
        if source_type == UpadeshaType.PRATYAYA:
            # १.३.६: षः प्रत्ययस्य
            idx6, tags6 = apply_shah_pratyayasya_1_3_6(varna_list)
            it_indices.update(idx6)
            all_it_tags.extend(tags6)

            # १.३.७: चुट्टू
            idx7, tags7 = apply_chuttu_1_3_7(varna_list)
            it_indices.update(idx7)
            all_it_tags.extend(tags7)

            # १.३.८: लशक्वतद्धिते
            idx8, tags8 = apply_lashakvataddhite_1_3_8(varna_list, is_taddhita)
            it_indices.update(idx8)
            all_it_tags.extend(tags8)

        # सूत्र १.३.२: उपदेशेऽजनुनासिक इत् (स्वर-इत् संज्ञा)
        idx2, tags2 = apply_upadeshe_ajanunasika_1_3_2(varna_list)
        it_indices.update(idx2)
        all_it_tags.extend(tags2)

        # सूत्र १.३.३: हलन्त्यम् (अन्त्य हल् संज्ञा)
        idx3, tags3 = apply_halantyam_1_3_3(varna_list, original_input, is_vibhakti)
        it_indices.update(idx3)
        all_it_tags.extend(tags3)

        # --- ३. तस्य लोपः (Execution Stage: 1.3.9) ---
        # अब उन सभी वर्णों का लोप (दर्शन) करें जिनकी संज्ञा हुई है।
        remaining_varnas = [
            v for idx, v in enumerate(varna_list)
            if idx not in it_indices
        ]

        return remaining_varnas, list(set(all_it_tags))