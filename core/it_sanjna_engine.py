# core/it_sanjna_engine.py
from core.upadesha_registry import UpadeshaType
from logic.sanjna_rules import (
    apply_upadeshe_ajanunasika_1_3_2,
    apply_halantyam_1_3_3,
    apply_adir_nitudavah_1_3_5
)
from utils.data_loader import get_all_vibhakti


class ItSanjnaEngine:
    @staticmethod
    def run_it_sanjna_prakaran(varna_list, original_word, source_type):
        """
        इत्-संज्ञा प्रकरण के सूत्रों का सामूहिक संचालन।
        विभक्ति ऑटो-डिटेक्शन और मूल-अवस्था सुरक्षा के साथ।
        """
        if not isinstance(source_type, UpadeshaType):
            return varna_list, []

        all_its = []

        # १. ऑटो-चेक: क्या यह मूल शब्द विभक्ति लिस्ट में है? (1.3.4 के लिए)
        vibhakti_list = get_all_vibhakti()
        is_vibhakti = original_word in vibhakti_list

        # २. महत्वपूर्ण: मूल अवस्था की पहचान (1.3.3 के गलत ट्रिगर को रोकने के लिए)
        # हम यह देख रहे हैं कि क्या मूल उपदेश के अंत में व्यंजन था
        original_last_varna = varna_list[-1] if varna_list else ""
        is_originally_halant = original_last_varna.endswith('्')

        # ३. आदिर्ञिटुडवः (1.3.5) - केवल धातु के लिए
        if source_type == UpadeshaType.DHATU:
            varna_list, adi_its = apply_adir_nitudavah_1_3_5(varna_list)
            all_its.extend(adi_its)

        # ४. उपदेशेऽजनुनासिक इत् (1.3.2) - सभी के लिए
        varna_list, anunasika_its = apply_upadeshe_ajanunasika_1_3_2(varna_list)
        all_its.extend(anunasika_its)

        # ५. हलन्त्यम् (1.3.3) और न विभक्तौ तुस्माः (1.3.4)
        # तर्क: हलन्त्यम् केवल तभी लगेगा जब मूल अंत हल् था और वह तुस्मा-विभक्ति नहीं है।
        if is_originally_halant:
            varna_list, hal_its = apply_halantyam_1_3_3(varna_list, original_word, is_vibhakti)
            all_its.extend(hal_its)

        return varna_list, all_its