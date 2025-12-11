import { test, expect } from "@playwright/test";

test.describe("Dashboard", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/");
  });

  test("should load the dashboard page", async ({ page }) => {
    await expect(page).toHaveTitle(/TailAdmin/);
  });

  test("should display the sidebar", async ({ page }) => {
    const sidebar = page.locator("aside");
    await expect(sidebar).toBeVisible();
  });

  test("should display the header", async ({ page }) => {
    const header = page.locator("header");
    await expect(header).toBeVisible();
  });

  test("should navigate to calendar page", async ({ page }) => {
    await page.click('a[href="/calendar"]');
    await expect(page).toHaveURL(/calendar/);
  });

  test("should navigate to profile page", async ({ page }) => {
    await page.click('a[href="/profile"]');
    await expect(page).toHaveURL(/profile/);
  });

  test("should toggle dark mode", async ({ page }) => {
    const themeToggle = page.locator('[data-testid="theme-toggle"]').or(
      page.locator('button:has-text("Dark")').or(
        page.locator('button[aria-label*="theme"]')
      )
    );

    if (await themeToggle.count() > 0) {
      await themeToggle.first().click();
      await expect(page.locator("html")).toHaveClass(/dark/);
    }
  });
});

test.describe("Responsive Design", () => {
  test("should display mobile menu on small screens", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto("/");

    const mobileMenuButton = page.locator('button[aria-label*="menu"]').or(
      page.locator('button:has-text("Menu")')
    );

    if (await mobileMenuButton.count() > 0) {
      await expect(mobileMenuButton.first()).toBeVisible();
    }
  });
});

test.describe("Navigation", () => {
  test("should navigate to form elements page", async ({ page }) => {
    await page.goto("/");
    await page.click('a[href="/form-elements"]');
    await expect(page).toHaveURL(/form-elements/);
  });

  test("should navigate to basic tables page", async ({ page }) => {
    await page.goto("/");
    await page.click('a[href="/basic-tables"]');
    await expect(page).toHaveURL(/basic-tables/);
  });

  test("should navigate to charts page", async ({ page }) => {
    await page.goto("/");
    await page.click('a[href="/line-chart"]');
    await expect(page).toHaveURL(/line-chart/);
  });
});

test.describe("Authentication Pages", () => {
  test("should display sign in page", async ({ page }) => {
    await page.goto("/signin");
    await expect(page.locator("form")).toBeVisible();
  });

  test("should display sign up page", async ({ page }) => {
    await page.goto("/signup");
    await expect(page.locator("form")).toBeVisible();
  });
});

test.describe("404 Page", () => {
  test("should display 404 page for unknown routes", async ({ page }) => {
    await page.goto("/unknown-route-that-does-not-exist");
    await expect(page.locator("body")).toContainText(/404|not found/i);
  });
});
