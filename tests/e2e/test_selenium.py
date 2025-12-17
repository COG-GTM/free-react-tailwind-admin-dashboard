#!/usr/bin/env python3
"""
Selenium E2E tests for TailAdmin React Dashboard.
Uses pytest classes and fixtures for structured testing.
"""

import pytest
import time
import sys
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import chromedriver_autoinstaller

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fixtures.test_data import (
    Selectors,
    Routes,
    VIEWPORTS,
    FormTestData,
)


@pytest.mark.e2e
class TestSeleniumDashboardBasics:
    """Basic dashboard functionality tests using Selenium."""

    def test_page_loads_successfully(self, selenium_driver, base_url, selenium_wait):
        """Test that the dashboard page loads successfully."""
        selenium_driver.get(base_url)
        
        # Wait for React app to load
        selenium_wait.until(
            lambda d: d.execute_script("return document.querySelector('#root').children.length > 0")
        )
        
        assert "TailAdmin" in selenium_driver.title

    def test_react_app_renders(self, selenium_driver, base_url, selenium_wait):
        """Test that the React app renders content."""
        selenium_driver.get(base_url)
        
        selenium_wait.until(
            lambda d: d.execute_script("return document.querySelector('#root').children.length > 0")
        )
        
        root = selenium_driver.find_element(By.CSS_SELECTOR, Selectors.ROOT)
        assert root is not None

    def test_sidebar_is_visible(self, selenium_driver, base_url, selenium_wait):
        """Test that the sidebar navigation is visible."""
        selenium_driver.get(base_url)
        
        selenium_wait.until(
            lambda d: d.execute_script("return document.querySelector('#root').children.length > 0")
        )
        time.sleep(1)
        
        sidebar = selenium_driver.find_element(By.CSS_SELECTOR, Selectors.SIDEBAR)
        assert sidebar is not None

    def test_dashboard_cards_present(self, selenium_driver, base_url, selenium_wait):
        """Test that dashboard cards/widgets are present."""
        selenium_driver.get(base_url)
        
        selenium_wait.until(
            lambda d: d.execute_script("return document.querySelector('#root').children.length > 0")
        )
        time.sleep(1)
        
        cards = selenium_driver.find_elements(By.CSS_SELECTOR, Selectors.DASHBOARD_CARD)
        assert len(cards) > 0

    def test_charts_render(self, selenium_driver, base_url, selenium_wait):
        """Test that charts/visualizations render."""
        selenium_driver.get(base_url)
        
        selenium_wait.until(
            lambda d: d.execute_script("return document.querySelector('#root').children.length > 0")
        )
        time.sleep(2)  # Charts may take longer to render
        
        charts = selenium_driver.find_elements(By.CSS_SELECTOR, Selectors.CHART_CONTAINER)
        assert len(charts) > 0


@pytest.mark.e2e
class TestSeleniumNavigation:
    """Navigation tests using Selenium."""

    def test_navigation_links_present(self, selenium_driver, base_url, selenium_wait):
        """Test that navigation links are present."""
        selenium_driver.get(base_url)
        
        selenium_wait.until(
            lambda d: d.execute_script("return document.querySelector('#root').children.length > 0")
        )
        
        nav_links = selenium_driver.find_elements(By.CSS_SELECTOR, Selectors.NAV_LINK)
        assert len(nav_links) > 0

    def test_navigate_to_calendar(self, selenium_driver, base_url, selenium_wait):
        """Test navigation to calendar page."""
        selenium_driver.get(base_url + Routes.CALENDAR)
        
        selenium_wait.until(
            lambda d: d.execute_script("return document.querySelector('#root').children.length > 0")
        )
        
        assert Routes.CALENDAR in selenium_driver.current_url

    def test_navigate_to_profile(self, selenium_driver, base_url, selenium_wait):
        """Test navigation to profile page."""
        selenium_driver.get(base_url + Routes.PROFILE)
        
        selenium_wait.until(
            lambda d: d.execute_script("return document.querySelector('#root').children.length > 0")
        )
        
        assert Routes.PROFILE in selenium_driver.current_url

    def test_navigate_to_form_elements(self, selenium_driver, base_url, selenium_wait):
        """Test navigation to form elements page."""
        selenium_driver.get(base_url + Routes.FORM_ELEMENTS)
        
        selenium_wait.until(
            lambda d: d.execute_script("return document.querySelector('#root').children.length > 0")
        )
        
        assert Routes.FORM_ELEMENTS in selenium_driver.current_url


@pytest.mark.e2e
class TestSeleniumFormInteraction:
    """Form interaction tests using Selenium."""

    def test_form_elements_page_loads(self, selenium_driver, base_url, selenium_wait):
        """Test that form elements page loads."""
        selenium_driver.get(base_url + Routes.FORM_ELEMENTS)
        
        selenium_wait.until(
            lambda d: d.execute_script("return document.querySelector('#root').children.length > 0")
        )
        
        inputs = selenium_driver.find_elements(By.CSS_SELECTOR, Selectors.INPUT)
        assert len(inputs) > 0

    def test_form_input_typing(self, selenium_driver, base_url, selenium_wait):
        """Test typing in form inputs."""
        selenium_driver.get(base_url + Routes.FORM_ELEMENTS)
        
        selenium_wait.until(
            lambda d: d.execute_script("return document.querySelector('#root').children.length > 0")
        )
        time.sleep(1)
        
        text_inputs = selenium_driver.find_elements(
            By.CSS_SELECTOR, f"{Selectors.INPUT_TEXT}, {Selectors.INPUT_EMAIL}"
        )
        
        if text_inputs:
            first_input = text_inputs[0]
            first_input.clear()
            first_input.send_keys(FormTestData.VALID_NAME)
            assert first_input.get_attribute("value") == FormTestData.VALID_NAME


@pytest.mark.e2e
class TestSeleniumScreenshots:
    """Screenshot capture tests using Selenium."""

    def test_capture_screenshot(self, selenium_driver, base_url, selenium_wait, screenshots_dir):
        """Test capturing screenshot."""
        selenium_driver.get(base_url)
        
        selenium_wait.until(
            lambda d: d.execute_script("return document.querySelector('#root').children.length > 0")
        )
        time.sleep(1)
        
        screenshot_path = screenshots_dir / "selenium_test_screenshot.png"
        selenium_driver.save_screenshot(str(screenshot_path))
        assert screenshot_path.exists()


# Legacy function for backward compatibility with run_browser_tests.py
def test_dashboard_with_selenium():
    """Legacy test function for backward compatibility."""
    print("Starting Selenium test for TailAdmin React Dashboard...")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    try:
        chromedriver_autoinstaller.install()
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"Chrome setup failed: {e}")
        raise e

    try:
        print("Navigating to http://localhost:5173")
        driver.get("http://localhost:5173")

        wait = WebDriverWait(driver, 10)

        print(f"Page title: {driver.title}")
        assert "TailAdmin" in driver.title, f"Expected 'TailAdmin' in title, got: {driver.title}"

        wait.until(lambda d: d.execute_script("return document.querySelector('#root').children.length > 0"))
        print("React app loaded successfully")

        time.sleep(2)

        try:
            sidebar = driver.find_element(By.CSS_SELECTOR, "aside")
            print("Sidebar navigation found")
        except Exception:
            print("Sidebar not found with common selectors")

        try:
            cards = driver.find_elements(By.CSS_SELECTOR, ".card, .widget, [class*='card'], [class*='widget']")
            print(f"Found {len(cards)} dashboard cards/widgets")
        except Exception:
            print("No dashboard cards found")

        try:
            charts = driver.find_elements(By.CSS_SELECTOR, ".apexcharts-canvas, canvas, svg")
            print(f"Found {len(charts)} charts/visualizations")
        except Exception:
            print("No charts found")

        screenshot_path = "tests/screenshots/selenium_screenshot.png"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved to: {screenshot_path}")

        try:
            nav_links = driver.find_elements(By.CSS_SELECTOR, "a[href], button")
            if nav_links:
                print(f"Found {len(nav_links)} navigation links/buttons")
        except Exception as e:
            print(f"Navigation test failed: {e}")

        print("Selenium test completed successfully!")
        return True

    except Exception as e:
        print(f"Selenium test failed: {e}")
        return False

    finally:
        driver.quit()
        print("Selenium WebDriver closed")


if __name__ == "__main__":
    success = test_dashboard_with_selenium()
    exit(0 if success else 1)
