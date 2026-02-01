"""
FILE: audit_active_logic.py
PURPOSE: Scan the codebase to find which Sutras are ACTIVELY implemented in Logic.
"""
import os
import re

def scan_directory(directory):
    sutra_pattern = re.compile(r'(\d+\.\d+\.\d+)')
    found_sutras = set()

    print(f"🕵️ Scanning logic in '{directory}'...")

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    matches = sutra_pattern.findall(content)
                    for m in matches:
                        found_sutras.add(m)

    return found_sutras

def main():
    active_sutras = scan_directory("logic")
    active_sutras.update(scan_directory("core")) # Also check core logic

    sorted_sutras = sorted(list(active_sutras), key=lambda x: tuple(map(int, x.split('.'))))

    print("\n============================================================")
    print(f"🚀 ACTIVE SUTRAS (Implemented in Code): {len(sorted_sutras)}")
    print("============================================================")

    # Simple list print
    col_count = 0
    for s in sorted_sutras:
        print(f"{s:<10}", end=" ")
        col_count += 1
        if col_count % 5 == 0: print()

    print("\n\n============================================================")
    print("These are the rules the engine can actually EXECUTE.")

if __name__ == "__main__":
    main()