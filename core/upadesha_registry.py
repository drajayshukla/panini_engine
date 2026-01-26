import json
import os
from enum import Enum


class UpadeshaType(Enum):
    DHATU = "Dhatu"
    PRATYAYA = "Pratyaya"
    AGAMA = "Agama"
    ADESH = "Adesha"
    SUTRA = "Sutra"
    GANA = "Gana"
    UNADI = "Unadi"
    VAKYA = "Vartika"
    LINGA = "Linganusasana"

    # क्लास लेवल पर डेटा कैश (Memory Cache)
    _cache = {}

    @classmethod
    def _load_data(cls, filename):
        """डेटा लोड करने के लिए इंटरनल हेल्पर फंक्शन (With Caching)"""
        if filename in cls._cache:
            return cls._cache[filename]

        path = os.path.join("data", filename)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    cls._cache[filename] = json.load(f)
                    return cls._cache[filename]
            except Exception:
                return []
        return []

    @classmethod
    def auto_detect(cls, text):
        """स्वचालित पहचान (Cached and Fast)"""
        if not text: return None
        cleaned_text = text.strip()

        # 1. धातु जाँच
        dhatus = cls._load_data('dhatu_master_structured.json')
        for d in dhatus:
            if cleaned_text == d.get('upadesha') or cleaned_text == d.get('mula_dhatu'):
                return cls.DHATU

        # 2. प्रत्यय जाँच (Combined Search)
        # A. विभक्ति
        v_master = cls._load_data('vibhakti_master.json')
        if v_master:
            all_v = v_master.get('sup_pratyayas', []) + \
                    v_master.get('tin_pratyayas', []) + \
                    v_master.get('extra_taddhita_avyaya', [])
            if any(cleaned_text == v.get('name') for v in all_v):
                return cls.PRATYAYA

        # B. कृत् और तद्धित
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