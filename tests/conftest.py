"""
Pytest configuration and shared fixtures for TailAdmin React Dashboard tests.
Provides fixtures for Playwright browser, Selenium WebDriver, and test utilities.
"""

import pytest
import asyncio
import os
import time
import requests
from pathlib import Path
from datetime import datetime
from typing import Generator, AsyncGenerator

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
import chromedriver_autoinstaller

# Playwright imports
from playwright.async_api import async_playwright, Browser, Page, BrowserContext
from playwright.sync_api import sync_playwright

# Test configuration
BASE_URL = "http://localhost:5173"
SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"
REPORTS_DIR = Path(__file__).parent / "reports"
BASELINES_DIR = Path(__file__).parent / "baselines"
DEFAULT_TIMEOUT = 30000  # 30 seconds
VIEWPORT_DESKTOP = {"width": 1920, "height": 1080}
VIEWPORT_TABLET = {"width": 768, "height": 1024}
VIEWPORT_MOBILE = {"width": 375, "height": 667}


def pytest_configure(config):
    """Configure pytest with custom markers and directories."""
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "accessibility: Accessibility tests")
    config.addinivalue_line("markers", "visual: Visual regression tests")
    config.addinivalue_line("markers", "performance: Performance tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
    
    # Ensure directories exist
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    BASELINES_DIR.mkdir(parents=True, exist_ok=True)


def pytest_html_report_title(report):
    """Set custom title for HTML report."""
    report.title = "TailAdmin React Dashboard - Test Report"


def pytest_html_results_summary(prefix, summary, postfix):
    """Add custom summary to HTML report."""
    prefix.extend([
        "<h3>Test Environment</h3>",
        "<p>Application: TailAdmin React Dashboard</p>",
        f"<p>Base URL: {BASE_URL}</p>",
        f"<p>Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>",
    ])


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test location."""
    for item in items:
        # Add markers based on test file location
        if "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        if "accessibility" in item.name or "accessibility" in str(item.fspath):
            item.add_marker(pytest.mark.accessibility)
        if "visual" in item.name or "visual_regression" in str(item.fspath):
            item.add_marker(pytest.mark.visual)
        if "performance" in item.name or "performance" in str(item.fspath):
            item.add_marker(pytest.mark.performance)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Add custom terminal summary with test statistics."""
    terminalreporter.write_sep("=", "Test Summary")
    
    # Count tests by outcome
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    errors = len(terminalreporter.stats.get('error', []))
    
    total = passed + failed + skipped + errors
    
    terminalreporter.write_line(f"Total tests: {total}")
    terminalreporter.write_line(f"  Passed: {passed}")
    terminalreporter.write_line(f"  Failed: {failed}")
    terminalreporter.write_line(f"  Skipped: {skipped}")
    terminalreporter.write_line(f"  Errors: {errors}")
    
    if total > 0:
        pass_rate = (passed / total) * 100
        terminalreporter.write_line(f"  Pass Rate: {pass_rate:.1f}%")
    
    # Save summary to JSON file
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "total": total,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "errors": errors,
        "pass_rate": (passed / total * 100) if total > 0 else 0,
        "exit_status": exitstatus,
    }
    
    summary_path = REPORTS_DIR / "test_summary.json"
    try:
        import json
        with open(summary_path, 'w') as f:
            json.dump(summary_data, f, indent=2)
        terminalreporter.write_line(f"\nSummary saved to: {summary_path}")
    except Exception as e:
        terminalreporter.write_line(f"\nFailed to save summary: {e}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture screenshots on test failure and add extra info to report."""
    outcome = yield
    report = outcome.get_result()
    
    # Add test duration to report
    if hasattr(report, 'duration'):
        report.extra_info = getattr(report, 'extra_info', {})
        report.extra_info['duration'] = f"{report.duration:.2f}s"
    
    if report.when == "call" and report.failed:
        # Try to capture screenshot on failure for Selenium
        if "selenium_driver" in item.funcargs:
            driver = item.funcargs["selenium_driver"]
            try:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = SCREENSHOTS_DIR / f"failure_{item.name}_{timestamp}.png"
                driver.save_screenshot(str(screenshot_path))
                print(f"\nScreenshot saved: {screenshot_path}")
                
                # Add screenshot path to report extras for HTML report
                if hasattr(report, 'extra'):
                    report.extra.append({
                        'name': 'Screenshot',
                        'content': str(screenshot_path),
                        'mime_type': 'image/png'
                    })
            except Exception as e:
                print(f"\nFailed to capture screenshot: {e}")
        
        # Log failure details
        failure_log = {
            "test_name": item.name,
            "timestamp": datetime.now().isoformat(),
            "error": str(report.longrepr) if report.longrepr else "Unknown error",
            "markers": [str(m) for m in item.iter_markers()],
        }
        
        failure_log_path = REPORTS_DIR / f"failure_{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        try:
            import json
            with open(failure_log_path, 'w') as f:
                json.dump(failure_log, f, indent=2)
        except Exception:
            pass


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def base_url() -> str:
    """Return the base URL for the application."""
    return BASE_URL


@pytest.fixture(scope="session")
def screenshots_dir() -> Path:
    """Return the screenshots directory path."""
    return SCREENSHOTS_DIR


@pytest.fixture(scope="session")
def baselines_dir() -> Path:
    """Return the baselines directory path for visual regression."""
    return BASELINES_DIR


def check_server_running(url: str = BASE_URL, timeout: int = 5) -> bool:
    """Check if the development server is running."""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


@pytest.fixture(scope="session")
def server_running(base_url: str) -> bool:
    """Fixture to check if the dev server is running."""
    is_running = check_server_running(base_url)
    if not is_running:
        pytest.skip(
            f"Development server not running at {base_url}. "
            "Start it with: npm run dev"
        )
    return is_running


# ============================================================================
# Selenium Fixtures
# ============================================================================

@pytest.fixture(scope="function")
def chrome_options() -> ChromeOptions:
    """Configure Chrome options for Selenium."""
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-notifications")
    return options


@pytest.fixture(scope="function")
def selenium_driver(
    chrome_options: ChromeOptions, 
    server_running: bool
) -> Generator[webdriver.Chrome, None, None]:
    """Create a Selenium WebDriver instance."""
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def selenium_wait(selenium_driver: webdriver.Chrome) -> WebDriverWait:
    """Create a WebDriverWait instance."""
    return WebDriverWait(selenium_driver, 10)


# ============================================================================
# Playwright Fixtures (Sync)
# ============================================================================

@pytest.fixture(scope="session")
def playwright_browser_sync():
    """Create a sync Playwright browser instance."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def playwright_page_sync(playwright_browser_sync, server_running: bool):
    """Create a sync Playwright page instance."""
    context = playwright_browser_sync.new_context(
        viewport=VIEWPORT_DESKTOP,
        ignore_https_errors=True
    )
    page = context.new_page()
    yield page
    context.close()


# ============================================================================
# Playwright Fixtures (Async)
# ============================================================================

@pytest.fixture(scope="function")
async def playwright_browser() -> AsyncGenerator[Browser, None]:
    """Create an async Playwright browser instance."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        yield browser
        await browser.close()


@pytest.fixture(scope="function")
async def playwright_context(
    playwright_browser: Browser
) -> AsyncGenerator[BrowserContext, None]:
    """Create an async Playwright browser context."""
    context = await playwright_browser.new_context(
        viewport=VIEWPORT_DESKTOP,
        ignore_https_errors=True
    )
    yield context
    await context.close()


@pytest.fixture(scope="function")
async def playwright_page(
    playwright_context: BrowserContext,
    server_running: bool
) -> AsyncGenerator[Page, None]:
    """Create an async Playwright page instance."""
    page = await playwright_context.new_page()
    yield page
    await page.close()


@pytest.fixture(scope="function")
async def playwright_mobile_page(
    playwright_browser: Browser,
    server_running: bool
) -> AsyncGenerator[Page, None]:
    """Create an async Playwright page with mobile viewport."""
    context = await playwright_browser.new_context(
        viewport=VIEWPORT_MOBILE,
        ignore_https_errors=True,
        is_mobile=True,
        has_touch=True
    )
    page = await context.new_page()
    yield page
    await context.close()


@pytest.fixture(scope="function")
async def playwright_tablet_page(
    playwright_browser: Browser,
    server_running: bool
) -> AsyncGenerator[Page, None]:
    """Create an async Playwright page with tablet viewport."""
    context = await playwright_browser.new_context(
        viewport=VIEWPORT_TABLET,
        ignore_https_errors=True
    )
    page = await context.new_page()
    yield page
    await context.close()


# ============================================================================
# Utility Fixtures
# ============================================================================

@pytest.fixture
def screenshot_on_failure(request, screenshots_dir: Path):
    """Fixture to capture screenshot on test failure."""
    yield
    if request.node.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"failure_{request.node.name}_{timestamp}.png"
        # Screenshot capture is handled in pytest_runtest_makereport hook


@pytest.fixture
def test_timestamp() -> str:
    """Return a timestamp string for unique file naming."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


@pytest.fixture
def wait_for_app():
    """Factory fixture to wait for React app to load."""
    async def _wait_for_app(page: Page, timeout: int = DEFAULT_TIMEOUT):
        await page.wait_for_function(
            'document.querySelector("#root").children.length > 0',
            timeout=timeout
        )
        await page.wait_for_load_state('networkidle')
    return _wait_for_app


@pytest.fixture
def take_screenshot():
    """Factory fixture to take screenshots."""
    async def _take_screenshot(
        page: Page, 
        name: str, 
        full_page: bool = True
    ) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = SCREENSHOTS_DIR / f"{name}_{timestamp}.png"
        await page.screenshot(path=str(screenshot_path), full_page=full_page)
        return screenshot_path
    return _take_screenshot


# ============================================================================
# Performance Metrics Fixture
# ============================================================================

@pytest.fixture
def get_performance_metrics():
    """Factory fixture to get performance metrics from page."""
    async def _get_metrics(page: Page) -> dict:
        metrics = await page.evaluate("""
            () => {
                const timing = performance.timing;
                const navigation = performance.getEntriesByType('navigation')[0];
                const paint = performance.getEntriesByType('paint');
                
                return {
                    // Navigation timing
                    domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
                    loadComplete: timing.loadEventEnd - timing.navigationStart,
                    firstByte: timing.responseStart - timing.navigationStart,
                    
                    // Paint timing
                    firstPaint: paint.find(p => p.name === 'first-paint')?.startTime || 0,
                    firstContentfulPaint: paint.find(p => p.name === 'first-contentful-paint')?.startTime || 0,
                    
                    // Resource timing
                    resourceCount: performance.getEntriesByType('resource').length,
                    
                    // Memory (if available)
                    jsHeapSize: performance.memory?.usedJSHeapSize || 0,
                };
            }
        """)
        return metrics
    return _get_metrics
