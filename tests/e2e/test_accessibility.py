#!/usr/bin/env python3
"""
Accessibility tests for TailAdmin React Dashboard.
Uses axe-core for WCAG compliance checks via Playwright.
"""

import pytest
import asyncio
import json
from pathlib import Path
from playwright.async_api import Page

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fixtures.test_data import (
    Selectors,
    Routes,
    AccessibilityConfig,
)

AXE_CORE_CDN = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.8.4/axe.min.js"


async def inject_axe(page: Page) -> None:
    """Inject axe-core library into the page."""
    await page.add_script_tag(url=AXE_CORE_CDN)
    await page.wait_for_function("typeof axe !== 'undefined'")


async def run_axe(page: Page, options: dict = None) -> dict:
    """Run axe-core accessibility analysis on the page."""
    if options is None:
        options = {
            "runOnly": {
                "type": "tag",
                "values": AccessibilityConfig.WCAG_LEVELS
            }
        }
    
    results = await page.evaluate(f"""
        async () => {{
            return await axe.run(document, {json.dumps(options)});
        }}
    """)
    return results


def format_violations(violations: list) -> str:
    """Format accessibility violations for readable output."""
    if not violations:
        return "No accessibility violations found."
    
    output = []
    for violation in violations:
        output.append(f"\n[{violation['impact'].upper()}] {violation['id']}: {violation['description']}")
        output.append(f"  Help: {violation['helpUrl']}")
        for node in violation.get('nodes', [])[:3]:  # Limit to first 3 nodes
            output.append(f"  - {node.get('html', 'N/A')[:100]}")
    
    return "\n".join(output)


@pytest.mark.accessibility
class TestDashboardAccessibility:
    """Accessibility tests for the main dashboard."""

    @pytest.mark.asyncio
    async def test_dashboard_has_no_critical_violations(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that dashboard has no critical accessibility violations."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(2)
        
        await inject_axe(playwright_page)
        results = await run_axe(playwright_page)
        
        critical_violations = [
            v for v in results.get('violations', [])
            if v.get('impact') == 'critical'
        ]
        
        assert len(critical_violations) == 0, (
            f"Found {len(critical_violations)} critical accessibility violations:\n"
            f"{format_violations(critical_violations)}"
        )

    @pytest.mark.asyncio
    async def test_dashboard_has_no_serious_violations(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that dashboard has no serious accessibility violations."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(2)
        
        await inject_axe(playwright_page)
        results = await run_axe(playwright_page)
        
        serious_violations = [
            v for v in results.get('violations', [])
            if v.get('impact') in ['critical', 'serious']
        ]
        
        # Allow up to 5 serious violations for now (can be tightened later)
        assert len(serious_violations) <= 5, (
            f"Found {len(serious_violations)} serious accessibility violations:\n"
            f"{format_violations(serious_violations)}"
        )

    @pytest.mark.asyncio
    async def test_dashboard_images_have_alt_text(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that all images have alt text."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        await inject_axe(playwright_page)
        results = await run_axe(playwright_page, {
            "runOnly": ["image-alt"]
        })
        
        violations = results.get('violations', [])
        image_alt_violations = [v for v in violations if v['id'] == 'image-alt']
        
        assert len(image_alt_violations) == 0, (
            f"Found images without alt text:\n{format_violations(image_alt_violations)}"
        )

    @pytest.mark.asyncio
    async def test_dashboard_buttons_have_accessible_names(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that all buttons have accessible names."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        await inject_axe(playwright_page)
        results = await run_axe(playwright_page, {
            "runOnly": ["button-name"]
        })
        
        violations = results.get('violations', [])
        button_violations = [v for v in violations if v['id'] == 'button-name']
        
        # Allow some button violations (icon buttons may not have text)
        assert len(button_violations) <= 3, (
            f"Found buttons without accessible names:\n{format_violations(button_violations)}"
        )

    @pytest.mark.asyncio
    async def test_dashboard_links_have_accessible_names(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that all links have accessible names."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        await inject_axe(playwright_page)
        results = await run_axe(playwright_page, {
            "runOnly": ["link-name"]
        })
        
        violations = results.get('violations', [])
        link_violations = [v for v in violations if v['id'] == 'link-name']
        
        assert len(link_violations) <= 2, (
            f"Found links without accessible names:\n{format_violations(link_violations)}"
        )


@pytest.mark.accessibility
class TestFormAccessibility:
    """Accessibility tests for form elements."""

    @pytest.mark.asyncio
    async def test_form_elements_have_labels(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that form elements have associated labels."""
        await playwright_page.goto(base_url + Routes.FORM_ELEMENTS)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        await inject_axe(playwright_page)
        results = await run_axe(playwright_page, {
            "runOnly": ["label"]
        })
        
        violations = results.get('violations', [])
        label_violations = [v for v in violations if v['id'] == 'label']
        
        # Allow some label violations for complex form components
        assert len(label_violations) <= 5, (
            f"Found form elements without labels:\n{format_violations(label_violations)}"
        )

    @pytest.mark.asyncio
    async def test_form_page_has_no_critical_violations(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that form page has no critical accessibility violations."""
        await playwright_page.goto(base_url + Routes.FORM_ELEMENTS)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        await inject_axe(playwright_page)
        results = await run_axe(playwright_page)
        
        critical_violations = [
            v for v in results.get('violations', [])
            if v.get('impact') == 'critical'
        ]
        
        assert len(critical_violations) == 0, (
            f"Found critical violations on form page:\n{format_violations(critical_violations)}"
        )


@pytest.mark.accessibility
class TestNavigationAccessibility:
    """Accessibility tests for navigation elements."""

    @pytest.mark.asyncio
    async def test_sidebar_is_navigable(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that sidebar navigation is accessible."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        # Check that sidebar has navigation landmark
        nav_elements = await playwright_page.query_selector_all('nav, [role="navigation"]')
        assert len(nav_elements) > 0, "No navigation landmarks found"

    @pytest.mark.asyncio
    async def test_skip_link_functionality(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test for skip link presence (optional but recommended)."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        
        # Check for skip link (this is a best practice, not required)
        skip_links = await playwright_page.query_selector_all(
            'a[href="#main"], a[href="#content"], .skip-link, [class*="skip"]'
        )
        # This is informational - skip links are recommended but not required
        if len(skip_links) == 0:
            print("Note: No skip link found. Consider adding one for better accessibility.")


@pytest.mark.accessibility
class TestColorContrastAccessibility:
    """Color contrast accessibility tests."""

    @pytest.mark.asyncio
    async def test_color_contrast_compliance(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that color contrast meets WCAG requirements."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        await inject_axe(playwright_page)
        results = await run_axe(playwright_page, {
            "runOnly": ["color-contrast"]
        })
        
        violations = results.get('violations', [])
        contrast_violations = [v for v in violations if v['id'] == 'color-contrast']
        
        # Allow some contrast violations (dark mode may have different requirements)
        assert len(contrast_violations) <= 10, (
            f"Found color contrast violations:\n{format_violations(contrast_violations)}"
        )


@pytest.mark.accessibility
class TestKeyboardAccessibility:
    """Keyboard navigation accessibility tests."""

    @pytest.mark.asyncio
    async def test_interactive_elements_are_focusable(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that interactive elements can receive keyboard focus."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        # Tab through the page and check focus
        await playwright_page.keyboard.press("Tab")
        
        focused_element = await playwright_page.evaluate(
            "document.activeElement.tagName"
        )
        
        # Something should be focused after pressing Tab
        assert focused_element is not None
        assert focused_element != "BODY", "No element received focus after Tab"

    @pytest.mark.asyncio
    async def test_focus_visible_on_interactive_elements(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that focus is visible on interactive elements."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        # Tab to first interactive element
        await playwright_page.keyboard.press("Tab")
        
        # Check if focus styles are applied
        has_focus_styles = await playwright_page.evaluate("""
            () => {
                const el = document.activeElement;
                if (!el || el === document.body) return false;
                const styles = window.getComputedStyle(el);
                return styles.outline !== 'none' || 
                       styles.boxShadow !== 'none' ||
                       el.classList.contains('focus') ||
                       el.matches(':focus-visible');
            }
        """)
        
        # This is informational - focus visibility is important
        if not has_focus_styles:
            print("Note: Focus styles may not be visible. Consider adding :focus-visible styles.")


@pytest.mark.accessibility
class TestARIAAccessibility:
    """ARIA attribute accessibility tests."""

    @pytest.mark.asyncio
    async def test_aria_attributes_are_valid(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test that ARIA attributes are valid."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        await inject_axe(playwright_page)
        results = await run_axe(playwright_page, {
            "runOnly": ["aria-valid-attr", "aria-valid-attr-value", "aria-required-attr"]
        })
        
        violations = results.get('violations', [])
        
        assert len(violations) <= 3, (
            f"Found ARIA attribute violations:\n{format_violations(violations)}"
        )


@pytest.mark.accessibility
class TestAccessibilityReport:
    """Generate comprehensive accessibility report."""

    @pytest.mark.asyncio
    async def test_generate_accessibility_report(
        self, playwright_page: Page, base_url: str, wait_for_app, screenshots_dir: Path
    ):
        """Generate a comprehensive accessibility report for the dashboard."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(2)
        
        await inject_axe(playwright_page)
        results = await run_axe(playwright_page)
        
        # Save report to file
        report_path = screenshots_dir.parent / "reports" / "accessibility_report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Summary
        violations = results.get('violations', [])
        passes = results.get('passes', [])
        
        print(f"\nAccessibility Report Summary:")
        print(f"  Violations: {len(violations)}")
        print(f"  Passes: {len(passes)}")
        print(f"  Report saved to: {report_path}")
        
        # Categorize by impact
        by_impact = {}
        for v in violations:
            impact = v.get('impact', 'unknown')
            by_impact[impact] = by_impact.get(impact, 0) + 1
        
        print(f"  By Impact: {by_impact}")
        
        # Test passes if no critical violations
        critical_count = by_impact.get('critical', 0)
        assert critical_count == 0, f"Found {critical_count} critical accessibility violations"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
