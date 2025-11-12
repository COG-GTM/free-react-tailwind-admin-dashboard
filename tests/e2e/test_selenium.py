#!/usr/bin/env python3
"""
Selenium test script for TailAdmin React Dashboard
This script tests basic functionality of the dashboard using Selenium WebDriver
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import time

def test_dashboard_with_selenium():
    print("🚀 Starting Selenium test for TailAdmin React Dashboard...")

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    # Set up the Chrome driver with automatic version matching
    try:
        chromedriver_autoinstaller.install()
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print(f"❌ Chrome setup failed: {e}")
        raise e

    try:
        # Navigate to the dashboard
        print("📍 Navigating to http://localhost:5173")
        driver.get("http://localhost:5173")

        # Wait for the page to load
        wait = WebDriverWait(driver, 10)

        # Check if the page title contains expected text
        print(f"📄 Page title: {driver.title}")
        assert "TailAdmin" in driver.title, f"Expected 'TailAdmin' in title, got: {driver.title}"

        # Wait for React app to load
        wait.until(lambda driver: driver.execute_script("return document.querySelector('#root').children.length > 0"))
        print("✅ React app loaded successfully")

        # Wait a bit more for content to render
        time.sleep(2)

        # Check for sidebar navigation
        try:
            sidebar = driver.find_element(By.CSS_SELECTOR, "[data-testid='sidebar'], .sidebar, nav")
            print("✅ Sidebar navigation found")
        except:
            print("⚠️  Sidebar not found with common selectors")

        # Check for dashboard cards/widgets
        try:
            cards = driver.find_elements(By.CSS_SELECTOR, ".card, .widget, [class*='card'], [class*='widget']")
            print(f"📊 Found {len(cards)} dashboard cards/widgets")
        except:
            print("⚠️  No dashboard cards found")

        # Check for any charts or data visualizations
        try:
            charts = driver.find_elements(By.CSS_SELECTOR, ".apexcharts-canvas, canvas, svg")
            print(f"📈 Found {len(charts)} charts/visualizations")
        except:
            print("⚠️  No charts found")

        # Take a screenshot
        screenshot_path = "tests/screenshots/selenium_screenshot.png"
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved to: {screenshot_path}")

        # Test navigation (try to find and click a menu item)
        try:
            nav_links = driver.find_elements(By.CSS_SELECTOR, "a[href], button")
            if nav_links:
                print(f"🔗 Found {len(nav_links)} navigation links/buttons")
                # Try clicking the first few links to test navigation
                for i, link in enumerate(nav_links[:3]):
                    try:
                        if link.is_displayed() and link.is_enabled():
                            link_text = link.text.strip()
                            if link_text:
                                print(f"🖱️  Testing click on: '{link_text}'")
                                link.click()
                                time.sleep(1)  # Wait for navigation
                                break
                    except Exception as e:
                        continue
        except Exception as e:
            print(f"⚠️  Navigation test failed: {e}")

        print("✅ Selenium test completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Selenium test failed: {e}")
        return False

    finally:
        driver.quit()
        print("🔚 Selenium WebDriver closed")

if __name__ == "__main__":
    success = test_dashboard_with_selenium()
    exit(0 if success else 1)
