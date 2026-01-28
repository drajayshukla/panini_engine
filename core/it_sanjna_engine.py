#/core/it_sanjna_engine.py
from core.upadesha_registry import UpadeshaType
from logic.sanjna_rules import (
    apply_upadeshe_ajanunasika_1_3_2,
    apply_na_vibhaktau_1_3_4,
    apply_halantyam_1_3_3,
    apply_adir_nitudavah_1_3_5,
    apply_shah_pratyayasya_1_3_6,
    apply_chuttu_1_3_7,
    apply_lashakvataddhite_1_3_8
)


# ==============================================================================
# INTEGRATED ENGINE FEATURES (KAUMUDI + BULK CAPABILITIES):
# 1. Sequential Sutra Processing: Follows Siddhanta Kaumudi's Sanjna Prakaran order.
# 2. Shield-First Architecture: na-vibhaktau (1.3.4) creates a blockade before halantyam (1.3.3).
# 3. Comprehensive Scoping: Distinct logic paths for Dhatu vs. Pratyaya/Vibhakti scope.
# 4. Global It-Registry: Collects all indices before a single surgical deletion (1.3.9).
# 5. Taddhita Isolation: Automatically restricts 1.3.8 if the Upadesha is a Taddhita.
# 6. Duplicate Prevention: Uses Set and list(set()) to ensure tags and indices are unique.
# ==============================================================================

class ItSanjnaEngine:
    """
    पाणिनीय इत्-संज्ञा मास्टर इंजन (एकीकृत कौमुदी-प्रकरण मॉडल)
    प्रवाह: अजनुनासिक -> विभक्ति सुरक्षा (1.3.4) -> हलन्त्यम् -> आदि-इत् (1.3.5-8) -> लोप
    """

    @staticmethod
    def run_it_sanjna_prakaran(varna_list, original_input, source_type, is_taddhita=False):
        """
        varna_list: विच्छेदित वर्णों की सूची
        source_type: UpadeshaType (DHATU, PRATYAYA, VIBHAKTI, etc.)
        is_taddhita: तद्धित मास्टर डेटा से प्राप्त ऑटो-फ्लैग
        """
        # क्लिनिकल चेक (Vital Signs)
        if not isinstance(source_type, UpadeshaType) or not varna_list:
            return varna_list, []

        it_indices = set()
        sutra_tags = []

        # १. उपदेशेऽजनुनासिक इत् (१.३.२) - सबसे पहले अच् (स्वर) का परीक्षण
        idx2, tags2 = apply_upadeshe_ajanunasika_1_3_2(varna_list)
        it_indices.update(idx2)
        sutra_tags.extend(tags2)

        # २. सुरक्षा कवच: न विभक्तौ तुस्माः (१.३.४) - विभक्ति निषेध सबसे पहले
        # यह विधि हलन्त्यम् (१.३.३) को 'Blocked' इंडेक्स की सूची प्रदान करती है
        blocked_indices = []
        if source_type == UpadeshaType.VIBHAKTI:
            blocked_indices = apply_na_vibhaktau_1_3_4(varna_list)

        # ३. हलन्त्यम् (१.३.३) - ब्लॉक्ड इंडेक्स (१.३.४) का सम्मान करते हुए
        idx3, tags3 = apply_halantyam_1_3_3(varna_list, blocked_indices)
        it_indices.update(idx3)
        sutra_tags.extend(tags3)

        # ४. आदि-इत् संज्ञा (Identification: आदिः - १.३.५ से १.३.८)

        # धातु-आदि नियम (१.३.५ आदिर्ञिटुडवः)
        if source_type == UpadeshaType.DHATU:
            idx5, tags5 = apply_adir_nitudavah_1_3_5(varna_list)
            it_indices.update(idx5)
            sutra_tags.extend(tags5)

        # प्रत्यय/विभक्ति-आदि नियम (१.३.६, १.३.७, १.३.८)
        elif source_type in [UpadeshaType.PRATYAYA, UpadeshaType.VIBHAKTI]:

            # १.३.६: षः प्रत्ययस्य (source_type जोड़ें)
            idx6, tags6 = apply_shah_pratyayasya_1_3_6(varna_list, source_type)
            it_indices.update(idx6)
            sutra_tags.extend(tags6)

            # १.३.७: चुटू (source_type जोड़ें)
            idx7, tags7 = apply_chuttu_1_3_7(varna_list, source_type)
            it_indices.update(idx7)
            sutra_tags.extend(tags7)

            # १.३.८: लशक्वतद्धिते (is_taddhita पहले से है, perfect)
            idx8, tags8 = apply_lashakvataddhite_1_3_8(varna_list, source_type, is_taddhita)
            it_indices.update(idx8)
            sutra_tags.extend(tags8)

        # ५. तस्य लोपः (१.३.९) - चिह्नित इंडेक्स के वर्णों का निष्कासन
        remaining_varnas = [
            v for idx, v in enumerate(varna_list)
            if idx not in it_indices
        ]

        return remaining_varnas, list(set(sutra_tags))