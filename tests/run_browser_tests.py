#!/usr/bin/env python3
"""
Browser automation test runner for TailAdmin React Dashboard
This script runs both Selenium and Playwright tests
"""

import subprocess
import sys
import time
import requests
import os
from pathlib import Path
from urllib.parse import urlparse

def check_server_running(url="http://localhost:5173", timeout=30):
    """Check if the development server is running"""
    print(f"🔍 Checking if server is running at {url}...")

    for i in range(timeout):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ Server is running at {url}")
                return True
        except requests.exceptions.RequestException:
            if i == 0:
                print(f"⏳ Waiting for server to start...")
            time.sleep(1)

    print(f"❌ Server is not running at {url}")
    return False

def run_test(test_file, test_name):
    """Run a specific test file"""
    print(f"\n{'='*50}")
    print(f"🧪 Running {test_name} Test")
    print(f"{'='*50}")

    try:
        result = subprocess.run([sys.executable, test_file],
                              capture_output=True, text=True, timeout=120)

        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        if result.returncode == 0:
            print(f"✅ {test_name} test PASSED")
            return True
        else:
            print(f"❌ {test_name} test FAILED (exit code: {result.returncode})")
            return False

    except subprocess.TimeoutExpired:
        print(f"⏰ {test_name} test TIMED OUT")
        return False
    except Exception as e:
        print(f"💥 {test_name} test ERROR: {e}")
        return False

def main():
    print("🚀 TailAdmin React Dashboard - Browser Automation Test Suite")
    print("=" * 60)

    # Ensure we're in the project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    print(f"📁 Working directory: {os.getcwd()}")

    # Ensure screenshots directory exists
    screenshots_dir = Path("tests/screenshots")
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    # Check if development server is running
    if not check_server_running():
        print("\n💡 To start the development server, run:")
        print("   cd ~/repos/free-react-tailwind-admin-dashboard && npm run dev")
        print("\nThen run this test suite again.")
        sys.exit(1)

    # Run tests
    results = {}

    # Run Selenium test
    results['Selenium'] = run_test('tests/e2e/test_selenium.py', 'Selenium')

    # Run Playwright test
    results['Playwright'] = run_test('tests/e2e/test_playwright.py', 'Playwright')

    # Summary
    print(f"\n{'='*50}")
    print("📊 TEST SUMMARY")
    print(f"{'='*50}")

    passed = sum(results.values())
    total = len(results)

    for test_name, passed_test in results.items():
        status = "✅ PASSED" if passed_test else "❌ FAILED"
        print(f"{test_name:12} : {status}")

    print(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed successfully!")
        sys.exit(0)
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()
