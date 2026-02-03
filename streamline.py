import os
from pathlib import Path

def clean_page_conflicts():
    print("🧹 Cleaning up page conflicts...")
    
    pages_dir = Path("pages")
    
    # 1. DEFINE THE CANONICAL MAP (The files we WANT to keep)
    # format: (current_filename_part, new_clean_name)
    canonical_pages = [
        ("Declension_Engine", "1_🔍_Declension_Engine.py"),
        ("Dhatu_Lab",         "2_🧪_Dhatu_Lab.py"),
        ("Tinanta_Lab",       "3_⚡_Tinanta_Lab.py"),
        ("Metadata_Tagger",   "4_🔍_Metadata_Tagger.py")
    ]
    
    # 2. IDENTIFY AND RENAME/DELETE
    # We read all files first
    all_files = list(pages_dir.glob("*.py"))
    
    # Track what we've handled to avoid deleting renamed files
    handled_files = set()

    for keyword, target_name in canonical_pages:
        # Find files matching the keyword (e.g., "Dhatu_Lab")
        matches = [f for f in all_files if keyword in f.name]
        
        if not matches:
            print(f"⚠️ Warning: Could not find source for {keyword}")
            continue
            
        # Pick the most "correct" looking one (usually the one with highest version logic, 
        # but since we just overwrote them all, any is fine. We take the last one to be safe).
        # Actually, let's keep the one that exactly matches if it exists, else rename the first match.
        
        target_path = pages_dir / target_name
        
        # If target already exists, keep it and mark as handled
        if target_path.exists():
            print(f"✅ Kept {target_name}")
            handled_files.add(target_path)
            # Delete duplicates
            for m in matches:
                if m != target_path and m not in handled_files:
                    m.unlink()
                    print(f"🗑️ Deleted duplicate: {m.name}")
        else:
            # Rename the first match to the target name
            src = matches[0]
            src.rename(target_path)
            print(f"✨ Renamed {src.name} -> {target_name}")
            handled_files.add(target_path)
            # Delete remaining duplicates
            for m in matches[1:]:
                m.unlink()
                print(f"🗑️ Deleted duplicate: {m.name}")

    # 3. DELETE "1_test.py" explicitly (The source of the crash)
    test_page = pages_dir / "1_test.py"
    if test_page.exists():
        test_page.unlink()
        print("🗑️ Deleted conflict source: 1_test.py")

    print("\n✅ Cleanup Complete. Your pages folder is now valid.")

if __name__ == "__main__":
    clean_page_conflicts()