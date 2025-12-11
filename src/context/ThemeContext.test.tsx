import { describe, it, expect, beforeEach, vi } from "vitest";
import { render, screen, fireEvent, act } from "@testing-library/react";
import { ThemeProvider, useTheme } from "./ThemeContext";

const localStorageMock = (() => {
  let store: Record<string, string> = {};
  return {
    getItem: vi.fn((key: string) => store[key] || null),
    setItem: vi.fn((key: string, value: string) => {
      store[key] = value;
    }),
    clear: vi.fn(() => {
      store = {};
    }),
    removeItem: vi.fn((key: string) => {
      delete store[key];
    }),
  };
})();

Object.defineProperty(window, "localStorage", { value: localStorageMock });

function TestComponent() {
  const { theme, toggleTheme } = useTheme();
  return (
    <div>
      <span data-testid="theme-value">{theme}</span>
      <button onClick={toggleTheme} data-testid="toggle-button">
        Toggle Theme
      </button>
    </div>
  );
}

describe("ThemeContext", () => {
  beforeEach(() => {
    localStorageMock.clear();
    document.documentElement.classList.remove("dark");
    vi.clearAllMocks();
  });

  it("provides default light theme", async () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    await act(async () => {
      await new Promise((resolve) => setTimeout(resolve, 0));
    });

    expect(screen.getByTestId("theme-value")).toHaveTextContent("light");
  });

  it("toggles theme from light to dark", async () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    await act(async () => {
      await new Promise((resolve) => setTimeout(resolve, 0));
    });

    const toggleButton = screen.getByTestId("toggle-button");

    await act(async () => {
      fireEvent.click(toggleButton);
    });

    expect(screen.getByTestId("theme-value")).toHaveTextContent("dark");
  });

  it("persists theme to localStorage", async () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    await act(async () => {
      await new Promise((resolve) => setTimeout(resolve, 0));
    });

    const toggleButton = screen.getByTestId("toggle-button");

    await act(async () => {
      fireEvent.click(toggleButton);
    });

    expect(localStorageMock.setItem).toHaveBeenCalledWith("theme", "dark");
  });

  it("adds dark class to document when theme is dark", async () => {
    render(
      <ThemeProvider>
        <TestComponent />
      </ThemeProvider>
    );

    await act(async () => {
      await new Promise((resolve) => setTimeout(resolve, 0));
    });

    const toggleButton = screen.getByTestId("toggle-button");

    await act(async () => {
      fireEvent.click(toggleButton);
    });

    expect(document.documentElement.classList.contains("dark")).toBe(true);
  });

  it("throws error when useTheme is used outside ThemeProvider", () => {
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => {});

    expect(() => render(<TestComponent />)).toThrow(
      "useTheme must be used within a ThemeProvider"
    );

    consoleError.mockRestore();
  });
});
