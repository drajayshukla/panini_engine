
from core.maheshwara_sutras import MaheshwaraSutras
from logic.sandhi_processor import SandhiProcessor

print("\n--- 🔍 PRATYAHARA CHECK ---")
at = MaheshwaraSutras.get_pratyahara("अट्")
print(f"AT contains Nna (ण)? {'ण' in at}")
# Should be False. AT ends at T (Sutra 5). Nna is in Sutra 7.

ac = MaheshwaraSutras.get_pratyahara("अच्")
print(f"AC contains O (ओ)? {'ओ' in ac}")
# Should be True.

in_prat = MaheshwaraSutras.get_pratyahara("इण्", force_n2=True)
print(f"IN (Shatva) contains Y (य)? {'य' in in_prat}")
# Should be True (Sutra 5).
