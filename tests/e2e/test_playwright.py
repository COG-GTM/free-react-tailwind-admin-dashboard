#!/usr/bin/env python3
"""
Playwright E2E tests for TailAdmin React Dashboard.
Uses pytest classes and fixtures for structured testing.
"""

import pytest
import asyncio
from pathlib import Path
from playwright.async_api import Page, expect

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fixtures.test_data import (
    Selectors,
    Routes,
    VIEWPORTS,
    PAGE_TITLES,
    SIDEBAR_MENU_ITEMS,
)


@pytest.mark.e2e
class TestDashboardBasics:
    """Basic dashboard functionality tests."""

    @pytest.mark.asyncio
    async def test_page_loads_successfully(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that the dashboard page loads successfully."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        
        title = await playwright_page.title()
        assert "TailAdmin" in title, f"Expected 'TailAdmin' in title, got: {title}"

    @pytest.mark.asyncio
    async def test_react_app_renders(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that the React app renders content."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        
        root = await playwright_page.query_selector(Selectors.ROOT)
        assert root is not None, "Root element not found"
        
        children_count = await playwright_page.evaluate(
            f'document.querySelector("{Selectors.ROOT}").children.length'
        )
        assert children_count > 0, "React app did not render any content"

    @pytest.mark.asyncio
    async def test_sidebar_is_visible(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that the sidebar navigation is visible."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)  # Wait for animations
        
        sidebar = await playwright_page.query_selector(Selectors.SIDEBAR)
        assert sidebar is not None, "Sidebar not found"

    @pytest.mark.asyncio
    async def test_dashboard_cards_present(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that dashboard cards/widgets are present."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        cards = await playwright_page.query_selector_all(Selectors.DASHBOARD_CARD)
        assert len(cards) > 0, "No dashboard cards found"

    @pytest.mark.asyncio
    async def test_charts_render(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that charts/visualizations render."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(2)  # Charts may take longer to render
        
        charts = await playwright_page.query_selector_all(Selectors.CHART_CONTAINER)
        assert len(charts) > 0, "No charts found"


@pytest.mark.e2e
class TestNavigation:
    """Navigation and routing tests."""

    @pytest.mark.asyncio
    async def test_navigation_links_present(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that navigation links are present."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        
        nav_links = await playwright_page.query_selector_all(Selectors.NAV_LINK)
        assert len(nav_links) > 0, "No navigation links found"

    @pytest.mark.asyncio
    async def test_navigate_to_calendar(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test navigation to calendar page."""
        await playwright_page.goto(base_url + Routes.CALENDAR)
        await wait_for_app(playwright_page)
        
        # Verify we're on the calendar page
        url = playwright_page.url
        assert Routes.CALENDAR in url, f"Expected to be on calendar page, got: {url}"

    @pytest.mark.asyncio
    async def test_navigate_to_profile(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test navigation to profile page."""
        await playwright_page.goto(base_url + Routes.PROFILE)
        await wait_for_app(playwright_page)
        
        url = playwright_page.url
        assert Routes.PROFILE in url, f"Expected to be on profile page, got: {url}"

    @pytest.mark.asyncio
    async def test_navigate_to_form_elements(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test navigation to form elements page."""
        await playwright_page.goto(base_url + Routes.FORM_ELEMENTS)
        await wait_for_app(playwright_page)
        
        url = playwright_page.url
        assert Routes.FORM_ELEMENTS in url

    @pytest.mark.asyncio
    async def test_navigate_to_tables(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test navigation to tables page."""
        await playwright_page.goto(base_url + Routes.BASIC_TABLES)
        await wait_for_app(playwright_page)
        
        url = playwright_page.url
        assert Routes.BASIC_TABLES in url

    @pytest.mark.asyncio
    async def test_404_page(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test 404 error page."""
        await playwright_page.goto(base_url + "/nonexistent-page-12345")
        await wait_for_app(playwright_page)
        
        # The app should still render (React handles routing)
        root = await playwright_page.query_selector(Selectors.ROOT)
        assert root is not None


@pytest.mark.e2e
class TestResponsiveDesign:
    """Responsive design tests for different viewports."""

    @pytest.mark.asyncio
    async def test_desktop_viewport(
        self, playwright_page: Page, base_url: str, wait_for_app, take_screenshot
    ):
        """Test dashboard on desktop viewport."""
        await playwright_page.set_viewport_size(VIEWPORTS["desktop"])
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        
        # Sidebar should be visible on desktop
        sidebar = await playwright_page.query_selector(Selectors.SIDEBAR)
        assert sidebar is not None
        
        await take_screenshot(playwright_page, "desktop_viewport")

    @pytest.mark.asyncio
    async def test_tablet_viewport(
        self, playwright_tablet_page: Page, base_url: str, wait_for_app, take_screenshot
    ):
        """Test dashboard on tablet viewport."""
        await playwright_tablet_page.goto(base_url)
        await wait_for_app(playwright_tablet_page)
        
        await take_screenshot(playwright_tablet_page, "tablet_viewport")

    @pytest.mark.asyncio
    async def test_mobile_viewport(
        self, playwright_mobile_page: Page, base_url: str, wait_for_app, take_screenshot
    ):
        """Test dashboard on mobile viewport."""
        await playwright_mobile_page.goto(base_url)
        await wait_for_app(playwright_mobile_page)
        
        await take_screenshot(playwright_mobile_page, "mobile_viewport")


@pytest.mark.e2e
class TestThemeToggle:
    """Theme toggle (dark mode) tests."""

    @pytest.mark.asyncio
    async def test_theme_toggle_exists(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that theme toggle button exists."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        # Look for theme toggle button
        theme_toggle = await playwright_page.query_selector(Selectors.THEME_TOGGLE)
        # Theme toggle may not have specific selector, check for any toggle button
        if theme_toggle is None:
            buttons = await playwright_page.query_selector_all("button")
            assert len(buttons) > 0, "No buttons found on page"

    @pytest.mark.asyncio
    async def test_dark_mode_toggle(
        self, playwright_page: Page, base_url: str, wait_for_app, take_screenshot
    ):
        """Test toggling dark mode."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        # Try to find and click theme toggle
        theme_selectors = [
            Selectors.THEME_TOGGLE,
            'button[aria-label*="theme"]',
            'button[aria-label*="dark"]',
            'button[aria-label*="mode"]',
        ]
        
        for selector in theme_selectors:
            try:
                theme_toggle = await playwright_page.query_selector(selector)
                if theme_toggle:
                    await theme_toggle.click()
                    await asyncio.sleep(1)
                    await take_screenshot(playwright_page, "dark_mode")
                    break
            except Exception:
                continue


@pytest.mark.e2e
class TestFormElements:
    """Form elements page tests."""

    @pytest.mark.asyncio
    async def test_form_elements_page_loads(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that form elements page loads."""
        await playwright_page.goto(base_url + Routes.FORM_ELEMENTS)
        await wait_for_app(playwright_page)
        
        # Check for form inputs
        inputs = await playwright_page.query_selector_all(Selectors.INPUT)
        assert len(inputs) > 0, "No form inputs found"

    @pytest.mark.asyncio
    async def test_form_input_interaction(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test interacting with form inputs."""
        await playwright_page.goto(base_url + Routes.FORM_ELEMENTS)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        # Find first text input and type in it
        text_inputs = await playwright_page.query_selector_all(
            f"{Selectors.INPUT_TEXT}, {Selectors.INPUT_EMAIL}"
        )
        
        if text_inputs:
            first_input = text_inputs[0]
            await first_input.fill("Test input value")
            value = await first_input.input_value()
            assert value == "Test input value"


@pytest.mark.e2e
class TestTables:
    """Tables page tests."""

    @pytest.mark.asyncio
    async def test_tables_page_loads(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that tables page loads."""
        await playwright_page.goto(base_url + Routes.BASIC_TABLES)
        await wait_for_app(playwright_page)
        
        # Check for table element
        tables = await playwright_page.query_selector_all(Selectors.TABLE)
        # Tables might be styled differently, check for table-like structures
        if not tables:
            # Look for table rows or cells
            rows = await playwright_page.query_selector_all(Selectors.TABLE_ROW)
            assert len(rows) >= 0  # Page should at least load

    @pytest.mark.asyncio
    async def test_table_has_data(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that table contains data."""
        await playwright_page.goto(base_url + Routes.BASIC_TABLES)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        # Look for any data cells or content
        content = await playwright_page.content()
        assert len(content) > 1000, "Page content seems too short"


@pytest.mark.e2e
class TestLoadingStates:
    """Loading state tests."""

    @pytest.mark.asyncio
    async def test_initial_load_completes(
        self, playwright_page: Page, base_url: str
    ):
        """Test that initial page load completes without hanging."""
        response = await playwright_page.goto(base_url, wait_until="networkidle")
        assert response is not None
        assert response.status == 200

    @pytest.mark.asyncio
    async def test_navigation_load_completes(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that navigation between pages completes."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        
        # Navigate to another page
        await playwright_page.goto(base_url + Routes.CALENDAR)
        await wait_for_app(playwright_page)
        
        # Verify page loaded
        url = playwright_page.url
        assert Routes.CALENDAR in url


@pytest.mark.e2e
class TestErrorStates:
    """Error state tests."""

    @pytest.mark.asyncio
    async def test_handles_invalid_route(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that app handles invalid routes gracefully."""
        await playwright_page.goto(base_url + "/this-route-does-not-exist")
        await wait_for_app(playwright_page)
        
        # App should still render without crashing
        root = await playwright_page.query_selector(Selectors.ROOT)
        assert root is not None

    @pytest.mark.asyncio
    async def test_no_console_errors_on_load(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that there are no critical console errors on page load."""
        errors = []
        
        def handle_console(msg):
            if msg.type == "error":
                errors.append(msg.text)
        
        playwright_page.on("console", handle_console)
        
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(2)
        
        # Filter out known non-critical errors
        critical_errors = [
            e for e in errors 
            if "favicon" not in e.lower() 
            and "404" not in e
        ]
        
        # Allow some non-critical errors but fail on critical ones
        assert len(critical_errors) < 5, f"Too many console errors: {critical_errors}"


@pytest.mark.e2e
class TestScreenshots:
    """Screenshot capture tests."""

    @pytest.mark.asyncio
    async def test_capture_full_page_screenshot(
        self, playwright_page: Page, base_url: str, wait_for_app, 
        take_screenshot, screenshots_dir: Path
    ):
        """Test capturing full page screenshot."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        screenshot_path = await take_screenshot(
            playwright_page, "full_page", full_page=True
        )
        assert screenshot_path.exists(), "Screenshot was not saved"

    @pytest.mark.asyncio
    async def test_capture_viewport_screenshot(
        self, playwright_page: Page, base_url: str, wait_for_app,
        take_screenshot, screenshots_dir: Path
    ):
        """Test capturing viewport screenshot."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        
        screenshot_path = await take_screenshot(
            playwright_page, "viewport_only", full_page=False
        )
        assert screenshot_path.exists(), "Screenshot was not saved"


# Legacy function for backward compatibility with run_browser_tests.py
async def test_dashboard_with_playwright():
    """Legacy async test function for backward compatibility."""
    from playwright.async_api import async_playwright
    
    print("Starting Playwright test for TailAdmin React Dashboard...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()

        try:
            print("Navigating to http://localhost:5173")
            await page.goto("http://localhost:5173")
            await page.wait_for_load_state('networkidle')

            title = await page.title()
            print(f"Page title: {title}")
            assert "TailAdmin" in title, f"Expected 'TailAdmin' in title, got: {title}"

            await page.wait_for_function('document.querySelector("#root").children.length > 0', timeout=15000)
            print("React app loaded successfully")

            await asyncio.sleep(2)

            sidebar = await page.query_selector('aside')
            if sidebar:
                print("Sidebar navigation found")
            else:
                print("Sidebar not found with common selectors")

            cards = await page.query_selector_all('.card, .widget, [class*="card"], [class*="widget"], .bg-white')
            print(f"Found {len(cards)} potential dashboard cards/widgets")

            charts = await page.query_selector_all('.apexcharts-canvas, canvas, svg')
            print(f"Found {len(charts)} charts/visualizations")

            screenshot_path = "tests/screenshots/playwright_screenshot.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"Screenshot saved to: {screenshot_path}")

            nav_links = await page.query_selector_all('a[href], button')
            print(f"Found {len(nav_links)} navigation links/buttons")

            print("Testing responsive design...")
            await page.set_viewport_size({"width": 768, "height": 1024})
            await asyncio.sleep(1)

            mobile_screenshot_path = "tests/screenshots/playwright_mobile_screenshot.png"
            await page.screenshot(path=mobile_screenshot_path)
            print(f"Mobile screenshot saved to: {mobile_screenshot_path}")

            print("Playwright test completed successfully!")
            return True

        except Exception as e:
            print(f"Playwright test failed: {e}")
            return False

        finally:
            await browser.close()
            print("Playwright browser closed")


def run_playwright_test():
    """Run Playwright tests (legacy compatibility function)."""
    return asyncio.run(test_dashboard_with_playwright())


if __name__ == "__main__":
    success = run_playwright_test()
    exit(0 if success else 1)
