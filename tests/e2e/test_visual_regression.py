#!/usr/bin/env python3
"""
Visual regression tests for TailAdmin React Dashboard.
Implements baseline screenshot comparison for detecting visual changes.
"""

import pytest
import asyncio
import hashlib
from pathlib import Path
from PIL import Image
import io
from playwright.async_api import Page

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fixtures.test_data import (
    Selectors,
    Routes,
    VIEWPORTS,
)


def calculate_image_hash(image_bytes: bytes) -> str:
    """Calculate MD5 hash of image for quick comparison."""
    return hashlib.md5(image_bytes).hexdigest()


def compare_images(baseline_path: Path, current_bytes: bytes, threshold: float = 0.05) -> tuple:
    """
    Compare current screenshot with baseline.
    Returns (is_match, diff_percentage, diff_image_path).
    """
    if not baseline_path.exists():
        return None, 0, None  # No baseline exists
    
    try:
        baseline_image = Image.open(baseline_path)
        current_image = Image.open(io.BytesIO(current_bytes))
        
        # Resize if dimensions don't match
        if baseline_image.size != current_image.size:
            current_image = current_image.resize(baseline_image.size)
        
        # Convert to same mode
        baseline_image = baseline_image.convert('RGB')
        current_image = current_image.convert('RGB')
        
        # Calculate pixel differences
        baseline_pixels = list(baseline_image.getdata())
        current_pixels = list(current_image.getdata())
        
        total_pixels = len(baseline_pixels)
        diff_pixels = 0
        
        for bp, cp in zip(baseline_pixels, current_pixels):
            # Calculate color difference
            diff = sum(abs(b - c) for b, c in zip(bp, cp))
            if diff > 30:  # Threshold for considering a pixel different
                diff_pixels += 1
        
        diff_percentage = diff_pixels / total_pixels
        is_match = diff_percentage <= threshold
        
        return is_match, diff_percentage, None
        
    except Exception as e:
        print(f"Error comparing images: {e}")
        return False, 1.0, None


async def capture_screenshot(page: Page, name: str, baselines_dir: Path) -> tuple:
    """
    Capture screenshot and compare with baseline.
    Returns (screenshot_bytes, baseline_path, is_new_baseline).
    """
    baseline_path = baselines_dir / f"{name}.png"
    screenshot_bytes = await page.screenshot(full_page=True)
    
    is_new_baseline = not baseline_path.exists()
    
    return screenshot_bytes, baseline_path, is_new_baseline


async def save_baseline(baseline_path: Path, screenshot_bytes: bytes) -> None:
    """Save screenshot as new baseline."""
    baseline_path.parent.mkdir(parents=True, exist_ok=True)
    with open(baseline_path, 'wb') as f:
        f.write(screenshot_bytes)


@pytest.mark.visual
class TestDashboardVisualRegression:
    """Visual regression tests for the main dashboard."""

    @pytest.mark.asyncio
    async def test_dashboard_visual_baseline(
        self, playwright_page: Page, base_url: str, wait_for_app, baselines_dir: Path
    ):
        """Test dashboard visual appearance against baseline."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(2)  # Wait for animations and charts
        
        screenshot_bytes, baseline_path, is_new = await capture_screenshot(
            playwright_page, "dashboard_desktop", baselines_dir
        )
        
        if is_new:
            await save_baseline(baseline_path, screenshot_bytes)
            print(f"Created new baseline: {baseline_path}")
            return  # First run creates baseline
        
        is_match, diff_pct, _ = compare_images(baseline_path, screenshot_bytes)
        
        assert is_match, (
            f"Visual regression detected! Difference: {diff_pct:.2%}\n"
            f"Baseline: {baseline_path}"
        )

    @pytest.mark.asyncio
    async def test_dashboard_mobile_visual_baseline(
        self, playwright_mobile_page: Page, base_url: str, wait_for_app, baselines_dir: Path
    ):
        """Test dashboard mobile visual appearance against baseline."""
        await playwright_mobile_page.goto(base_url)
        await wait_for_app(playwright_mobile_page)
        await asyncio.sleep(2)
        
        screenshot_bytes, baseline_path, is_new = await capture_screenshot(
            playwright_mobile_page, "dashboard_mobile", baselines_dir
        )
        
        if is_new:
            await save_baseline(baseline_path, screenshot_bytes)
            print(f"Created new baseline: {baseline_path}")
            return
        
        is_match, diff_pct, _ = compare_images(baseline_path, screenshot_bytes)
        
        assert is_match, (
            f"Mobile visual regression detected! Difference: {diff_pct:.2%}"
        )

    @pytest.mark.asyncio
    async def test_dashboard_tablet_visual_baseline(
        self, playwright_tablet_page: Page, base_url: str, wait_for_app, baselines_dir: Path
    ):
        """Test dashboard tablet visual appearance against baseline."""
        await playwright_tablet_page.goto(base_url)
        await wait_for_app(playwright_tablet_page)
        await asyncio.sleep(2)
        
        screenshot_bytes, baseline_path, is_new = await capture_screenshot(
            playwright_tablet_page, "dashboard_tablet", baselines_dir
        )
        
        if is_new:
            await save_baseline(baseline_path, screenshot_bytes)
            print(f"Created new baseline: {baseline_path}")
            return
        
        is_match, diff_pct, _ = compare_images(baseline_path, screenshot_bytes)
        
        assert is_match, (
            f"Tablet visual regression detected! Difference: {diff_pct:.2%}"
        )


@pytest.mark.visual
class TestDarkModeVisualRegression:
    """Visual regression tests for dark mode."""

    @pytest.mark.asyncio
    async def test_dashboard_dark_mode_baseline(
        self, playwright_page: Page, base_url: str, wait_for_app, baselines_dir: Path
    ):
        """Test dashboard dark mode visual appearance."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        # Enable dark mode via localStorage
        await playwright_page.evaluate("""
            localStorage.setItem('theme', 'dark');
            document.documentElement.classList.add('dark');
        """)
        
        # Reload to apply theme
        await playwright_page.reload()
        await wait_for_app(playwright_page)
        await asyncio.sleep(2)
        
        screenshot_bytes, baseline_path, is_new = await capture_screenshot(
            playwright_page, "dashboard_dark_mode", baselines_dir
        )
        
        if is_new:
            await save_baseline(baseline_path, screenshot_bytes)
            print(f"Created new dark mode baseline: {baseline_path}")
            return
        
        is_match, diff_pct, _ = compare_images(baseline_path, screenshot_bytes)
        
        assert is_match, (
            f"Dark mode visual regression detected! Difference: {diff_pct:.2%}"
        )


@pytest.mark.visual
class TestPageVisualRegression:
    """Visual regression tests for individual pages."""

    @pytest.mark.asyncio
    async def test_calendar_page_baseline(
        self, playwright_page: Page, base_url: str, wait_for_app, baselines_dir: Path
    ):
        """Test calendar page visual appearance."""
        await playwright_page.goto(base_url + Routes.CALENDAR)
        await wait_for_app(playwright_page)
        await asyncio.sleep(2)
        
        screenshot_bytes, baseline_path, is_new = await capture_screenshot(
            playwright_page, "calendar_page", baselines_dir
        )
        
        if is_new:
            await save_baseline(baseline_path, screenshot_bytes)
            print(f"Created new baseline: {baseline_path}")
            return
        
        is_match, diff_pct, _ = compare_images(baseline_path, screenshot_bytes, threshold=0.1)
        
        # Calendar may have date-dependent content, allow higher threshold
        assert is_match, (
            f"Calendar visual regression detected! Difference: {diff_pct:.2%}"
        )

    @pytest.mark.asyncio
    async def test_profile_page_baseline(
        self, playwright_page: Page, base_url: str, wait_for_app, baselines_dir: Path
    ):
        """Test profile page visual appearance."""
        await playwright_page.goto(base_url + Routes.PROFILE)
        await wait_for_app(playwright_page)
        await asyncio.sleep(2)
        
        screenshot_bytes, baseline_path, is_new = await capture_screenshot(
            playwright_page, "profile_page", baselines_dir
        )
        
        if is_new:
            await save_baseline(baseline_path, screenshot_bytes)
            print(f"Created new baseline: {baseline_path}")
            return
        
        is_match, diff_pct, _ = compare_images(baseline_path, screenshot_bytes)
        
        assert is_match, (
            f"Profile visual regression detected! Difference: {diff_pct:.2%}"
        )

    @pytest.mark.asyncio
    async def test_form_elements_page_baseline(
        self, playwright_page: Page, base_url: str, wait_for_app, baselines_dir: Path
    ):
        """Test form elements page visual appearance."""
        await playwright_page.goto(base_url + Routes.FORM_ELEMENTS)
        await wait_for_app(playwright_page)
        await asyncio.sleep(2)
        
        screenshot_bytes, baseline_path, is_new = await capture_screenshot(
            playwright_page, "form_elements_page", baselines_dir
        )
        
        if is_new:
            await save_baseline(baseline_path, screenshot_bytes)
            print(f"Created new baseline: {baseline_path}")
            return
        
        is_match, diff_pct, _ = compare_images(baseline_path, screenshot_bytes)
        
        assert is_match, (
            f"Form elements visual regression detected! Difference: {diff_pct:.2%}"
        )

    @pytest.mark.asyncio
    async def test_tables_page_baseline(
        self, playwright_page: Page, base_url: str, wait_for_app, baselines_dir: Path
    ):
        """Test tables page visual appearance."""
        await playwright_page.goto(base_url + Routes.BASIC_TABLES)
        await wait_for_app(playwright_page)
        await asyncio.sleep(2)
        
        screenshot_bytes, baseline_path, is_new = await capture_screenshot(
            playwright_page, "tables_page", baselines_dir
        )
        
        if is_new:
            await save_baseline(baseline_path, screenshot_bytes)
            print(f"Created new baseline: {baseline_path}")
            return
        
        is_match, diff_pct, _ = compare_images(baseline_path, screenshot_bytes)
        
        assert is_match, (
            f"Tables visual regression detected! Difference: {diff_pct:.2%}"
        )


@pytest.mark.visual
class TestComponentVisualRegression:
    """Visual regression tests for specific components."""

    @pytest.mark.asyncio
    async def test_sidebar_visual_baseline(
        self, playwright_page: Page, base_url: str, wait_for_app, baselines_dir: Path
    ):
        """Test sidebar component visual appearance."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        # Capture just the sidebar
        sidebar = await playwright_page.query_selector(Selectors.SIDEBAR)
        if sidebar:
            screenshot_bytes = await sidebar.screenshot()
            baseline_path = baselines_dir / "sidebar_component.png"
            
            if not baseline_path.exists():
                await save_baseline(baseline_path, screenshot_bytes)
                print(f"Created new sidebar baseline: {baseline_path}")
                return
            
            is_match, diff_pct, _ = compare_images(baseline_path, screenshot_bytes)
            
            assert is_match, (
                f"Sidebar visual regression detected! Difference: {diff_pct:.2%}"
            )

    @pytest.mark.asyncio
    async def test_charts_visual_baseline(
        self, playwright_page: Page, base_url: str, wait_for_app, baselines_dir: Path
    ):
        """Test charts visual appearance."""
        await playwright_page.goto(base_url + Routes.LINE_CHART)
        await wait_for_app(playwright_page)
        await asyncio.sleep(3)  # Charts need time to render
        
        screenshot_bytes, baseline_path, is_new = await capture_screenshot(
            playwright_page, "line_chart_page", baselines_dir
        )
        
        if is_new:
            await save_baseline(baseline_path, screenshot_bytes)
            print(f"Created new chart baseline: {baseline_path}")
            return
        
        # Charts may have slight variations, allow higher threshold
        is_match, diff_pct, _ = compare_images(baseline_path, screenshot_bytes, threshold=0.15)
        
        assert is_match, (
            f"Chart visual regression detected! Difference: {diff_pct:.2%}"
        )


@pytest.mark.visual
class TestAuthPagesVisualRegression:
    """Visual regression tests for authentication pages."""

    @pytest.mark.asyncio
    async def test_signin_page_baseline(
        self, playwright_page: Page, base_url: str, wait_for_app, baselines_dir: Path
    ):
        """Test sign in page visual appearance."""
        await playwright_page.goto(base_url + Routes.SIGNIN)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        screenshot_bytes, baseline_path, is_new = await capture_screenshot(
            playwright_page, "signin_page", baselines_dir
        )
        
        if is_new:
            await save_baseline(baseline_path, screenshot_bytes)
            print(f"Created new baseline: {baseline_path}")
            return
        
        is_match, diff_pct, _ = compare_images(baseline_path, screenshot_bytes)
        
        assert is_match, (
            f"Sign in visual regression detected! Difference: {diff_pct:.2%}"
        )

    @pytest.mark.asyncio
    async def test_signup_page_baseline(
        self, playwright_page: Page, base_url: str, wait_for_app, baselines_dir: Path
    ):
        """Test sign up page visual appearance."""
        await playwright_page.goto(base_url + Routes.SIGNUP)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        screenshot_bytes, baseline_path, is_new = await capture_screenshot(
            playwright_page, "signup_page", baselines_dir
        )
        
        if is_new:
            await save_baseline(baseline_path, screenshot_bytes)
            print(f"Created new baseline: {baseline_path}")
            return
        
        is_match, diff_pct, _ = compare_images(baseline_path, screenshot_bytes)
        
        assert is_match, (
            f"Sign up visual regression detected! Difference: {diff_pct:.2%}"
        )


@pytest.mark.visual
class TestVisualRegressionUtilities:
    """Utility tests for visual regression infrastructure."""

    @pytest.mark.asyncio
    async def test_update_all_baselines(
        self, playwright_page: Page, base_url: str, wait_for_app, baselines_dir: Path
    ):
        """
        Utility test to update all baselines.
        Run with: pytest -k "test_update_all_baselines" --update-baselines
        """
        # This test is for manually updating baselines when needed
        # Skip by default
        pytest.skip("Run with --update-baselines flag to update all baselines")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
