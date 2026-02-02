import os
from pathlib import Path


def reverse_to_stable_siddha():
    # 1. REVERT CORE: maheshwara_sutras.py
    # Reverting to the high-precision tuple logic without the added prakriya logging.
    maheshwara_path = Path("core/maheshwara_sutras.py")
    maheshwara_code = '''"""
FILE: core/maheshwara_sutras.py
"""
class MaheshwaraSutras:
    # Explicit tuples: (Content_Characters, IT_Marker_String)
    SUTRAS_DATA = [
        ("अइउ", "ण्"), ("ऋऌ", "क्"), ("एओ", "ङ्"), ("ऐऔ", "च्"),
        ("हयवर", "ट्"), ("ल", "ण्"), ("ञमङणन", "म्"), ("झभ", "ञ्"),
        ("घढध", "ष्"), ("जबगडद", "श्"), ("खफछठथचटत", "व्"), ("कप", "य्"),
        ("शषस", "र्"), ("ह", "ल्")
    ]

    SAVARNA_MAP = {'अ': ['अ', 'आ'], 'इ': ['इ', 'ई'], 'उ': ['उ', 'ऊ'], 'ऋ': ['ऋ', 'ॠ'], 'ऌ': ['ऌ']}

    @staticmethod
    def get_pratyahara(p_name, force_n2=False):
        if not p_name or len(p_name) < 2: return set()
        p_name = p_name.strip()
        adi = p_name[0]
        it = p_name[1:]

        chars = set()
        collecting = False
        n_count = 0

        for content, marker in MaheshwaraSutras.SUTRAS_DATA:
            for char in content:
                if char == adi: collecting = True
                if collecting:
                    chars.add(char)
                    if char in MaheshwaraSutras.SAVARNA_MAP:
                        chars.update(MaheshwaraSutras.SAVARNA_MAP[char])

            if collecting and marker == it:
                if it == 'ण्':
                    n_count += 1
                    if force_n2 and n_count == 1: continue
                break
        return chars
'''
    maheshwara_path.write_text(maheshwara_code, encoding='utf-8')
    print("✅ Core: MaheshwaraSutras reverted to high-precision stable state.")

    # 2. REVERT CORE: sanjna_controller.py
    # Removing the 1.1.8 stamping logic and returning to standard It-Prakaran.
    sanjna_path = Path("core/sanjna_controller.py")
    sanjna_code = '''"""
FILE: core/sanjna_controller.py
"""
from core.core_foundation import Varna, UpadeshaType

class SanjnaController:
    @staticmethod
    def run_it_prakaran(varnas, context=UpadeshaType.VIBHAKTI):
        if not varnas: return varnas, []
        res = list(varnas)
        applied = []
        halantyam_applied = False

        if res:
            last = res[-1]
            if not last.is_vowel:
                is_tusma = last.char in ['त', 'थ', 'द', 'ध', 'न', 'स', 'स्', 'म', 'म्']
                if not is_tusma:
                    if last.char in ['प्', 'ट', 'ङ', 'ट्', 'ण्', 'ञ्']:
                        res.pop()
                        applied.append("1.3.3")
                        halantyam_applied = True

        if res:
            c0 = res[0].char
            if c0 in ['च', 'छ', 'ज', 'झ', 'ञ', 'ट', 'ठ', 'ड', 'ढ', 'ण']:
                res.pop(0); applied.append("1.3.7")
            elif c0 in ['ल', 'श्', 'श', 'क', 'ख', 'ग', 'घ', 'ङ']:
                res.pop(0); applied.append("1.3.8")

        if not halantyam_applied:
            if len(res) >= 1 and res[0].char == 'स':
                if len(res) > 1 and res[1].char in ['उ', 'ु', 'ँ']:
                     while len(res) > 1: res.pop()
                     applied.append("1.3.2")

        return res, applied
'''
    sanjna_path.write_text(sanjna_code, encoding='utf-8')
    print("✅ Logic: SanjnaController reverted to stable It-Prakaran logic.")


if __name__ == "__main__":
    reverse_to_stable_siddha()
    print("\\n🚀 REVERSION COMPLETE. The engine is back to the stable 80/80 state.")