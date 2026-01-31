"""
FILE: master_runner.py
PAS-v6.0 (Siddha) | PILLAR: R17 Lakṣya-Lakṣaṇa (Validation)
PURPOSE: Automatically discovers and runs ALL tests in the 'tests/' directory.
         Now also shows which test files were actually found and executed.
"""

import unittest
import sys
import os
import time
from pathlib import Path


def run_all_tests():
    # ───────────────────────────────────────────────
    # 1. Setup Environment
    # ───────────────────────────────────────────────
    project_root = Path(__file__).resolve().parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    tests_dir = project_root / "tests"

    print("=" * 70)
    print("🚀 PĀṆINIAN ENGINE MASTER TEST SUITE")
    print(f"📂 Scanning: {tests_dir}")
    print("=" * 70)

    # ───────────────────────────────────────────────
    # 2. Discover Tests
    # ───────────────────────────────────────────────
    loader = unittest.TestLoader()

    try:
        suite = loader.discover(
            start_dir=str(tests_dir),
            pattern="test_*.py",
            top_level_dir=str(project_root),
        )
    except Exception as e:
        print(f"❌ Error during test discovery: {e}")
        return

    if suite.countTestCases() == 0:
        print("⚠️  No tests found!")
        print("    → Make sure files start with 'test_'")
        print("    → and contain classes that inherit from unittest.TestCase")
        sys.exit(1)

    # ───────────────────────────────────────────────
    # 3. Collect & Show which files were actually discovered
    # ───────────────────────────────────────────────
    discovered_files = set()

    def collect_test_files(suite_or_case):
        if isinstance(suite_or_case, unittest.TestSuite):
            for item in suite_or_case:
                collect_test_files(item)
        elif isinstance(suite_or_case, unittest.TestCase):
            file_path = suite_or_case.__class__.__module__.replace(".", os.sep) + ".py"
            full_path = (tests_dir / file_path).resolve()
            discovered_files.add(str(full_path.relative_to(project_root)))

    collect_test_files(suite)

    print("\n📋 Discovered and will run test files:")
    for f in sorted(discovered_files):
        print(f"  • {f}")
    print(f"   (total: {len(discovered_files)} files)\n")

    # ───────────────────────────────────────────────
    # 4. Run Tests
    # ───────────────────────────────────────────────
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    start_time = time.time()

    result = runner.run(suite)

    end_time = time.time()
    duration = end_time - start_time

    # ───────────────────────────────────────────────
    # 5. Final Report
    # ───────────────────────────────────────────────
    print("\n" + "═" * 70)
    print(f"⏱  Time taken:     {duration:.3f} s")
    print(f"   Tests run:      {result.testsRun}")
    print(f"   ✅ Passed:       {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"   ❌ Failures:     {len(result.failures)}")
    print(f"   ⚠  Errors:       {len(result.errors)}")
    print("═" * 70)

    if result.wasSuccessful():
        print("🎉 SIDDHAM! All systems operational.")
        sys.exit(0)
    else:
        print("🔥 REGRESSION DETECTED — please fix failing tests.")
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()