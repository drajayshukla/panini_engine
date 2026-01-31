import os
from pathlib import Path

# Configuration
OUTPUT_FILE = "all_source_code.txt"

# 1. Names of directories to skip anywhere they appear in the project
EXCLUDE_DIR_NAMES = {
    'scripts',  # Added this to exclude the scripts folder and its contents
    'data', 'venv', '__pycache__',
    '.pytest_cache', '.git', '.venv', '.vscode', 'node_modules',
    'logs', 'temp', 'backup', 'dist', 'build'
}

# 2. Specific relative paths to skip (useful for nested subfolders)
EXCLUDE_RELATIVE_PATHS = {
    'panini_engine/core/sutra_store',
    'core/sutra_store',
}

INCLUDE_EXT = {'.py'}

SKIP_FILES = {
    'export_all_code.py',
    'requirements.txt',
    'README.md',
    'panini_engine.log',
    'streamline.py'
}


def main():
    root = Path.cwd().resolve()
    output_path = root / OUTPUT_FILE

    print(f"🚀 Scanning project root: {root}")

    try:
        with open(output_path, 'w', encoding='utf-8') as out:
            file_count = 0

            # os.walk allows us to prune directories on the fly
            for current_root, dirs, files in os.walk(root):
                curr_path = Path(current_root)

                # PRUNING LOGIC: Remove dirs so os.walk doesn't even enter them
                for d in list(dirs):
                    # Get the relative path of this directory
                    rel_dir_path = (curr_path / d).relative_to(root).as_posix()

                    # Criteria for exclusion:
                    # - Name matches EXCLUDE_DIR_NAMES
                    # - Is a hidden folder (starts with .)
                    # - Matches a specific relative path string
                    is_excluded = (
                            d in EXCLUDE_DIR_NAMES or
                            d.startswith('.') or
                            any(rel_dir_path.startswith(ex.strip('/')) for ex in EXCLUDE_RELATIVE_PATHS)
                    )

                    if is_excluded:
                        dirs.remove(d)

                # FILE PROCESSING
                for file in files:
                    file_path = curr_path / file
                    rel_file_path = file_path.relative_to(root)

                    # Check extension and skip list
                    if file_path.suffix.lower() in INCLUDE_EXT and file not in SKIP_FILES:
                        try:
                            content = file_path.read_text(encoding='utf-8')
                            out.write(f"{'=' * 80}\n")
                            out.write(f"FILE: {rel_file_path.as_posix()}\n")
                            out.write(f"{'=' * 80}\n\n")
                            out.write(content)
                            out.write("\n\n\n")
                            file_count += 1
                            print(f" ✅ Added: {rel_file_path}")
                        except Exception as e:
                            print(f" ❌ Error reading {rel_file_path}: {e}")

        print(f"\n✨ Done! {file_count} files written to {OUTPUT_FILE}")
        print(f" 📊 Size: {output_path.stat().st_size / 1024:.1f} KB")

    except PermissionError:
        print(f"🚨 Error: Permission denied writing to {OUTPUT_FILE}.")


if __name__ == '__main__':
    main()