# core/it_sanjna_engine.py
from core.upadesha_registry import UpadeshaType
from logic.sanjna_rules import (
    apply_upadeshe_ajanunasika_1_3_2,
    apply_halantyam_1_3_3,
    apply_adir_nitudavah_1_3_5
)

class ItSanjnaEngine:
    @staticmethod
    def process_it_sanjna(varna_list, original_word, source_type):
        """
        सभी इत्-संज्ञा सूत्रों का क्रमवार संचालन।
        """
        # Step 0: सुरक्षा जाँच
        if not isinstance(source_type, UpadeshaType):
            return varna_list, []

        all_its = []

        # १. आदिर्ञिटुडवः (1.3.5) - केवल धातुओं के लिए प्रमुख
        if source_type == UpadeshaType.DHATU:
            varna_list, adi_its = apply_adir_nitudavah_1_3_5(varna_list)
            all_its.extend(adi_its)

        # २. उपदेशेऽजनुनासिक इत् (1.3.2)
        varna_list, anunasika_its = apply_upadeshe_ajanunasika_1_3_2(varna_list)
        all_its.extend(anunasika_its)

        # ३. हलन्त्यम् (1.3.3)
        varna_list, hal_its = apply_halantyam_1_3_3(varna_list, original_word)
        all_its.extend(hal_its)

        return varna_list, all_its