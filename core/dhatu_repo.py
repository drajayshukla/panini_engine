"""
FILE: core/dhatu_repo.py
PURPOSE: Singleton Manager to load and query Dhatu Data (R1: Upadeśa).
"""
import json
import os

class DhatuRepository:
    _dhatu_map = {}
    _loaded = False

    @classmethod
    def load_data(cls):
        if cls._loaded: return
        
        path = "data/dhatu_master_structured.json"
        if not os.path.exists(path):
            print(f"⚠️ Warning: Dhatu DB not found at {path}")
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for entry in data:
                    # Map 'mula_dhatu' to its details
                    mula = entry.get('mula_dhatu', '').strip()
                    if mula:
                        cls._dhatu_map[mula] = entry
            cls._loaded = True
            # print(f"✅ Loaded {len(cls._dhatu_map)} Dhatus into Memory.")
        except Exception as e:
            print(f"❌ Error loading Dhatu DB: {e}")

    @classmethod
    def get_dhatu_info(cls, word):
        """Returns metadata dict if word is a Dhatu, else None."""
        if not cls._loaded:
            cls.load_data()
        return cls._dhatu_map.get(word)
