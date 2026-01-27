import json
import os
from enum import Enum

# 'Surgical' Cache
_UPADESHA_CACHE = {}

class UpadeshaType(Enum):
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

        # १. विभक्तियों में खोजें (vibhaktipatha.json) - Priority for 1.3.4
        v_patha = cls._load_data('vibhaktipatha.json')
        if v_patha:
            all_vibs = v_patha.get('sup_pratyayas', []) + \
                       v_patha.get('tin_pratyayas', []) + \
                       v_patha.get('extra_taddhita_avyaya', [])
            if any(cleaned_text == v.get('name') for v in all_vibs):
                return cls.VIBHAKTI, False

        # २. तद्धित मास्टर डेटा चेक (Specific for Sutra 1.3.8)
        t_data = cls._load_data('taddhita_master_data.json')
        # यदि डेटाबेस में मिले, तो इसे Pratyaya मानकर taddhita flag को True करें
        if t_data and any(cleaned_text == p.get('name') or cleaned_text == p.get('pratyaya') for p in t_data):
            return cls.PRATYAYA, True

        # ३. धातुओं में खोजें
        dhatus = cls._load_data('dhatu_master_structured.json')
        if isinstance(dhatus, list):
            if any(cleaned_text == d.get('upadesha') or cleaned_text == d.get('mula_dhatu') for d in dhatus):
                return cls.DHATU, False

        # ४. अन्य षित् और सामान्य प्रत्यय
        for f in ['shit_pratyayas.json', 'krut_pratyayas.json']:
            data = cls._load_data(f)
            # षित् प्रत्यय के लिए नेस्टेड स्ट्रक्चर चेक
            if f == 'shit_pratyayas.json':
                db = data.get('shit_pratyaya_database', {})
                p_list = db.get('krut_pratyayas', []) + db.get('taddhita_pratyayas', [])
                target_key = 'pratyaya'
            else:
                p_list = data.get('data', data) if isinstance(data, dict) else data
                target_key = 'pratyay'

            if isinstance(p_list, list) and any(cleaned_text == p.get(target_key) for p in p_list):
                # यहाँ चेक करें कि क्या षित् डेटाबेस में इसे तद्धित मार्क किया गया है
                is_t = any(cleaned_text == p.get(target_key) and p.get('type') == 'Taddhita' for p in p_list)
                return cls.PRATYAYA, is_t

        return None, False