from logic.sanjna_rules import check_vriddhi_1_1_1, check_guna_1_1_2


def analyze_sanjna(varna_list):
    """
    अष्टाध्यायी के संज्ञा सूत्रों के आधार पर वर्णों का विश्लेषण।
    """
    analysis_report = []

    for varna in varna_list:
        tags = []

        # 1.1.1 वृद्धि संज्ञा की जाँच
        v_tag = check_vriddhi_1_1_1(varna)
        if v_tag: tags.append(v_tag)

        # 1.1.2 गुण संज्ञा की जाँच
        g_tag = check_guna_1_1_2(varna)
        if g_tag: tags.append(g_tag)

        analysis_report.append({"varna": varna, "tags": tags})

    return analysis_report