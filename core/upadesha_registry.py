import json
import os
from enum import Enum


class UpadeshaType(Enum):
    """
    पाणिनीय व्याकरण के उपदेशों की श्रेणियाँ और उनके डेटाबेस से संबंध।
    """
    DHATU = "Dhatu"  # संबंधित: dhatu_master_structured.json
    PRATYAYA = "Pratyaya"  # संबंधित: vibhakti_master, krut, taddhita
    AGAMA = "Agama"
    ADESH = "Adesha"
    SUTRA = "Sutra"
    GANA = "Gana"
    UNADI = "Unadi"
    VAKYA = "Vartika"
    LINGA = "Linganusasana"

    @staticmethod
    def _load_data(filename):
        """डेटा लोड करने के लिए इंटरनल हेल्पर फंक्शन"""
        path = os.path.join("data", filename)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    @staticmethod
    def auto_detect(text):
        """
        बिना यूजर इनपुट के, डेटाबेस के आधार पर उपदेश के प्रकार (Type) का पता लगाना।
        यह 'उपदेश रूप' और 'मूल रूप' दोनों की जाँच करता है।
        """
        if not text:
            return None

        cleaned_text = text.strip()

        # 1. धातुओं में खोजें (dhatu_master_structured.json)
        dhatus = UpadeshaType._load_data('dhatu_master_structured.json')
        for d in dhatus:
            # उपदेश (एधँ) या मूल धातु (एध्) में से कोई भी मिले
            if cleaned_text == d.get('upadesha') or cleaned_text == d.get('mula_dhatu'):
                return UpadeshaType.DHATU

        # 2. प्रत्ययों में खोजें (Multiple JSON Sources)

        # A. विभक्ति मास्टर (सुप् और तिङ्)
        v_master = UpadeshaType._load_data('vibhakti_master.json')
        if v_master:
            # सुप् प्रत्यय जाँच
            for s in v_master.get('sup_pratyayas', []):
                if cleaned_text == s.get('name'):
                    return UpadeshaType.PRATYAYA
            # तिङ् प्रत्यय जाँच
            for t in v_master.get('tin_pratyayas', []):
                if cleaned_text == t.get('name'):
                    return UpadeshaType.PRATYAYA
            # एक्स्ट्रा तद्धित/अव्यय/उपसर्ग जाँच
            for ex in v_master.get('extra_taddhita_avyaya', []):
                if cleaned_text == ex.get('name'):
                    return UpadeshaType.PRATYAYA

        # B. कृत् प्रत्यय (krut_pratyayas.json)
        krut = UpadeshaType._load_data('krut_pratyayas.json')
        krut_list = krut.get('data', krut) if isinstance(krut, dict) else krut
        for k in krut_list:
            if cleaned_text == k.get('pratyay'):
                return UpadeshaType.PRATYAYA

        # C. तद्धित प्रत्यय (taddhita_pratyayas.json)
        taddhita = UpadeshaType._load_data('taddhita_pratyayas.json')
        t_list = taddhita.get('data', taddhita) if isinstance(taddhita, dict) else taddhita
        for t in t_list:
            if cleaned_text == t.get('pratyay'):
                return UpadeshaType.PRATYAYA

        # 3. अगर कहीं न मिले, तो None
        return None

    @staticmethod
    def validate_input(text, upadesha_type):
        """
        चेक करता है कि क्या इनपुट टेक्स्ट चुने गए टाइप के डेटाबेस में मौजूद है।
        """
        detected = UpadeshaType.auto_detect(text)
        return detected == upadesha_type