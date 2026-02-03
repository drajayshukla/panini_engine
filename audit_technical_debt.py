import os
import re

# We define "Smells" - patterns that indicate non-Paninian logic
SMELLS = {
    "HARDCODED_LOOKUP": r'replacements\s*=\s*\{',
    "STRING_PATCH": r'\.replace\(".*",\s*".*"\)',
    "GOLDEN_EXCEPTION": r'#\s*Golden\s*Exceptions',
    "MAGIC_MAP": r'(sup|tin|vibhakti)_map\s*=\s*\{',
    "BYPASS_COMMENT": r'#\s*.*(Pragmatic|Artificial|Hack|Fix)',
    "RETURN_LITERAL": r'return\s+["\'].*["\']'  # e.g., return "Ramah"
}

def scan_file_for_debt(filepath):
    issues = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        for smell_name, pattern in SMELLS.items():
            if re.search(pattern, line):
                # Filter out valid Python replaces that aren't hacks (heuristics)
                if smell_name == "STRING_PATCH" and "normalize" in line: continue
                
                issues.append({
                    "line": i + 1,
                    "type": smell_name,
                    "content": line.strip()[:60] + "..."
                })
    return issues

def generate_audit_report():
    print("🏥 PĀṆINIAN INTEGRITY AUDIT REPORT")
    print("===================================")
    print("Scanning for non-sūtra logic (Hardcoding, Patches, Bypasses)...\n")
    
    target_files = [
        "logic/sandhi_processor.py",
        "logic/subanta_processor.py",
        "core/core_foundation.py",
        "logic/tinanta_processor.py"
    ]
    
    total_issues = 0
    
    for file_path in target_files:
        if not os.path.exists(file_path): continue
        
        issues = scan_file_for_debt(file_path)
        if issues:
            print(f"📄 FILE: {file_path}")
            for issue in issues:
                print(f"   ⚠️  Line {issue['line']:<4} [{issue['type']}] : {issue['content']}")
                total_issues += 1
            print("")
            
    if total_issues == 0:
        print("✅ No obvious bypasses found (Unlikely!).")
    else:
        print(f"🚩 Diagnosis: {total_issues} areas identified for 'Real Logic' transplant.")
        print("   Recommendation: Replace dictionary lookups with Sūtra logic stepwise.")

if __name__ == "__main__":
    generate_audit_report()