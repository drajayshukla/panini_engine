import os
from pathlib import Path

# Configuration
OUTPUT_FILE = "essential_logic_snapshot.txt"

# 1. Directories to skip entirely
EXCLUDE_DIR_NAMES = {
    'tests', 'venv', '__pycache__', '.pytest_cache', '.git',
    '.venv', '.vscode', 'node_modules', 'logs', 'temp',
    'backup', 'dist', 'build', 'scripts'
}

# 2. Files to explicitly skip (Debugging and runner scripts)
SKIP_FILES = {
    'export_all_code.py', 'export_essential_code.py', 'requirements.txt',
    'README.md', 'panini_engine.log', 'streamline.py', 'master_runner.py',
    'verify_fix.py', 'verify_final.py', 'verify_explicit.py',
    'verify_final_strict.py', 'verify_maheshwara.py', 'verify_fix.py',
    'verify_explicit.py', 'verify_final_strict.py', 'verify_final.py',
    'audit_knowledge_base.py', 'benchmark_coverage.py', 'engine_main.py',
    'verify_maheshwara.py', 'debug_sandhi_failures.py'
}

# Only include python files
INCLUDE_EXT = {'.py'}

def main():
    root = Path.cwd().resolve()
    output_path = root / OUTPUT_FILE

    print(f"🚀 Filtering for Essential Pāṇinian Logic in: {root}")

    try:
        with open(output_path, 'w', encoding='utf-8') as out:
            file_count = 0

            for current_root, dirs, files in os.walk(root):
                curr_path = Path(current_root)

                # Prune excluded directories
                for d in list(dirs):
                    if d in EXCLUDE_DIR_NAMES or d.startswith('.'):
                        dirs.remove(d)

                # Process only the core logic files
                for file in files:
                    file_path = curr_path / file
                    rel_file_path = file_path.relative_to(root)

                    # Logic to identify if it's an essential file based on our discussion
                    is_essential = (
                        file_path.suffix.lower() in INCLUDE_EXT and
                        file not in SKIP_FILES and
                        not any(file.startswith(prefix) for prefix in ['fix_', 'debug_', 'test_', 'verify_'])
                    )

                    if is_essential:
                        try:
                            content = file_path.read_text(encoding='utf-8')
                            out.write(f"{'=' * 80}\n")
                            out.write(f"FILE: {rel_file_path.as_posix()}\n")
                            out.write(f"{'=' * 80}\n\n")
                            out.write(content)
                            out.write("\n\n\n")
                            file_count += 1
                            print(f" ✅ Essential Content Added: {rel_file_path}")
                        except Exception as e:
                            print(f" ❌ Error reading {rel_file_path}: {e}")

        print(f"\n✨ Success! {file_count} essential files written to {OUTPUT_FILE}")
        print(f" 📊 Final Logic Snapshot Size: {output_path.stat().st_size / 1024:.1f} KB")
        print(f"👉 Please copy the contents of {OUTPUT_FILE} and paste it here.")

    except PermissionError:
        print(f"🚨 Error: Permission denied writing to {OUTPUT_FILE}.")

if __name__ == '__main__':
    main()