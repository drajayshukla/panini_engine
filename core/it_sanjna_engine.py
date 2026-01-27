from core.upadesha_registry import UpadeshaType
from logic.sanjna_rules import (
    apply_upadeshe_ajanunasika_1_3_2,
    apply_halantyam_1_3_3,
    apply_adir_nitudavah_1_3_5,
    apply_shah_pratyayasya_1_3_6,
    apply_chuttu_1_3_7,
    apply_lashakvataddhite_1_3_8
)

class ItSanjnaEngine:
    """
    पाणिनीय इत्-संज्ञा मास्टर इंजन (Initial Priority Model)
    कार्यप्रणाली: पहले सभी सूत्रों ($1.3.2$ - $1.3.8$) द्वारा वर्णों की संज्ञा/टैगिंग,
    और अंत में $1.3.9$ (तस्य लोपः) द्वारा निष्कासन।
    """

    @staticmethod
    def run_it_sanjna_prakaran(varna_list, original_input, source_type, is_taddhita=False):
        """
        varna_list: विच्छेदित वर्णों की सूची
        source_type: UpadeshaType (DHATU, PRATYAYA, VIBHAKTI, etc.)
        is_taddhita: तद्धित मास्टर डेटा से प्राप्त ऑटो-फ्लैग
        """
        # १. क्लिनिकल चेक (Vital Signs)
        if not isinstance(source_type, UpadeshaType) or not varna_list:
            return varna_list, []

        all_it_tags = []
        it_indices = set()  # यूनिक इंडेक्स स्टोर करने के लिए

        # २. प्रत्यय और विभक्ति दोनों पर प्रत्यय-आदि नियम लागू होते हैं
        is_pratyaya_scope = source_type in [UpadeshaType.PRATYAYA, UpadeshaType.VIBHAKTI]

        # --- ३. आदि-इत् संज्ञा (Identification: आदिः) ---

        # सूत्र $1.3.5$: आदिर्ञिटुडवः (केवल धातु के लिए)
        if source_type == UpadeshaType.DHATU:
            idx5, tags5 = apply_adir_nitudavah_1_3_5(varna_list)
            it_indices.update(idx5)
            all_it_tags.extend(tags5)

        # प्रत्यय-आदि नियम ($1.3.6, 1.3.7, 1.3.8$)
        if is_pratyaya_scope:
            # $1.3.6$: षः प्रत्ययस्य (आदि 'ष्')
            idx6, tags6 = apply_shah_pratyayasya_1_3_6(varna_list)
            it_indices.update(idx6)
            all_it_tags.extend(tags6)

            # $1.3.7$: चुट्टू (आदि च-वर्ग/ट-वर्ग)
            idx7, tags7 = apply_chuttu_1_3_7(varna_list, source_type)
            it_indices.update(idx7)
            all_it_tags.extend(tags7)

            # $1.3.8$: लशक्वतद्धिते (is_taddhita द्वारा ऑटो-ब्लॉक क्षमता के साथ)
            idx8, tags8 = apply_lashakvataddhite_1_3_8(varna_list, source_type, is_taddhita)
            it_indices.update(idx8)
            all_it_tags.extend(tags8)

        # --- ४. सार्वत्रिक और अन्त्य नियम (Universal & Final Rules) ---

        # सूत्र $1.3.2$: उपदेशेऽजनुनासिक इत् (अनुनासिक स्वर)
        idx2, tags2 = apply_upadeshe_ajanunasika_1_3_2(varna_list)
        it_indices.update(idx2)
        all_it_tags.extend(tags2)

        # सूत्र $1.3.3$: हलन्त्यम् (विभक्ति होने पर $1.3.4$ निषेध ऑटो-एक्टिवेट होगा)
        idx3, tags3 = apply_halantyam_1_3_3(varna_list, original_input, source_type)
        it_indices.update(idx3)
        all_it_tags.extend(tags3)

        # --- ५. तस्य लोपः (Execution: $1.3.9$) ---
        # चिह्नित इंडेक्स के वर्णों को हटाकर शेष अङ्ग का निर्माण
        remaining_varnas = [
            v for idx, v in enumerate(varna_list)
            if idx not in it_indices
        ]

        return remaining_varnas, list(set(all_it_tags))