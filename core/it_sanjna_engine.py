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
    पाणिनीय इत्-संज्ञा मास्टर इंजन (Refined Version)
    १.३.२ से १.३.८ तक के सभी नियमों का पूर्ण कार्यान्वयन।
    """

    @staticmethod
    def run_it_sanjna_prakaran(varna_list, original_input, source_type, is_taddhita=False):
        if not isinstance(source_type, UpadeshaType) or not varna_list:
            return varna_list, []

        it_tags = []

        # --- १. तैयारी (Context Setup) ---
        vibhakti_list = get_all_vibhakti()
        is_vibhakti = original_input in vibhakti_list

        # हलन्त्यम् के लिए मूल स्थिति को याद रखना आवश्यक है
        original_last_varna = varna_list[-1]
        is_originally_halant = original_last_varna.endswith('्')

        # --- २. आदि-इत् संज्ञा (Initial Varna Rules) ---

        # १.३.५: आदिर्ञिटुडवः (केवल धातु)
        if source_type == UpadeshaType.DHATU:
            varna_list, tags5 = apply_adir_nitudavah_1_3_5(varna_list)
            it_tags.extend(tags5)

        # १.३.६, १.३.७, १.३.८ (केवल प्रत्यय)
        if source_type == UpadeshaType.PRATYAYA:
            # १.३.६ षः प्रत्ययस्य
            varna_list, tags6 = apply_shah_pratyayasya_1_3_6(varna_list)
            it_tags.extend(tags6)

            # १.३.७ चुट्टू
            varna_list, tags7 = apply_chuttu_1_3_7(varna_list)
            it_tags.extend(tags7)

            # १.३.८ लशक्वतद्धिते (is_taddhita फ्लैग के साथ)
            varna_list, tags8 = apply_lashakvataddhite_1_3_8(varna_list, is_taddhita)
            it_tags.extend(tags8)

        # --- ३. स्वर-इत् संज्ञा (Universal Vowel Rules) ---

        # १.३.२: उपदेशेऽजनुनासिक इत्
        varna_list, tags2 = apply_upadeshe_ajanunasika_1_3_2(varna_list)
        it_tags.extend(tags2)

        # --- ४. अन्त्य-इत् संज्ञा (Final Varna Rules) ---

        # १.३.३: हलन्त्यम् (१.३.४ के प्रतिषेध के साथ)
        if is_originally_halant:
            varna_list, tags3 = apply_halantyam_1_3_3(varna_list, original_input, is_vibhakti)
            it_tags.extend(tags3)

        return varna_list, it_tags