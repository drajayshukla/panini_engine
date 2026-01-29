"""
FILE: core/controller.py
PAS-v2.0: 5.0 (Siddha)
ROLE: The Master Orchestrator (Pradhāna-Sūtradhāra)
"""

from core.phonology import ad, sanskrit_varna_samyoga
from core.analyzer import analyze_sanjna
from logic.it_engine import ItEngine
from core.upadesha_registry import UpadeshaType

def process_word_full_cycle(text, sutra_origin="0.0.0", source_type=UpadeshaType.DHATU, is_taddhita=False):
    """
    [PAS-5.0] सञ्चालक: - The Master Controller.
    Executes the full Prakriyā cycle from input to Siddha-rūpa.
    """

    # १. वर्ण विच्छेद (Varṇodaya - Pillar 0)
    # Generates Varna objects with Sthāna/Prayatna DNA.
    varna_list = ad(text)

    # २. Adhikāra Injection (DNA Enhancement)
    # Instead of re-wrapping, we inject the Upadesha metadata directly
    # into the existing Varna objects to maintain PAS-5 data integrity.
    for v in varna_list:
        v.origin = sutra_origin
        v.source_type = source_type
        # Trace the birth of the Upadesha
        v.trace.append(f"Injected as {source_type.name} via {sutra_origin}")

    # ३. संज्ञा विश्लेषण (Zone 1: Definitions)
    # Labels technical identities (Vriddhi, Guna, Samyoga).
    # PAS-5 Audit: Ensure analyze_sanjna uses the ordered rules.
    analysis = analyze_sanjna(varna_list)

    # ४. इत्-संज्ञा प्रकरण (Zone 1: The Surgical Scrub)
    # Identifies markers and performs 1.3.9 तस्य लोपः
    remaining_varnas, it_tags = ItEngine.run_it_prakaran(
        varna_list,
        source_type=source_type,
        is_taddhita=is_taddhita
    )

    # ५. वर्ण संयोग (Prakriyā Synthesis)
    # Joins the remaining surgical units back into a readable Sanskrit string.
    final_text = sanskrit_varna_samyoga(remaining_varnas)

    return {
        "original_varnas": varna_list,
        "analysis": analysis,
        "it_tags": it_tags,
        "remaining_varnas": remaining_varnas,
        "final_result": final_text
    }