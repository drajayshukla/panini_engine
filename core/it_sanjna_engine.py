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
        # १. बेसिक चेक (Vital Signs Check)
        if not isinstance(source_type, UpadeshaType) or not varna_list:
            return varna_list, []

        all_it_tags = []
        it_indices = set()  # इत् वर्णों की अनुक्रमणिकाएँ

        # २. 'विभक्ति' भी एक 'प्रत्यय' है, इसलिए प्रत्यय के नियम (1.3.6, 1.3.7, 1.3.8)
        # इस पर भी लागू होने चाहिए।
        is_pratyaya_type = source_type in [UpadeshaType.PRATYAYA, UpadeshaType.VIBHAKTI]

        # --- ३. आदि-इत् संज्ञा (Identification: आदिः प्रत्ययस्य) ---

        # १.३.५: आदिर्ञिटुडवः (केवल धातु)
        if source_type == UpadeshaType.DHATU:
            idx5, tags5 = apply_adir_nitudavah_1_3_5(varna_list)
            it_indices.update(idx5)
            all_it_tags.extend(tags5)

        # प्रत्यय-विशिष्ट आदि-नियम (VIBHAKTI पर भी लागू होंगे)
        if is_pratyaya_type:
            # १.३.६: षः प्रत्ययस्य
            idx6, tags6 = apply_shah_pratyayasya_1_3_6(varna_list)
            it_indices.update(idx6)
            all_it_tags.extend(tags6)

            # १.३.७: चुट्टू (आदि च-वर्ग/ट-वर्ग)
            idx7, tags7 = apply_chuttu_1_3_7(varna_list, source_type)
            it_indices.update(idx7)
            all_it_tags.extend(tags7)

            # १.३.८: लशक्वतद्धिते (is_taddhita फ्लैग के साथ)
            idx8, tags8 = apply_lashakvataddhite_1_3_8(varna_list, source_type, is_taddhita)
            it_indices.update(idx8)
            all_it_tags.extend(tags8)

        # --- ४. सार्वत्रिक और अन्त्य नियम (Universal & Final Rules) ---

        # १.३.२: उपदेशेऽजनुनासिक इत् (स्वर-इत् संज्ञा)
        idx2, tags2 = apply_upadeshe_ajanunasika_1_3_2(varna_list)
        it_indices.update(idx2)
        all_it_tags.extend(tags2)

        # १.३.३: हलन्त्यम् (यहाँ source_type भेजना अनिवार्य है ताकि 1.3.4 सक्रिय हो)
        # जस् (Jasa) के 'स्' को बचाने के लिए यही 'Critical' पॉइंट है।
        idx3, tags3 = apply_halantyam_1_3_3(varna_list, original_input, source_type)
        it_indices.update(idx3)
        all_it_tags.extend(tags3)

        # --- ५. तस्य लोपः (Execution: १.३.९) ---
        # अंत में उन सभी वर्णों का लोप करें जिनकी संज्ञा हुई है।
        remaining_varnas = [
            v for idx, v in enumerate(varna_list)
            if idx not in it_indices
        ]

        return remaining_varnas, list(set(all_it_tags))