"""
FILE: scripts/force_sync.py
PAS-v2.0: 5.0 (Siddha)
"""
from core.sutra_manager import SutraManager
import os

# Delete the old cache to ensure a fresh start
if os.path.exists("data/sutra_cache.json"):
    os.remove("data/sutra_cache.json")
    print("🗑️ Old cache removed.")

manager = SutraManager()
# Use the direct raw link to the Vasu Summary JSON
manager.GITHUB_URL = "https://raw.githubusercontent.com/ashtadhyayi-com/data/master/sutraani/vasu_english_summary.json"
manager.sync_with_github()

print(f"✅ Sync Complete. Items in cache: {len(manager.kosa)}")