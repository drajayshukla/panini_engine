"""
FILE: fix_sandhi.py
PURPOSE: Force-update the Sandhi logic and clear cache to solve the 'Ramau' bug.
"""
import os
import shutil
import subprocess
import sys

# 1. Define the Correct Code (No 'joined' variable)
NEW_SANDHI_CODE = '''"""
FILE: logic/sandhi_processor.py
PAS-v6.0 (Siddha) | PILLAR: Sandhi & Tripadi
"""
print("✅ SANDHI PROCESSOR v3.0 (LIVE) LOADED") 

from core.core_foundation import Varna, sanskrit_varna_samyoga, PratyaharaEngine

pe = PratyaharaEngine()

class SandhiProcessor:

    @staticmethod
    def apply_ac_sandhi(anga, suffix):
        """
        Orchestrator for 6.1.x Vowel Sandhis.
        Returns: (modified_varnas, rule_code)
        """
        if not anga or not suffix: return anga + suffix, None

        last = anga[-1]
        first = suffix[0]

        # ----------------------------------------------------------------------
        # 1. VRIDDHIRECI (6.1.88) vs PRATHAMAYOH PURVASAVARNAH (6.1.102)
        # ----------------------------------------------------------------------
        if last.char in ['अ', 'आ']:
            if first.is_vowel:

                # Check Exception: 6.1.104 Nadici
                is_ic = pe.is_in(first.char, "इच्")

                if is_ic:
                    # 6.1.104 blocks 6.1.102.
                    # Fallback to 6.1.88 Vriddhireci (a + ec -> Vriddhi)
                    if pe.is_in(first.char, "एच"): # e, o, ai, au
                        # Rama + Au -> Ramau
                        last.char = 'औ' # Update Anga (In-Place)
                        last.trace.append("6.1.88")
                        suffix.pop(0)   # Remove Suffix Vowel (In-Place)

                        # [CRITICAL FIX]: Return fresh combination
                        return anga + suffix, "6.1.88"

                else:
                    # 6.1.102 applies (e.g., Rama + As)
                    if first.char == 'अ':
                        last.char = 'आ'
                        last.trace.append("6.1.102")
                        suffix.pop(0)
                        return anga + suffix, "6.1.102"

        # ----------------------------------------------------------------------
        # 2. AKA SAVARNE DIRGHA (6.1.101)
        # ----------------------------------------------------------------------
        savarna_pairs = {
            'अ': ['अ','आ'], 'आ': ['अ','आ'],
            'इ': ['इ','ई'], 'ई': ['इ','ई'],
            'उ': ['उ','ऊ'], 'ऊ': ['उ','ऊ']
        }

        if last.char in savarna_pairs and first.char in savarna_pairs[last.char]:
            long_map = {'अ':'आ', 'आ':'आ', 'इ':'ई', 'ई':'ई', 'उ':'ऊ', 'ऊ':'ऊ'}
            last.char = long_map[last.char]
            last.trace.append("6.1.101")
            suffix.pop(0)
            return anga + suffix, "6.1.101"

        return anga + suffix, None

    # ==========================================================================
    # TRIPADI (8.2 - 8.4)
    # ==========================================================================
    @staticmethod
    def run_tripadi(varna_list):
        """Ramah: s -> ru -> r -> h"""
        if not varna_list: return []

        # 8.2.66 Sasajusho Ruh
        if varna_list[-1].char in ['स्', 'ष्']:
            varna_list[-1].char = 'र्'
            varna_list[-1].trace.append("8.2.66")

        # 8.3.15 Kharavasanayor Visarjaniyah
        if varna_list[-1].char == 'र्':
             varna_list[-1].char = 'ः'
             varna_list[-1].trace.append("8.3.15")

        return varna_list
'''

# 2. Overwrite the File
target_path = os.path.join("logic", "sandhi_processor.py")
with open(target_path, "w", encoding="utf-8") as f:
    f.write(NEW_SANDHI_CODE)
print(f"✅ FORCED UPDATE: {target_path} written successfully.")

# 3. Nuke __pycache__
for root, dirs, files in os.walk("."):
    for d in dirs:
        if d == "__pycache__":
            shutil.rmtree(os.path.join(root, d))
print("✅ CACHE CLEARED: All __pycache__ folders deleted.")

# 4. Run the Master Test
print("\n🚀 RUNNING MASTER TEST...")
subprocess.run([sys.executable, "tests/master_test.py"])