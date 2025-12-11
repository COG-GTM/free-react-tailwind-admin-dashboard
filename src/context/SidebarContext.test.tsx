import { describe, it, expect, beforeEach, vi } from "vitest";
import { render, screen, fireEvent, act } from "@testing-library/react";
import { SidebarProvider, useSidebar } from "./SidebarContext";

function TestComponent() {
  const {
    isExpanded,
    isMobileOpen,
    isHovered,
    activeItem,
    openSubmenu,
    toggleSidebar,
    toggleMobileSidebar,
    setIsHovered,
    setActiveItem,
    toggleSubmenu,
  } = useSidebar();

  return (
    <div>
      <span data-testid="is-expanded">{isExpanded.toString()}</span>
      <span data-testid="is-mobile-open">{isMobileOpen.toString()}</span>
      <span data-testid="is-hovered">{isHovered.toString()}</span>
      <span data-testid="active-item">{activeItem || "none"}</span>
      <span data-testid="open-submenu">{openSubmenu || "none"}</span>
      <button onClick={toggleSidebar} data-testid="toggle-sidebar">
        Toggle Sidebar
      </button>
      <button onClick={toggleMobileSidebar} data-testid="toggle-mobile-sidebar">
        Toggle Mobile Sidebar
      </button>
      <button onClick={() => setIsHovered(true)} data-testid="set-hovered">
        Set Hovered
      </button>
      <button onClick={() => setActiveItem("dashboard")} data-testid="set-active">
        Set Active
      </button>
      <button onClick={() => toggleSubmenu("menu1")} data-testid="toggle-submenu">
        Toggle Submenu
      </button>
    </div>
  );
}

describe("SidebarContext", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    Object.defineProperty(window, "innerWidth", {
      writable: true,
      configurable: true,
      value: 1024,
    });
  });

  it("provides default sidebar state", () => {
    render(
      <SidebarProvider>
        <TestComponent />
      </SidebarProvider>
    );

    expect(screen.getByTestId("is-expanded")).toHaveTextContent("true");
    expect(screen.getByTestId("is-mobile-open")).toHaveTextContent("false");
    expect(screen.getByTestId("is-hovered")).toHaveTextContent("false");
    expect(screen.getByTestId("active-item")).toHaveTextContent("none");
    expect(screen.getByTestId("open-submenu")).toHaveTextContent("none");
  });

  it("toggles sidebar expanded state", () => {
    render(
      <SidebarProvider>
        <TestComponent />
      </SidebarProvider>
    );

    const toggleButton = screen.getByTestId("toggle-sidebar");

    act(() => {
      fireEvent.click(toggleButton);
    });

    expect(screen.getByTestId("is-expanded")).toHaveTextContent("false");

    act(() => {
      fireEvent.click(toggleButton);
    });

    expect(screen.getByTestId("is-expanded")).toHaveTextContent("true");
  });

  it("toggles mobile sidebar state", () => {
    render(
      <SidebarProvider>
        <TestComponent />
      </SidebarProvider>
    );

    const toggleButton = screen.getByTestId("toggle-mobile-sidebar");

    act(() => {
      fireEvent.click(toggleButton);
    });

    expect(screen.getByTestId("is-mobile-open")).toHaveTextContent("true");

    act(() => {
      fireEvent.click(toggleButton);
    });

    expect(screen.getByTestId("is-mobile-open")).toHaveTextContent("false");
  });

  it("sets hovered state", () => {
    render(
      <SidebarProvider>
        <TestComponent />
      </SidebarProvider>
    );

    const setHoveredButton = screen.getByTestId("set-hovered");

    act(() => {
      fireEvent.click(setHoveredButton);
    });

    expect(screen.getByTestId("is-hovered")).toHaveTextContent("true");
  });

  it("sets active item", () => {
    render(
      <SidebarProvider>
        <TestComponent />
      </SidebarProvider>
    );

    const setActiveButton = screen.getByTestId("set-active");

    act(() => {
      fireEvent.click(setActiveButton);
    });

    expect(screen.getByTestId("active-item")).toHaveTextContent("dashboard");
  });

  it("toggles submenu", () => {
    render(
      <SidebarProvider>
        <TestComponent />
      </SidebarProvider>
    );

    const toggleSubmenuButton = screen.getByTestId("toggle-submenu");

    act(() => {
      fireEvent.click(toggleSubmenuButton);
    });

    expect(screen.getByTestId("open-submenu")).toHaveTextContent("menu1");

    act(() => {
      fireEvent.click(toggleSubmenuButton);
    });

    expect(screen.getByTestId("open-submenu")).toHaveTextContent("none");
  });

  it("throws error when useSidebar is used outside SidebarProvider", () => {
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => {});

    expect(() => render(<TestComponent />)).toThrow(
      "useSidebar must be used within a SidebarProvider"
    );

    consoleError.mockRestore();
  });
});
