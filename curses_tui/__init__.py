#!/usr/bin/env python3
"""curses-tui: reusable theme and widget support for Python curses apps."""
import sys

try:
    from .colors import ColorManager
    from .config_theme import ConfigTheme, ConfigTheme3D, load_theme_from_file
    from .declarative import ActionHandler, build_menus, build_window_manager, dispatch_action
    from .geometry import Rect, SizeConstraints
    from .input import enable_mouse, is_cancel, is_confirm, is_down, is_mouse, is_primary_click, is_up, list_index_at, mouse_event, mouse_position, primary_button_mask, primary_click, resolve_list_mouse
    from .manager import ThemeManager
    from .menus import AcceleratorError, Menu, MenuItem, key_to_accelerator, normalize_accelerator
    from .schema import SCHEMA_URL, SCHEMA_VERSION, SchemaError, load_schema, validate
    from .theme import ColorPair, ComponentColors, SemanticColors, Theme
    from .theme3d import Theme3D
    from .themes import Borland3DTheme, DarkTheme, DBase3Theme, DBase4_3DTheme, DBase4Theme, DefaultTheme, DOSTheme, LightTheme, TI994ATheme, TRS80Theme
    from .widgets import Dropdown, Option, Table, Tabs
    from .windows import HitRegion, Window, WindowManager
except ImportError as e:
    if "curses" in str(e).lower() and sys.platform == "win32":
        raise ImportError("curses-tui requires curses on Windows; install windows-curses or curses-tui[windows]") from e
    raise

__version__ = "0.15"
__author__ = "FlossWare"
__license__ = "MIT"

__all__ = ["ActionHandler", "AcceleratorError", "Borland3DTheme", "ColorManager", "ColorPair", "ComponentColors", "ConfigTheme", "ConfigTheme3D", "DBase3Theme", "DBase4Theme", "DBase4_3DTheme", "DOSTheme", "DarkTheme", "DefaultTheme", "Dropdown", "HitRegion", "LightTheme", "Menu", "MenuItem", "Option", "Rect", "SCHEMA_URL", "SCHEMA_VERSION", "SchemaError", "SemanticColors", "SizeConstraints", "TI994ATheme", "TRS80Theme", "Table", "Tabs", "Theme", "Theme3D", "ThemeManager", "Window", "WindowManager", "build_menus", "build_window_manager", "dispatch_action", "enable_mouse", "is_cancel", "is_confirm", "is_down", "is_mouse", "is_primary_click", "is_up", "key_to_accelerator", "list_index_at", "load_schema", "load_theme_from_file", "mouse_event", "mouse_position", "normalize_accelerator", "primary_button_mask", "primary_click", "resolve_list_mouse", "validate"]
