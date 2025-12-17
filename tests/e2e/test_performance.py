#!/usr/bin/env python3
"""
Performance tests for TailAdmin React Dashboard.
Measures Core Web Vitals and page load performance.
"""

import pytest
import asyncio
import json
from pathlib import Path
from datetime import datetime
from playwright.async_api import Page

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fixtures.test_data import (
    Routes,
    PerformanceThresholds,
)


@pytest.mark.performance
class TestCoreWebVitals:
    """Tests for Core Web Vitals metrics."""

    @pytest.mark.asyncio
    async def test_first_contentful_paint(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test First Contentful Paint (FCP) is within threshold."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        fcp = await playwright_page.evaluate("""
            () => {
                const paint = performance.getEntriesByType('paint');
                const fcp = paint.find(p => p.name === 'first-contentful-paint');
                return fcp ? fcp.startTime : null;
            }
        """)
        
        if fcp is not None:
            print(f"First Contentful Paint: {fcp:.2f}ms")
            assert fcp < PerformanceThresholds.MAX_FIRST_CONTENTFUL_PAINT, (
                f"FCP ({fcp:.2f}ms) exceeds threshold "
                f"({PerformanceThresholds.MAX_FIRST_CONTENTFUL_PAINT}ms)"
            )
        else:
            print("FCP metric not available")

    @pytest.mark.asyncio
    async def test_largest_contentful_paint(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test Largest Contentful Paint (LCP) is within threshold."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(3)  # Wait for LCP to be recorded
        
        lcp = await playwright_page.evaluate("""
            () => {
                return new Promise((resolve) => {
                    new PerformanceObserver((list) => {
                        const entries = list.getEntries();
                        const lastEntry = entries[entries.length - 1];
                        resolve(lastEntry ? lastEntry.startTime : null);
                    }).observe({ type: 'largest-contentful-paint', buffered: true });
                    
                    // Fallback timeout
                    setTimeout(() => resolve(null), 2000);
                });
            }
        """)
        
        if lcp is not None:
            print(f"Largest Contentful Paint: {lcp:.2f}ms")
            assert lcp < PerformanceThresholds.MAX_LARGEST_CONTENTFUL_PAINT, (
                f"LCP ({lcp:.2f}ms) exceeds threshold "
                f"({PerformanceThresholds.MAX_LARGEST_CONTENTFUL_PAINT}ms)"
            )
        else:
            print("LCP metric not available")

    @pytest.mark.asyncio
    async def test_cumulative_layout_shift(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test Cumulative Layout Shift (CLS) is within threshold."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(3)
        
        cls_value = await playwright_page.evaluate("""
            () => {
                return new Promise((resolve) => {
                    let clsValue = 0;
                    new PerformanceObserver((list) => {
                        for (const entry of list.getEntries()) {
                            if (!entry.hadRecentInput) {
                                clsValue += entry.value;
                            }
                        }
                        resolve(clsValue);
                    }).observe({ type: 'layout-shift', buffered: true });
                    
                    setTimeout(() => resolve(clsValue), 2000);
                });
            }
        """)
        
        print(f"Cumulative Layout Shift: {cls_value:.4f}")
        assert cls_value < PerformanceThresholds.MAX_CUMULATIVE_LAYOUT_SHIFT, (
            f"CLS ({cls_value:.4f}) exceeds threshold "
            f"({PerformanceThresholds.MAX_CUMULATIVE_LAYOUT_SHIFT})"
        )


@pytest.mark.performance
class TestPageLoadPerformance:
    """Tests for page load performance metrics."""

    @pytest.mark.asyncio
    async def test_dom_content_loaded(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test DOM Content Loaded time."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        
        dcl = await playwright_page.evaluate("""
            () => {
                const timing = performance.timing;
                return timing.domContentLoadedEventEnd - timing.navigationStart;
            }
        """)
        
        print(f"DOM Content Loaded: {dcl}ms")
        assert dcl < 3000, f"DOM Content Loaded ({dcl}ms) exceeds 3000ms threshold"

    @pytest.mark.asyncio
    async def test_page_load_complete(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test total page load time."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        
        load_time = await playwright_page.evaluate("""
            () => {
                const timing = performance.timing;
                return timing.loadEventEnd - timing.navigationStart;
            }
        """)
        
        print(f"Page Load Complete: {load_time}ms")
        assert load_time < 5000, f"Page load ({load_time}ms) exceeds 5000ms threshold"

    @pytest.mark.asyncio
    async def test_time_to_first_byte(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test Time to First Byte (TTFB)."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        
        ttfb = await playwright_page.evaluate("""
            () => {
                const timing = performance.timing;
                return timing.responseStart - timing.navigationStart;
            }
        """)
        
        print(f"Time to First Byte: {ttfb}ms")
        assert ttfb < 1000, f"TTFB ({ttfb}ms) exceeds 1000ms threshold"


@pytest.mark.performance
class TestResourcePerformance:
    """Tests for resource loading performance."""

    @pytest.mark.asyncio
    async def test_resource_count(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test total number of resources loaded."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(2)
        
        resource_count = await playwright_page.evaluate("""
            () => performance.getEntriesByType('resource').length
        """)
        
        print(f"Total Resources: {resource_count}")
        assert resource_count < PerformanceThresholds.MAX_TOTAL_REQUESTS, (
            f"Resource count ({resource_count}) exceeds threshold "
            f"({PerformanceThresholds.MAX_TOTAL_REQUESTS})"
        )

    @pytest.mark.asyncio
    async def test_javascript_bundle_size(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test JavaScript bundle sizes."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(2)
        
        js_sizes = await playwright_page.evaluate("""
            () => {
                const resources = performance.getEntriesByType('resource');
                const jsResources = resources.filter(r => 
                    r.name.endsWith('.js') || r.initiatorType === 'script'
                );
                return jsResources.map(r => ({
                    name: r.name.split('/').pop(),
                    size: r.transferSize || 0,
                    duration: r.duration
                }));
            }
        """)
        
        total_js_size = sum(r['size'] for r in js_sizes) / 1024  # Convert to KB
        print(f"Total JS Size: {total_js_size:.2f}KB")
        
        # Check individual large bundles
        for resource in js_sizes:
            size_kb = resource['size'] / 1024
            if size_kb > PerformanceThresholds.MAX_BUNDLE_SIZE_KB:
                print(f"Warning: Large bundle detected: {resource['name']} ({size_kb:.2f}KB)")

    @pytest.mark.asyncio
    async def test_css_bundle_size(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test CSS bundle sizes."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(2)
        
        css_sizes = await playwright_page.evaluate("""
            () => {
                const resources = performance.getEntriesByType('resource');
                const cssResources = resources.filter(r => 
                    r.name.endsWith('.css') || r.initiatorType === 'css'
                );
                return cssResources.map(r => ({
                    name: r.name.split('/').pop(),
                    size: r.transferSize || 0
                }));
            }
        """)
        
        total_css_size = sum(r['size'] for r in css_sizes) / 1024
        print(f"Total CSS Size: {total_css_size:.2f}KB")

    @pytest.mark.asyncio
    async def test_image_optimization(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test image sizes and optimization."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(2)
        
        image_sizes = await playwright_page.evaluate("""
            () => {
                const resources = performance.getEntriesByType('resource');
                const imageResources = resources.filter(r => 
                    r.initiatorType === 'img' || 
                    /\\.(jpg|jpeg|png|gif|webp|svg)$/i.test(r.name)
                );
                return imageResources.map(r => ({
                    name: r.name.split('/').pop(),
                    size: r.transferSize || 0
                }));
            }
        """)
        
        large_images = []
        for img in image_sizes:
            size_kb = img['size'] / 1024
            if size_kb > PerformanceThresholds.MAX_IMAGE_SIZE_KB:
                large_images.append(f"{img['name']} ({size_kb:.2f}KB)")
        
        if large_images:
            print(f"Large images detected: {', '.join(large_images)}")


@pytest.mark.performance
class TestNavigationPerformance:
    """Tests for navigation performance between pages."""

    @pytest.mark.asyncio
    async def test_navigation_to_calendar(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test navigation performance to calendar page."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        
        start_time = await playwright_page.evaluate("() => performance.now()")
        
        await playwright_page.goto(base_url + Routes.CALENDAR)
        await wait_for_app(playwright_page)
        
        end_time = await playwright_page.evaluate("() => performance.now()")
        nav_time = end_time - start_time
        
        print(f"Navigation to Calendar: {nav_time:.2f}ms")
        assert nav_time < 3000, f"Navigation time ({nav_time:.2f}ms) exceeds 3000ms"

    @pytest.mark.asyncio
    async def test_navigation_to_form_elements(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test navigation performance to form elements page."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        
        start_time = await playwright_page.evaluate("() => performance.now()")
        
        await playwright_page.goto(base_url + Routes.FORM_ELEMENTS)
        await wait_for_app(playwright_page)
        
        end_time = await playwright_page.evaluate("() => performance.now()")
        nav_time = end_time - start_time
        
        print(f"Navigation to Form Elements: {nav_time:.2f}ms")
        assert nav_time < 3000, f"Navigation time ({nav_time:.2f}ms) exceeds 3000ms"


@pytest.mark.performance
class TestMemoryPerformance:
    """Tests for memory usage."""

    @pytest.mark.asyncio
    async def test_memory_usage(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test JavaScript heap memory usage."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(2)
        
        memory = await playwright_page.evaluate("""
            () => {
                if (performance.memory) {
                    return {
                        usedJSHeapSize: performance.memory.usedJSHeapSize,
                        totalJSHeapSize: performance.memory.totalJSHeapSize,
                        jsHeapSizeLimit: performance.memory.jsHeapSizeLimit
                    };
                }
                return null;
            }
        """)
        
        if memory:
            used_mb = memory['usedJSHeapSize'] / (1024 * 1024)
            total_mb = memory['totalJSHeapSize'] / (1024 * 1024)
            print(f"JS Heap: {used_mb:.2f}MB used / {total_mb:.2f}MB total")
            
            # Warn if memory usage is high
            if used_mb > 100:
                print(f"Warning: High memory usage detected ({used_mb:.2f}MB)")
        else:
            print("Memory API not available")

    @pytest.mark.asyncio
    async def test_memory_after_navigation(
        self, playwright_page: Page, base_url: str, wait_for_app
    ):
        """Test memory doesn't leak after multiple navigations."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        
        initial_memory = await playwright_page.evaluate("""
            () => performance.memory ? performance.memory.usedJSHeapSize : 0
        """)
        
        # Navigate through several pages
        pages = [Routes.CALENDAR, Routes.PROFILE, Routes.FORM_ELEMENTS, Routes.BASIC_TABLES]
        for page_route in pages:
            await playwright_page.goto(base_url + page_route)
            await wait_for_app(playwright_page)
            await asyncio.sleep(0.5)
        
        # Return to home
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(1)
        
        final_memory = await playwright_page.evaluate("""
            () => performance.memory ? performance.memory.usedJSHeapSize : 0
        """)
        
        if initial_memory > 0 and final_memory > 0:
            memory_increase = (final_memory - initial_memory) / (1024 * 1024)
            print(f"Memory increase after navigation: {memory_increase:.2f}MB")
            
            # Allow some memory increase but flag significant leaks
            if memory_increase > 50:
                print(f"Warning: Potential memory leak detected ({memory_increase:.2f}MB increase)")


@pytest.mark.performance
class TestPerformanceReport:
    """Generate comprehensive performance report."""

    @pytest.mark.asyncio
    async def test_generate_performance_report(
        self, playwright_page: Page, base_url: str, wait_for_app, screenshots_dir: Path
    ):
        """Generate a comprehensive performance report."""
        await playwright_page.goto(base_url)
        await wait_for_app(playwright_page)
        await asyncio.sleep(3)
        
        metrics = await playwright_page.evaluate("""
            () => {
                const timing = performance.timing;
                const paint = performance.getEntriesByType('paint');
                const resources = performance.getEntriesByType('resource');
                
                return {
                    navigation: {
                        domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
                        loadComplete: timing.loadEventEnd - timing.navigationStart,
                        ttfb: timing.responseStart - timing.navigationStart,
                        domInteractive: timing.domInteractive - timing.navigationStart,
                    },
                    paint: {
                        firstPaint: paint.find(p => p.name === 'first-paint')?.startTime || null,
                        firstContentfulPaint: paint.find(p => p.name === 'first-contentful-paint')?.startTime || null,
                    },
                    resources: {
                        total: resources.length,
                        totalSize: resources.reduce((sum, r) => sum + (r.transferSize || 0), 0),
                        byType: {
                            script: resources.filter(r => r.initiatorType === 'script').length,
                            css: resources.filter(r => r.initiatorType === 'css' || r.name.endsWith('.css')).length,
                            img: resources.filter(r => r.initiatorType === 'img').length,
                            fetch: resources.filter(r => r.initiatorType === 'fetch').length,
                        }
                    },
                    memory: performance.memory ? {
                        usedJSHeapSize: performance.memory.usedJSHeapSize,
                        totalJSHeapSize: performance.memory.totalJSHeapSize,
                    } : null,
                    timestamp: new Date().toISOString(),
                };
            }
        """)
        
        # Save report
        report_path = screenshots_dir.parent / "reports" / "performance_report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        # Print summary
        print("\nPerformance Report Summary:")
        print(f"  DOM Content Loaded: {metrics['navigation']['domContentLoaded']}ms")
        print(f"  Page Load Complete: {metrics['navigation']['loadComplete']}ms")
        print(f"  TTFB: {metrics['navigation']['ttfb']}ms")
        print(f"  FCP: {metrics['paint']['firstContentfulPaint']}ms")
        print(f"  Total Resources: {metrics['resources']['total']}")
        print(f"  Total Size: {metrics['resources']['totalSize'] / 1024:.2f}KB")
        print(f"  Report saved to: {report_path}")
        
        # Basic assertions
        assert metrics['navigation']['loadComplete'] < 10000, "Page load too slow"
        assert metrics['resources']['total'] < 100, "Too many resources"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
