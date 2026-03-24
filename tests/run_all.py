#!/usr/bin/env python3
"""Run all MY UNIVERSE tests."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# Import all test modules
from tests import test_calibrate, test_reflect, test_audit


def run_module(module):
    """Run all test_ functions in a module."""
    passed = 0
    failed = 0
    name = module.__name__.split(".")[-1]
    print(f"\n  {name}")
    print(f"  {'-' * 40}")

    for attr_name in sorted(dir(module)):
        if attr_name.startswith("test_"):
            func = getattr(module, attr_name)
            try:
                # Check if function expects tmp_path argument
                import inspect
                sig = inspect.signature(func)
                if sig.parameters:
                    with tempfile.TemporaryDirectory() as td:
                        func(Path(td))
                else:
                    func()
                print(f"    PASS  {attr_name}")
                passed += 1
            except Exception as e:
                print(f"    FAIL  {attr_name}: {e}")
                failed += 1

    return passed, failed


def main():
    print("=" * 50)
    print("  MY UNIVERSE — Test Suite")
    print("=" * 50)

    total_passed = 0
    total_failed = 0

    for module in [test_calibrate, test_reflect, test_audit]:
        p, f = run_module(module)
        total_passed += p
        total_failed += f

    print(f"\n{'=' * 50}")
    print(f"  TOTAL: {total_passed} passed, {total_failed} failed")
    print(f"{'=' * 50}\n")

    sys.exit(1 if total_failed > 0 else 0)


if __name__ == "__main__":
    main()
