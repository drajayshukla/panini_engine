"""
FILE: core/upadesha_registry.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Adhikāra (Legal Identity & Source Tracking)
"""

import json
import os
from enum import Enum
from core.phonology import Varna  # PAS-5: Inherit Phonetic DNA
from core.adhikara_manager import AdhikaraManager

# 'Surgical' Cache: To prevent redundant disk I/O
_UPADESHA_CACHE = {}


class UpadeshaType(Enum):
    """
    पाणिनीय-उपदेश-श्रेणयः (Categorical Types)
    Defines the legal nature of the input for Rule 1.3.x application.
    """
    DHATU = "Dhatu"  # Roots (Bhvadi, etc.)
    PRATYAYA = "Pratyaya"  # Suffixes (Sup, Tin, Krit, Taddhita)
    VIBHAKTI = "Vibhakti"  # Case endings (Subclass of Pratyaya)
    AGAMA = "Agama"  # Augments (Tit, Kit, Mit)
    ADESH = "Adesha"  # Substitutes
    SUTRA = "Sutra"  # The rules themselves
    GANA = "Gana"  # Lists (Sarvadi, etc.)
    UNADI = "Unadi"  # Unadi suffixes
    VAKYA = "Vartika"  # Supplementary rules
    LINGA = "Linganusasana"  # Gender rules

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
                return []
        return []

    @classmethod
    def auto_detect(cls, text):
        """
        [DIAGNOSTIC]: Scans all Shastric databases to identify the input.
        Returns: (UpadeshaType, Is_Taddhita_Bool, Sutra_Origin_String)
        """
        if not text:
            return None, False, "0.0.0"

        cleaned_text = text.strip()

        # 1. Vibhakti Check (Highest Priority for Subanta)
        v_patha = cls._load_data('vibhaktipatha.json')
        if isinstance(v_patha, dict):
            for category in ['sup_pratyayas', 'tin_pratyayas', 'extra_taddhita_avyaya']:
                for item in v_patha.get(category, []):
                    if item.get('name') == cleaned_text:
                        return cls.VIBHAKTI, False, item.get('sutra', '4.1.2')

        # 2. Taddhita Master Check
        t_raw = cls._load_data('taddhita_master_data.json')
        if t_raw:
            # Flatten logic handles both list and dict structures
            t_data = []
            if isinstance(t_raw, dict):
                if 'taddhita_sections' in t_raw:
                    for section in t_raw['taddhita_sections'].values():
                        t_data.extend(section)
                else:
                    t_data = t_raw.get('data', [])

            for p in t_data:
                if isinstance(p, dict) and (p.get('name') == cleaned_text or p.get('pratyaya') == cleaned_text):
                    return cls.PRATYAYA, True, p.get('sutra', '4.1.76')

        # 3. Dhatu Check (Roots)
        d_raw = cls._load_data('dhatu_master_structured.json')
        if d_raw:
            dhatus = d_raw.get('dhatus', d_raw) if isinstance(d_raw, dict) else d_raw
            if isinstance(dhatus, list):
                for d in dhatus:
                    if isinstance(d, dict) and (
                            d.get('mula_dhatu') == cleaned_text or d.get('upadesha') == cleaned_text):
                        return cls.DHATU, False, d.get('sutra', '1.3.1')

        # 4. General Pratyaya Check
        for f_name, key in [('shit_pratyayas.json', 'pratyaya'), ('krut_pratyayas.json', 'pratyay')]:
            data = cls._load_data(f_name)
            p_list = data.get('data', data) if isinstance(data, dict) else data
            if isinstance(p_list, list):
                for p in p_list:
                    if isinstance(p, dict) and p.get(key) == cleaned_text:
                        return cls.PRATYAYA, ('taddhita' in f_name), p.get('sutra', '3.1.1')

        return None, False, "0.0.0"


class Upadesha(Varna):
    """
    [PAS-5.0] The Siddha Upadesha Object.
    INHERITS FROM VARNA to preserve Sthana/Prayatna.
    Wraps the phoneme with its Legal Identity (Adhikara).
    """

    def __init__(self, char, sutra_origin):
        """
        char: The pure phoneme (e.g., 'स्')
        sutra_origin: The Sutra (e.g., '4.1.2') providing the legal basis.
        """
        # 1. Initialize the Biological Layer (Phonology)
        super().__init__(char)

        # 2. Initialize the Legal Layer (Adhikara)
        self.sutra_origin = sutra_origin

        # Query AdhikaraManager for Scope
        self.is_pratyaya = AdhikaraManager.is_in_pratyaya_adhikara(sutra_origin)
        self.is_para = AdhikaraManager.is_para_adhikara(sutra_origin)

        # Trace is inherited from Varna, but we add the Legal Birth trace
        self.trace.append(f"Born as Upadesha via {sutra_origin}")

    def __repr__(self):
        """Clinical Debugger View"""
        base = super().__repr__()
        p_status = "P" if self.is_pratyaya else "NP"
        return f"{base}[{p_status}:{self.sutra_origin}]"