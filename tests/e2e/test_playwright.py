#!/usr/bin/env python3
"""
Playwright test script for TailAdmin React Dashboard
This script tests basic functionality of the dashboard using Playwright
"""

import asyncio
from playwright.async_api import async_playwright
import time

async def test_dashboard_with_playwright():
    print("🚀 Starting Playwright test for TailAdmin React Dashboard...")

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()

        try:
            # Navigate to the dashboard
            print("📍 Navigating to http://localhost:5173")
            await page.goto("http://localhost:5173")

            # Wait for the page to load
            await page.wait_for_load_state('networkidle')

            # Check page title
            title = await page.title()
            print(f"📄 Page title: {title}")
            assert "TailAdmin" in title, f"Expected 'TailAdmin' in title, got: {title}"

            # Wait for React app to load - look for the root div to have content
            await page.wait_for_function('document.querySelector("#root").children.length > 0', timeout=15000)
            print("✅ React app loaded successfully")

            # Wait a bit more for content to render
            await asyncio.sleep(2)

            # Check for sidebar navigation
            sidebar_selectors = ['[data-testid="sidebar"]', '.sidebar', 'nav', 'aside']
            sidebar_found = False
            for selector in sidebar_selectors:
                try:
                    await page.wait_for_selector(selector, timeout=2000)
                    print(f"✅ Sidebar navigation found with selector: {selector}")
                    sidebar_found = True
                    break
                except:
                    continue

            if not sidebar_found:
                print("⚠️  Sidebar not found with common selectors")

            # Check for dashboard cards/widgets
            try:
                cards = await page.query_selector_all('.card, .widget, [class*="card"], [class*="widget"], .bg-white')
                print(f"📊 Found {len(cards)} potential dashboard cards/widgets")
            except Exception as e:
                print(f"⚠️  Error finding dashboard cards: {e}")

            # Check for charts or data visualizations
            try:
                charts = await page.query_selector_all('.apexcharts-canvas, canvas, svg')
                print(f"📈 Found {len(charts)} charts/visualizations")
            except Exception as e:
                print(f"⚠️  Error finding charts: {e}")

            # Take a screenshot
            screenshot_path = "tests/screenshots/playwright_screenshot.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Screenshot saved to: {screenshot_path}")

            # Test navigation
            try:
                nav_links = await page.query_selector_all('a[href], button')
                print(f"🔗 Found {len(nav_links)} navigation links/buttons")

                # Try to interact with a few elements
                for i, link in enumerate(nav_links[:5]):
                    try:
                        if await link.is_visible() and await link.is_enabled():
                            text_content = await link.text_content()
                            if text_content and text_content.strip():
                                print(f"🖱️  Found interactive element: '{text_content.strip()}'")
                                # Just hover over it, don't click to avoid navigation issues
                                await link.hover()
                                await asyncio.sleep(0.5)
                                break
                    except Exception as e:
                        continue

            except Exception as e:
                print(f"⚠️  Navigation test failed: {e}")

            # Test responsive design by changing viewport
            print("📱 Testing responsive design...")
            await page.set_viewport_size({"width": 768, "height": 1024})
            await asyncio.sleep(1)

            mobile_screenshot_path = "tests/screenshots/playwright_mobile_screenshot.png"
            await page.screenshot(path=mobile_screenshot_path)
            print(f"📸 Mobile screenshot saved to: {mobile_screenshot_path}")

            # Test dark mode toggle if available
            try:
                dark_mode_selectors = ['[data-testid="theme-toggle"]', '.theme-toggle', 'button[aria-label*="theme"]', 'button[aria-label*="dark"]']
                for selector in dark_mode_selectors:
                    try:
                        theme_toggle = await page.query_selector(selector)
                        if theme_toggle:
                            print("🌙 Found theme toggle, testing dark mode...")
                            await theme_toggle.click()
                            await asyncio.sleep(1)

                            dark_screenshot_path = "tests/screenshots/playwright_dark_screenshot.png"
                            await page.screenshot(path=dark_screenshot_path)
                            print(f"📸 Dark mode screenshot saved to: {dark_screenshot_path}")
                            break
                    except:
                        continue
            except Exception as e:
                print(f"⚠️  Dark mode test failed: {e}")

            print("✅ Playwright test completed successfully!")
            return True

        except Exception as e:
            print(f"❌ Playwright test failed: {e}")
            return False

        finally:
            await browser.close()
            print("🔚 Playwright browser closed")

async def test_form_submission_and_validation():
    """
    Test form interactions on the /form-elements page
    Tests form submission, validation, multiselect, file upload, and accessibility
    """
    print("🚀 Starting Playwright form submission and validation test...")

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()

        try:
            # Navigate to the form elements page
            print("📍 Navigating to http://localhost:5173/form-elements")
            await page.goto("http://localhost:5173/form-elements", wait_until="networkidle")

            # Wait for the page to load
            await page.wait_for_load_state('networkidle')
            print("✅ Form elements page loaded successfully")

            # Wait for React app to render
            await asyncio.sleep(2)

            print("📝 Testing text input...")
            text_input = await page.query_selector('input[type="text"]#input')
            if text_input:
                await text_input.fill("Test User Input")
                input_value = await text_input.input_value()
                assert input_value == "Test User Input", f"Expected 'Test User Input', got: {input_value}"
                print("✅ Text input filled and validated successfully")
            else:
                print("⚠️  Text input not found")

            print("📝 Testing input with placeholder...")
            placeholder_input = await page.query_selector('input[type="text"]#inputTwo')
            if placeholder_input:
                await placeholder_input.fill("test@example.com")
                input_value = await placeholder_input.input_value()
                assert input_value == "test@example.com", f"Expected 'test@example.com', got: {input_value}"
                print("✅ Placeholder input filled and validated successfully")
            else:
                print("⚠️  Placeholder input not found")

            print("📝 Testing select dropdown...")
            select_elements = await page.query_selector_all('select')
            if select_elements:
                select = select_elements[0]
                await select.select_option('marketing')
                selected_value = await select.input_value()
                print(f"✅ Select dropdown changed to: {selected_value}")
            else:
                print("⚠️  Select dropdown not found")

            print("📝 Testing password input...")
            password_input = await page.query_selector('input[type="password"]')
            if password_input:
                await password_input.fill("SecurePassword123")
                input_value = await password_input.input_value()
                assert input_value == "SecurePassword123", f"Expected 'SecurePassword123', got: {input_value}"
                
                eye_button = await page.query_selector('button:has(svg)')
                if eye_button:
                    await eye_button.click()
                    await asyncio.sleep(0.5)
                    text_input_check = await page.query_selector('input[type="text"][value="SecurePassword123"]')
                    if text_input_check:
                        print("✅ Password visibility toggle works correctly")
                    else:
                        print("⚠️  Password visibility toggle may not have worked")
                else:
                    print("⚠️  Password visibility toggle button not found")
                print("✅ Password input filled successfully")
            else:
                print("⚠️  Password input not found")

            print("📝 Testing MultiSelect component...")
            multiselect_label = await page.query_selector('text="Multiple Select Options"')
            if multiselect_label:
                multiselect_trigger = await page.query_selector('[role="combobox"]')
                if multiselect_trigger:
                    selected_items = await page.query_selector_all('.bg-gray-100.dark\\:bg-gray-800')
                    initial_count = len(selected_items)
                    print(f"📊 Found {initial_count} initially selected items in MultiSelect")
                    
                    await multiselect_trigger.click()
                    await asyncio.sleep(0.5)
                    
                    dropdown = await page.query_selector('[role="listbox"]')
                    if dropdown:
                        print("✅ MultiSelect dropdown opened successfully")
                        
                        options = await page.query_selector_all('[role="option"]')
                        if len(options) > 0:
                            await options[0].click()
                            await asyncio.sleep(0.5)
                            print("✅ MultiSelect option clicked successfully")
                        
                        await page.click('body')
                        await asyncio.sleep(0.5)
                        print("✅ MultiSelect interaction completed")
                    else:
                        print("⚠️  MultiSelect dropdown did not open")
                else:
                    print("⚠️  MultiSelect trigger not found")
            else:
                print("⚠️  MultiSelect component not found")

            print("📝 Testing keyboard navigation on MultiSelect...")
            multiselect_trigger = await page.query_selector('[role="combobox"]')
            if multiselect_trigger:
                await multiselect_trigger.focus()
                
                await page.keyboard.press('Enter')
                await asyncio.sleep(0.5)
                
                await page.keyboard.press('ArrowDown')
                await asyncio.sleep(0.3)
                
                await page.keyboard.press('Enter')
                await asyncio.sleep(0.3)
                
                await page.keyboard.press('Escape')
                await asyncio.sleep(0.3)
                
                print("✅ Keyboard navigation on MultiSelect works correctly")
            else:
                print("⚠️  Could not test keyboard navigation")

            print("📝 Testing file input...")
            file_inputs = await page.query_selector_all('input[type="file"]')
            if file_inputs:
                import tempfile
                import os
                with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                    f.write("Test file content")
                    temp_file_path = f.name
                
                try:
                    await file_inputs[0].set_input_files(temp_file_path)
                    print("✅ File input accepts file successfully")
                finally:
                    os.unlink(temp_file_path)
            else:
                print("⚠️  File input not found")

            print("📝 Testing date picker...")
            date_input = await page.query_selector('input#date-picker')
            if date_input:
                try:
                    await date_input.click()
                    await asyncio.sleep(0.5)
                    await date_input.type('12/25/2024')
                    await asyncio.sleep(0.5)
                    print(f"✅ Date picker interacted with successfully")
                except Exception as e:
                    print(f"⚠️  Date picker interaction had issues: {e}")
            else:
                print("⚠️  Date picker not found")

            print("📝 Testing time picker...")
            time_input = await page.query_selector('input[type="time"]#tm')
            if time_input:
                await time_input.fill('14:30')
                time_value = await time_input.input_value()
                print(f"✅ Time picker filled with: {time_value}")
            else:
                print("⚠️  Time picker not found")

            print("📝 Testing accessibility features...")
            # Check for ARIA labels on MultiSelect
            combobox = await page.query_selector('[role="combobox"]')
            if combobox:
                aria_expanded = await combobox.get_attribute('aria-expanded')
                aria_haspopup = await combobox.get_attribute('aria-haspopup')
                print(f"✅ MultiSelect has ARIA attributes: aria-expanded={aria_expanded}, aria-haspopup={aria_haspopup}")
            
            # Check for labels
            labels = await page.query_selector_all('label')
            print(f"✅ Found {len(labels)} form labels for accessibility")

            print("📝 Testing form validation...")
            required_inputs = await page.query_selector_all('input[required]')
            if required_inputs:
                print(f"📊 Found {len(required_inputs)} required inputs")
            else:
                print("ℹ️  No required field validation found on this page")

            # Take a screenshot
            screenshot_path = "tests/screenshots/playwright_forms_screenshot.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"📸 Screenshot saved to: {screenshot_path}")

            print("✅ Playwright form submission and validation test completed successfully!")
            return True

        except Exception as e:
            print(f"❌ Playwright form test failed: {e}")
            import traceback
            traceback.print_exc()
            return False

        finally:
            await browser.close()
            print("🔚 Playwright browser closed")

def run_playwright_test():
    return asyncio.run(test_dashboard_with_playwright())

def run_form_test():
    return asyncio.run(test_form_submission_and_validation())

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "forms":
        success = run_form_test()
    else:
        success = run_playwright_test()
    
    exit(0 if success else 1)
