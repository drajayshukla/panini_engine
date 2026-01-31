"""
FILE: scripts/normalize_numbers.py
PAS-v2.0: 5.0 (Siddha)
PILLAR: Maintenance (परिवर्धनम्)
REFERENCE: Numerals Normalization for DNA Audit
TIMESTAMP: 2026-01-30 10:30:00
RATIO: ~15% Documentation | LIMIT: < 200 Lines
"""
import os
import re

# Mapping for Sanskrit (Devanagari) to International (Arabic) Numerals
SN_TO_IN = str.maketrans('0123456789', '0123456789')

def normalize_file(file_path):
    """
    Reads a file and replaces all Devanagari numerals with International digits.
    Ensures DNA traces (e.g., 7.4.60) are compatible with JSON lookups.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Translate Sanskrit Numerals to International
        new_content = content.translate(SN_TO_IN)

        # 2. Safety: Only rewrite if changes detected
        if new_content != content:
            # Prevent overwriting critical binary-like data if any
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
        return False
    except Exception as e:
        print(f"⚠️ Could not process {file_path}: {e}")
        return False

def run_normalization(root_dir):
    """
    Walks through the engine and normalizes .py and .txt files.
    """
    print(f"🚀 [{os.path.basename(root_dir)}] Starting Siddha Normalization...")
    count = 0
    # Include .txt if your test files or JSON sources need normalization
    target_extensions = ('.py', '.txt', '.json')

    for root, _, files in os.walk(root_dir):
        # Skip virtual environments or git folders
        if any(x in root for x in ['venv', '.git', '__pycache__']):
            continue

        for name in files:
            if name.endswith(target_extensions):
                path = os.path.join(root, name)
                if normalize_file(path):
                    print(f"✅ Normalized: {path}")
                    count += 1

    print(f"🏁 Normalization Complete. {count} files synchronized.")

if __name__ == "__main__":
    # Ensure we are in the panini_engine root
    run_normalization('.')