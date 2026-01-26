# core/it_sanjna_engine.py
from core.upadesha_registry import UpadeshaType
from logic.sanjna_rules import (
    apply_upadeshe_ajanunasika_1_3_2,
    apply_halantyam_1_3_3,
    apply_adir_nitudavah_1_3_5
)


class ItSanjnaEngine:
    @staticmethod
    def run_it_sanjna_prakaran(varna_list, original_word, source_type):
        """
        इत्-संज्ञा प्रकरण के सूत्रों का सामूहिक संचालन।
        """
        if not isinstance(source_type, UpadeshaType):
            return varna_list, []

        all_its = []

        # --- महत्वपूर्ण: मूल अवस्था की पहचान ---
        # हम यह देख रहे हैं कि क्या मूल उपदेश के अंत में व्यंजन था या स्वर/अनुनासिक
        original_last_varna = varna_list[-1] if varna_list else ""
        is_originally_halant = original_last_varna.endswith('्')
        # ----------------------------------

        # १. आदिर्ञिटुडवः (1.3.5)
        if source_type == UpadeshaType.DHATU:
            varna_list, adi_its = apply_adir_nitudavah_1_3_5(varna_list)
            all_its.extend(adi_its)

        # २. उपदेशेऽजनुनासिक इत् (1.3.2)
        varna_list, anunasika_its = apply_upadeshe_ajanunasika_1_3_2(varna_list)
        all_its.extend(anunasika_its)

        # ३. हलन्त्यम् (1.3.3)
        # तर्क: हलन्त्यम् केवल तभी लगेगा जब मूल उपदेश के अंत में व्यंजन था।
        # यदि अंत में 'ँ' था, तो वह १.३.२ का विषय है, १.३.३ का नहीं।
        if is_originally_halant:
            varna_list, hal_its = apply_halantyam_1_3_3(varna_list, original_word)
            all_its.extend(hal_its)

        return varna_list, all_its