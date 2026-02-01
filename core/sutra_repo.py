"""
FILE: core/sutra_repo.py
PURPOSE: Load Panini Sutra definitions from JSON.
"""
import json
import os

class SutraRepository:
    _data = {}
    _loaded = False

    @classmethod
    def load_data(cls):
        path = "data/panini_sutras.json"
        if not os.path.exists(path): return
        try:
            with open(path, "r", encoding="utf-8") as f:
                raw_list = json.load(f)
                for entry in raw_list:
                    num = entry.get("sutra_num", "").strip()
                    if num:
                        cls._data[num] = entry
            cls._loaded = True
        except Exception as e:
            print(f"❌ Error loading Sutra DB: {e}")

    @classmethod
    def get(cls, rule_num):
        if not cls._loaded: cls.load_data()
        # Clean rule_num (sometimes passed as "6.1.101 (Name)")
        clean_num = rule_num.split(' ')[0].strip()
        return cls._data.get(clean_num)
