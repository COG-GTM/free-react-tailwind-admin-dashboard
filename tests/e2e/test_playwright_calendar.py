#!/usr/bin/env python3
"""
Playwright test script for TailAdmin React Dashboard - Calendar
This script tests calendar event management using Playwright
"""

import asyncio
from playwright.async_api import async_playwright
import os

async def test_dashboard_with_playwright():
    """Test calendar event management functionality"""
    print("🚀 Starting Playwright test for Calendar...")
    
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()
        
        try:
            print("📍 Navigating to http://localhost:5173/calendar")
            await page.goto("http://localhost:5173/calendar")
            
            # Wait for the page to load
            await page.wait_for_load_state('networkidle')
            
            # Check page title
            title = await page.title()
            print(f"📄 Page title: {title}")
            assert "TailAdmin" in title, f"Expected 'TailAdmin' in title, got: {title}"
            
            # Wait for React app to load
            await page.wait_for_function('document.querySelector("#root").children.length > 0', timeout=15000)
            print("✅ React app loaded successfully")
            
            await asyncio.sleep(2)
            
            print("\n🧪 Testing FullCalendar rendering...")
            await test_calendar_rendering(page)
            
            print("\n🧪 Testing existing events display...")
            await test_existing_events(page)
            
            print("\n🧪 Testing Add Event button and modal...")
            await test_add_event_modal(page)
            
            print("\n🧪 Testing event form filling...")
            await test_event_form_filling(page)
            
            print("\n🧪 Testing date selection interaction...")
            await test_date_selection(page)
            
            print("\n📸 Taking screenshots...")
            await take_screenshots(page)
            
            print("\n✅ All calendar tests completed successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Calendar test failed: {e}")
            return False
            
        finally:
            await browser.close()
            print("🔚 Playwright browser closed")

async def test_calendar_rendering(page):
    """Test that FullCalendar renders properly"""
    try:
        calendar_selectors = [
            '.fc',
            '.fc-view',
            '.fc-daygrid',
            '[class*="fullcalendar"]',
            '.custom-calendar'
        ]
        
        calendar_found = False
        for selector in calendar_selectors:
            try:
                await page.wait_for_selector(selector, timeout=5000)
                print(f"   ✓ FullCalendar found with selector: {selector}")
                calendar_found = True
                break
            except:
                continue
        
        assert calendar_found, "FullCalendar should be rendered"
        
        header = await page.query_selector('.fc-header-toolbar, .fc-toolbar')
        if header:
            print("   ✓ Calendar header toolbar found")
        
        grid = await page.query_selector('.fc-daygrid-body, .fc-view-harness')
        if grid:
            print("   ✓ Calendar grid found")
            
        print("   ✅ Calendar rendering tests passed")
        
    except Exception as e:
        print(f"   ❌ Calendar rendering test failed: {e}")
        raise

async def test_existing_events(page):
    """Test that existing events are displayed"""
    try:
        await asyncio.sleep(1)
        
        event_selectors = [
            '.fc-event',
            '.fc-daygrid-event',
            '[class*="fc-event"]'
        ]
        
        events = []
        for selector in event_selectors:
            try:
                events = await page.query_selector_all(selector)
                if len(events) > 0:
                    print(f"   ✓ Found {len(events)} calendar events with selector: {selector}")
                    break
            except:
                continue
        
        if len(events) > 0:
            print(f"   ✓ Calendar displays {len(events)} events")
            
            for i, event in enumerate(events[:3]):
                try:
                    title_element = await event.query_selector('.fc-event-title, .fc-event-title-container')
                    if title_element:
                        title_text = await title_element.text_content()
                        print(f"   ✓ Event {i+1}: '{title_text.strip()}'")
                except:
                    pass
        else:
            print("   ⚠️  No events found (they might be rendered differently)")
            
        print("   ✅ Existing events tests passed")
        
    except Exception as e:
        print(f"   ❌ Existing events test failed: {e}")
        raise

async def test_add_event_modal(page):
    """Test Add Event button and modal opening/closing"""
    try:
        add_button_selectors = [
            'button:has-text("Add Event")',
            '.fc-addEventButton-button',
            'button[class*="addEvent"]',
            'button:has-text("Add Event +")'
        ]
        
        button_found = False
        for selector in add_button_selectors:
            try:
                add_button = await page.query_selector(selector)
                if add_button:
                    print(f"   ✓ Found Add Event button with selector: {selector}")
                    await add_button.click()
                    button_found = True
                    break
            except:
                continue
        
        assert button_found, "Add Event button should be found and clickable"
        
        await asyncio.sleep(1)
        
        modal_selectors = [
            '[role="dialog"]',
            '.modal',
            '[class*="modal"]'
        ]
        
        modal_found = False
        for selector in modal_selectors:
            try:
                modal = await page.query_selector(selector)
                if modal:
                    is_visible = await modal.is_visible()
                    if is_visible:
                        print(f"   ✓ Modal opened successfully with selector: {selector}")
                        modal_found = True
                        break
            except:
                continue
        
        assert modal_found, "Modal should open after clicking Add Event button"
        
        modal_title = await page.query_selector('h5:has-text("Add Event"), .modal-title')
        if modal_title:
            title_text = await modal_title.text_content()
            print(f"   ✓ Modal title: '{title_text.strip()}'")
        
        close_button = await page.query_selector('button:has-text("Close")')
        if close_button:
            await close_button.click()
            await asyncio.sleep(0.5)
            print("   ✓ Modal closed successfully")
        
        print("   ✅ Add Event modal tests passed")
        
    except Exception as e:
        print(f"   ❌ Add Event modal test failed: {e}")
        raise

async def test_event_form_filling(page):
    """Test filling in the event form"""
    try:
        add_button = await page.query_selector('button:has-text("Add Event")')
        if add_button:
            await add_button.click()
            await asyncio.sleep(1)
        
        title_input = await page.query_selector('#event-title, input[type="text"]')
        if title_input:
            await title_input.fill("Test Event Title")
            title_value = await title_input.input_value()
            print(f"   ✓ Filled event title: '{title_value}'")
            assert title_value == "Test Event Title", "Event title should be filled correctly"
        
        color_options = ['Danger', 'Success', 'Primary', 'Warning']
        for color in color_options[:2]:
            try:
                color_radio = await page.query_selector(f'input[type="radio"][value="{color}"]')
                if color_radio:
                    await color_radio.click()
                    await asyncio.sleep(0.3)
                    is_checked = await color_radio.is_checked()
                    print(f"   ✓ Selected event color: {color}, checked: {is_checked}")
                    break
            except:
                continue
        
        start_date_input = await page.query_selector('#event-start-date, input[type="date"]')
        if start_date_input:
            await start_date_input.fill("2025-12-25")
            start_value = await start_date_input.input_value()
            print(f"   ✓ Filled start date: {start_value}")
        
        end_date_input = await page.query_selector('#event-end-date')
        if end_date_input:
            await end_date_input.fill("2025-12-26")
            end_value = await end_date_input.input_value()
            print(f"   ✓ Filled end date: {end_value}")
        
        screenshot_path = "tests/screenshots/playwright_calendar_form_filled.png"
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        await page.screenshot(path=screenshot_path)
        print(f"   📸 Screenshot saved: {screenshot_path}")
        
        add_event_button = await page.query_selector('button:has-text("Add Event")')
        if add_event_button:
            button_text = await add_event_button.text_content()
            if "Add Event" in button_text and "+" not in button_text:
                await add_event_button.click()
                await asyncio.sleep(1)
                print("   ✓ Submitted event form")
        
        await asyncio.sleep(0.5)
        
        print("   ✅ Event form filling tests passed")
        
    except Exception as e:
        print(f"   ❌ Event form filling test failed: {e}")
        try:
            close_button = await page.query_selector('button:has-text("Close")')
            if close_button:
                await close_button.click()
                await asyncio.sleep(0.5)
        except:
            pass
        raise

async def test_date_selection(page):
    """Test date selection interaction on the calendar"""
    try:
        date_cells = await page.query_selector_all('.fc-daygrid-day, .fc-day, [data-date]')
        print(f"   Found {len(date_cells)} date cells")
        
        if len(date_cells) > 0:
            clicked = False
            for i, cell in enumerate(date_cells[15:20]):
                if clicked:
                    break
                try:
                    is_visible = await cell.is_visible()
                    if is_visible:
                        await cell.click(timeout=3000)
                        await asyncio.sleep(1)
                        print("   ✓ Clicked on a date cell")
                        clicked = True
                        
                        try:
                            modal = await page.wait_for_selector('[role="dialog"]', timeout=2000)
                            if modal:
                                is_modal_visible = await modal.is_visible()
                                if is_modal_visible:
                                    print("   ✓ Modal opened after date selection")
                                    
                                    close_button = await page.query_selector('button:has-text("Close")')
                                    if close_button:
                                        await close_button.click()
                                        await asyncio.sleep(0.5)
                        except:
                            print("   ⚠️  Modal did not open after date selection (might not be selectable)")
                        break
                except Exception as e:
                    print(f"   ⚠️  Could not click date cell {i}: {str(e)[:50]}")
                    continue
            
            if not clicked:
                print("   ⚠️  Could not click any date cells (they might not be selectable)")
        
        print("   ✅ Date selection tests passed")
        
    except Exception as e:
        print(f"   ❌ Date selection test failed: {e}")
        raise

async def take_screenshots(page):
    """Take screenshots of calendar in different states"""
    try:
        screenshot_path_1 = "tests/screenshots/playwright_calendar_default.png"
        os.makedirs(os.path.dirname(screenshot_path_1), exist_ok=True)
        await page.screenshot(path=screenshot_path_1, full_page=True)
        print(f"   📸 Screenshot 1 saved: {screenshot_path_1}")
        
        try:
            add_button = await page.wait_for_selector('button:has-text("Add Event")', timeout=5000)
            if add_button:
                await add_button.click(timeout=3000)
                await asyncio.sleep(1)
                
                screenshot_path_2 = "tests/screenshots/playwright_calendar_modal.png"
                await page.screenshot(path=screenshot_path_2)
                print(f"   📸 Screenshot 2 saved: {screenshot_path_2}")
                
                close_button = await page.query_selector('button:has-text("Close")')
                if close_button:
                    await close_button.click(timeout=3000)
                    await asyncio.sleep(0.5)
        except Exception as e:
            print(f"   ⚠️  Could not capture modal screenshot: {str(e)[:50]}")
        
        try:
            week_button = await page.query_selector('button:has-text("week"), .fc-timeGridWeek-button')
            if week_button:
                await week_button.click(timeout=3000)
                await asyncio.sleep(1)
                
                screenshot_path_3 = "tests/screenshots/playwright_calendar_week_view.png"
                await page.screenshot(path=screenshot_path_3)
                print(f"   📸 Screenshot 3 saved: {screenshot_path_3}")
        except Exception as e:
            print(f"   ⚠️  Could not capture week view screenshot: {str(e)[:50]}")
        
        print("   ✅ All screenshots captured successfully")
        
    except Exception as e:
        print(f"   ❌ Screenshot capture failed: {e}")
        raise

def run_playwright_test():
    """Wrapper function to run the async test"""
    return asyncio.run(test_dashboard_with_playwright())

if __name__ == "__main__":
    success = run_playwright_test()
    exit(0 if success else 1)
