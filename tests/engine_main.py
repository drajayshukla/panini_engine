# tests/engine_test.py
import sys
import os

# core फोल्डर को ढूंढने के लिए पाथ जोड़ना
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.phonology import sanskrit_varna_vichhed
from logic.it_engine import ItSanjnaEngine
from core.upadesha_registry import UpadeshaType


def test_it_sanjna(word, u_type):
    print(f"\n--- परीक्षण: {word} ---")
    tokens = sanskrit_varna_vichhed(word)
    print(f"१. विच्छेद: {tokens}")

    # ItSanjnaEngine के नए स्ट्रक्चर का उपयोग
    remaining, its = ItSanjnaEngine.run_it_sanjna_prakaran(tokens, word, u_type)

    print(f"२. इत् वर्ण: {its}")
    print(f"३. शेष अङ्ग: {remaining}")


if __name__ == "__main__":
    # टेस्ट १: ल्युट् प्रत्यय
    test_it_sanjna("ल्युट्", UpadeshaType.PRATYAYA)

    # टेस्ट २: पठँ धातु
    test_it_sanjna("पठँ", UpadeshaType.DHATU)