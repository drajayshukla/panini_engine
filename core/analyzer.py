# core/analyzer.py
from core.sanjna_engine import SanjnaEngine

def analyze_sanjna(varna_list):
    """
    अष्टाध्यायी के संज्ञा सूत्रों के आधार पर Varna Objects का विश्लेषण।
    Diagnostic Tool for Zone 1 (Definitions).
    """
    analysis_report = []

    # संयोग संज्ञा के लिए व्यंजन (हल्) की स्थिति की पहचान
    # Sutra 1.1.7: हलोऽनन्तराः संयोगः
    is_hal_map = [SanjnaEngine.is_hal(v.char) for v in varna_list]

    for i, varna_obj in enumerate(varna_list):
        tags = []

        # १. वृद्धि संज्ञा (१.१.१) - वृद्धिरादैच्
        if SanjnaEngine.is_vriddhi_1_1_1(varna_obj.char):
            tags.append("वृद्धि (१.१.१)")

        # २. गुण संज्ञा (१.१.२) - अदेङ्गुणः
        if SanjnaEngine.is_guna_1_1_2(varna_obj.char):
            tags.append("गुण (१.१.२)")

        # ३. संयोग संज्ञा (१.१.७) - हलोऽनन्तराः संयोगः
        # Logic: If this is a Hal AND it is adjacent to another Hal without a vowel.
        if is_hal_map[i]:
            has_prev_hal = (i > 0 and is_hal_map[i - 1])
            has_next_hal = (i < len(varna_list) - 1 and is_hal_map[i + 1])
            if has_prev_hal or has_next_hal:
                tags.append("संयोग (१.१.७)")

        # ४. अनुनासिक संज्ञा (१.१.८) - मुखनासिकावचनोऽनुनासिकः
        # Logic: Check if it's anunasika via Upadesha metadata or Sthana.
        if hasattr(varna_obj, 'is_anunasika') and varna_obj.is_anunasika:
            tags.append("अनुनासिक (१.१.८)")
        elif hasattr(varna_obj, 'sthana') and varna_obj.sthana and "नासिका" in varna_obj.sthana:
            tags.append("अनुनासिक (१.१.८)")

        analysis_report.append({
            "varna": varna_obj.char,
            "tags": tags,
            "sthana": getattr(varna_obj, 'sthana', 'Unknown'),
            "is_hal": is_hal_map[i]
        })

    return analysis_report