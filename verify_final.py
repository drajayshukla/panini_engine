
from core.maheshwara_sutras import MaheshwaraSutras
from logic.sandhi_processor import SandhiProcessor

print("\n--- 🔍 VERIFYING FIXES ---")
ac = MaheshwaraSutras.get_pratyahara("अच्")
print(f"AC Vowels (Size {len(ac)}): {sorted(list(ac))}")

at = MaheshwaraSutras.get_pratyahara("अट्")
print(f"AT (Size {len(at)}): {sorted(list(at))}")

ina = MaheshwaraSutras.get_pratyahara("इण्", force_n2=True)
print(f"IN (Shatva, Size {len(ina)}): {sorted(list(ina))}")

if 'ए' in at and 'ओ' in at: print("✅ AT is correct.")
else: print("❌ AT is missing vowels.")

if 'ए' in ina and 'य' in ina: print("✅ IN is correct.")
else: print("❌ IN is wrong.")
