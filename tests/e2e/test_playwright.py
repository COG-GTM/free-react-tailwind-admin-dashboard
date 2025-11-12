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

def run_playwright_test():
    return asyncio.run(test_dashboard_with_playwright())

if __name__ == "__main__":
    success = run_playwright_test()
    exit(0 if success else 1)
