#!/usr/bin/env python3
"""
curses-themes: Lightweight theme support for Python curses applications

Inspired by FlossWare curses-java, this library brings professional theme
support to Python's standard curses module with zero external dependencies.

Copyright (C) 2024 FlossWare

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

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

    Creating a custom theme::

        from curses_themes import Theme, ThemeManager

        class MyTheme(Theme):
            def __init__(self):
                super().__init__(
                    name="My Theme",
                    description="A custom theme",
                    author="Your Name"
                )

            def get_color_map(self):
                return {
                    'background': (0, 0, 0),
                    'foreground': (255, 255, 255),
                    'primary': (0, 120, 215),
                    'success': (16, 124, 16),
                    'error': (232, 17, 35),
                    'warning': (193, 156, 0),
                    'info': (0, 120, 212),
                    'accent': (142, 68, 173),
                }

        # Register and use
        ThemeManager.register(MyTheme)
        theme = ThemeManager.load('my-theme')
"""

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

__version__ = "0.3"
__author__ = "FlossWare"
__license__ = "GPL-3.0"

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
