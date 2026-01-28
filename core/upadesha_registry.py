
# panini_engine/core/upadesha_registry.py
import json
import os
from enum import Enum

# 'Surgical' Cache: डेटा को बार-बार लोड होने से बचाने के लिए
_UPADESHA_CACHE = {}


class UpadeshaType(Enum):
    """पाणिनीय व्याकरण के उपदेशों की श्रेणियाँ।"""
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
        """डेटा लोड करने के लिए इंटरनल हेल्पर।"""
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
        Diagnostic Detection: उपदेश का प्रकार और तद्धित स्टेटस पहचानना।
        Returns: (UpadeshaType, is_taddhita)
        """
        if not text:
            return None, False

        cleaned_text = text.strip()

        # १. विभक्तियों में खोजें (vibhaktipatha.json) - Priority 1
        v_patha = cls._load_data('vibhaktipatha.json')
        if v_patha and isinstance(v_patha, dict):
            all_vibs = v_patha.get('sup_pratyayas', []) + \
                       v_patha.get('tin_pratyayas', []) + \
                       v_patha.get('extra_taddhita_avyaya', [])

            # Clinical Check: सुनिश्चित करें कि v एक डिक्शनरी है
            if any(cleaned_text == v.get('name') for v in all_vibs if isinstance(v, dict)):
                return cls.VIBHAKTI, False

        # २. तद्धित मास्टर डेटा चेक (Surgical Focus for 1.3.8)
        t_raw = cls._load_data('taddhita_master_data.json')

        # Structure Fix: डेटा लिस्ट है या डिक्शनरी में रैप्ड लिस्ट?
        if isinstance(t_raw, dict):
            t_data = t_raw.get('data', t_raw.get('taddhita_pratyayas', []))
        else:
            t_data = t_raw

        if isinstance(t_data, list):
            if any(cleaned_text == p.get('name') or cleaned_text == p.get('pratyaya')
                   for p in t_data if isinstance(p, dict)):
                return cls.PRATYAYA, True

        # ३. धातुओं में खोजें (dhatu_master_structured.json)
        dhatus = cls._load_data('dhatu_master_structured.json')
        if isinstance(dhatus, list):
            if any(cleaned_text == d.get('upadesha') or cleaned_text == d.get('mula_dhatu')
                   for d in dhatus if isinstance(d, dict)):
                return cls.DHATU, False

        # ४. अन्य षित् और सामान्य प्रत्यय
        for f in ['shit_pratyayas.json', 'krut_pratyayas.json']:
            data = cls._load_data(f)

            # षित् प्रत्यय के लिए नेस्टेड स्ट्रक्चर चेक
            if f == 'shit_pratyayas.json' and isinstance(data, dict):
                db = data.get('shit_pratyaya_database', {})
                p_list = db.get('krut_pratyayas', []) + db.get('taddhita_pratyayas', [])
                target_key = 'pratyaya'
            else:
                p_list = data.get('data', data) if isinstance(data, dict) else data
                target_key = 'pratyay'

            if isinstance(p_list, list):
                if any(cleaned_text == p.get(target_key) for p in p_list if isinstance(p, dict)):
                    # तद्धित फ्लैग चेक करें
                    is_t = any(cleaned_text == p.get(target_key) and p.get('type') == 'Taddhita'
                               for p in p_list if isinstance(p, dict))
                    return cls.PRATYAYA, is_t

        return None, False

    @classmethod
    def validate_input(cls, text, upadesha_type):
        detected_type, _ = cls.auto_detect(text)
        return detected_type == upadesha_type