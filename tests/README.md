# Testing Suite for TailAdmin React Dashboard

This directory contains automated browser tests for the TailAdmin React dashboard using both Selenium and Playwright.

## Directory Structure

```
tests/
├── README.md                 # This file
├── run_browser_tests.py     # Main test runner
├── e2e/                     # End-to-end tests
│   ├── test_selenium.py     # Selenium WebDriver tests
│   └── test_playwright.py   # Playwright tests
└── screenshots/             # Test screenshots (auto-generated)
    ├── selenium_screenshot.png
    ├── playwright_screenshot.png
    ├── playwright_mobile_screenshot.png
    └── playwright_dark_screenshot.png
```

## Prerequisites

### Python Dependencies
```bash
pip install selenium playwright webdriver-manager chromedriver-autoinstaller requests
```

### Browser Setup
```bash
# Install Playwright browsers
playwright install
```

## Running Tests

### 1. Start the Development Server
First, make sure the React development server is running:
```bash
cd ~/repos/free-react-tailwind-admin-dashboard
npm run dev
```
The server should be accessible at http://localhost:5173

### 2. Run All Tests
```bash
# From the project root directory
python tests/run_browser_tests.py
```

### 3. Run Individual Tests
```bash
# Run only Selenium tests
python tests/e2e/test_selenium.py

# Run only Playwright tests
python tests/e2e/test_playwright.py
```

## What the Tests Do

### Selenium Tests (`test_selenium.py`)
- ✅ Verifies page loads correctly
- ✅ Checks page title contains "TailAdmin"
- ✅ Finds sidebar navigation
- ✅ Counts dashboard widgets and charts
- ✅ Tests basic navigation interaction
- ✅ Takes a full-page screenshot

### Playwright Tests (`test_playwright.py`)
- ✅ All Selenium test features plus:
- ✅ Tests responsive design (mobile viewport)
- ✅ Attempts to test dark mode toggle
- ✅ Takes multiple screenshots (desktop, mobile, dark mode)
- ✅ More robust element detection

## Test Output

Both tests will:
1. Print detailed progress information
2. Save screenshots to `tests/screenshots/`
3. Return exit code 0 on success, 1 on failure

## Troubleshooting

### Server Not Running
If you get "Server is not running" error:
```bash
cd ~/repos/free-react-tailwind-admin-dashboard
npm run dev
```

### Chrome/ChromeDriver Issues
The tests use `chromedriver-autoinstaller` which should automatically handle Chrome version compatibility. If you encounter issues:
```bash
pip install --upgrade chromedriver-autoinstaller selenium
```

### Playwright Browser Issues
If Playwright browsers are missing:
```bash
playwright install chromium
```

## Adding New Tests

To add new tests:
1. Create new test files in `tests/e2e/`
2. Follow the existing pattern for error handling and logging
3. Update `run_browser_tests.py` to include your new tests
4. Save screenshots to `tests/screenshots/` directory

## Best Practices

- Always check if the server is running before starting tests
- Use relative paths for screenshots and file operations
- Include comprehensive error handling and logging
- Test both desktop and mobile viewports when possible
- Clean up browser instances in finally blocks