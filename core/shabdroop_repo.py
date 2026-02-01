"""
FILE: core/shabdroop_repo.py
PURPOSE: Load Gold Standard Data for Validation.
"""
import json
import os

class ShabdroopRepository:
    _data = []
    _loaded = False

    @classmethod
    def load_data(cls):
        path = "data/shabdroop.json"
        if not os.path.exists(path): return
        try:
            with open(path, "r", encoding="utf-8") as f:
                cls._data = json.load(f)
            cls._loaded = True
        except Exception as e:
            print(f"❌ Error loading Shabdroop DB: {e}")

    @classmethod
    def get_all(cls):
        if not cls._loaded: cls.load_data()
        return cls._data
