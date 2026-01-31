"""
FILE: core/knowledge_base.py
"""
class KnowledgeBase:
    SUP_MAP = {
        1: [("सुँ", set()), ("औ", set()), ("जस्", set())],
        2: [("अम्", set()), ("औट्", set()), ("शस्", set())],
        3: [("टा", set()), ("भ्याम्", set()), ("भिस्", set())],
        4: [("ङे", set()), ("भ्याम्", set()), ("भ्यस्", set())],
        5: [("ङसिँ", set()), ("भ्याम्", set()), ("भ्यस्", set())],
        6: [("ङस्", set()), ("ओस्", set()), ("आम्", set())],
        7: [("ङि", set()), ("ओस्", set()), ("सुप्", set())],
        8: [("सुँ", set()), ("औ", set()), ("जस्", set())] # Sambodhana (Reuse Prathama)
    }
    @staticmethod
    def get_sup(vibhakti, vacana):
        if vibhakti in KnowledgeBase.SUP_MAP:
            row = KnowledgeBase.SUP_MAP[vibhakti]
            if 1 <= vacana <= 3: return row[vacana-1]
        return None
    @staticmethod
    def is_sarvanama(word):
        sarva_list = ["सर्व", "विश्व", "उभ", "उभय", "डतर", "डतम", "अन्य", "अन्यतर", "इतर", "त्वत्", "त्व", "नेम", "सम", "सिम", "पूर्व", "पर", "अवर", "दक्षिण", "उत्तर", "अपर", "अधर", "स्व", "अन्तर", "त्यद्", "तद्", "यद्", "एतद्", "इदम्", "अदस्", "एक", "द्वि", "युष्मद्", "अस्मद्", "भवत्", "किम्"]
        return word in sarva_list
