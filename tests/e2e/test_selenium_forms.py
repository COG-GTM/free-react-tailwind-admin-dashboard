#!/usr/bin/env python3
"""
Selenium test script for TailAdmin React Dashboard - Form Elements
This script tests form validation and interaction using Selenium WebDriver
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
import time
import os
import unittest

class TestFormElements(unittest.TestCase):
    def setUp(self):
        """Set up the Chrome driver before each test"""
        print("🚀 Starting Selenium test for Form Elements...")
        
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
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
        except Exception as e:
            print(f"❌ Chrome setup failed: {e}")
            raise e

    def tearDown(self):
        """Clean up after each test"""
        if hasattr(self, 'driver'):
            self.driver.quit()
            print("🔚 Selenium WebDriver closed")

    def test_form_elements(self):
        """Test all form elements on the form-elements page"""
        try:
            print("📍 Navigating to http://localhost:5173/form-elements")
            self.driver.get("http://localhost:5173/form-elements")
            
            # Wait for the page to load
            self.wait.until(lambda driver: driver.execute_script("return document.querySelector('#root').children.length > 0"))
            print("✅ React app loaded successfully")
            
            time.sleep(2)
            
            # Check page title
            print(f"📄 Page title: {self.driver.title}")
            self.assertIn("TailAdmin", self.driver.title)
            
            print("\n🧪 Testing input field interactions...")
            self._test_input_fields()
            
            print("\n🧪 Testing checkbox toggling...")
            self._test_checkboxes()
            
            print("\n🧪 Testing radio button toggling...")
            self._test_radio_buttons()
            
            print("\n🧪 Testing select dropdown interactions...")
            self._test_select_dropdowns()
            
            print("\n🧪 Testing file upload functionality...")
            self._test_file_upload()
            
            # Take a screenshot
            screenshot_path = "tests/screenshots/selenium_forms_screenshot.png"
            os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
            self.driver.save_screenshot(screenshot_path)
            print(f"\n📸 Screenshot saved to: {screenshot_path}")
            
            print("\n✅ All form element tests completed successfully!")
            
        except Exception as e:
            print(f"❌ Form elements test failed: {e}")
            raise

    def _test_input_fields(self):
        """Test input field interactions - typing text and clearing fields"""
        try:
            inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="text"]')
            print(f"   Found {len(inputs)} text input fields")
            
            if len(inputs) > 0:
                first_input = inputs[0]
                first_input.clear()
                test_text = "Test Input Text"
                first_input.send_keys(test_text)
                print(f"   ✓ Typed text into input field: '{test_text}'")
                
                entered_value = first_input.get_attribute('value')
                self.assertEqual(entered_value, test_text)
                print(f"   ✓ Verified input value: '{entered_value}'")
                
                first_input.clear()
                cleared_value = first_input.get_attribute('value')
                self.assertEqual(cleared_value, "")
                print(f"   ✓ Cleared input field successfully")
                
            placeholder_inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[placeholder]')
            if len(placeholder_inputs) > 0:
                placeholder_input = placeholder_inputs[0]
                placeholder_text = placeholder_input.get_attribute('placeholder')
                print(f"   ✓ Found input with placeholder: '{placeholder_text}'")
                
                placeholder_input.clear()
                placeholder_input.send_keys("test@example.com")
                print(f"   ✓ Typed email into placeholder input")
                
            print("   ✅ Input field tests passed")
            
        except Exception as e:
            print(f"   ❌ Input field test failed: {e}")
            raise

    def _test_checkboxes(self):
        """Test checkbox toggling"""
        try:
            checkboxes = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="checkbox"]')
            print(f"   Found {len(checkboxes)} checkboxes")
            
            if len(checkboxes) > 0:
                first_checkbox = checkboxes[0]
                initial_state = first_checkbox.is_selected()
                print(f"   Initial state of first checkbox: {initial_state}")
                
                first_checkbox.click()
                time.sleep(0.5)
                new_state = first_checkbox.is_selected()
                print(f"   ✓ Toggled first checkbox to: {new_state}")
                self.assertNotEqual(initial_state, new_state)
                
                first_checkbox.click()
                time.sleep(0.5)
                final_state = first_checkbox.is_selected()
                print(f"   ✓ Toggled first checkbox back to: {final_state}")
                self.assertEqual(initial_state, final_state)
                
            for i, checkbox in enumerate(checkboxes[:3]):  # Test first 3 checkboxes
                if checkbox.is_enabled():
                    try:
                        checkbox.click()
                        time.sleep(0.3)
                        print(f"   ✓ Toggled checkbox {i+1}")
                    except:
                        print(f"   ⚠️  Checkbox {i+1} not clickable (might be disabled)")
                        
            print("   ✅ Checkbox tests passed")
            
        except Exception as e:
            print(f"   ❌ Checkbox test failed: {e}")
            raise

    def _test_radio_buttons(self):
        """Test radio button toggling"""
        try:
            radio_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="radio"]')
            print(f"   Found {len(radio_buttons)} radio buttons")
            
            if len(radio_buttons) > 0:
                for i, radio in enumerate(radio_buttons[:3]):  # Test first 3 radio buttons
                    if radio.is_enabled():
                        try:
                            radio.click()
                            time.sleep(0.3)
                            is_selected = radio.is_selected()
                            print(f"   ✓ Clicked radio button {i+1}, selected: {is_selected}")
                        except Exception as e:
                            print(f"   ⚠️  Radio button {i+1} not clickable: {e}")
                            
            print("   ✅ Radio button tests passed")
            
        except Exception as e:
            print(f"   ❌ Radio button test failed: {e}")
            raise

    def _test_select_dropdowns(self):
        """Test select dropdown interactions"""
        try:
            selects = self.driver.find_elements(By.CSS_SELECTOR, 'select')
            print(f"   Found {len(selects)} select dropdowns")
            
            if len(selects) > 0:
                first_select = selects[0]
                
                options = first_select.find_elements(By.TAG_NAME, 'option')
                print(f"   Select has {len(options)} options")
                
                if len(options) > 1:
                    options[1].click()
                    time.sleep(0.5)
                    selected_option = first_select.find_element(By.CSS_SELECTOR, 'option:checked')
                    print(f"   ✓ Selected option: '{selected_option.text}'")
                    
            custom_selects = self.driver.find_elements(By.CSS_SELECTOR, '[role="combobox"], .select, [class*="select"]')
            if len(custom_selects) > 0:
                print(f"   Found {len(custom_selects)} custom select components")
                
            print("   ✅ Select dropdown tests passed")
            
        except Exception as e:
            print(f"   ❌ Select dropdown test failed: {e}")
            raise

    def _test_file_upload(self):
        """Test file upload functionality"""
        try:
            file_inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="file"]')
            print(f"   Found {len(file_inputs)} file input elements")
            
            if len(file_inputs) > 0:
                test_file_path = "/tmp/test_upload_file.txt"
                with open(test_file_path, 'w') as f:
                    f.write("This is a test file for upload")
                
                first_file_input = file_inputs[0]
                first_file_input.send_keys(test_file_path)
                time.sleep(0.5)
                
                file_value = first_file_input.get_attribute('value')
                print(f"   ✓ File input value: {file_value}")
                self.assertIn("test_upload_file.txt", file_value)
                print(f"   ✓ File upload test successful")
                
                os.remove(test_file_path)
            else:
                print("   ⚠️  No file input elements found")
                
            print("   ✅ File upload tests passed")
            
        except Exception as e:
            print(f"   ❌ File upload test failed: {e}")
            raise

def test_dashboard_with_selenium():
    """Main test function for compatibility with existing test runner"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestFormElements)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

if __name__ == "__main__":
    success = test_dashboard_with_selenium()
    exit(0 if success else 1)
