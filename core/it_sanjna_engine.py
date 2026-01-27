from core.upadesha_registry import UpadeshaType
from logic.sanjna_rules import (
    apply_upadeshe_ajanunasika_1_3_2,
    apply_halantyam_1_3_3,
    apply_na_vibhaktau_1_3_4,  # New: Clinical Shield
    apply_adir_nitudavah_1_3_5,
    apply_shah_pratyayasya_1_3_6,
    apply_chuttu_1_3_7,
    apply_lashakvataddhite_1_3_8
)


# ==============================================================================
# ENGINE FEATURES (KAUMUDI ALIGNMENT):
# 1. Sequential Sutra Processing: Follows Siddhanta Kaumudi's Sanjna Prakaran order.
# 2. Protection First (1.3.4): Applies the Vibhakti shield before Halantyam (1.3.3).
# 3. Targeted Scoping: Distinct logic paths for Dhatu vs. Pratyaya/Vibhakti.
# 4. Global It-Registry: Collects all indices before a single surgical deletion (1.3.9).
# 5. Taddhita Awareness: Auto-blocks 1.3.8 if the Upadesha is a Taddhita suffix.
# 6. Granular Tagging: Returns human-readable sutra citations for diagnostic UI.
# ==============================================================================

class ItSanjnaEngine:
    """
    पाणिनीय इत्-संज्ञा मास्टर इंजन (कौमुदी-प्रकरण मॉडल)
    संशोधित क्रम: अजनुनासिक -> विभक्ति निषेध (Shield) -> हलन्त्यम् -> आदि-इत् -> लोप
    """

    @staticmethod
    def run_it_sanjna_prakaran(varna_list, original_input, source_type, is_taddhita=False):
        """
        कौमुदी के संज्ञा-प्रकरण के क्रम में सूत्रों का निष्पादन।
        """
        # क्लिनिकल चेक
        if not isinstance(source_type, UpadeshaType) or not varna_list:
            return varna_list, []

        it_indices = set()
        sutra_tags = []

        # १. उपदेशेऽजनुनासिक इत् (१.३.२) - सबसे पहले अच् (स्वर) का परीक्षण
        idx2, tags2 = apply_upadeshe_ajanunasika_1_3_2(varna_list)
        it_indices.update(idx2)
        sutra_tags.extend(tags2)

        # २. न विभक्तौ तुस्माः (१.३.४) - सुरक्षा कवच (Clinical Shield)
        # यह सूत्र हलन्त्यम् (१.३.३) के लिए 'Blocked' इंडेक्स की सूची तैयार करता है
        blocked_indices = []
        if source_type == UpadeshaType.VIBHAKTI:
            blocked_indices = apply_na_vibhaktau_1_3_4(varna_list)

        # ३. हलन्त्यम् (१.३.३) - केवल उन्हीं को छुएगा जो १.३.४ द्वारा सुरक्षित नहीं हैं
        idx3, tags3 = apply_halantyam_1_3_3(varna_list, blocked_indices)
        it_indices.update(idx3)
        sutra_tags.extend(tags3)

        # ४. आदि-इत् संज्ञा (धातु एवं प्रत्यय के विशिष्ट नियम)

        # धातु-आदि नियम: १.३.५ आदिर्ञिटुडवः
        if source_type == UpadeshaType.DHATU:
            idx5, tags5 = apply_adir_nitudavah_1_3_5(varna_list)
            it_indices.update(idx5)
            sutra_tags.extend(tags5)

        # प्रत्यय/विभक्ति-आदि नियम: १.३.६, १.३.७, १.३.८
        elif source_type in [UpadeshaType.PRATYAYA, UpadeshaType.VIBHAKTI]:

            # १.३.६: षः प्रत्ययस्य (आदि 'ष्')
            idx6, tags6 = apply_shah_pratyayasya_1_3_6(varna_list)
            it_indices.update(idx6)
            sutra_tags.extend(tags6)

            # १.३.७: चुट्टू (आदि च-वर्ग/ट-वर्ग)
            idx7, tags7 = apply_chuttu_1_3_7(varna_list)
            it_indices.update(idx7)
            sutra_tags.extend(tags7)

            # १.३.८: लशक्वतद्धिते (आदि ल, श, कु - तद्धित वर्जित)
            # 'ङि' का 'ङ्' इसी सूत्र द्वारा 'Surgically' निकाला जाएगा
            idx8, tags8 = apply_lashakvataddhite_1_3_8(varna_list, source_type, is_taddhita)
            it_indices.update(idx8)
            sutra_tags.extend(tags8)

        # ५. तस्य लोपः (१.३.९) - चिह्नित वर्णों का अंतिम निष्कासन
        remaining_varnas = [
            v for idx, v in enumerate(varna_list)
            if idx not in it_indices
        ]

        return remaining_varnas, list(set(sutra_tags))