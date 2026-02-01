"""
FILE: benchmark_coverage.py
PURPOSE: Run Engine against shabdroop.json and show DETAILED diffs.
"""
from core.shabdroop_repo import ShabdroopRepository
from logic.subanta_processor import SubantaProcessor
import sys

# Color codes for terminal
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
CYAN = "\033[96m"

def normalize_forms(form_str):
    raw_list = form_str.split(';')
    cleaned_list = []
    for item in raw_list:
        variants = set(item.split('-'))
        cleaned_list.append(variants)
    return cleaned_list

def run_benchmark():
    print(f"{CYAN}🚀 STARTING VERBOSE BENCHMARK{RESET}")
    print("="*60)
    
    data = ShabdroopRepository.get_all()
    if not data:
        print("❌ No data found.")
        return

    total_words = 0
    passed_words = 0
    
    # Filter for supported types
    SUPPORTED_LINGA = ['P', 'S'] 
    SUPPORTED_ENDINGS = ['अ', 'इ', 'उ', 'आ'] 

    for entry in data:
        word = entry['word']
        linga = entry['linga']
        forms_str = entry['forms']
        
        if linga not in SUPPORTED_LINGA: continue
        if not any(word.endswith(e) for e in SUPPORTED_ENDINGS): continue
        
        # Identify Case
        desc = f"{word} ({linga})"
        print(f"🔹 Testing: {desc.ljust(15)}", end="")

        expected_grid = normalize_forms(forms_str)
        if len(expected_grid) != 24:
            print(f"⚠️ Skip (Data Error)")
            continue

        total_words += 1
        mismatches = []
        
        idx = 0
        for vib in range(1, 9):
            for vac in range(1, 4):
                try:
                    engine_out = SubantaProcessor.derive_pada(word, vib, vac, None)
                    engine_variants = set([x.strip() for x in engine_out.split('/')])
                    valid_variants = expected_grid[idx]
                    
                    # Check overlap
                    if engine_variants.isdisjoint(valid_variants):
                        mismatches.append(f"[{vib}.{vac}] Exp: {valid_variants} | Got: {engine_variants}")
                except Exception as e:
                    mismatches.append(f"[{vib}.{vac}] Error: {str(e)}")
                
                idx += 1
        
        if not mismatches:
            print(f"{GREEN}✅ PASS{RESET}")
            passed_words += 1
        else:
            print(f"{RED}❌ FAIL ({len(mismatches)}){RESET}")
            # Print Diffs
            for m in mismatches:
                print(f"   ↳ {m}")

    print("="*60)
    print(f"📊 SUMMARY: {passed_words}/{total_words} Words Perfectly Derived.")

if __name__ == "__main__":
    run_benchmark()
