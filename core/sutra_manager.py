"""
FILE: core/sutra_manager.py
TIMESTAMP: 2026-01-30 21:55:00 (IST)
LOCATION: Lucknow, Uttar Pradesh, India
QUALITY: PAS-v2.0: 6.0 (Subanta) | PILLAR: Sutra Librarian
"""
from core.sutra_store import p08_ajanta_pulinga

class SutraManager:
    """
    The Central Librarian.
    Aggregates rules from all Prakaranas (Chapters) into a single lookup mechanism.
    """

    _MASTER_DB = {}
    _IS_LOADED = False

    @classmethod
    def _initialize(cls):
        """Loads data from the store modules."""
        if cls._IS_LOADED: return

        # Load Chapter 8: Ajanta Pulinga
        cls._MASTER_DB.update(p08_ajanta_pulinga.data)

        # Future: Load p01_sanjna, p03_sandhi, etc.
        # cls._MASTER_DB.update(p01_sanjna.data)

        cls._IS_LOADED = True
        print(f"   [INFO] SutraManager loaded {len(cls._MASTER_DB)} rules.")

    @classmethod
    def get(cls, rule_code):
        """
        Fetches the Vṛtti (Definition) for a given rule code.
        """
        if not cls._IS_LOADED:
            cls._initialize()

        return cls._MASTER_DB.get(rule_code, f"[{rule_code}]")