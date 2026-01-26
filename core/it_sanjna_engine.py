from core.upadesha_registry import UpadeshaType
from logic.sanjna_rules import (
    apply_upadeshe_ajanunasika_1_3_2,
    apply_halantyam_1_3_3,
    apply_adir_nitudavah_1_3_5
)
from utils.data_loader import get_all_vibhakti


class ItSanjnaEngine:
    """
    पाणिनीय इत्-संज्ञा मास्टर इंजन (Integrated Version)
    नियम: १.३.२ से १.३.८ तक का सामूहिक संचालन।
    """

    @staticmethod
    def run_it_sanjna_prakaran(varna_list, original_input, source_type):
        if not isinstance(source_type, UpadeshaType):
            return varna_list, []

        it_tags = []

        # --- १. तैयारी और डेटा डिटेक्शन ---
        vibhakti_list = get_all_vibhakti()
        is_vibhakti = original_input in vibhakti_list

        # हलन्त्यम् की सुरक्षा के लिए मूल स्थिति की जांच
        original_last_varna = varna_list[-1] if varna_list else ""
        is_originally_halant = original_last_varna.endswith('्')

        # --- २. आदि-इत् संज्ञा सूत्र (Initial Rules) ---

        # सूत्र १.३.५: आदिर्ञिटुडवः (केवल धातु के लिए)
        if source_type == UpadeshaType.DHATU:
            varna_list, adi_its = apply_adir_nitudavah_1_3_5(varna_list)
            if adi_its: it_tags.extend([f"१.३.५ (आदिर्ञिटुडवः) - {i} इत्" for i in adi_its])

        # सूत्र १.३.६: षः प्रत्ययस्य (केवल प्रत्यय के लिए)
        varna_list, tag_6 = ItSanjnaEngine.apply_shah_pratyayasya(varna_list, source_type)
        if tag_6: it_tags.append(tag_6)

        # --- ३. मध्य/स्वर इत् संज्ञा सूत्र ---

        # सूत्र १.३.२: उपदेशेऽजनुनासिक इत् (सभी के लिए)
        varna_list, anunasika_its = apply_upadeshe_ajanunasika_1_3_2(varna_list)
        if anunasika_its: it_tags.extend([f"१.३.२ (उपदेशेऽजनुनासिक इत्) - {i} इत्" for i in anunasika_its])

        # --- ४. अन्त्य-इत् संज्ञा सूत्र (Final Rules) ---

        # सूत्र १.३.३: हलन्त्यम् (सुरक्षा: १.३.४ न विभक्तौ तुस्माः के साथ)
        if is_originally_halant:
            varna_list, hal_its = apply_halantyam_1_3_3(varna_list, original_input, is_vibhakti)
            if hal_its: it_tags.extend([f"१.३.३ (हलन्त्यम्) - {i} इत्" for i in hal_its])

        # भविष्य के लिए: १.३.७ (चुट्टू) और १.३.८ (लशक्वतद्धिते) यहाँ जोड़े जाएंगे

        return varna_list, it_tags

    @staticmethod
    def apply_shah_pratyayasya(varna_list, source_type):
        """
        नियम १.३.६: प्रत्यय के आदि 'ष्' का लोप।
        """
        if source_type == UpadeshaType.PRATYAYA:
            if varna_list and varna_list[0] == 'ष्':
                varna_list.pop(0)
                return varna_list, "१.३.६ (षः प्रत्ययस्य) - ष् इत्"
        return varna_list, None