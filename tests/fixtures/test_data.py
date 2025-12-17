"""
Test data and selectors for TailAdmin React Dashboard tests.
Contains component selectors, test credentials, and test data.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


# ============================================================================
# CSS Selectors for Dashboard Components
# ============================================================================

@dataclass
class Selectors:
    """CSS selectors for dashboard components."""
    
    # Root and Layout
    ROOT = "#root"
    APP_LAYOUT = "[data-testid='app-layout']"
    MAIN_CONTENT = "main"
    
    # Sidebar
    SIDEBAR = "aside"
    SIDEBAR_NAV = "nav"
    SIDEBAR_MENU_ITEM = ".menu-item"
    SIDEBAR_MENU_ITEM_ACTIVE = ".menu-item-active"
    SIDEBAR_SUBMENU = ".menu-dropdown-item"
    SIDEBAR_LOGO = "aside img[alt='Logo']"
    SIDEBAR_WIDGET = "[data-testid='sidebar-widget']"
    
    # Header
    HEADER = "header"
    HEADER_SEARCH = "[data-testid='header-search']"
    THEME_TOGGLE = "button[aria-label*='theme'], button[aria-label*='dark'], [data-testid='theme-toggle']"
    NOTIFICATION_DROPDOWN = "[data-testid='notification-dropdown']"
    USER_DROPDOWN = "[data-testid='user-dropdown']"
    MOBILE_MENU_TOGGLE = "[data-testid='mobile-menu-toggle']"
    
    # Dashboard Cards and Widgets
    DASHBOARD_CARD = ".card, .widget, [class*='card'], [class*='widget'], .bg-white"
    METRICS_CARD = "[data-testid='metrics-card']"
    CHART_CONTAINER = ".apexcharts-canvas, canvas, svg"
    APEX_CHART = ".apexcharts-canvas"
    
    # Forms
    FORM = "form"
    INPUT = "input"
    INPUT_TEXT = "input[type='text']"
    INPUT_EMAIL = "input[type='email']"
    INPUT_PASSWORD = "input[type='password']"
    TEXTAREA = "textarea"
    SELECT = "select"
    CHECKBOX = "input[type='checkbox']"
    RADIO = "input[type='radio']"
    BUTTON = "button"
    SUBMIT_BUTTON = "button[type='submit']"
    LABEL = "label"
    
    # Tables
    TABLE = "table"
    TABLE_HEADER = "thead"
    TABLE_BODY = "tbody"
    TABLE_ROW = "tr"
    TABLE_CELL = "td"
    TABLE_HEADER_CELL = "th"
    
    # UI Elements
    ALERT = "[role='alert'], .alert"
    MODAL = "[role='dialog'], .modal"
    MODAL_OVERLAY = "[data-testid='modal-overlay']"
    DROPDOWN = "[data-testid='dropdown']"
    BADGE = ".badge, [class*='badge']"
    AVATAR = ".avatar, [class*='avatar']"
    
    # Navigation Links
    NAV_LINK = "a[href]"
    NAV_BUTTON = "button"
    
    # Loading States
    LOADING_SPINNER = ".spinner, .loading, [data-testid='loading']"
    SKELETON = ".skeleton, [class*='skeleton']"
    
    # Error States
    ERROR_MESSAGE = ".error, [class*='error'], [role='alert']"
    VALIDATION_ERROR = ".validation-error, [class*='invalid']"


# ============================================================================
# Page Routes
# ============================================================================

@dataclass
class Routes:
    """Application routes for navigation testing."""
    
    HOME = "/"
    DASHBOARD = "/"
    CALENDAR = "/calendar"
    PROFILE = "/profile"
    FORM_ELEMENTS = "/form-elements"
    BASIC_TABLES = "/basic-tables"
    BLANK = "/blank"
    ERROR_404 = "/error-404"
    LINE_CHART = "/line-chart"
    BAR_CHART = "/bar-chart"
    ALERTS = "/alerts"
    AVATARS = "/avatars"
    BADGE = "/badge"
    BUTTONS = "/buttons"
    IMAGES = "/images"
    VIDEOS = "/videos"
    SIGNIN = "/signin"
    SIGNUP = "/signup"


# ============================================================================
# Test Credentials
# ============================================================================

@dataclass
class TestCredentials:
    """Test credentials for authentication testing."""
    
    VALID_EMAIL = "test@example.com"
    VALID_PASSWORD = "TestPassword123!"
    INVALID_EMAIL = "invalid-email"
    INVALID_PASSWORD = "short"
    EMPTY_EMAIL = ""
    EMPTY_PASSWORD = ""


# ============================================================================
# Test Data
# ============================================================================

@dataclass
class FormTestData:
    """Test data for form validation testing."""
    
    VALID_NAME = "John Doe"
    VALID_EMAIL = "john.doe@example.com"
    VALID_PHONE = "+1234567890"
    VALID_MESSAGE = "This is a test message for form validation."
    
    INVALID_EMAIL = "not-an-email"
    INVALID_PHONE = "abc123"
    
    LONG_TEXT = "A" * 1000
    SPECIAL_CHARS = "<script>alert('xss')</script>"
    SQL_INJECTION = "'; DROP TABLE users; --"


@dataclass
class TableTestData:
    """Expected data for table testing."""
    
    EXPECTED_COLUMNS = ["User", "Project", "Team", "Status", "Budget"]
    MIN_ROWS = 1
    MAX_ROWS = 100


# ============================================================================
# Viewport Configurations
# ============================================================================

VIEWPORTS = {
    "desktop": {"width": 1920, "height": 1080},
    "laptop": {"width": 1366, "height": 768},
    "tablet": {"width": 768, "height": 1024},
    "mobile": {"width": 375, "height": 667},
    "mobile_landscape": {"width": 667, "height": 375},
}


# ============================================================================
# Performance Thresholds
# ============================================================================

@dataclass
class PerformanceThresholds:
    """Performance thresholds for testing."""
    
    # Page load times (milliseconds)
    MAX_FIRST_CONTENTFUL_PAINT = 2000
    MAX_LARGEST_CONTENTFUL_PAINT = 2500
    MAX_TIME_TO_INTERACTIVE = 3500
    MAX_TOTAL_BLOCKING_TIME = 300
    MAX_CUMULATIVE_LAYOUT_SHIFT = 0.1
    
    # Resource limits
    MAX_BUNDLE_SIZE_KB = 500
    MAX_IMAGE_SIZE_KB = 200
    MAX_TOTAL_REQUESTS = 50


# ============================================================================
# Accessibility Configuration
# ============================================================================

@dataclass
class AccessibilityConfig:
    """Configuration for accessibility testing."""
    
    # WCAG levels to test
    WCAG_LEVELS = ["wcag2a", "wcag2aa"]
    
    # Rules to include
    INCLUDE_RULES = [
        "color-contrast",
        "label",
        "image-alt",
        "button-name",
        "link-name",
        "form-field-multiple-labels",
        "aria-required-attr",
        "aria-valid-attr",
    ]
    
    # Rules to exclude (if any)
    EXCLUDE_RULES: List[str] = None
    
    # Elements to exclude from testing
    EXCLUDE_SELECTORS = [
        ".third-party-widget",
        "[data-testid='skip-a11y']",
    ]


# ============================================================================
# Navigation Test Data
# ============================================================================

NAVIGATION_ITEMS = [
    {"name": "Dashboard", "path": "/", "has_submenu": True},
    {"name": "Calendar", "path": "/calendar", "has_submenu": False},
    {"name": "User Profile", "path": "/profile", "has_submenu": False},
    {"name": "Forms", "path": None, "has_submenu": True},
    {"name": "Tables", "path": None, "has_submenu": True},
    {"name": "Pages", "path": None, "has_submenu": True},
]

SIDEBAR_MENU_ITEMS = [
    {"name": "Ecommerce", "path": "/"},
    {"name": "Calendar", "path": "/calendar"},
    {"name": "User Profile", "path": "/profile"},
    {"name": "Form Elements", "path": "/form-elements"},
    {"name": "Basic Tables", "path": "/basic-tables"},
    {"name": "Blank Page", "path": "/blank"},
    {"name": "404 Error", "path": "/error-404"},
    {"name": "Line Chart", "path": "/line-chart"},
    {"name": "Bar Chart", "path": "/bar-chart"},
    {"name": "Alerts", "path": "/alerts"},
    {"name": "Avatar", "path": "/avatars"},
    {"name": "Badge", "path": "/badge"},
    {"name": "Buttons", "path": "/buttons"},
    {"name": "Images", "path": "/images"},
    {"name": "Videos", "path": "/videos"},
    {"name": "Sign In", "path": "/signin"},
    {"name": "Sign Up", "path": "/signup"},
]


# ============================================================================
# Expected Page Titles
# ============================================================================

PAGE_TITLES = {
    "/": "TailAdmin",
    "/calendar": "TailAdmin",
    "/profile": "TailAdmin",
    "/form-elements": "TailAdmin",
    "/basic-tables": "TailAdmin",
    "/signin": "TailAdmin",
    "/signup": "TailAdmin",
}


# ============================================================================
# Error Messages
# ============================================================================

ERROR_MESSAGES = {
    "required_field": "This field is required",
    "invalid_email": "Please enter a valid email address",
    "password_too_short": "Password must be at least 8 characters",
    "passwords_dont_match": "Passwords do not match",
    "invalid_phone": "Please enter a valid phone number",
}
