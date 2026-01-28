# panini_engine/logic/anuvritti_handler.py

class AnuvrittiHandler:
    """
    पाणिनीय अनुवृत्ति इंजन।
    उद्देश्य: पिछले सूत्रों से पदों (Keywords) को वर्तमान सूत्र में लाना।
    """

    @staticmethod
    def get_inherited_terms(current_sutra_num, master_sutra_list):
        """
        वर्तमान सूत्र संख्या के आधार पर अनुवृत्त पदों की पहचान करना।
        उदाहरण: 'हलन्त्यम्' (1.3.3) में 'उपदेशे' और 'इत्' की अनुवृत्ति 1.3.2 से आती है।
        """
        # अभी के लिए एक साधारण मैपिंग (Hard-coded logic for core Sanjna Sutras)
        # भविष्य में इसे अष्टाध्यायी के 'Adhyaya.Pada' रेंज के आधार पर डायनामिक करेंगे।

        inheritance_map = {
            "1.3.3": ["उपदेशे", "इत्"],
            "1.3.4": ["उपदेशे", "इत्"],
            "1.3.5": ["उपदेशे", "इत्"],
            "1.3.6": ["उपदेशे", "इत्"],
            "1.3.7": ["उपदेशे", "इत्"],
            "1.3.8": ["उपदेशे", "इत्", "प्रत्ययस्य"],
            "1.3.9": ["इत्"]  # तस्य (इतः) लोपः
        }

        return inheritance_map.get(current_sutra_num, [])

    @staticmethod
    def apply_anuvritti_context(sutra_obj, master_list):
        """
        सूत्र के अर्थ को अनुवृत्ति के साथ जोड़कर पूर्ण 'Clinical' व्याख्या तैयार करना।
        """
        terms = AnuvrittiHandler.get_inherited_terms(sutra_obj['sutra_num'], master_list)
        if terms:
            sutra_obj['context_terms'] = terms
            sutra_obj['full_meaning'] = f"{' '.join(terms)} {sutra_obj['name']}"
        return sutra_obj