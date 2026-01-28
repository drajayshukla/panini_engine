import json
import os
from enum import Enum

# 'Surgical' Cache: डेटा को बार-बार डिस्क से लोड होने से बचाने के लिए
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
        """डेटा लोड करने के लिए इंटरनल हेल्पर (With Caching Logic)।"""
        if filename in _UPADESHA_CACHE:
            return _UPADESHA_CACHE[filename]

        # Path relative to project root /data/
        path = os.path.join("data", filename)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    _UPADESHA_CACHE[filename] = data
                    return data
            except Exception:
                # सुरक्षित रिटर्न यदि फ़ाइल करप्ट हो
                return {} if any(x in filename for x in ["master", "patha", "data"]) else []
        return None

    @classmethod
    def auto_detect(cls, text):
        """
        Diagnostic Scanner: उपदेश का प्रकार और १.२.४६ (तद्धित) स्टेटस की पहचान।
        Returns: (UpadeshaType, is_taddhita)
        """
        if not text:
            return None, False

        cleaned_text = text.strip()

        # १. विभक्तियों में खोजें (vibhaktipatha.json) - Priority 1 (Exclusion for 1.2.45)
        v_patha = cls._load_data('vibhaktipatha.json')
        if v_patha and isinstance(v_patha, dict):
            # सुँप्, तिङ् और अन्य विभक्ति प्रत्ययों का एकीकरण
            all_vibs = v_patha.get('sup_pratyayas', []) + \
                       v_patha.get('tin_pratyayas', []) + \
                       v_patha.get('extra_taddhita_avyaya', [])

            if any(cleaned_text == v.get('name') for v in all_vibs if isinstance(v, dict)):
                return cls.VIBHAKTI, False

        # २. तद्धित मास्टर डेटा चेक (Surgical Inclusion for 1.2.46)
        t_raw = cls._load_data('taddhita_master_data.json')
        if t_raw:
            # सपोर्ट: 'taddhita_sections' (nested) या 'data' (flat list)
            t_data = []
            if isinstance(t_raw, dict):
                if 'taddhita_sections' in t_raw:
                    for section in t_raw['taddhita_sections'].values():
                        t_data.extend(section)
                else:
                    t_data = t_raw.get('data', t_raw.get('taddhita_pratyayas', []))

            if any(cleaned_text == p.get('name') or cleaned_text == p.get('pratyaya')
                   for p in t_data if isinstance(p, dict)):
                return cls.PRATYAYA, True

        # ३. धातुओं में खोजें (dhatu_master_structured.json) - (Exclusion for 1.2.45)
        d_raw = cls._load_data('dhatu_master_structured.json')
        dhatus = d_raw.get('dhatus', d_raw) if isinstance(d_raw, dict) else d_raw

        if isinstance(dhatus, list):
            if any(cleaned_text == d.get('upadesha') or cleaned_text == d.get('mula_dhatu')
                   for d in dhatus if isinstance(d, dict)):
                return cls.DHATU, False

        # ४. अन्य कृत् और षित् प्रत्ययों की विस्तृत खोज
        files_to_scan = [
            ('shit_pratyayas.json', 'pratyaya'),
            ('krut_pratyayas.json', 'pratyay'),  # Note: JSON key variation handled
            ('krit_pratyaya.json', 'pratyay')
        ]

        for f_name, target_key in files_to_scan:
            data = cls._load_data(f_name)
            if not data: continue

            # डेटा लिस्ट को एक्सट्रैक्ट करें (Handles different JSON structures)
            p_list = []
            if isinstance(data, dict):
                if 'shit_pratyaya_database' in data:
                    db = data['shit_pratyaya_database']
                    p_list = db.get('krut_pratyayas', []) + db.get('taddhita_pratyayas', [])
                else:
                    p_list = data.get('data', data.get('krut_pratyayas', []))
            else:
                p_list = data

            if isinstance(p_list, list):
                for p in p_list:
                    if isinstance(p, dict) and cleaned_text == p.get(target_key):
                        # १.२.४६ के लिए तद्धित फ्लैग चेक करें
                        is_t = (p.get('type') == 'Taddhita' or 'taddhita' in f_name)
                        return cls.PRATYAYA, is_t

        return None, False

    @classmethod
    def validate_input(cls, text, upadesha_type):
        """इनपुट और अपेक्षित टाइप का मिलान।"""
        detected_type, _ = cls.auto_detect(text)
        return detected_type == upadesha_type