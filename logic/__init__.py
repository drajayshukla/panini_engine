# panini_engine/logic/__init__.py

# १. संज्ञा नियम (Sanjna Rules)
from .sanjna_rules import (
    apply_upadeshe_ajanunasika_1_3_2,
    apply_halantyam_1_3_3,
    apply_na_vibhaktau_1_3_4,
    apply_adir_nitudavah_1_3_5,
    apply_shah_pratyayasya_1_3_6,
    apply_chuttu_1_3_7,
    apply_lashakvataddhite_1_3_8
)

# २. स्थान और स्वर नियम (Phonetic Rules)
from .sthana_rules import apply_sthana_to_varna
from .svara_rules import apply_svara_sanjna

# ३. अङ्ग कार्य (Morphology - भविष्य के लिए)
# from .morph_rules import apply_ata_upadhayah_7_2_116