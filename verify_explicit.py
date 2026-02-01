
from core.maheshwara_sutras import MaheshwaraSutras
from logic.sandhi_processor import SandhiProcessor

print("\n--- 🔍 EXPLICIT VERIFICATION ---")
ac = MaheshwaraSutras.get_pratyahara("अच्")
print(f"AC Vowels: {sorted(list(ac))}")

required = {'अ', 'इ', 'उ', 'ऋ', 'ऌ', 'ए', 'ओ', 'ऐ', 'औ'}
if required.issubset(ac) and 'ण्' not in ac:
    print("✅ Maheshwara Logic FIXED (Explicit Tuples).")
else:
    print(f"❌ Still Broken. AC: {ac}")

# Reload SandhiProcessor to pick up new AC
import importlib
import logic.sandhi_processor
importlib.reload(logic.sandhi_processor)
from logic.sandhi_processor import SandhiProcessor

print(f"SandhiProcessor.AC size: {len(SandhiProcessor.AC)}")
