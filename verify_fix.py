
from core.maheshwara_sutras import MaheshwaraSutras

print("\n--- 🔍 DEBUG: RE-VERIFYING PRATYAHARAS ---")

# 1. Check AC (Vowels)
ac = MaheshwaraSutras.get_pratyahara("अच्")
print(f"AC ({len(ac)}): {sorted(list(ac))}")
expected_ac = {'अ', 'इ', 'उ', 'ऋ', 'ऌ', 'ए', 'ओ', 'ऐ', 'औ'}
if expected_ac.issubset(ac): print("✅ AC is Correct.")
else: print(f"❌ AC Failed. Missing: {expected_ac - ac}")

# 2. Check IN (Shatva Trigger - a i u r l e o ai au h y v r l)
# Note: 'In' typically refers to the one ending in 'LaN' for Shatva/Natva.
ina = MaheshwaraSutras.get_pratyahara("इण्")
print(f"IN ({len(ina)}): {sorted(list(ina))}")
if 'ए' in ina and 'ह' in ina: print("✅ IN seems Correct.")
else: print("❌ IN Failed.")

# 3. Check AT (Natva Intervener - Vowels + h y v r)
at = MaheshwaraSutras.get_pratyahara("अट्")
print(f"AT ({len(at)}): {sorted(list(at))}")
if 'अ' in at and 'ह' in at and 'र' in at: print("✅ AT seems Correct.")
else: print("❌ AT Failed.")
