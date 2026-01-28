import json
import os
from enum import Enum

# 'Surgical' Cache: To prevent redundant disk I/O during Streamlit reruns
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
        """Internal helper with caching logic."""
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
                return {} if any(x in filename for x in ["master", "patha", "data"]) else []
        return None

    @classmethod
    def auto_detect(cls, text):
        """
        Diagnostic Scanner: Identifies Upadesha type and 1.2.46 (Taddhita) status.
        Specifically designed to block Dhatus (like एध्) from Pratipadika derivation.
        """
        if not text:
            return None, False

        cleaned_text = text.strip()

        # १. Vibhakti Check (vibhaktipatha.json) - Priority 1 (Exclusion for 1.2.45)
        v_patha = cls._load_data('vibhaktipatha.json')
        if v_patha and isinstance(v_patha, dict):
            all_vibs = v_patha.get('sup_pratyayas', []) + \
                       v_patha.get('tin_pratyayas', []) + \
                       v_patha.get('extra_taddhita_avyaya', [])

            if any(cleaned_text == v.get('name') for v in all_vibs if isinstance(v, dict)):
                return cls.VIBHAKTI, False

        # २. Taddhita Inclusion (taddhita_master_data.json) - (Inclusion for 1.2.46)
        t_raw = cls._load_data('taddhita_master_data.json')
        if t_raw:
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

        # ३. Dhatu Check (dhatu_master_structured.json) - (Strict Exclusion for 1.2.45)
        # Clinical Fix: Checks both 'mula_dhatu' (एध्) and 'upadesha' (एधँ)
        d_raw = cls._load_data('dhatu_master_structured.json')
        dhatus = d_raw.get('dhatus', d_raw) if isinstance(d_raw, dict) else d_raw

        if isinstance(dhatus, list):
            for d in dhatus:
                if isinstance(d, dict):
                    # High-precision match across both the base root and instructional form
                    if cleaned_text == d.get('mula_dhatu') or cleaned_text == d.get('upadesha'):
                        return cls.DHATU, False

        # ४. General Pratyaya/Krit/Shit Search
        files_to_scan = [
            ('shit_pratyayas.json', 'pratyaya'),
            ('krut_pratyayas.json', 'pratyay'),
            ('krit_pratyaya.json', 'pratyay')
        ]

        for f_name, target_key in files_to_scan:
            data = cls._load_data(f_name)
            if not data: continue

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
                        is_t = (p.get('type') == 'Taddhita' or 'taddhita' in f_name)
                        return cls.PRATYAYA, is_t

        return None, False

    @classmethod
    def validate_input(cls, text, upadesha_type):
        """Validates if the input matches the expected Upadesha category."""
        detected_type, _ = cls.auto_detect(text)
        return detected_type == upadesha_type