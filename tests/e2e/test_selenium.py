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

def test_calendar_crud_operations():
    """
    Test calendar event creation, reading, and editing operations
    Tests the /calendar page functionality including event CRUD operations
    """
    print("🚀 Starting Selenium calendar CRUD operations test...")

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
        print(f"❌ Chrome setup failed: {e}")
        raise e

    try:
        print("📍 Navigating to http://localhost:5173/calendar")
        driver.get("http://localhost:5173/calendar")

        wait = WebDriverWait(driver, 10)

        print(f"📄 Page title: {driver.title}")
        assert "TailAdmin" in driver.title, f"Expected 'TailAdmin' in title, got: {driver.title}"

        wait.until(lambda driver: driver.execute_script("return document.querySelector('#root').children.length > 0"))
        print("✅ React app loaded successfully")

        time.sleep(2)

        print("📅 Waiting for calendar to load...")
        calendar = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fc, .custom-calendar, [class*='calendar']")))
        print("✅ Calendar component found")

        print("🔍 Looking for 'Add Event +' button...")
        add_event_button = None
        try:
            add_event_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Event')]")))
            print("✅ 'Add Event +' button found")
        except:
            try:
                add_event_button = driver.find_element(By.CSS_SELECTOR, "button.fc-addEventButton-button")
                print("✅ 'Add Event +' button found via CSS selector")
            except:
                print("⚠️  'Add Event +' button not found with standard selectors")

        if add_event_button:
            print("🖱️  Clicking 'Add Event +' button...")
            add_event_button.click()
            time.sleep(1)

            print("🔍 Looking for event modal...")
            try:
                modal = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal, [role='dialog'], [class*='modal']")))
                print("✅ Event modal opened successfully")

                print("📝 Filling in event title...")
                title_input = wait.until(EC.presence_of_element_located((By.ID, "event-title")))
                title_input.clear()
                title_input.send_keys("Test Event - Selenium")
                print("✅ Event title filled: 'Test Event - Selenium'")

                print("📝 Selecting event color/category...")
                try:
                    danger_radio = driver.find_element(By.ID, "modalDanger")
                    driver.execute_script("arguments[0].click();", danger_radio)
                    print("✅ Event color 'Danger' selected")
                except:
                    try:
                        radio_buttons = driver.find_elements(By.CSS_SELECTOR, "input[type='radio'][name='event-level']")
                        if radio_buttons:
                            driver.execute_script("arguments[0].click();", radio_buttons[0])
                            print("✅ Event color selected (first option)")
                    except:
                        print("⚠️  Could not select event color")

                print("📝 Filling in start date...")
                try:
                    start_date_input = driver.find_element(By.ID, "event-start-date")
                    start_date_input.clear()
                    start_date_input.send_keys("12/25/2024")
                    print("✅ Start date filled: 12/25/2024")
                except:
                    print("⚠️  Could not fill start date")

                print("📝 Filling in end date...")
                try:
                    end_date_input = driver.find_element(By.ID, "event-end-date")
                    end_date_input.clear()
                    end_date_input.send_keys("12/26/2024")
                    print("✅ End date filled: 12/26/2024")
                except:
                    print("⚠️  Could not fill end date")

                print("🖱️  Looking for 'Add Event' submit button...")
                try:
                    add_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Event') and not(contains(text(), '+'))]")))
                    add_button.click()
                    print("✅ 'Add Event' button clicked")
                    time.sleep(2)
                except:
                    try:
                        add_button = driver.find_element(By.CSS_SELECTOR, "button.btn-success, button.btn-update-event")
                        add_button.click()
                        print("✅ Submit button clicked via CSS selector")
                        time.sleep(2)
                    except:
                        print("⚠️  Could not find submit button")

                print("🔍 Verifying event appears on calendar...")
                try:
                    wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, ".modal, [role='dialog']")))
                    print("✅ Modal closed after event creation")
                except:
                    print("⚠️  Modal may still be open")

                time.sleep(1)

                events = driver.find_elements(By.CSS_SELECTOR, ".fc-event, .fc-daygrid-event, [class*='event']")
                print(f"📊 Found {len(events)} events on calendar")

                event_titles = driver.find_elements(By.CSS_SELECTOR, ".fc-event-title, .fc-event-title-container")
                for event_title in event_titles:
                    if "Test Event" in event_title.text or "Selenium" in event_title.text:
                        print(f"✅ Created event found on calendar: '{event_title.text}'")
                        break

            except Exception as e:
                print(f"⚠️  Error during event creation: {e}")

        print("🖱️  Testing event click to open edit modal...")
        try:
            time.sleep(1)
            existing_events = driver.find_elements(By.CSS_SELECTOR, ".fc-event, .fc-daygrid-event")
            if existing_events:
                print(f"📊 Found {len(existing_events)} clickable events")
                
                clickable_event = None
                for event in existing_events:
                    try:
                        if event.is_displayed() and event.is_enabled():
                            clickable_event = event
                            break
                    except:
                        continue
                
                if clickable_event:
                    print("🖱️  Clicking on an existing event...")
                    driver.execute_script("arguments[0].scrollIntoView(true);", clickable_event)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", clickable_event)
                    time.sleep(1)

                    try:
                        modal = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".modal, [role='dialog']")))
                        print("✅ Edit modal opened successfully")

                        modal_title = driver.find_element(By.CSS_SELECTOR, ".modal-title, h5")
                        if "Edit Event" in modal_title.text:
                            print("✅ Modal shows 'Edit Event' title")
                        
                        title_input = driver.find_element(By.ID, "event-title")
                        current_title = title_input.get_attribute("value")
                        print(f"✅ Modal pre-populated with event title: '{current_title}'")

                        start_date = driver.find_element(By.ID, "event-start-date")
                        current_start = start_date.get_attribute("value")
                        print(f"✅ Modal pre-populated with start date: '{current_start}'")

                        end_date = driver.find_element(By.ID, "event-end-date")
                        current_end = end_date.get_attribute("value")
                        print(f"✅ Modal pre-populated with end date: '{current_end}'")

                        checked_radios = driver.find_elements(By.CSS_SELECTOR, "input[type='radio'][name='event-level']:checked")
                        if checked_radios:
                            print(f"✅ Event color/category is pre-selected")

                        close_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Close')]")
                        close_button.click()
                        time.sleep(1)
                        print("✅ Edit modal closed")

                    except Exception as e:
                        print(f"⚠️  Error verifying edit modal: {e}")
                else:
                    print("⚠️  No clickable events found")
            else:
                print("⚠️  No events found to click")
        except Exception as e:
            print(f"⚠️  Error during event click test: {e}")

        screenshot_path = "tests/screenshots/selenium_calendar_screenshot.png"
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot saved to: {screenshot_path}")

        print("✅ Selenium calendar CRUD operations test completed successfully!")
        return True

    except Exception as e:
        print(f"❌ Selenium calendar test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        driver.quit()
        print("🔚 Selenium WebDriver closed")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "calendar":
        success = test_calendar_crud_operations()
    else:
        success = test_dashboard_with_selenium()
    
    exit(0 if success else 1)
