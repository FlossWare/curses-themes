#!/usr/bin/env python3
"""
curses-themes: Lightweight theme support for Python curses applications

Inspired by FlossWare curses-java, this library brings professional theme
support to Python's standard curses module with zero external dependencies.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

import sys

try:
    from .colors import ColorManager
    from .config_theme import ConfigTheme, ConfigTheme3D, load_theme_from_file
    from .manager import ThemeManager
    from .theme import ColorPair, ComponentColors, SemanticColors, Theme
    from .theme3d import Theme3D
    from .themes import (
        Borland3DTheme,
        CatppuccinTheme,
        DarkTheme,
        DBase3Theme,
        DBase4_3DTheme,
        DBase4Theme,
        DefaultTheme,
        DOSTheme,
        DraculaTheme,
        LightTheme,
        MonokaiTheme,
        NordTheme,
        SolarizedDarkTheme,
        SolarizedLightTheme,
        TI994ATheme,
        TRS80Theme,
    )
except ImportError as e:
    if "curses" in str(e).lower() and sys.platform == "win32":
        raise ImportError(
            "curses-themes requires the 'curses' module, which is not included "
            "with Python on Windows. Install windows-curses:\n\n"
            "    pip install curses-themes[windows]\n\n"
            "Or directly:\n\n"
            "    pip install windows-curses"
        ) from e
    raise

__version__ = "0.9"
__author__ = "FlossWare"
__license__ = "MIT"

__all__ = [
    "Borland3DTheme",
    "CatppuccinTheme",
    "ColorManager",
    "ColorPair",
    "ComponentColors",
    "ConfigTheme",
    "ConfigTheme3D",
    "DBase3Theme",
    "DBase4Theme",
    "DBase4_3DTheme",
    "DOSTheme",
    "DarkTheme",
    "DefaultTheme",
    "DraculaTheme",
    "LightTheme",
    "MonokaiTheme",
    "NordTheme",
    "SemanticColors",
    "SolarizedDarkTheme",
    "SolarizedLightTheme",
    "TI994ATheme",
    "TRS80Theme",
    "Theme",
    "Theme3D",
    "ThemeManager",
    "__version__",
    "load_theme_from_file",
]
