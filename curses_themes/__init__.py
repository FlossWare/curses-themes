#!/usr/bin/env python3
"""
curses-themes: Lightweight theme support for Python curses applications

Inspired by FlossWare curses-java, this library brings professional theme
support to Python's standard curses module with zero external dependencies.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.

Example:
    Basic usage with built-in theme::

        import curses
        from curses_themes import ThemeManager

        def main(stdscr):
            # Load and apply a theme
            theme = ThemeManager.load('dark')
            theme.apply(stdscr)

            # Use semantic colors
            stdscr.addstr(0, 0, "Success!", curses.color_pair(theme.colors.success))
            stdscr.addstr(1, 0, "Error!", curses.color_pair(theme.colors.error))

            # Draw themed boxes
            theme.draw_box(stdscr, 3, 2, 10, 40, title="My Panel")

            stdscr.refresh()
            stdscr.getch()

        if __name__ == "__main__":
            curses.wrapper(main)

    Creating a custom theme with class attributes::

        from curses_themes import Theme, ThemeManager

        class MyTheme(Theme):
            color_map = {
                'background': (0, 0, 0),
                'foreground': (255, 255, 255),
                'primary': (0, 120, 215),
                'success': (16, 124, 16),
                'error': (232, 17, 35),
                'warning': (193, 156, 0),
                'info': (0, 120, 212),
                'accent': (142, 68, 173),
            }
            component_colors = {
                'background': ((255, 255, 255), (0, 0, 0)),
                'button': ((0, 120, 215), (0, 0, 0)),
                'button_focused': ((0, 0, 0), (0, 120, 215)),
                'border': ((255, 255, 255), (0, 0, 0)),
            }

            def __init__(self):
                super().__init__(
                    name="My Theme",
                    description="A custom theme",
                    author="Your Name",
                )

        ThemeManager.register(MyTheme)
        theme = ThemeManager.load('my-theme')

    Or create a theme without subclassing::

        theme = ThemeManager.create(
            "Quick Theme",
            color_map={
                'background': (0, 0, 0), 'foreground': (255, 255, 255),
                'primary': (0, 120, 215), 'success': (16, 124, 16),
                'error': (232, 17, 35), 'warning': (193, 156, 0),
                'info': (0, 120, 212), 'accent': (142, 68, 173),
            },
        )
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
        DarkTheme,
        DBase3Theme,
        DBase4_3DTheme,
        DBase4Theme,
        DefaultTheme,
        DOSTheme,
        LightTheme,
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

__version__ = "0.5"
__author__ = "FlossWare"
__license__ = "MIT"

__all__ = [
    "Borland3DTheme",
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
    "LightTheme",
    "SemanticColors",
    "TI994ATheme",
    "TRS80Theme",
    "Theme",
    "Theme3D",
    "ThemeManager",
    "__version__",
    "load_theme_from_file",
]
