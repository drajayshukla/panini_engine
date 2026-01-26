import json
import os
from enum import Enum

# 'Surgical' Cache: Memory-efficient data storage
_UPADESHA_CACHE = {}


class UpadeshaType(Enum):
    """
    पाणिनीय व्याकरण के उपदेशों की श्रेणियाँ।
    """
    DHATU = "Dhatu"
    PRATYAYA = "Pratyaya"
    VIBHAKTI = "Vibhakti"
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

        path = os.path.join("data", filename)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    _UPADESHA_CACHE[filename] = data
                    return data
            except Exception:
                # मास्टर फाइल्स के लिए एम्प्टी डिक्ट लौटें
                return {} if "master" in filename or "patha" in filename else []
        return {}

    @classmethod
    def auto_detect(cls, text):
        """
        Highest Priority: विभक्तियों की पहचान (vibhaktipatha.json)
        ताकि 1.3.4 सूत्र 'स', 'म' और 'त-वर्ग' को बचा सके।
        """
        if not text:
            return None

        cleaned_text = text.strip()

        # १. विभक्तियों में खोजें (vibhaktipatha.json) - TOP PRIORITY
        v_patha = cls._load_data('vibhaktipatha.json')
        if v_patha:
            # सुप्, तिङ् और एक्स्ट्रा तद्धित को एक साथ चेक करें
            sup = v_patha.get('sup_pratyayas', [])
            tin = v_patha.get('tin_pratyayas', [])
            extra = v_patha.get('extra_taddhita_avyaya', [])

            all_vibs = sup + tin + extra
            if any(cleaned_text == v.get('name') for v in all_vibs):
                return cls.VIBHAKTI

        # २. धातुओं में खोजें (dhatu_master_structured.json)
        dhatus = cls._load_data('dhatu_master_structured.json')
        if isinstance(dhatus, list):
            if any(cleaned_text == d.get('upadesha') or cleaned_text == d.get('mula_dhatu') for d in dhatus):
                return cls.DHATU

        # ३. षित्-प्रत्यय डेटाबेस (shit_pratyayas.json)
        shit_data = cls._load_data('shit_pratyayas.json')
        if shit_data:
            db = shit_data.get('shit_pratyaya_database', {})
            all_shit = db.get('krut_pratyayas', []) + db.get('taddhita_pratyayas', [])
            if any(cleaned_text == p.get('pratyaya') for p in all_shit):
                return cls.PRATYAYA

        # ४. सामान्य कृत् और तद्धित प्रत्यय
        for f in ['krut_pratyayas.json', 'taddhita_pratyayas.json']:
            data = cls._load_data(f)
            p_list = data.get('data', data) if isinstance(data, dict) else data
            if isinstance(p_list, list):
                if any(cleaned_text == p.get('pratyay') for p in p_list):
                    return cls.PRATYAYA

        return None

    @classmethod
    def validate_input(cls, text, upadesha_type):
        detected = cls.auto_detect(text)
        return detected == upadesha_type