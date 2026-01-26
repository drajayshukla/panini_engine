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
    पाणिनीय इत्-संज्ञा मास्टर इंजन (Initial Priority Model)
    सिद्धांत: १.३.९ (तस्य लोपः) से पहले सभी 'आदि', 'अन्त्य' और 'मध्य' वर्णों को मार्क करना।
    """

    @staticmethod
    def run_it_sanjna_prakaran(varna_list, original_input, source_type, is_taddhita=False):
        if not isinstance(source_type, UpadeshaType) or not varna_list:
            return varna_list, []

        all_it_tags = []
        it_indices = set()  # 重複 (Duplicate) इंडेक्स से बचने के लिए Set का उपयोग

        # --- १. तैयारी (Context Setup) ---
        vibhakti_list = get_all_vibhakti()
        is_vibhakti = original_input in vibhakti_list

        # --- २. आदि-इत् संज्ञा (Identification of Initial Varnas) ---
        # नियम: ये सभी नियम varna_list[0] या शुरुआत के वर्णों की जाँच करते हैं।

        #

        # सूत्र १.३.५: आदिर्ञिटुडवः (केवल धातु के लिए)
        if source_type == UpadeshaType.DHATU:
            idx5, tags5 = apply_adir_nitudavah_1_3_5(varna_list)
            it_indices.update(idx5)
            all_it_tags.extend(tags5)

        # सूत्र १.३.६, १.३.७, १.३.८ (प्रत्यय के लिए 'आदि' नियम)
        if source_type == UpadeshaType.PRATYAYA:
            # १.३.६: षः प्रत्ययस्य (आदि 'ष्')
            idx6, tags6 = apply_shah_pratyayasya_1_3_6(varna_list)
            it_indices.update(idx6)
            all_it_tags.extend(tags6)

            # १.३.७: चुट्टू (आदि च-वर्ग/ट-वर्ग)
            idx7, tags7 = apply_chuttu_1_3_7(varna_list, source_type)
            it_indices.update(idx7)
            all_it_tags.extend(tags7)

            # १.३.८: लशक्वतद्धिते (आदि ल, श, कु - तद्धित वर्जित)
            idx8, tags8 = apply_lashakvataddhite_1_3_8(varna_list, source_type, is_taddhita)
            it_indices.update(idx8)
            all_it_tags.extend(tags8)

        # --- ३. सार्वत्रिक और अन्त्य नियम (Universal & Final Rules) ---

        # सूत्र १.३.२: उपदेशेऽजनुनासिक इत् (स्वर बॉन्डिंग के साथ)
        idx2, tags2 = apply_upadeshe_ajanunasika_1_3_2(varna_list)
        it_indices.update(idx2)
        all_it_tags.extend(tags2)

        # सूत्र १.३.३: हलन्त्यम् (केवल तभी जब मूल रूप हलन्त हो)
        idx3, tags3 = apply_halantyam_1_3_3(varna_list, original_input, is_vibhakti)
        it_indices.update(idx3)
        all_it_tags.extend(tags3)

        # --- ४. तस्य लोपः (Final Execution - 1.3.9) ---
        # चिह्नित (Marked) इंडेक्स के आधार पर नए वर्ण-क्रम का निर्माण
        remaining_varnas = [
            v for idx, v in enumerate(varna_list)
            if idx not in it_indices
        ]

        return remaining_varnas, list(set(all_it_tags))