# panini_engine/core/upadesha_registry.py

import json
import os
from enum import Enum
from core.adhikara_manager import AdhikaraManager

# 'Surgical' Cache: To prevent redundant disk I/O and speed up the cycle
_UPADESHA_CACHE = {}


class UpadeshaType(Enum):
    """पाणिनीय व्याकरण के उपदेशों की श्रेणियाँ (As per 1.3.2 - 1.3.8)"""
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
        """Internal helper with caching logic to prevent phonetic friction."""
        if filename in _UPADESHA_CACHE:
            return _UPADESHA_CACHE[filename]

        # Adjust path to your project structure
        path = os.path.join("data", filename)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    _UPADESHA_CACHE[filename] = data
                    return data
            except Exception:
                # Return empty structures if file is corrupted
                return {} if any(x in filename for x in ["master", "patha", "data"]) else []
        return None

    @classmethod
    def auto_detect(cls, text):
        """
        Diagnostic Scanner: Identifies the technical category and Sutra origin.
        Crucial for Zone 4 (Adhikara) and Zone 1 (It-Sanjna).
        """
        if not text:
            return None, False, "0.0.0"

        cleaned_text = text.strip()

        # १. Vibhakti Check (vibhaktipatha.json) - Highest Priority
        v_patha = cls._load_data('vibhaktipatha.json')
        if v_patha and isinstance(v_patha, dict):
            for category in ['sup_pratyayas', 'tin_pratyayas', 'extra_taddhita_avyaya']:
                items = v_patha.get(category, [])
                for item in items:
                    if isinstance(item, dict) and cleaned_text == item.get('name'):
                        # Returns: Type, is_taddhita, sutra_origin
                        return cls.VIBHAKTI, False, item.get('sutra', '4.1.2')

        # २. Taddhita Inclusion (taddhita_master_data.json)
        t_raw = cls._load_data('taddhita_master_data.json')
        if t_raw:
            t_data = []
            if isinstance(t_raw, dict):
                if 'taddhita_sections' in t_raw:
                    for section in t_raw['taddhita_sections'].values():
                        t_data.extend(section)
                else:
                    t_data = t_raw.get('data', t_raw.get('taddhita_pratyayas', []))

            for p in t_data:
                if isinstance(p, dict) and (cleaned_text == p.get('name') or cleaned_text == p.get('pratyaya')):
                    return cls.PRATYAYA, True, p.get('sutra', '4.1.76')

        # ३. Dhatu Check (Dhatu-patha 1.3.1)
        d_raw = cls._load_data('dhatu_master_structured.json')
        if d_raw:
            dhatus = d_raw.get('dhatus', d_raw) if isinstance(d_raw, dict) else d_raw
            if isinstance(dhatus, list):
                for d in dhatus:
                    if isinstance(d, dict):
                        if cleaned_text == d.get('mula_dhatu') or cleaned_text == d.get('upadesha'):
                            return cls.DHATU, False, d.get('sutra', '1.3.1')

        # ४. General Pratyaya (Krit/Shit) Search
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

            for p in p_list:
                if isinstance(p, dict) and cleaned_text == p.get(target_key):
                    is_t = (p.get('type') == 'Taddhita' or 'taddhita' in f_name)
                    return cls.PRATYAYA, is_t, p.get('sutra', '3.1.1')

        return None, False, "0.0.0"


class Upadesha:
    """
    अणूरूप-उपदेश: (The Phonological Unit)
    A single Varna that carries inherited Shastric GPS and technical metadata.
    """

    def __init__(self, char, sutra_origin):
        """
        char: The pure phoneme (e.g., 'स्', 'आ')
        sutra_origin: The Sutra (e.g., '4.1.2') providing the legal basis.
        """
        self.char = char
        self.sutra_origin = sutra_origin

        # --- १. संज्ञा-अधिकार (३.१.१ प्रत्ययः / ३.१.२ परश्च) ---
        # Logic is queried from AdhikaraManager (Zone 4)
        self.is_pratyaya = AdhikaraManager.is_in_pratyaya_adhikara(sutra_origin)
        self.is_para = AdhikaraManager.is_para_adhikara(sutra_origin)

        # --- २. Shastric Metadata (Critical for It-Engine 1.3.x) ---
        # 1.1.8: Anunasika check - crucial for 'upadeshe-ajanunasika-it'
        self.is_anunasika = 'ँ' in char

        # Technical Slot for labels (It, Guna, Vriddhi, Savarna, etc.)
        self.sanjnas = set()

        # Clinical history: Trace which rules modified this Varna
        self.trace = []

    def __repr__(self):
        """Clinical Debugger View"""
        p_status = "P" if self.is_pratyaya else "NP"
        loc_status = "PARA" if self.is_para else "INTERNAL"
        s_tags = f"({','.join(self.sanjnas)})" if self.sanjnas else "None"
        return f"Varna('{self.char}', [{p_status}|{loc_status}], Sanjnas={s_tags})"