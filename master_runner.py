"""
FILE: master_runner.py
PAS-v7.5 (Siddha) | PILLAR: R17 Lakṣya-Lakṣaṇa (Validation)
PURPOSE: Robust Test Orchestration with File Audit and Granular Reporting.
"""

import unittest
import sys
import os
import time
from pathlib import Path
from collections import defaultdict

# --- ANSI Colors for "Glassbox" Visibility ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def run_all_tests():
    # ───────────────────────────────────────────────
    # 1. Setup Environment
    # ───────────────────────────────────────────────
    project_root = Path(__file__).resolve().parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    tests_dir = project_root / "tests"

    print(f"{Colors.HEADER}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.BOLD}🚀 PĀṆINIAN ENGINE MASTER TEST SUITE (Audit Grade){Colors.ENDC}")
    print(f"{Colors.CYAN}📂 Scanning Root: {tests_dir}{Colors.ENDC}")
    print(f"{Colors.HEADER}{'=' * 80}{Colors.ENDC}")

    # ───────────────────────────────────────────────
    # 2. FILE SYSTEM AUDIT (The "Truth Check")
    # ───────────────────────────────────────────────
    # Find every file that *looks* like a test
    physical_files = set()
    for p in tests_dir.rglob("test_*.py"):
        rel_path = p.relative_to(project_root)
        physical_files.add(str(rel_path))

    # ───────────────────────────────────────────────
    # 3. Discover Tests (The "Loader Check")
    # ───────────────────────────────────────────────
    loader = unittest.TestLoader()
    try:
        suite = loader.discover(
            start_dir=str(tests_dir),
            pattern="test_*.py",
            top_level_dir=str(project_root),
        )
    except Exception as e:
        print(f"{Colors.FAIL}❌ FATAL ERROR during test discovery: {e}{Colors.ENDC}")
        return

    # ───────────────────────────────────────────────
    # 4. Map & Audit
    # ───────────────────────────────────────────────
    # Map: filename -> [list of test names]
    file_map = defaultdict(list)
    loaded_files = set()
    total_tests = 0

    def map_tests(test_structure):
        nonlocal total_tests
        if isinstance(test_structure, unittest.TestSuite):
            for item in test_structure:
                map_tests(item)
        elif isinstance(test_structure, unittest.TestCase):
            total_tests += 1
            mod = test_structure.__module__
            # Heuristic to find file path from module name
            parts = mod.split('.')
            # Assuming standard structure project/tests/test_foo.py
            # If discovery runs from root, module is 'tests.test_foo'

            probable_file = Path(project_root)
            for part in parts:
                probable_file = probable_file / part
            probable_file = probable_file.with_suffix(".py")

            if probable_file.exists():
                rel = str(probable_file.relative_to(project_root))
                file_map[rel].append(test_structure.id())
                loaded_files.add(rel)
            else:
                # Fallback for complex imports
                file_map[f"{mod}.py"].append(test_structure.id())

    map_tests(suite)

    # CHECK FOR MISSING FILES (The "Silent Killer" Check)
    # Convert paths to match format if needed, simplistic check here
    # Filter physical_files to only those in the 'tests' folder for comparison
    missing_files = []
    for p_file in physical_files:
        # Check if this physical file contributed any tests to the suite
        # This covers cases where a file exists but has syntax errors preventing import
        if p_file not in loaded_files:
            # unittest discovery silently skips files with ImportErrors sometimes
            # We want to know about them!
            missing_files.append(p_file)

    print(f"\n{Colors.BLUE}📋 Inventory Audit:{Colors.ENDC}")
    for f in sorted(file_map.keys()):
        count = len(file_map[f])
        print(f"  ✅ {f:<45} [{count} tests]")

    if missing_files:
        print(f"\n{Colors.WARNING}⚠️  WARNING: These files exist but were NOT loaded (Check Imports/Syntax):{Colors.ENDC}")
        for mf in missing_files:
            print(f"  ❌ {mf}")

    print(f"\n  {Colors.BOLD}Total Loaded: {len(file_map)} files | {total_tests} tests{Colors.ENDC}\n")

    if total_tests == 0:
        print(f"{Colors.FAIL}❌ No tests found to run.{Colors.ENDC}")
        sys.exit(1)

    # ───────────────────────────────────────────────
    # 5. Execution
    # ───────────────────────────────────────────────
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)

    print(f"{Colors.HEADER}⚡ STARTING EXECUTION CYCLE...{Colors.ENDC}")
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    duration = end_time - start_time

    # ───────────────────────────────────────────────
    # 6. The Report
    # ───────────────────────────────────────────────
    print(f"\n{Colors.HEADER}{'=' * 80}{Colors.ENDC}")
    print(f"{Colors.BOLD}📊 DIAGNOSTIC SUMMARY{Colors.ENDC}")
    print(f"{Colors.HEADER}{'-' * 80}{Colors.ENDC}")

    passed = result.testsRun - len(result.failures) - len(result.errors)
    failed = len(result.failures)
    errors = len(result.errors)

    print(f"⏱  Duration: {duration:.3f}s")
    print(f"🏃 Run:      {result.testsRun}")

    p_color = Colors.GREEN if passed > 0 else Colors.ENDC
    f_color = Colors.FAIL if failed > 0 else Colors.ENDC
    e_color = Colors.FAIL if errors > 0 else Colors.ENDC

    print(f"✅ Passed:   {p_color}{passed}{Colors.ENDC}")
    print(f"❌ Failures: {f_color}{failed}{Colors.ENDC}")
    print(f"🔥 Errors:   {e_color}{errors}{Colors.ENDC}")
    print(f"{Colors.HEADER}{'=' * 80}{Colors.ENDC}")

    if not result.wasSuccessful():
        print(f"\n{Colors.FAIL}🔥 REGRESSION DETAILS:{Colors.ENDC}")
        for test, traceback in result.errors:
            print(f"{Colors.FAIL}>> ERROR: {test.id()}{Colors.ENDC}")
            print(f"   {traceback.splitlines()[-1]}") # Short error
        for test, traceback in result.failures:
            print(f"{Colors.FAIL}>> FAIL:  {test.id()}{Colors.ENDC}")
            print(f"   {traceback.splitlines()[-1]}") # Short error
        sys.exit(1)

    print(f"\n{Colors.GREEN}🎉 SIDDHAM! The Engine is structurally sound.{Colors.ENDC}")
    sys.exit(0)

if __name__ == "__main__":
    run_all_tests()