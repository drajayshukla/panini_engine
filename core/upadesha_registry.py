import json
import os
from enum import Enum

# 'Surgical' Cache: इसे क्लास के बाहर रखने से Enum की जटिलताओं से बचाव होता है
_UPADESHA_CACHE = {}


class UpadeshaType(Enum):
    """
    पाणिनीय व्याकरण के उपदेशों की श्रेणियाँ।
    """
    DHATU = "Dhatu"
    PRATYAYA = "Pratyaya"
    AGAMA = "Agama"
    ADESH = "Adesha"
    SUTRA = "Sutra"
    GANA = "Gana"
    UNADI = "Unadi"
    VAKYA = "Vartika"
    LINGA = "Linganusasana"

    @staticmethod
    def _load_data(filename):
        """डेटा लोड करने के लिए इंटरनल हेल्पर फंक्शन (With Global Caching)"""
        if filename in _UPADESHA_CACHE:
            return _UPADESHA_CACHE[filename]

        # पाथ का निर्माण
        path = os.path.join("data", filename)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    _UPADESHA_CACHE[filename] = data
                    return data
            except Exception:
                return []
        return []

    @classmethod
    def auto_detect(cls, text):
        """
        बिना यूजर इनपुट के उपदेश के प्रकार का पता लगाना।
        """
        if not text:
            return None

        cleaned_text = text.strip()

        # 1. धातुओं में खोजें
        dhatus = cls._load_data('dhatu_master_structured.json')
        for d in dhatus:
            if cleaned_text == d.get('upadesha') or cleaned_text == d.get('mula_dhatu'):
                return cls.DHATU

        # 2. प्रत्ययों में खोजें (Multiple Sources)
        # A. विभक्ति मास्टर
        v_master = cls._load_data('vibhakti_master.json')
        if v_master:
            # सुप्, तिङ् और एक्स्ट्रा तद्धित को एक साथ चेक करें
            all_names = [s.get('name') for s in v_master.get('sup_pratyayas', [])] + \
                        [t.get('name') for t in v_master.get('tin_pratyayas', [])] + \
                        [ex.get('name') for ex in v_master.get('extra_taddhita_avyaya', [])]

            if cleaned_text in all_names:
                return cls.PRATYAYA

        # B. कृत् और तद्धित प्रत्यय
        for f in ['krut_pratyayas.json', 'taddhita_pratyayas.json']:
            data = cls._load_data(f)
            p_list = data.get('data', data) if isinstance(data, dict) else data
            if any(cleaned_text == p.get('pratyay') for p in p_list):
                return cls.PRATYAYA

        return None

    @classmethod
    def validate_input(cls, text, upadesha_type):
        detected = cls.auto_detect(text)
        return detected == upadesha_type