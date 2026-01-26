import os
# फंक्शन्स को उनके सही स्थान (logic/sanjna_rules.py) से बुलाना
from logic.sanjna_rules import check_vriddhi_1_1_1, check_guna_1_1_2, get_sutra_link


def analyze_sanjna(varna_list):
    """
    अष्टाध्यायी के संज्ञा सूत्रों के आधार पर वर्णों का विश्लेषण।
    """
    analysis_report = []

    # संयोग संज्ञा के लिए व्यंजन (हल्) की पहचान
    is_hal = [v.endswith('्') for v in varna_list]

    for i, varna in enumerate(varna_list):
        tags = []

        # १. वृद्धि संज्ञा (१.१.१)
        v_tag = check_vriddhi_1_1_1(varna)
        if v_tag: tags.append(v_tag)

        # २. गुण संज्ञा (१.१.२)
        g_tag = check_guna_1_1_2(varna)
        if g_tag: tags.append(g_tag)

        # ३. संयोग संज्ञा (१.१.७) - बिना स्वर के व्यंजन का जुड़ना
        if is_hal[i]:
            has_prev_hal = (i > 0 and is_hal[i - 1])
            has_next_hal = (i < len(varna_list) - 1 and is_hal[i + 1])
            if has_prev_hal or has_next_hal:
                link = get_sutra_link("1.1.7")
                tags.append(f"[संयोग (१.१.७)]({link})")

        # ४. अनुनासिक संज्ञा (१.१.८)
        anunasika_markers = ['ँ', 'ङ्', 'ञ्', 'ण्', 'न्', 'म्']
        if any(m in varna for m in anunasika_markers):
            link = get_sutra_link("1.1.8")
            tags.append(f"[अनुनासिक (१.१.८)]({link})")

        analysis_report.append({"varna": varna, "tags": tags})

    return analysis_report