# panini_engine/core/controller.py

from core.phonology import sanskrit_varna_vichhed, sanskrit_varna_samyoga
from core.analyzer import analyze_sanjna
from core.it_sanjna_engine import ItSanjnaEngine
from core import UpadeshaType


def process_word_full_cycle(text, source_type=UpadeshaType.DHATU, is_vibhakti=False, is_taddhita=False):
    """
    पूरे पाणिनीय चक्र को नियंत्रित करने वाला फंक्शन:
    Vichhed -> Sanjna Analysis -> It-Sanjna -> Samyoga
    """
    # १. वर्ण विच्छेद (Physiology)
    varna_list = sanskrit_varna_vichhed(text)

    # २. संज्ञा विश्लेषण (Diagnosis)
    analysis = analyze_sanjna(varna_list)

    # ३. इत्-संज्ञा प्रकरण (Surgical Identification)
    remaining_varnas, it_tags = ItSanjnaEngine.run_it_sanjna_prakaran(
        varna_list.copy(),
        source_type=source_type,
        is_vibhakti=is_vibhakti,
        is_taddhita=is_taddhita
    )

    # ४. तस्य लोपः (१.३.९) और अंतिम संयोग
    final_text = sanskrit_varna_samyoga(remaining_varnas)

    return {
        "original_varnas": varna_list,
        "analysis": analysis,
        "it_tags": it_tags,
        "remaining_varnas": remaining_varnas,
        "final_result": final_text
    }