import os
from logic.sanjna_rules import check_vriddhi_1_1_1, check_guna_1_1_2, get_sutra_link

def analyze_sanjna(varna_list):
    """
    अष्टाध्यायी के संज्ञा सूत्रों के आधार पर Varna Objects का विश्लेषण।
    """
    analysis_report = []

    # संयोग संज्ञा के लिए व्यंजन (हल्) की पहचान (is_vowel का उपयोग करें)
    is_hal = [not v.is_vowel for v in varna_list]

    for i, varna_obj in enumerate(varna_list):
        tags = []

        # १. वृद्धि संज्ञा (१.१.१)
        v_tag = check_vriddhi_1_1_1(varna_obj)
        if v_tag: tags.append(v_tag)

        # २. गुण संज्ञा (१.१.२)
        g_tag = check_guna_1_1_2(varna_obj)
        if g_tag: tags.append(g_tag)

        # ३. संयोग संज्ञा (१.१.७) - हलोऽनन्तराः संयोगः
        # बिना किसी स्वर के व्यवधान के जब दो या अधिक व्यंजन मिलते हैं
        if is_hal[i]:
            has_prev_hal = (i > 0 and is_hal[i - 1])
            has_next_hal = (i < len(varna_list) - 1 and is_hal[i + 1])
            if has_prev_hal or has_next_hal:
                link = get_sutra_link("1.1.7")
                tags.append(f"[संयोग (१.१.७)]({link})")

        # ४. अनुनासिक संज्ञा (१.१.८) - मुखनासिकावचनोऽनुनासिकः
        # Varna Object के .is_anunasika या स्थान (नासिका) का उपयोग करें
        if varna_obj.is_anunasika or (varna_obj.sthana and "नासिका" in varna_obj.sthana):
            link = get_sutra_link("1.1.8")
            tags.append(f"[अनुनासिक (१.१.८)]({link})")

        analysis_report.append({
            "varna": varna_obj.char,
            "tags": tags,
            "sthana": varna_obj.sthana  # स्थान विश्लेषण भी रिपोर्ट में जोड़ें
        })

    return analysis_report