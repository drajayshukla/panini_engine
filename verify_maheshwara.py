
from core.maheshwara_sutras import MaheshwaraSutras
from logic.sandhi_processor import SandhiProcessor

print("--- 🔍 VERIFYING MAHESHWARA SUTRAS ---")
ac = MaheshwaraSutras.get_pratyahara("अच्")
hal = MaheshwaraSutras.get_pratyahara("हल्")
yan = MaheshwaraSutras.get_pratyahara("यण्")
jhal = MaheshwaraSutras.get_pratyahara("झल्")

print(f"AC (Vowels): {sorted(list(ac))}")
print(f"YAN (Semi-vowels): {sorted(list(yan))}")
print(f"Is 'a' in AC? {'अ' in ac}")
print(f"Is 'k' in AC? {'क' in ac}")
print(f"Is 'y' in YAN? {'य' in yan}")

print("\n--- 🔍 VERIFYING SANDHI PROCESSOR INTEGRATION ---")
print(f"SandhiProcessor.AC loaded? {len(SandhiProcessor.AC) > 0}")
print(f"SandhiProcessor.AT (for Natva) loaded? {len(SandhiProcessor.AT_PRATYAHARA) > 0}")
