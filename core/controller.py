# panini_engine/core/controller.py

from core.phonology import ad, sanskrit_varna_samyoga
from core.analyzer import analyze_sanjna
from logic.it_engine import ItEngine
from core.upadesha_registry import UpadeshaType, Upadesha


def process_word_full_cycle(text, sutra_origin="0.0.0", source_type=UpadeshaType.DHATU, is_taddhita=False):
    """
    सञ्चालक: - The Master Controller.
    Physiology (ad) -> DNA (Upadesha) -> Diagnosis (Sanjna) -> Scrub (It-Engine) -> Synthesis
    """

    # १. वर्ण विच्छेद (Physiology)
    # Using the master foundation 'ad' to analyze the raw string.
    # Returns a list of Varna objects.
    base_varnas = ad(text)

    # २. DNA Birth (Upadesha Wrapping)
    # Every character is promoted to an Upadesha object to carry its Shastric GPS.
    # We use v.char to extract the pure phonetic unit for the Upadesha constructor.
    varna_list = [Upadesha(v.char, sutra_origin) for v in base_varnas]

    # ३. संज्ञा विश्लेषण (Diagnosis - Zone 1)
    # Labels technical identities like Vṛddhi, Guṇa, and Saṃyoga.
    analysis = analyze_sanjna(varna_list)

    # ४. इत्-संज्ञा प्रकरण (The Surgical Scrub - logic/it_engine.py)
    # Identifies markers and performs तस्य लोपः (1.3.9) with specific source logic.
    remaining_varnas, it_tags = ItEngine.run_it_prakaran(
        varna_list,
        source_type=source_type,
        is_taddhita=is_taddhita
    )

    # ५. वर्ण संयोग (Final Synthesis)
    # Joins the remaining surgical units back into a readable Sanskrit string.
    final_text = sanskrit_varna_samyoga(remaining_varnas)

    return {
        "original_varnas": varna_list,
        "analysis": analysis,
        "it_tags": it_tags,
        "remaining_varnas": remaining_varnas,
        "final_result": final_text
    }