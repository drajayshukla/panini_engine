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
                return {} if "master" in filename or "patha" in filename else []
        return {}

    @classmethod
    def auto_detect(cls, text):
        """
        GitHub Data के आधार पर उपदेश के प्रकार का 'Diagnostic' पता लगाना।
        """
        if not text:
            return None

        cleaned_text = text.strip()

        # १. विभक्तियों में खोजें (vibhaktipatha.json) - Priority for 'जस्' Fix
        v_patha = cls._load_data('vibhaktipatha.json')
        if v_patha:
            # सुप् और तिङ् प्रत्ययों की सूची में 'name' फील्ड चेक करें
            sup_list = v_patha.get('sup_pratyayas', [])
            tin_list = v_patha.get('tin_pratyayas', [])
            extra_list = v_patha.get('extra_taddhita_avyaya', [])

            if any(cleaned_text == v.get('name') for v in (sup_list + tin_list + extra_list)):
                return cls.VIBHAKTI

        # २. धातुओं में खोजें (dhatu_master_structured.json)
        dhatus = cls._load_data('dhatu_master_structured.json')
        # धातु मास्टर आमतौर पर एक लिस्ट होती है
        if isinstance(dhatus, list):
            for d in dhatus:
                if cleaned_text == d.get('upadesha') or cleaned_text == d.get('mula_dhatu'):
                    return cls.DHATU

        # ३. षित् प्रत्ययों में खोजें (shit_pratyayas.json)
        shit_data = cls._load_data('shit_pratyayas.json')
        if shit_data:
            # shit_pratyaya_database के अंदर krut और taddhita चेक करें
            db = shit_data.get('shit_pratyaya_database', {})
            all_shit = db.get('krut_pratyayas', []) + db.get('taddhita_pratyayas', [])
            if any(cleaned_text == p.get('pratyaya') for p in all_shit):
                return cls.PRATYAYA

        # ४. अन्य कृत् और तद्धित प्रत्यय (krut_pratyayas.json, taddhita_pratyayas.json)
        for f in ['krut_pratyayas.json', 'taddhita_pratyayas.json']:
            data = cls._load_data(f)
            # यह चेक करें कि डेटा डिक्शनरी है या लिस्ट
            p_list = data.get('data', data) if isinstance(data, dict) else data
            if isinstance(p_list, list):
                if any(cleaned_text == p.get('pratyay') for p in p_list):
                    return cls.PRATYAYA

        return None

    @classmethod
    def validate_input(cls, text, upadesha_type):
        detected = cls.auto_detect(text)
        return detected == upadesha_type