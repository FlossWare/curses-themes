#!/usr/bin/env python3
"""curses-themes: theme and reusable widget support for Python curses apps."""
import sys

try:
    from .colors import ColorManager
    from .config_theme import ConfigTheme, ConfigTheme3D, load_theme_from_file
    from .manager import ThemeManager
    from .theme import ColorPair, ComponentColors, SemanticColors, Theme
    from .theme3d import Theme3D
    from .themes import (Borland3DTheme, DarkTheme, DBase3Theme, DBase4_3DTheme,
                         DBase4Theme, DefaultTheme, DOSTheme, LightTheme, TI994ATheme, TRS80Theme)
    from .widgets import Dropdown, Option, Table, Tabs
except ImportError as e:
    if "curses" in str(e).lower() and sys.platform == "win32":
        raise ImportError("curses-themes requires curses on Windows; install curses-themes[windows]") from e
    raise

__version__ = "0.9"
__author__ = "FlossWare"
__license__ = "MIT"

__all__ = ["Borland3DTheme", "ColorManager", "ColorPair", "ComponentColors", "ConfigTheme",
           "ConfigTheme3D", "DBase3Theme", "DBase4Theme", "DBase4_3DTheme", "DOSTheme",
           "DarkTheme", "DefaultTheme", "Dropdown", "LightTheme", "Option", "SemanticColors",
           "Table", "Tabs", "TI994ATheme", "TRS80Theme", "Theme", "Theme3D", "ThemeManager",
           "__version__", "load_theme_from_file"]
