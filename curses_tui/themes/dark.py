#!/usr/bin/env python3
"""
DarkTheme implementation matching curses-java API.

Copyright (C) 2024 FlossWare

MIT License - see LICENSE file for details.
"""

from ..theme import Theme

# Dark theme color values matching Java DarkTheme
BLACK = (0, 0, 0)  # background
CYAN = (0, 255, 255)  # foreground, accent
BLUE = (0, 0, 255)  # primary
WHITE = (255, 255, 255)  # info
GREEN = (0, 255, 0)  # success
YELLOW = (255, 255, 0)  # warning
RED = (255, 0, 0)  # error


class DarkTheme(Theme):
    """Dark theme with muted colors and dark background. Modern dark mode aesthetic."""

    color_map = {
        "background": BLACK,
        "foreground": CYAN,
        "primary": BLUE,
        "success": GREEN,
        "error": RED,
        "warning": YELLOW,
        "info": WHITE,
        "accent": CYAN,
    }

    component_colors = {
        "background": (CYAN, BLACK),
        "button": (BLUE, BLACK),
        "button_focused": (BLACK, BLUE),
        "text_input": (WHITE, BLACK),
        "border": (BLUE, BLACK),
        "selection": (BLACK, CYAN),
        "disabled": (BLUE, BLACK),
    }

    border_chars = "┌─┐││└─┘"

    def __init__(self):
        super().__init__(
            name="Dark",
            description="Dark theme with muted colors and dark background. Modern dark mode aesthetic.",
            author="FlossWare",
        )
