import { createContext, useContext, useReducer, useEffect } from "react";

type SidebarState = {
  isExpanded: boolean;
  isMobileOpen: boolean;
  isMobile: boolean;
  isHovered: boolean;
  activeItem: string | null;
  openSubmenu: string | null;
};

type SidebarAction =
  | { type: "TOGGLE_SIDEBAR" }
  | { type: "TOGGLE_MOBILE_SIDEBAR" }
  | { type: "SET_IS_HOVERED"; payload: boolean }
  | { type: "SET_ACTIVE_ITEM"; payload: string | null }
  | { type: "TOGGLE_SUBMENU"; payload: string }
  | { type: "SET_IS_MOBILE"; payload: boolean };

type SidebarContextType = {
  isExpanded: boolean;
  isMobileOpen: boolean;
  isHovered: boolean;
  activeItem: string | null;
  openSubmenu: string | null;
  toggleSidebar: () => void;
  toggleMobileSidebar: () => void;
  setIsHovered: (isHovered: boolean) => void;
  setActiveItem: (item: string | null) => void;
  toggleSubmenu: (item: string) => void;
};

const initialState: SidebarState = {
  isExpanded: true,
  isMobileOpen: false,
  isMobile: false,
  isHovered: false,
  activeItem: null,
  openSubmenu: null,
};

function sidebarReducer(state: SidebarState, action: SidebarAction): SidebarState {
  switch (action.type) {
    case "TOGGLE_SIDEBAR":
      return { ...state, isExpanded: !state.isExpanded };
    case "TOGGLE_MOBILE_SIDEBAR":
      return { ...state, isMobileOpen: !state.isMobileOpen };
    case "SET_IS_HOVERED":
      return { ...state, isHovered: action.payload };
    case "SET_ACTIVE_ITEM":
      return { ...state, activeItem: action.payload };
    case "TOGGLE_SUBMENU":
      return {
        ...state,
        openSubmenu: state.openSubmenu === action.payload ? null : action.payload,
      };
    case "SET_IS_MOBILE":
      return {
        ...state,
        isMobile: action.payload,
        isMobileOpen: action.payload ? state.isMobileOpen : false,
      };
    default:
      return state;
  }
}

const SidebarContext = createContext<SidebarContextType | undefined>(undefined);

export const useSidebar = () => {
  const context = useContext(SidebarContext);
  if (!context) {
    throw new Error("useSidebar must be used within a SidebarProvider");
  }
  return context;
};

export const SidebarProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [state, dispatch] = useReducer(sidebarReducer, initialState);

  useEffect(() => {
    const handleResize = () => {
      const mobile = window.innerWidth < 768;
      dispatch({ type: "SET_IS_MOBILE", payload: mobile });
    };

    handleResize();
    window.addEventListener("resize", handleResize);

    return () => {
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  const toggleSidebar = () => {
    dispatch({ type: "TOGGLE_SIDEBAR" });
  };

  const toggleMobileSidebar = () => {
    dispatch({ type: "TOGGLE_MOBILE_SIDEBAR" });
  };

  const setIsHovered = (isHovered: boolean) => {
    dispatch({ type: "SET_IS_HOVERED", payload: isHovered });
  };

  const setActiveItem = (item: string | null) => {
    dispatch({ type: "SET_ACTIVE_ITEM", payload: item });
  };

  const toggleSubmenu = (item: string) => {
    dispatch({ type: "TOGGLE_SUBMENU", payload: item });
  };

  return (
    <SidebarContext.Provider
      value={{
        isExpanded: state.isMobile ? false : state.isExpanded,
        isMobileOpen: state.isMobileOpen,
        isHovered: state.isHovered,
        activeItem: state.activeItem,
        openSubmenu: state.openSubmenu,
        toggleSidebar,
        toggleMobileSidebar,
        setIsHovered,
        setActiveItem,
        toggleSubmenu,
      }}
    >
      {children}
    </SidebarContext.Provider>
  );
};
